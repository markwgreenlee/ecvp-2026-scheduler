#!/usr/bin/env python3
"""
Parse the ECVP 2026 conference programme into assets/ecvp-data.json.

Sources (saved under scripts/source_html/ for reproducibility; pass --fetch to
re-download the live versions):
  - talks:   https://ecvp2026.uk/ECVP2026_TalksProgramme_FULL.html
  - posters: https://ecvp2026.uk/posters_programme.html
  - keynotes: https://ecvp2026.uk/conference/index.html  (3 lectures, entered by hand
              below because the page lists only speaker/affiliation/day, not
              titles, abstracts, or exact times)

Both programme pages embed their data as a JSON array in a <script> block
(`const talks=[...]` / `const posters=[...]`), so we extract that directly.

Output schema (matches the IMRF/VSS scheduler so the UI is shared):
  id, kind, talk_number, time, time_tbc, title, authors[], author_numbers[],
  affiliations, presenter, organizer, bio, abstract, day, date, room,
  session_title, session_kind, session_start, session_end
"""

import html as ihtml
import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SOURCE_DIR = os.path.join(HERE, "source_html")
OUT_PATH = os.path.join(ROOT, "assets", "ecvp-data.json")

# The organisers' 2026-08 export truncates every abstract at the first double-
# quote character (it writes `\` and drops the remainder), and leaves two empty.
# `recovered_abstracts.json` maps SubmissionID -> the full abstract, recovered
# from the previous complete dataset, and is used only to backfill abstracts the
# source has broken. A future corrected export supersedes it automatically (a
# non-truncated abstract is never overwritten). See README "Data Source".
RECOVERED_PATH = os.path.join(HERE, "recovered_abstracts.json")

URLS = {
    "talks": "https://ecvp2026.uk/ECVP2026_TalksProgramme_FULL.html",
    "posters": "https://ecvp2026.uk/posters_programme.html",
    "conference": "https://ecvp2026.uk/conference/index.html",
}

# ECVP 2026: Sunday Aug 23 -> Thursday Aug 27, Bournemouth, UK
DAY_TO_DATE = {
    "Sunday": "2026-08-23",
    "Monday": "2026-08-24",
    "Tuesday": "2026-08-25",
    "Wednesday": "2026-08-26",
    "Thursday": "2026-08-27",
}

VENUE = "Bournemouth International Centre"

# A few source entries have no title in the published programme; show this so
# the card still renders and stays searchable by author/abstract.
TITLE_PLACEHOLDER = "[Title to be announced]"


def load_html(name):
    """Return the HTML for a source page, fetching it if --fetch was passed."""
    path = os.path.join(SOURCE_DIR, f"{name}.html")
    if "--fetch" in sys.argv or not os.path.exists(path):
        import urllib.request
        print(f"Fetching {URLS[name]} ...")
        with urllib.request.urlopen(URLS[name]) as resp:
            html = resp.read().decode("utf-8", "replace")
        os.makedirs(SOURCE_DIR, exist_ok=True)
        with open(path, "w") as f:
            f.write(html)
    else:
        with open(path) as f:
            html = f.read()
    return html


# A value's closing quote is always followed by `}`/`]`, or by a comma that
# introduces the next key (`, "Foo":`) or the next element of an array. Anything
# else is a quote the author typed, which the export failed to escape.
_IN_OBJECT_END = re.compile(r'"\s*(?:[}\]]|,\s*"[A-Za-z_][A-Za-z0-9_]*"\s*:)')
_IN_ARRAY_END = re.compile(r'"\s*[,\]]')


def escape_stray_quotes(text):
    """Escape double quotes that appear *inside* exported string values.

    The organisers' export does not escape quotes the authors typed, so a title
    like `What Does "Curvy" Mean to You?` terminates its JSON string early and
    breaks the whole file. Rather than hand-patch each one, walk the text and
    escape every quote that is not a real delimiter.

    Keys are tracked separately from values: a key never contains a stray quote,
    so it always closes on its first quote, while a value only closes where one
    of the patterns above matches.

    Returns (repaired_text, number_of_quotes_escaped).
    """
    out = []
    i, n = 0, len(text)
    stack = []            # nesting of '{' and '[' containers
    in_string = False
    is_key = False
    expect_key = False    # next string starts a key rather than a value
    fixed = 0

    while i < n:
        ch = text[i]

        if in_string:
            if ch == "\\":                      # keep existing escapes intact
                out.append(text[i:i + 2])
                i += 2
                continue
            if ch == '"':
                end = _IN_ARRAY_END if (stack and stack[-1] == "[") else _IN_OBJECT_END
                if is_key or end.match(text, i):
                    in_string = False
                else:                           # a quote the author typed
                    out.append('\\"')
                    fixed += 1
                    i += 1
                    continue
        else:
            if ch == '"':
                in_string = True
                is_key = expect_key
            elif ch in "{[":
                stack.append(ch)
                expect_key = ch == "{"
            elif ch in "}]":
                if stack:
                    stack.pop()
            elif ch == ",":
                expect_key = bool(stack) and stack[-1] == "{"
            elif ch == ":":
                expect_key = False

        out.append(ch)
        i += 1

    return "".join(out), fixed


def extract_json_array(html, var_name):
    """Pull `const <var>=[...]` out of a <script> block."""
    m = re.search(rf"const\s+{var_name}\s*=\s*(\[.*?\]);", html, re.DOTALL)
    if not m:
        raise ValueError(f"Could not find `const {var_name}=[...]` in HTML")
    raw = m.group(1)
    # The poster abstracts contain literal newlines inside strings, so be lenient.
    try:
        return json.loads(raw, strict=False)
    except json.JSONDecodeError:
        repaired, fixed = escape_stray_quotes(raw)
        data = json.loads(repaired, strict=False)
        print(f"  NOTE: repaired {fixed} unescaped quote(s) in the {var_name} export")
        return data


def split_coauthors(raw):
    """Turn a co-author string into a clean list of names."""
    if not raw:
        return []
    names = []
    for part in re.split(r"\s*,\s*|\s*;\s*", str(raw)):
        name = part.strip()
        name = re.sub(r"^(?:&|and)\s+", "", name, flags=re.IGNORECASE).strip()
        name = re.sub(r"^&\s*", "", name).strip()
        if name:
            names.append(clean_name(name))
    return names


def clean(value):
    return (str(value).strip() if value is not None else "")


def clean_name(value):
    """Like `clean`, but also collapses whitespace *inside* a personal name.

    A handful of source records carry a stray tab or a double space between the
    given and family name (e.g. `Akihisa\tTakemura`, `Frederick  A.A. Kingdom`),
    which renders oddly and breaks search on the full name. Abstracts keep their
    internal whitespace, so this is deliberately separate from `clean`.
    """
    return re.sub(r"\s+", " ", clean(value))


def load_recovered_abstracts():
    """SubmissionID -> full abstract, for entries the source export truncated."""
    if os.path.exists(RECOVERED_PATH):
        with open(RECOVERED_PATH) as f:
            return json.load(f)
    return {}


def _submission_keys(submission_id):
    """Candidate string keys for a SubmissionID (int/float/str tolerant)."""
    if submission_id in (None, ""):
        return []
    keys = [str(submission_id)]
    try:
        keys.append(str(int(round(float(submission_id)))))
    except (TypeError, ValueError):
        pass
    return keys


# Ids whose abstract was actually taken from the recovery file on this run. The
# recovery file deliberately holds more entries than are needed (it is also a
# safety net if a future export regresses), so reporting its size would overstate
# how much of the programme is not coming straight from the organisers.
BACKFILLED = []


def resolve_abstract(raw_abstract, submission_id, recovered):
    """Return the abstract, backfilling from `recovered` when the source value is
    empty or truncated. Truncated abstracts end in a stray backslash because the
    export cut them at the first double-quote character."""
    a = clean(raw_abstract)
    if a and not a.endswith("\\"):
        return a
    for key in _submission_keys(submission_id):
        if key in recovered:
            BACKFILLED.append(str(submission_id))
            return recovered[key]
    return a


def build_author_fields(record):
    """Build (authors, author_numbers, affiliations) from the organiser's
    structured `Authors` / `Affiliations` fields.

    `Authors` is a list of {"name", "aff": [1-indexed ints]} and `Affiliations`
    is the matching 1-indexed list of affiliation strings. We render authors with
    superscript numbers (e.g. author¹ ²) and the affiliations as a numbered block,
    matching the IMRF/VSS schedulers. Returns (None, None, None) when the record
    lacks the structured fields so callers can fall back to Speaker/CoAuthors.
    """
    author_objs = record.get("Authors")
    if not isinstance(author_objs, list) or not author_objs:
        return None, None, None

    names, numbers = [], []
    for a in author_objs:
        name = clean_name(a.get("name"))
        if not name:
            continue
        names.append(name)
        aff = a.get("aff") or []
        numbers.append(",".join(str(int(n)) for n in aff))
    if not names:
        return None, None, None

    affs = record.get("Affiliations") or []
    affiliations = "\n".join(
        f"{i + 1}. {clean(a)}" for i, a in enumerate(affs) if clean(a)
    )
    return names, numbers, affiliations


def build_talks(raw_talks, recovered):
    entries = []
    seen_ids = {}
    for t in raw_talks:
        session = clean(t.get("Session"))
        is_sym = session.lower().startswith("symposium")
        speaker = clean_name(t.get("Speaker"))
        day = clean(t.get("Day"))
        time = clean(t.get("Time"))

        # Prefer the organiser's structured Authors/Affiliations (superscript
        # numbers); fall back to Speaker + CoAuthors for older source files.
        authors, author_numbers, affiliations = build_author_fields(t)
        if authors is None:
            coauthors = split_coauthors(t.get("CoAuthors"))
            authors = ([speaker] if speaker else []) + coauthors
            author_numbers = ["" for _ in authors]
            affiliations = ""

        sub = t.get("SubmissionID")
        base_id = f"T{int(round(float(sub)))}" if sub not in (None, "") else None
        if base_id is None or base_id in seen_ids:
            # Fall back to a positional id to guarantee uniqueness.
            base_id = f"T{len(entries) + 1:03d}-x"
        seen_ids[base_id] = True

        entries.append({
            "id": base_id,
            "kind": "symposium" if is_sym else "talk",
            "talk_number": None,
            "time": time,
            "time_tbc": False,
            "title": clean(t.get("Title")) or TITLE_PLACEHOLDER,
            "authors": authors,
            "author_numbers": author_numbers,
            "affiliations": affiliations,
            "presenter": speaker,
            "organizer": "",
            "bio": "",
            "abstract": resolve_abstract(t.get("Abstract"), sub, recovered),
            "day": day,
            "date": DAY_TO_DATE.get(day, ""),
            "room": clean(t.get("Room")),
            "session_title": session,
            "session_kind": "Symposium" if is_sym else "Talk Session",
            "session_start": time,
            "session_end": "",
        })

    # Keep every talk session together: talks that share a (day, session, room)
    # block are listed contiguously and in chronological order, and the blocks
    # themselves are ordered by start time so parallel sessions (other rooms)
    # follow one after another rather than interleaving slot by slot.
    group_start = {}
    for e in entries:
        key = (e["date"], e["session_title"], e["room"])
        t = e["session_start"] or e["time"]
        if key not in group_start or t < group_start[key]:
            group_start[key] = t
    entries.sort(key=lambda e: (
        e["date"],
        group_start[(e["date"], e["session_title"], e["room"])],
        e["room"],
        e["session_title"],
        e["time"],
    ))
    return entries


# Poster sessions: the morning and afternoon blocks Mon–Wed, plus Thursday
# morning, numbered 1..7 to match the printed grid's "Poster 1" … "Poster 7".
POSTER_SESSION_NUM = {
    ("Monday", "AM"): 1, ("Monday", "PM"): 2,
    ("Tuesday", "AM"): 3, ("Tuesday", "PM"): 4,
    ("Wednesday", "AM"): 5, ("Wednesday", "PM"): 6,
    ("Thursday", "AM"): 7,
}

# From 2026-08-08 the organisers carry their own board code in SubmissionID, and
# it is what will be printed on the boards: <day><line><AM|PM><n>, e.g. M1AM8 is
# the 8th poster in line 1 on Monday morning. Boards are laid out as 7 lines with
# one topic per line per session, and n restarts at 1 on each line -- so the code
# tells an attendee which line to walk to, which the old running P{session}.{n}
# number did not. Matched case-sensitively: "T" is Tuesday, "Th" is Thursday.
POSTER_CODE_RE = re.compile(r"^(Su|Th|M|T|W)(\d+)(AM|PM)(\d+)$")

POSTER_CODE_DAY = {
    "Su": "Sunday", "M": "Monday", "T": "Tuesday",
    "W": "Wednesday", "Th": "Thursday",
}


def parse_poster_code(code):
    """Split an organiser board code into (day, line, block, n), or None."""
    m = POSTER_CODE_RE.match(clean(code))
    if not m:
        return None
    return POSTER_CODE_DAY[m.group(1)], int(m.group(2)), m.group(3), int(m.group(4))


def build_posters(raw_posters, recovered):
    entries = []
    board_counter = {}
    for p in raw_posters:
        author = clean_name(p.get("Author"))
        day = clean(p.get("Day"))
        topic = clean(p.get("Topic"))

        # Prefer the organiser's structured Authors/Affiliations (superscript
        # numbers); fall back to Author + CoAuthors for older source files.
        authors, author_numbers, affiliations = build_author_fields(p)
        if authors is None:
            coauthors = split_coauthors(p.get("CoAuthors"))
            authors = ([author] if author else []) + coauthors
            author_numbers = ["" for _ in authors]
            affiliations = ""

        # Time is the poster session block, e.g. "09:00–10:30"
        time_raw = clean(p.get("Time"))
        parts = re.split(r"[–\-—]", time_raw)
        start = parts[0].strip() if parts else ""
        end = parts[1].strip() if len(parts) > 1 else ""

        block = "AM" if start and start < "12:00" else "PM"
        snum = POSTER_SESSION_NUM.get((day, block))
        session_title = (
            f"Poster Session {snum} · {topic}" if topic and snum
            else (f"Poster Session {snum}" if snum else topic)
        )

        # Prefer the organiser's board code; it is what is printed on the board.
        code = clean(p.get("SubmissionID"))
        parsed = parse_poster_code(code)
        if parsed:
            code_day, line, code_block, seq = parsed
            if code_day != day or code_block != block:
                print(f"  WARNING board code {code} disagrees with the programme "
                      f"({day} {block}); using the code")
            poster_id = code
            poster_number = code
            sort_key = (snum or 99, line, seq)
        elif snum is not None:
            # Older exports carried no board code: fall back to the running
            # P{session}.{board} number this script used to assign.
            board = board_counter.get(snum, 0) + 1
            board_counter[snum] = board
            poster_id = f"P{snum}.{board}"
            poster_number = f"{snum}.{board}"
            sort_key = (snum, 0, board)
        else:
            poster_id = f"P{len(entries) + 1:03d}-x"
            poster_number = None
            sort_key = (99, 0, len(entries) + 1)

        entries.append({
            "id": poster_id,
            "kind": "poster",
            "talk_number": poster_number,
            "time": start,
            "time_tbc": False,
            "title": clean(p.get("Title")) or TITLE_PLACEHOLDER,
            "authors": authors,
            "author_numbers": author_numbers,
            "affiliations": affiliations,
            "presenter": author,
            "organizer": "",
            "bio": "",
            "abstract": resolve_abstract(p.get("Abstract"), p.get("SubmissionID"), recovered),
            "day": day,
            "date": DAY_TO_DATE.get(day, ""),
            "room": "",
            "session_title": session_title,
            "session_kind": "Poster Session",
            "session_start": start,
            "session_end": end,
            "_sort": sort_key,
        })

    # Walking order: session 1 line 1 boards 1..n, then line 2, … then session 2.
    entries.sort(key=lambda e: e["_sort"])
    for e in entries:
        del e["_sort"]
    return entries


# Keynotes are entered by hand: the conference page lists only speaker,
# affiliation, and a rough time-of-day. Times below are APPROXIMATE placeholders
# (to be confirmed) so calendar export has something to anchor to.
KEYNOTE_TBC_NOTE = (
    "Lecture title and abstract to be announced. The time shown is an "
    "approximate placeholder and is yet to be confirmed by the organisers."
)

KEYNOTES = [
    {
        "id": "KN1",
        "title": "Perception Keynote Lecture",
        "speaker": "Karl Gegenfurtner",
        "affiliation": "Justus Liebig University of Giessen",
        "day": "Sunday",
        "time": "18:00",
        "duration_min": 120,
        "session_title": "Perception Keynote Lecture",
    },
    {
        "id": "KN2",
        "title": "Spotlight in Vision Lecture",
        "speaker": "Nadine Dijkstra",
        "affiliation": "University College London",
        "day": "Tuesday",
        "time": "17:00",
        "duration_min": 90,
        "session_title": "Spotlight in Vision Lecture",
    },
    {
        "id": "KN3",
        "title": "Rank Prize Lecture",
        "speaker": "Monica Gori",
        "affiliation": "Istituto Italiano di Tecnologia",
        "day": "Wednesday",
        "time": "17:00",
        "duration_min": 90,
        "session_title": "Rank Prize Lecture",
    },
]


# Social events are entered by hand from the conference programme grid.
# Times are the published start times; venues from the programme ("tbc" kept as-is).
SOCIAL_EVENTS = [
    {
        "id": "SOC1",
        "title": "Opening Reception",
        "day": "Sunday",
        "time": "20:00",
        "end": "22:00",
        "room": "Bournemouth International Centre",
    },
    {
        "id": "SOC2",
        "title": "Illusion Night",
        "day": "Tuesday",
        "time": "19:00",
        "end": "22:00",
        "room": "Russell Cotes Art Gallery & Museum (tbc)",
    },
    {
        "id": "SOC3",
        "title": "Conference Dinner",
        "day": "Wednesday",
        "time": "19:00",
        "end": "22:30",
        "room": "Pavilion",
    },
    {
        "id": "SOC4",
        "title": "Farewell Party",
        "day": "Thursday",
        "time": "19:00",
        "end": "23:00",
        "room": "Bournemouth Pier",
    },
]


def build_socials():
    entries = []
    for s in SOCIAL_EVENTS:
        entries.append({
            "id": s["id"],
            "kind": "social",
            "talk_number": None,
            "time": s["time"],
            "time_tbc": False,
            "title": s["title"],
            "authors": [],
            "author_numbers": [],
            "affiliations": "",
            "presenter": "",
            "organizer": "",
            "bio": "",
            "abstract": "",
            "day": s["day"],
            "date": DAY_TO_DATE.get(s["day"], ""),
            "room": s["room"],
            "session_title": "Social Event",
            "session_kind": "Social",
            "session_start": s["time"],
            "session_end": s.get("end", ""),
        })
    return entries


def html_to_text(s):
    """Collapse an HTML fragment to readable plain text."""
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"</p>", "\n", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = ihtml.unescape(s)
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n", s)
    return s.strip()


def extract_keynote_details(conf_html):
    """Pull (summary, abstract) pairs from the conference page <details> dropdowns
    that carry a keynote abstract."""
    pairs = []
    for block in re.findall(r"<details\b.*?</details>", conf_html, re.DOTALL):
        m = re.search(r"<summary\b[^>]*>(.*?)</summary>", block, re.DOTALL)
        if not m:
            continue
        summary = html_to_text(m.group(1))
        if "Abstract" not in summary:
            continue
        body = re.sub(r"<summary\b.*?</summary>", "", block, flags=re.DOTALL)
        body = re.sub(r"^<details[^>]*>", "", body)
        body = re.sub(r"</details>\s*$", "", body)
        pairs.append((summary, html_to_text(body)))
    return pairs


def find_keynote(pairs, speaker):
    """Return (lecture_title, abstract) for a speaker from the extracted pairs."""
    for summary, abstract in pairs:
        if speaker in summary:
            # Summary form: "<Series> – <Speaker> - <Lecture Title> – Abstract:"
            title = re.split(r"Abstract\s*:?", summary)[0]
            idx = title.find(speaker)
            if idx != -1:
                title = title[idx + len(speaker):]
            title = title.strip(" -–—\n\t")
            return title, abstract
    return None, None


def add_minutes(hhmm, minutes):
    """Return HH:MM offset from a HH:MM string by `minutes`."""
    h, m = (int(x) for x in hhmm.split(":"))
    total = h * 60 + m + minutes
    return f"{(total // 60) % 24:02d}:{total % 60:02d}"


def build_keynotes(detail_pairs):
    entries = []
    for k in KEYNOTES:
        lecture_title, abstract = find_keynote(detail_pairs, k["speaker"])
        # Fall back to the series name / TBC note if the page hasn't published the
        # title or abstract yet.
        title = lecture_title or k["title"]
        body = abstract or KEYNOTE_TBC_NOTE
        if not lecture_title:
            print(f"  NOTE: no published title/abstract found for {k['speaker']}; using placeholder")
        entries.append({
            "id": k["id"],
            "kind": "keynote",
            "talk_number": None,
            "time": k["time"],
            "time_tbc": False,
            "title": title,
            "authors": [k["speaker"]],
            "author_numbers": [""],
            "affiliations": k["affiliation"],
            "presenter": k["speaker"],
            "organizer": "",
            "bio": "",
            "abstract": body,
            "day": k["day"],
            "date": DAY_TO_DATE.get(k["day"], ""),
            "room": VENUE,
            "session_title": k["session_title"],
            "session_kind": "Keynote",
            "session_start": k["time"],
            "session_end": add_minutes(k["time"], k["duration_min"]),
        })
    return entries


def main():
    talks_html = load_html("talks")
    posters_html = load_html("posters")
    conf_html = load_html("conference")

    raw_talks = extract_json_array(talks_html, "talks")
    raw_posters = extract_json_array(posters_html, "posters")
    keynote_details = extract_keynote_details(conf_html)
    recovered = load_recovered_abstracts()

    keynotes = build_keynotes(keynote_details)
    socials = build_socials()
    talks = build_talks(raw_talks, recovered)
    posters = build_posters(raw_posters, recovered)

    data = keynotes + socials + talks + posters

    # Validation
    ids = [d["id"] for d in data]
    dupes = [i for i, c in Counter(ids).items() if c > 1]
    missing_date = [d["id"] for d in data if not d["date"]]
    contrib = [d for d in data if d["kind"] in ("talk", "symposium", "poster")]
    truncated = [d["id"] for d in contrib if d["abstract"].endswith("\\")]
    empty_abs = [d["id"] for d in contrib if not d["abstract"].strip()]

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    print(f"\nWrote {len(data)} entries to {OUT_PATH}")
    print("  by kind:", dict(Counter(d["kind"] for d in data)))
    print("  by day :", dict(Counter(d["day"] for d in data)))
    sym = sum(1 for d in data if d["kind"] == "symposium")
    print(f"  symposium talks: {sym} across "
          f"{len(set(d['session_title'] for d in data if d['kind'] == 'symposium'))} symposia")
    if dupes:
        print(f"  WARNING duplicate ids: {dupes}")
    else:
        print("  all ids unique ✓")
    if missing_date:
        print(f"  WARNING entries with no date: {missing_date}")
    else:
        print("  all entries have a date ✓")
    print(f"  abstracts backfilled from recovery file: {len(BACKFILLED)}"
          f" of {len(recovered)} available"
          + (f" -> {sorted(set(BACKFILLED))}" if BACKFILLED else ""))
    if truncated:
        print(f"  WARNING still-truncated abstracts: {truncated}")
    else:
        print("  no truncated abstracts ✓")
    if empty_abs:
        print(f"  abstracts still empty (none in source): {empty_abs}")


if __name__ == "__main__":
    main()
