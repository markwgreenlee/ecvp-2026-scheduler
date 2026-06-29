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


def extract_json_array(html, var_name):
    """Pull `const <var>=[...]` out of a <script> block."""
    m = re.search(rf"const\s+{var_name}\s*=\s*(\[.*?\]);", html, re.DOTALL)
    if not m:
        raise ValueError(f"Could not find `const {var_name}=[...]` in HTML")
    # The poster abstracts contain literal newlines inside strings, so be lenient.
    return json.loads(m.group(1), strict=False)


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
            names.append(name)
    return names


def clean(value):
    return (str(value).strip() if value is not None else "")


def build_talks(raw_talks):
    entries = []
    seen_ids = {}
    for t in raw_talks:
        session = clean(t.get("Session"))
        is_sym = session.lower().startswith("symposium")
        speaker = clean(t.get("Speaker"))
        coauthors = split_coauthors(t.get("CoAuthors"))
        authors = ([speaker] if speaker else []) + coauthors
        day = clean(t.get("Day"))
        time = clean(t.get("Time"))

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
            "author_numbers": ["" for _ in authors],
            "affiliations": "",
            "presenter": speaker,
            "organizer": "",
            "bio": "",
            "abstract": clean(t.get("Abstract")),
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


def build_posters(raw_posters):
    entries = []
    seen_ids = {}
    for p in raw_posters:
        author = clean(p.get("Author"))
        coauthors = split_coauthors(p.get("CoAuthors"))
        authors = ([author] if author else []) + coauthors
        day = clean(p.get("Day"))
        topic = clean(p.get("Topic"))

        # Time is the poster session block, e.g. "09:00–10:30"
        time_raw = clean(p.get("Time"))
        parts = re.split(r"[–\-—]", time_raw)
        start = parts[0].strip() if parts else ""
        end = parts[1].strip() if len(parts) > 1 else ""

        sub = p.get("SubmissionID")
        base_id = f"P{int(round(float(sub)))}" if sub not in (None, "") else None
        if base_id is None or base_id in seen_ids:
            base_id = f"P{len(entries) + 1:03d}-x"
        seen_ids[base_id] = True

        entries.append({
            "id": base_id,
            "kind": "poster",
            "talk_number": None,
            "time": start,
            "time_tbc": False,
            "title": clean(p.get("Title")) or TITLE_PLACEHOLDER,
            "authors": authors,
            "author_numbers": ["" for _ in authors],
            "affiliations": "",
            "presenter": author,
            "organizer": "",
            "bio": "",
            "abstract": clean(p.get("Abstract")),
            "day": day,
            "date": DAY_TO_DATE.get(day, ""),
            "room": "",
            "session_title": topic,
            "session_kind": "Poster Session",
            "session_start": start,
            "session_end": end,
        })
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

    keynotes = build_keynotes(keynote_details)
    socials = build_socials()
    talks = build_talks(raw_talks)
    posters = build_posters(raw_posters)

    data = keynotes + socials + talks + posters

    # Validation
    ids = [d["id"] for d in data]
    dupes = [i for i, c in Counter(ids).items() if c > 1]
    missing_date = [d["id"] for d in data if not d["date"]]

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


if __name__ == "__main__":
    main()
