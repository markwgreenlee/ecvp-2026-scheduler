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

> **A couple of entries are still incomplete in the source programme.** Two contributions (one talk, one poster) have no abstract published yet; every presentation now has a title. The missing abstracts are being requested from the organisers and will be added when available.

### Can't find presentations

- Try shorter search terms (e.g., "motion" instead of "motion perception")
- Search by author last name (e.g., "Gegenfurtner", "Dijkstra")
- Check that day and type filters are cleared
- Refresh the page to verify all 622 presentations loaded

---

## Features

- **622 presentations** from the official ECVP 2026 online programme — 3 keynotes, 10 symposia (45 symposium talks), 120 talk-session talks, 450 posters, and 4 social events
- Full-text search by title, author, co-authors, abstract, session, and topic
- **Author affiliations** for every talk and poster — authors shown with superscript numbers and a numbered institution list
- Filter by day (Sun–Thu) and type (Keynote / Symposium / Talk / Poster / Social)
- **Tap any card** to read the full abstract, authors, and session details in a pop-up sheet
- Build a personal schedule — add/remove directly from the detail sheet
- Export to **Google Calendar** (opens in browser) or **Apple Calendar** (adds events directly)
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

The organisers' August 2026 app-export truncates every abstract at the first double-quote character (it emits a stray `\` and drops the rest), leaving 29 abstracts cut off mid-sentence and 2 empty. `scripts/recovered_abstracts.json` maps `SubmissionID → full abstract` (recovered from the previous complete dataset, verified to share the same opening text) and the parser uses it to backfill **only** abstracts the source has broken — so a future corrected export supersedes it automatically. Two entries (`T397`, `P2.35`) had no abstract in any version and remain blank pending the organisers.

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

### Project Structure

```
ecvp-2026-scheduler/
├── App.js                          # Entry point, tab navigation, SW registration
├── app.json                        # Expo / PWA configuration
├── assets/
│   ├── icon.png                    # App icon (stylised eye)
│   └── ecvp-data.json              # 622 presentations
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

Each entry in `assets/ecvp-data.json` has: `id`, `kind` (`keynote` / `symposium` / `talk` / `poster` / `social`), `title`, `authors[]`, `author_numbers[]`, `affiliations`, `presenter`, `organizer`, `bio`, `abstract`, `day`, `date`, `room`, `session_title`, `session_kind`, `session_start`, `session_end`, `talk_number`, `time`, `time_tbc`. For talks and posters, `authors[]` and its parallel `author_numbers[]` (superscript affiliation numbers, e.g. `"1"` or `"2,3,4"`) and the numbered `affiliations` block come from the organiser-supplied `Authors`/`Affiliations` fields in the source pages; keynotes and socials leave these as their hand-entered values. Talks/symposia carry a room (Tregonwell Hall, Bayview Suite, Purbeck Lounge); posters have no room in the source, so they are assigned a board number `P{session}.{board}` (e.g. `P5.12`) — one of the seven poster sessions (morning + evening Mon–Wed, Thursday morning, matching the printed grid's "Poster 1"–"Poster 7") and a 1..n board within it — with the topic kept in the session label. Keynote and social entries carry a full `session_end` so they export to the calendar as full-length events (Perception keynote 120 min, the other keynotes 90 min, talks 15 min). `time_tbc` is retained for future use and is currently `false` for all entries.

---

## Version History

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
