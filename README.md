# ECVP 2026 Schedule Organizer

A Progressive Web App (PWA) for iOS and Android to search and organize your European Conference on Visual Perception (ECVP) conference schedule, August 23–27, 2026, Bournemouth, UK. No installation required — works in any phone browser.

## For Conference Attendees

### Use the web version — no installation required

Go directly to: **https://markwgreenlee.github.io/ecvp-2026-scheduler**

📖 **Documentation:** https://markwgreenlee.github.io/ecvp-2026-scheduler/docs/

Works on any iPhone or Android. No app, no account, no setup. Google Calendar export works.

> **Tip: load the app before you arrive at the venue.** Open the link at home or on cellular so the app is cached on your phone. It will then continue to work even on slow or unreliable conference WiFi.

### Save to your home screen for the best experience

The app installs as a Progressive Web App (PWA) — it opens full-screen like a native app and **works offline** after the first load. No App Store required.

> **Note:** Use Safari on iPhone and Chrome on Android. Other browsers may not offer the Add to Home Screen option. Chrome on iPhone does **not** support PWA installation — Safari only.
> To make Safari your default browser on iPhone: **Settings → Apps → Default Apps → Browser → Safari**. This ensures QR code scans open in Safari automatically.

**iPhone (Safari):**
1. Open the URL in Safari
2. Tap the Share button (box with arrow pointing up) at the bottom of the screen
3. Scroll down and tap **Add to Home Screen**
4. Tap **Add** — the app icon appears on your home screen

**Android (Chrome):**
1. Open the URL in Chrome
2. Tap the three-dot menu (⋮) in the top right corner
3. Tap **Add to Home Screen** (or **Install app**)
4. Tap **Add** — the app icon appears on your home screen

> **Beta:** This is a community-built tool. Data is sourced from the official ECVP 2026 online programme; some inaccuracies may remain. Feedback and corrections welcome — open a [GitHub issue](https://github.com/markwgreenlee/ecvp-2026-scheduler/issues) or email markwgreenlee@gmail.com.

---

## Troubleshooting

### Web version won't load

- Make sure you have an internet connection
- Try refreshing the page
- If on slow conference WiFi, switch to cellular data for the initial load, then switch back

### Calendar times are wrong

Calendar events are anchored to British Summer Time (Bournemouth, `Europe/London`). Check that automatic timezone is enabled on your phone:
- **iPhone:** Settings → General → Date & Time → "Set Automatically" ON
- **Android:** Settings → System → Date & Time → "Automatic date/time" ON

Then close and reopen the Calendar app.

> **The programme is now complete.** Every one of the 614 presentations has a title and an abstract, following the organisers' 2026-08-08 corrections.

### Can't find presentations

- Try shorter search terms (e.g., "motion" instead of "motion perception")
- Search by author last name (e.g., "Gegenfurtner", "Dijkstra")
- Check that day and type filters are cleared
- Refresh the page to verify all 614 presentations loaded

---

## Features

- **614 presentations** from the official ECVP 2026 online programme — 3 keynotes, 10 symposia (45 symposium talks), 120 talk-session talks, 442 posters, and 4 social events
- Full-text search by title, author, co-authors, abstract, session, and topic
- **Author affiliations** for every talk and poster — authors shown with superscript numbers and a numbered institution list
- Filter by day (Sun–Thu) and type (Keynote / Symposium / Talk / Poster / Social)
- **Tap any card** to read the full abstract, authors, and session details in a pop-up sheet
- Build a personal schedule — add/remove directly from the detail sheet
- Export to **Google Calendar** (opens in browser); the native iOS build can also add events directly to **Apple Calendar**
- Persistent schedule — survives app restarts
- Works offline after first load

---

## For Developers

This app is adapted from the [IMRF 2026 Schedule Organizer](https://github.com/markwgreenlee/imrf-2026-scheduler) / [VSS 2026 Schedule Organizer](https://github.com/markwgreenlee/vss-2026-scheduler) codebase. The conference-specific data lives in `assets/ecvp-data.json`, generated from the ECVP online programme by `scripts/parse_ecvp.py`.

### A Note on the Tech Stack for Non-Developers

This app was built with [Claude Code](https://claude.ai/code) (Anthropic's AI coding assistant) by a vision scientist with no prior mobile app development experience.

**JavaScript** runs in web browsers and handles all logic, data, and interactivity. **React** (developed by Meta) builds user interfaces from reusable *components* — self-contained building blocks like a search bar or a detail pop-up. **React Native** extends React so the same JavaScript codebase renders native UI on iOS, Android, and web. **Expo** sits on top of React Native and simplifies building, deployment, and device features (like the calendar). A **Progressive Web App (PWA)** is a set of web standards that let a browser-based app install to the home screen, run full-screen, and work offline — making the app feel native without an App Store submission.

### Quick Start

```bash
git clone https://github.com/markwgreenlee/ecvp-2026-scheduler.git
cd ecvp-2026-scheduler
npm install
npx expo start
```

### Regenerating the data

The presentation dataset is parsed from the three official ECVP 2026 pages — the talks programme and poster programme (each embeds its records as a JSON array) and the conference page (keynote lecture titles and abstracts, pulled from its dropdowns). Keynote speakers/affiliations/times and the four social events are entered by hand. Talks are grouped so each session (same day, session, and room) is listed contiguously and chronologically, with parallel sessions following one another:

```bash
python3 scripts/parse_ecvp.py           # uses the saved copies in scripts/source_html/
python3 scripts/parse_ecvp.py --fetch   # re-download the live programme pages first
```

This writes `assets/ecvp-data.json` and prints per-type counts and a validation report (unique ids, every entry dated, abstracts backfilled, none left truncated).

The organisers' app-export mishandles double quotes the authors typed. In an **abstract** it truncates at the first `"` (emitting a stray `\` and dropping the rest); in a **title** it writes them unescaped, which breaks the JSON outright.

The organisers resolved this across both files by **2026-08-10**, substituting typographic single quotes (`'…'`) for the offending double quotes. **All 614 abstracts now come straight from the source export — nothing is patched or recovered.** The validation report confirms it on every run: `abstracts backfilled from recovery file: 0 of 47 available`.

The workarounds are retained but dormant, because these exports have regressed before:

- `scripts/recovered_abstracts.json` maps `SubmissionID → full abstract`, recovered from an earlier complete dataset. The parser backfills **only** where the source is empty or genuinely truncated, so a corrected export supersedes it automatically. Keyed by both the old numeric ids and the board codes, so either export vintage works.
- `escape_stray_quotes()` repairs unescaped quotes in titles by walking the export and escaping every quote that is not a real delimiter, tracking keys separately from values.
- `resolve_abstract()` does **not** treat a trailing `\` as proof of truncation. One abstract regained its full text while keeping the stray backslash, so the backslash is weighed against the recovered copy: backfill only if that copy is materially longer, otherwise strip the backslash and keep the source text.

The organisers' current export emits each abstract as a single block, losing the paragraph structure earlier versions carried. `restore_paragraphs()` puts it back for the 9 affected abstracts, taking the structure from the recovery copy while keeping the organisers' wording: the two texts are aligned on their letters and digits alone, so differences in quotes, dashes or spacing are irrelevant, and the function refuses to act unless the spelling matches exactly. It inserts whitespace and nothing else, and verifies that before returning — the diff against the previous release is 9 whitespace-only changes and zero text changes.

### Regenerating the app icons

```bash
python3 scripts/make_icons.py    # generates an original ECVP "eye" icon set (requires Pillow)
```

The icon is an original stylised eye on the ECVP navy — a placeholder generated to avoid logo copyright concerns. Replace `assets/icon.png` (and rerun `make_icons.py`, or swap the source) with an official logo if one becomes available.

### Building a Standalone App

```bash
eas build --platform android   # produces .apk / .aab — requires free Expo account
eas build --platform ios       # produces .ipa — requires Apple Developer account ($99/yr)
```

### Analytics (optional)

Visitor numbers come from [Umami Cloud](https://cloud.umami.is). Register the site there with the domain **`markwgreenlee.github.io`** — a bare hostname, no scheme and no path — then set the site id as a repository variable:

```bash
gh variable set UMAMI_WEBSITE_ID --body "<the id Umami gives you>"
```

The deploy workflow injects the tracking tag into `dist/index.html` on every run, because Expo rewrites that file on each export. If the variable is unset the tag is simply left out and the run logs a warning — the site still deploys normally, but the Umami dashboard will record nothing.

This counts page views, not installs: someone who adds the app to their home screen looks the same as someone who only glances at it, and once installed the service worker may serve them from cache without a fresh page view. Treat it as a measure of reach rather than of downloads.

### Security

The site is static: no server, no database, no login, and the programme data is compiled into the JS bundle rather than served as a fetchable file. There is therefore nothing to tamper with at runtime — the only realistic risk is someone gaining push access to this repository, since the deploy workflow publishes whatever is on `main`.

Measures in place:

- **Actions pinned to commit SHAs**, not tags. A tag can be moved to point at new code, so `@v5` would silently run whatever upstream publishes next. Update deliberately: resolve the tag to a SHA (`gh api repos/actions/checkout/git/refs/tags/v5`) and edit the pin.
- **A ruleset on `main`** blocking force-pushes and branch deletion, so history cannot be quietly rewritten.
- **A Content-Security-Policy** injected into `index.html`, restricting scripts to this origin plus `cloud.umami.is`. Note `frame-ancestors` is absent — it is ignored in a `<meta>` tag, and GitHub Pages cannot set response headers.
- **Default workflow permissions are read-only**, so a compromised action cannot push to the repo.

Not covered here, and worth keeping current: two-factor authentication on the GitHub account, and periodically reviewing authorised OAuth apps and personal access tokens. Account takeover is the whole threat model.

If the site is ever defaced, recovery is fast: revert the offending commit and re-run the deploy — the entire site is regenerable from this repository.

### Project Structure

```
ecvp-2026-scheduler/
├── App.js                          # Entry point, tab navigation, SW registration
├── app.json                        # Expo / PWA configuration
├── assets/
│   ├── icon.png                    # App icon (stylised eye)
│   └── ecvp-data.json              # 614 presentations
├── public/
│   ├── sw.js                       # Service worker (offline caching)
│   └── icons/                      # PWA + apple-touch icons (192 / 512 / 180)
├── scripts/
│   ├── parse_ecvp.py               # programme HTML → ecvp-data.json
│   ├── make_icons.py               # generate icon set
│   └── source_html/                # saved copies of the programme pages
├── src/
│   ├── screens/                    # Search, Schedule, Settings
│   ├── components/                 # SessionCard, SessionDetailModal, ExportButton, …
│   └── context/
│       └── DataContext.js          # Global state & search logic
```

### Tech Stack

- React Native 0.85 / React 19.2
- Expo SDK 56
- expo-calendar (direct Apple Calendar event creation)
- AsyncStorage (persistent schedule)
- Progressive Web App (PWA) with service worker for offline support
- Deployed via GitHub Pages (GitHub Actions)

### Data Schema

Each entry in `assets/ecvp-data.json` has: `id`, `kind` (`keynote` / `symposium` / `talk` / `poster` / `social`), `title`, `authors[]`, `author_numbers[]`, `affiliations`, `presenter`, `organizer`, `bio`, `abstract`, `day`, `date`, `room`, `session_title`, `session_kind`, `session_start`, `session_end`, `talk_number`, `time`, `time_tbc`. For talks and posters, `authors[]` and its parallel `author_numbers[]` (superscript affiliation numbers, e.g. `"1"` or `"2,3,4"`) and the numbered `affiliations` block come from the organiser-supplied `Authors`/`Affiliations` fields in the source pages; keynotes and socials leave these as their hand-entered values. Talks/symposia carry a room (Tregonwell Hall, Bayview Suite, Purbeck Lounge); posters carry the organisers' board code as their `id` and `talk_number` (e.g. `M1AM8`), taken from the export's `SubmissionID` — `<day><line><AM|PM><n>`, where the boards are laid out as seven lines with one topic per line per session and `n` restarts at 1 on each line, so `M1AM8` is the 8th poster in line 1 on Monday morning. This is the code printed on the board, and it is searchable, so typing a code jumps straight to that poster. The topic is kept in the session label. Older exports carried no board code; for those the parser falls back to the running `P{session}.{board}` number it used to assign. Keynote and social entries carry a full `session_end` so they export to the calendar as full-length events (Perception keynote 120 min, the other keynotes 90 min, talks 15 min). `time_tbc` is retained for future use and is currently `false` for all entries.

---

## Version History

**v1.3.4** (2026-08-11)
- **Two Tuesday-afternoon posters exchanged board codes** at a presenter's request, per the organisers' 2026-08-11 export: *Eye-movement manifestations of differential safety-behaviour strategies* (Antolin, Bournemouth) moves from `T2PM8` to `T2PM2`, and *Rapid Negative Evaluation without Explicit Recognition in the Uncanny Valley* (Sasaki, Chuo) moves from `T2PM2` to `T2PM8`
- Both stay in the same Tuesday 15:30 session; only the board position changes. Each presentation carried its own title, authors, affiliation and abstract with it
- Verified against the previous release: the source export differs in exactly two `SubmissionID` fields and nothing else, and the built data differs in exactly those two entries. Same 614 ids, same 442 posters, nothing added, removed, rescheduled or reworded

**v1.3.3** (2026-08-10)
- **Paragraph breaks restored** in the 9 abstracts that had them before the organisers' current export flattened each abstract into a single block. Long abstracts read as paragraphs again rather than one dense wall of text
- The wording stays exactly as the organisers wrote it: `restore_paragraphs()` inserts whitespace only, aligns the two texts on letters and digits alone so quote and dash differences do not matter, and refuses to act unless the spelling matches. Verified as 9 whitespace-only changes and zero text changes
- Every abstract still comes straight from the source export — nothing is backfilled

**v1.3.2** (2026-08-10)
- **Every abstract now comes straight from the organisers' export.** The final talks file clears the last 7 truncated abstracts, so nothing in the app is recovered or patched any more — the validation report reads `backfilled: 0 of 47 available`
- No straight double quotes and no stray backslashes remain anywhere in the data
- `resolve_abstract()` no longer treats a trailing `\` as proof of truncation: one abstract (Wexler, *Temporal evolution of idiosyncratic visual biases*) regained its full text while keeping the backslash, so the source is now compared against the recovered copy and only backfilled if that copy is materially longer
- Nothing added, removed, renumbered or rescheduled: the only changes are 7 talk abstracts, all quote substitutions

**v1.3.1** (2026-08-08)
- **Every presentation now has an abstract.** The organisers supplied the two that had been missing throughout — `T397` (*Continuous Psychophysics in the Clinic*) and `M2PM12` (*Illusion of absence*)
- **The poster export is clean at source.** The organisers replaced the double quotes that had been truncating abstracts with typographic single quotes, so all 442 poster abstracts now come straight from the programme instead of being backfilled; 7 talk abstracts still need the recovery file, as the same fix was not applied to the talks export
- `T5AM5` now carries a real board code, so the `POSTER_CODE_OVERRIDE` stopgap is removed
- One title changed with the quote substitution: *What Does 'Curvy' Mean to You?* (was `"Curvy"`)
- The validation report now prints how many abstracts were **actually** backfilled rather than how many the recovery file holds
- No presentation was added, removed, renumbered or rescheduled in this refresh

**v1.3.0** (2026-08-08)
- **Posters now use the organisers' board codes.** A poster is identified by the code printed on its board — `<day><line><AM|PM><n>`, e.g. `M1AM8` is the 8th poster in line 1 on Monday morning — replacing the running `P{session}.{board}` number the app used to assign. The boards are arranged as seven lines with one topic per line per session, so the code names the line to walk to, which the old number did not
- **Board codes are searchable**: typing `M1AM8` goes straight to that poster
- Posters are listed in walking order: session, then line, then position along the line
- **Saved schedules survive the renumbering.** Selections are re-resolved against the current programme on load (by id, then by title and day), so a poster saved as `P1.58` becomes `M1AM8` and also picks up any corrected abstract or time; entries no longer in the programme are dropped
- The parser now repairs unescaped double quotes in the export instead of failing on them (one poster title, *What Does "Curvy" Mean to You?*, breaks the source JSON outright)

**v1.2.2** (2026-08-06)
- **Corrected programme from the organisers.** Eight posters that the previous export listed twice (Monday evening *and* Thursday morning) now appear once, on Monday evening; one poster (*VisionBridge*) moved from Thursday morning to Monday evening. The programme is now **614 presentations** (was 622), with **442 posters** (was 450)
- Two entries had another submission's abstract attached and are now correct: the talk *Stress and visual illusions: Is there a relationship?* and the poster *Pre-microsaccade enhancement of the current and future foveal input*
- One poster title shortened to the submitted version (*Mind the Affective Gap: Human vs. Machine Perception of Emotion in Biological Motion*), one affiliation corrected (University of Cambridge now carries its country code), and three abstracts regained their paragraph breaks
- Poster board numbers shift accordingly, since they are numbered 1..n in programme order within each session — the two abstract-less entries are now `T397` and `P2.36` (`P2.35` before this refresh)
- The corrected export still truncates 27 abstracts at the first double-quote character, so `scripts/recovered_abstracts.json` is still applied
- **Author names are now whitespace-normalised.** Seven source records carried a stray tab or double space inside a name (`Akihisa\tTakemura`, `Frederick  A.A. Kingdom`, …), which rendered oddly and stopped the full name matching in search; the parser now collapses whitespace inside names, while abstracts keep their paragraph breaks

**v1.2.1** (2026-08-03)
- **Restored 29 truncated abstracts.** The organisers' updated export cut every abstract off at the first double-quote character; the parser now backfills the full text from the previous complete dataset (`scripts/recovered_abstracts.json`), verified to match each abstract's opening. Only `T397` and `P2.35`, which never had an abstract, remain blank

**v1.2.0** (2026-08-03)
- **Author affiliations** added for every talk and poster, from an updated programme supplied by the organisers: each author now shows superscript affiliation number(s) with a numbered institution list in the detail sheet (matching the IMRF/VSS schedulers)
- Programme refreshed to **622 presentations** (was 618): 45 symposium talks (was 46) and 450 posters (was 445)
- Every presentation now has a published title — the previous six **[Title to be announced]** placeholders are resolved; two entries (one talk, one poster) still lack an abstract in the source

**v1.1.2** (2026-06-29)
- Poster board numbers now use the authors' blue, making them easier to tell apart from the title

**v1.1.1** (2026-06-29)
- Added poster board numbers (the programme has none): each poster shows `P{session}.{board}` (e.g. P5.12), numbered 1..n within each of the seven poster sessions, displayed before the title like the IMRF/VSS schedulers

**v1.1.0** (2026-06-29)
- Added a **Social** category with four events (Opening Reception, Illusion Night, Conference Dinner, Farewell Party), exported to the calendar as full evening blocks
- Keynotes now show their real **lecture titles and abstracts** (parsed from the conference page dropdowns) and confirmed durations — Perception 120 min, Spotlight in Vision & Rank Prize 90 min — exported as full-length events; the TBC time marker was removed
- **Talks are grouped by session**: each (day, session, room) block is listed contiguously and chronologically, with parallel sessions following one another instead of interleaving slot by slot
- Six contributions missing a title in the source programme now show **[Title to be announced]** (corrected details requested from the organisers)
- GitHub Pages deploy workflow updated to Node 24 action versions
- Added a printable QR-code flyer (`ECVP_2026_Scheduler_QR.pdf`) and generator script

**v1.0.0** (2026-06-29)
- Initial release for ECVP 2026 (Bournemouth, August 23–27)
- 618 presentations parsed from the official online programme: 3 keynotes, 10 symposia (46 symposium talks), 120 talk-session talks, 445 posters, and 4 social events
- Full-text search, day/type filters, personal schedule, and Google/Apple Calendar export (anchored to `Europe/London`)
- PWA with offline support and home-screen install
- Adapted from the IMRF 2026 / VSS 2026 Schedule Organizer codebase (Expo SDK 56)

---

## Data Source & Attribution

Presentation data is sourced from the **official ECVP 2026 online programme** for the European Conference on Visual Perception. This app was inspired by [MiYoung Kwon's](https://kwonlab.psych.umn.edu) HTML conference scheduler, which she generously shared with the community.

## Support

- **ECVP 2026 website:** https://ecvp2026.uk/
- **GitHub:** https://github.com/markwgreenlee/ecvp-2026-scheduler
- **Issues:** Open a GitHub issue

---

ECVP 2026 | August 23–27, 2026 | Bournemouth, UK
