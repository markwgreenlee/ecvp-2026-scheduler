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

### During the conference

The **Now** tab answers "where do I need to be". It lists every session running at this moment — keynote, talk session, symposium or poster session — with the room, the presentation currently on, and a star against anything in your schedule. Between sessions it counts down to what's next, so at the end of a coffee break it tells you how long you have and where to go.

Times are reckoned in Bournemouth time, so the tab is right even if your phone's clock is still on the timezone you flew in from.

### Getting reminded

Two things nudge you, and it's worth knowing which is which:

- **Calendar reminders** work with the app closed. Pick a lead time under **Settings → Session Reminders** (default 10 minutes), then export from the Schedule tab. On an iPhone, iPad or Mac the first button reads **Apple Calendar**; elsewhere it reads **Calendar file (.ics)**. Either way it hands over your whole schedule in one step, with an alarm on every event — choose **Add All** when Calendar opens. Your phone does the alerting from then on, offline and in the background.
  Re-exporting later **updates** those events rather than duplicating them, because each carries a stable identifier. So add more talks, export again, and your calendar simply catches up.
- **The in-app bar** appears at the top when one of your picks is about to start, but only while the app is open.

> **Why the app can't text you or buzz your phone by itself.** SMS needs a server and your phone number — this app has neither, and collecting numbers would make it something quite different. And a web app cannot schedule a notification for later: there's no such browser API, and a push would need a server awake at the right minute to send it. Handing the reminder to your calendar is what gets an alert to a pocketed phone without any of that.

### Move your schedule to another device

Build your schedule on a laptop, then carry it to your phone — no account, no file, no cable.

1. On the **laptop**, open **Settings** in the app. Under *Send this schedule*, a QR code appears
2. On the **phone**, open the app, go to **Settings**, and tap **Scan a code**
3. Allow camera access, then point the phone at the laptop screen
4. The app asks whether to **Merge** (keep what's there and add the rest) or **Replace** (make this device match)

Scanning from *inside* the app matters: the schedule then lands in the app you scanned from, including when the app lives on your iPhone's Home Screen. You can also point the phone's own camera app at the code, but on iPhone that opens the link in Safari, which does not always share storage with a Home Screen app.

The code holds only the list of presentations you picked — nothing is uploaded, and no server sees it. It works the same way for handing your picks to a colleague. Schedules of up to about 400 presentations fit in a single code.

> **If the camera won't work:** the scanner falls back to a box where you can paste the link, which is shown as text under the QR code on the sending device. Camera access needs a secure connection — that's automatic on the published site.

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

### The Now tab shows the wrong time

Times come from the device clock, converted to Bournemouth time. If the tab looks wrong, the device clock itself is wrong — check that automatic date and time is on (see *Calendar times are wrong* above).

### I'm not getting reminders

- Reminders ride on calendar events, so they only exist for presentations you actually exported. Export again after changing the lead time — existing calendar events keep the alarm they were created with
- On the web, the **Apple Calendar** / **Calendar file** (`.ics`) button is the one that carries alarms. Google's event-edit page cannot accept a reminder through a link, so events added that way use whatever default your Google calendar applies
- On an iPhone the button opens the share sheet; pick **Calendar**, or save the file and tap it. If nothing appears to happen in a Home Screen install, open the app in Safari and export from there
- The in-app bar only appears while the app is open. Nothing the app itself can do will alert a phone that's locked in a pocket — that's what the calendar alarm is for

### A shared schedule didn't import

- The link must come from this app. A link from the VSS or IMRF scheduler is rejected, by design
- Links are one-shot per page load: the app clears the code from the address bar once it has read it, so reloading won't prompt again. Scan the code again
- Use **Settings → Scan a code** inside the app rather than the phone's camera app. Scanning from the camera app opens Safari, and on iPhone a Home Screen app may not share storage with Safari
- If the camera is blocked, iOS grants it per-site: **Settings → Apps → Safari → Camera**. The scanner also accepts the link pasted as text

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
- **Tap an author's name** in that sheet to see everything else they are presenting, and jump straight to any of it
- Build a personal schedule — add/remove directly from the detail sheet
- **Your schedule is a day-by-day itinerary**, ordered by day and start time, with the same cards, day/type filters and tap-for-abstract as Search. Filter to a single day and the calendar export covers just that day
- Export to **Google Calendar** (opens in browser); the native iOS build can also add events directly to **Apple Calendar**
- **What's on now** — a live tab showing every session running at this moment with its room, the presentation currently on, and your own picks starred; counts down to the next session during breaks. Reckoned in conference time, not the phone's timezone
- **Apple Calendar from the web app** — one button hands your whole schedule to Apple Calendar (or Outlook, or any calendar app) as a single `.ics`, with a reminder on every event so your phone alerts you with the app closed. Re-exporting updates events instead of duplicating them
- **Move your schedule between devices by QR code** — Settings shows a code encoding your picks, and a built-in scanner reads one from another screen. Scanning inside the app means the schedule lands in the app, Home Screen installs included. Works for sharing with a colleague too
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

### One origin, three apps

All three schedulers are served from `markwgreenlee.github.io`, which means they share a single
`localStorage`. They previously used identical keys (`selectedSessions`, `reminderMinutes`), so
opening one app overwrote another's saved schedule — and because a saved schedule is reconciled
against the current programme on load, a foreign schedule resolves to nothing and silently
disappears.

Every key is now namespaced with `conference.storagePrefix` via `src/utils/storage.js`. A schedule
saved under the old bare key is still read once as a fallback and written back namespaced;
reconciliation drops anything belonging to another conference. The old key is left in place so the
sibling apps can do the same migration.

### Porting to the VSS and IMRF apps

All three schedulers share this codebase. Everything conference-specific lives in
`src/config/conference.js` — share tag, timezone, presentation-type labels, poster grouping,
calendar identifiers — so the modules under `src/utils/` are byte-identical across the three
repositories. Porting a fix means copying the utils and editing that one file.

What the config has to get right, learned from the other two datasets:

- **`timeZone`** drives both the live clock and the UTC stamps in the `.ics`. The conversion is
  derived from the zone rather than a fixed offset, so it stays correct in London, Florida or
  Genova and across a daylight-saving change. `fallbackUtcOffsetMinutes` applies only where the
  platform has no timezone-aware `Intl`.
- **`shareTag`** must be unique. It is what makes a VSS link fail cleanly in the IMRF app.
- **`kindLabels`** needs an entry for any irregular plural. Unlisted kinds are humanised, so IMRF's
  `symposium_overview` reads as *Symposium overviews* rather than as a raw field value.
- **`cityName`** is shown beside the clock in the Now tab, so no one is told the time in a city
  they are not in.
- **`kindAlias`** folds a kind into another everywhere: no filter chip of its own, matched by its
  target's chip, and its entries join the target's session block. IMRF carries a separate
  `symposium_overview` record per symposium — without this it gets a chip nobody wants and every
  symposium is listed twice in the live view. Cards keep their own badge, so an overview still
  reads as one, and it sorts first within its symposium because the tie-break keeps programme
  order.
- **`posterSessionName`** decides how poster topic lines collapse. ECVP titles are
  `Poster Session 1 · Attention`, so the topic is dropped. VSS titles carry no session prefix, so it
  returns a constant and posters group by hall instead — 15 blocks rather than 107.

Two things the other datasets exposed that the shared code now handles:

- **Not every programme times each talk.** All of IMRF's sessions, and six of VSS's, give every talk
  the session's start time. `hasRunningOrder()` detects this and the Now tab shows
  *"5 talks in this session"* instead of naming a talk it cannot know is on.
- **Poster blocks are keyed by room.** VSS runs two halls at the same hour; without the room they
  would merge into one block wearing whichever room sorted first.

### Session views

Tapping the session name in a presentation's detail card opens the rest of that session — every talk
or poster in it, in order, each tappable through to its own abstract. The name carries the count
(`Motion Perception  ·  all 6`) so it is clear there is something behind it, and it is only a link
when the session holds more than the presentation being read.

The grouping is `buildBlocks()`, already built for the Now tab, so this reuses the session
definition rather than inventing a second one: a poster session is one block per hall, and a talk
session's end is derived from its last talk where the data gives no `session_end`.

The author sheet and the session sheet are one component, `PresentationSheet`. Both want the same
thing — a list of presentations over the detail card — so they share it, and choosing an entry
replaces what the card shows rather than stacking another layer. That means author → paper →
session → another paper walks indefinitely without a pile of sheets to dismiss.

### Linking authors across the programme

`src/utils/authors.js` answers one question: when are two author strings the same person? The
programme records a name however each submission typed it, so one person genuinely appears several
ways — in the 2026 data, *Mark Greenlee* twice and *Mark W. Greenlee* once, on three different
abstracts.

`authorKey()` therefore ignores case, accents, hyphenation, spacing and initials:
`"Mark W. Greenlee"` and `"Mark Greenlee"` both reduce to `mark greenlee`. That also merges
`Michael H. Herzog` with `Michael Herzog` and `Stéphanie Caharel` with `Stephanie Caharel`, while
keeping `Li-Li Yeh` apart from `Lu-Chun Yeh` and `Zaifeng Gao` from `Zhihan Gao` — a
surname-plus-initial rule would wrongly join those last two, which is why it is not used.

Two genuinely different people sharing a first and last name would be merged. No instance exists in
the ECVP, VSS or IMRF programmes, and the data carries no signal that would separate them: the
names that look suspicious on an affiliation check (Heiko Schütt, Melissa Võ, Peter Neri) are single
individuals who publish across institutions. If a real namesake ever appears, an override file
keyed on the raw strings is a small addition rather than a rewrite.

Details worth knowing:

- The heading shows the **longest** spelling found, as the most complete form of the name.
- Only authors with work **beyond the abstract being read** are linked. About three names in four
  appear exactly once, and a link back to the page you are already on reads as broken — so most
  names stay plain text, and an underline genuinely means "presenting elsewhere too".
- Names are linked only in the detail card, not on list cards: a list card is itself one large tap
  target, and nesting smaller ones inside it makes a fumbled tap do the wrong thing.
- `AuthorSheet` renders as an overlay **inside** the detail card rather than as its own `Modal`.
  A modal within a `pageSheet` modal is unreliable on iOS, and choosing a presentation replaces what
  the card shows rather than stacking another layer, so author → paper → co-author → paper walks
  indefinitely without a pile of sheets to dismiss.
- The index is built once per programme in `DataContext` and memoised; it is 2,100 name slots for
  ECVP and 4,300 for VSS.

### What's on now, and session blocks

`src/utils/conferenceTime.js` converts the device clock into conference-local time with
`Intl.DateTimeFormat` and a `Europe/London` timezone, falling back to a fixed +01:00 offset if the
platform cannot do timezone-aware formatting. Everything time-related reads from it, so an attendee
whose phone never updated its timezone still sees the right thing.

`src/utils/blocks.js` groups the programme into the blocks a person actually walks to.
Keynotes, socials and poster sessions carry a `session_end` in the data; **talk and symposium
sessions do not**, so their end is the last talk plus one 15-minute slot. That reproduces the real
timetable (talks 10:30–12:00, 14:00–15:30, 17:00–18:30; posters 09:00–10:30 and 15:30–17:00) and
correctly makes the shorter symposia finish early. Poster sessions collapse their seven topic lines
into one block, since they are one place at one time.

If a future export starts supplying `session_end` for talks, the derivation steps aside
automatically — a declared end always wins.

### Reminders

There is no server, so there is no push. A PWA cannot schedule a local notification for later
either: the Notification Triggers proposal was never shipped, and Web Push requires a server awake
at the moment of delivery. Reminders are therefore delegated to the operating system's calendar:

- Native build — `expo-calendar` events are created with `alarms: [{ relativeOffset: -minutes }]`.
- Web — `src/utils/calendar.js` builds an `.ics` with a `VALARM` per event. Google's event-edit URL
  has no reminder parameter, which is why the calendar file exists at all; it also adds the whole
  schedule in one step instead of one event at a time. **This is the Apple Calendar path for the
  PWA** — no web API writes to Apple Calendar directly — so on Apple platforms the button is
  labelled accordingly (`src/utils/platform.js`).

Getting the file to iOS is a fallback chain, not a single call, because no one mechanism is
dependable there and downloads are least dependable of all inside a Home Screen install:

1. `navigator.share({ files })` — the share sheet, which does work when installed. Tried only on
   iOS, so desktops still get a plain download rather than a surprise share dialog.
2. An `<a download>` click on a blob URL — correct everywhere on desktop.
3. `window.open` on the blob, letting the OS decide.

Only the first can be feature-detected, so steps 2 and 3 are a chain rather than a retry after a
detected failure. A user *cancelling* the share sheet (`AbortError`) stops there and does not fall
through — that is a decision, not a failure.

Event UIDs are `<id>@ecvp-2026-scheduler` and therefore stable across exports, so a second import
updates the existing events instead of duplicating them. The Google flow has no such property,
which is why it carries its own `googleExportedIds` bookkeeping.

The `.ics` writer folds content lines at 75 **octets**, not characters, and never splits a
multi-byte character — 164 of the 614 entries contain non-ASCII text, and a character-based fold
silently produces over-long lines that some calendar apps reject.

### Sharing a schedule between devices

A schedule is shared as the app's own URL with the selection in the fragment:

```
https://markwgreenlee.github.io/ecvp-2026-scheduler/#s=ecvp26.1.KN1,M1AM9,T131,…
```

`ecvp26` tags the conference and `1` the format, so a link made by the VSS or IMRF scheduler is
rejected with a message instead of being half-read. The payload is the list of ids — board codes
for posters — which means a shared link picks up corrected titles, times and abstracts on the
receiving device rather than carrying a stale copy of the programme. Ids that no longer exist are
reported in the import prompt and skipped.

The **fragment** matters: fragments are never sent to the server and never enter the service
worker's cache keys, so a shared schedule stays between the two devices. The app reads it on load,
clears it from the address bar (so a reload doesn't re-prompt), and holds the selection until the
user chooses Merge or Replace.

QR rendering uses `qrcode-generator` — pure JavaScript, no dependencies of its own, no native
module. On web the matrix is painted to a canvas and shown as a PNG; the native build draws it as
views, collapsing runs of same-coloured modules. At error-correction level M a 50-presentation
schedule is a 73×73 code, and about **408 presentations** is the ceiling for a single QR; past that
the panel shows the link as text instead.

Reading a code back is `src/components/ScheduleScanner.js`: `getUserMedia` with the rear camera into
a `<video>`, frames drawn to an offscreen canvas at 800px wide and decoded with `jsqr` on each
animation frame. It is **web only** — `Platform.OS !== 'web'` renders nothing, because a native
scanner would mean adding `expo-camera`, a permission string and a rebuild for a build that is not
currently distributed. The video needs `playsinline` and `muted` or iOS takes it fullscreen and
refuses to autoplay. If the camera is denied or absent the same sheet offers a paste box.

Every route in — opening a shared link, scanning, pasting — funnels through
`buildPendingImport()`, so the confirmation sheet and the error messages are identical whichever
way a schedule arrives.

### Offline at the venue

The service worker splits what it serves in two, because conference WiFi does not fail cleanly —
it stalls, and a worker that waits on a socket that never closes looks like a frozen app rather
than an error.

- **Content-addressed files** — the JS bundle, icon fonts, images — are served **cache-first**.
  Their filename carries a hash, so the bytes behind a URL can never change and a cached copy is
  never stale. This is almost the whole payload, so the app opens instantly and is immune to a bad
  network.
- **`index.html`** is served **network-first with a 2-second timeout**, falling back to cache. It
  is tiny, and it is how a new programme reaches a device: the data is compiled into the bundle, so
  a data change produces a new bundle hash and therefore a new `index.html`.

Measured against a server deliberately stalled for 30 seconds: the previous worker rendered in
**31.3 s**, this one in **3.3 s**.

On install the worker reads the shell and pre-caches the hashed files it references. Without that,
the bundle was only cached on a *second* visit — a worker does not control the page that installs
it — which quietly contradicted the advice to open the app once before travelling. One visit is now
enough: verified by wiping the browser's HTTP cache, killing the server, and reloading.

When the timeout fires, the cached page is served and the request continues in the background. If
what arrives differs from what was served, the page shows *"An updated programme is available"* with
a reload. That covers the attendee who opened the app before the programme was frozen.

Two things this got wrong on the way, worth not repeating:

- `event.waitUntil()` must be called **synchronously** in the fetch handler. Called after an `await`
  the event no longer accepts it, so nothing keeps the worker alive, it is killed the moment it
  answers from cache, and the background request dies silently with it.
- The response used for the comparison must be cloned **before** the cached response is returned.
  Once a body is being consumed, cloning it throws and the notification is lost.

The cache name carries the app version, stamped into `sw.js` at deploy time. It was previously
hard-coded and had drifted several releases out of date, so old caches were never discarded.

### Checking the programme data

```bash
python3 scripts/validate_data.py                # checks assets/ecvp-data.json
python3 scripts/validate_data.py candidate.json # check a new export first
```

This runs in CI before every build, so bad data cannot deploy. It is the same script in all three
schedulers and finds the data file on its own.

It exists because `room`, `day` and `kind` are **identifiers, not labels**. The live view groups
sessions by room, the filter chips are built from the set of kinds, and days are ordered by their
date. A value differing only in case silently becomes a second room, a second chip or a second day,
and reading the file will not catch it — which is exactly how one VSS session came to record
`Talk Room 1` against the other 110 entries' `TALK ROOM 1`.

It complements `scripts/parse_ecvp.py` rather than replacing it: the parser checks what only it can see while
rebuilding the data (truncated abstracts, board codes, damaged author-affiliation mappings) and is
run by hand; this runs unattended on every deploy and catches the controlled-vocabulary drift the
parser does not look for.

Errors (exit 1, stops the deploy): two spellings of one room, day or kind; a day carrying two dates;
duplicate or missing ids; a time that is not `HH:MM`; a missing date. Warnings (exit 0): stray
whitespace, empty controlled fields.

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

**v1.3.8** (2026-08-21)
- **The organisers' final talks export is in, and it confirms the room correction.** Their 2026-08-21 file puts `T506`, `T361`, `T327` and `T397` in Bayview Suite at source — exactly what v1.3.7 corrected — so `ROOM_OVERRIDE` reported itself redundant and has been removed. Adopting the export changed the built data not at all: byte-identical. The missing closing quote on `T74` is fixed too, so the file needs no repair on import and nothing in the source is hand-edited any more
- **Affiliations no author is attached to are no longer shown.** Four entries listed an institution with nothing pointing at it, usually a co-author who moved on: `M2PM1`, `M6PM4`, `M7AM9` and `T3AM2`. Numbering is left alone rather than closed up, so the superscripts beside the authors still match the list
- **Six records are deliberately left as supplied**, because their author-to-affiliation mapping is damaged at source and "unreferenced" cannot be determined. `M2PM7`, `T2AM9`, `305` and `96` have a lost comma inside `aff` — `[1,2]` serialised as the float `[1.2]` — so an author attached to two institutions reads as attached to one. `96` is the sharp case: on the truncated reading its third affiliation looks unused, and pruning would have deleted a real one. `M6PM9` cites affiliation 9 of 8, and `W4PM1` cites 0. All six are reported to the organisers and named in the validation report on every run

**v1.3.7** (2026-08-20)
- **The CPC @ ECVP symposium is now all in one room.** The export put its opening talk (`T387`, Graf, Thursday 14:00) in Bayview Suite and the other four in Purbeck Lounge — where the *Spatial Vision* session was already running 14:00–15:15. The four are corrected to Bayview Suite, which was otherwise empty between 11:45 and 17:00
- **This was the last room double-booking in the programme**, and the check now reports zero. It also split the symposium into two blocks in the schedule view, since talks are grouped by `(date, session, room)`; the five now list contiguously
- Applied as a checked `ROOM_OVERRIDE` in `parse_ecvp.py` rather than an edit to the export, so the organisers' next file cannot silently revert it. The override verifies the export still says `Purbeck Lounge` before changing anything: if the organisers fix it at source it reports itself redundant and asks to be removed, and if the export says anything else it warns and leaves the value alone. Reported to the organisers; remove the override once their file is corrected
- The validation report gained a `rooms corrected` line, so any override in force is visible on every run

**v1.3.6** (2026-08-20)
- **The Thursday 17:00 symposium moved room**, per the organisers' 2026-08-20 talks export: *Visuomotor transforms in prostheses, virtual reality, and teleoperation* (`T74`, `T75`, `T110`, `T379`) moves from **Bayview Suite** to **Purbeck Lounge**. The other 53 Bayview Suite entries are unaffected
- **One malformed record repaired before import, and reported to the organisers.** The export was missing a closing quote on `T74`'s room field — `"Room": "Purbeck Lounge, "Title": …` — which swallowed the title into the room string. Imported as-is, that talk would have lost its title entirely and displayed a room containing the title text. One character was added to close the quote; nothing else in the file was touched
- With that closed the export parses clean: `extract_json_array` now reports zero repaired quotes, where the raw file needed three, all at that one site. The previous talks export needed none
- Verified against the previous release: the source differs in exactly four `Room` fields and the built data in exactly those four entries, `room` only. Same 614 ids, nothing added, removed, rescheduled or reworded

**v1.3.5** (2026-08-20)
- **One poster author's affiliation corrected**, per the organisers' 2026-08-20 export: on `M6PM4` (*Retinotopic specificity of the perceptual effects of focused transcranial ultrasound stimulation of the primary visual cortex*), Julien Besle is now listed under University of Plymouth alongside his four co-authors instead of University of Iceland
- The source export differs from the previous one in exactly one field — that author's affiliation index — and the built data differs in exactly one entry. Same 614 ids, same 442 posters, nothing else touched
- Known, reported to the organisers: `M6PM4` still carries *University of Iceland (UK)* as affiliation 2, which no author now references, so it renders with nothing pointing to it. Four other posters (`M7AM9`, `M2PM1`, `M2PM7`, `T3AM2`) already list affiliations no author cites. The app shows the organisers' affiliation list as supplied rather than pruning it, so these are fixed at source

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
