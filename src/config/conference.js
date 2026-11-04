/**
 * Conference configuration
 *
 * Everything that differs between the ECVP, VSS and IMRF builds of this app.
 * The modules under src/utils/ read from here and are otherwise identical
 * across the three repositories, so porting a fix means copying the utils
 * and editing only this file.
 */

const conference = {
  // --- Meeting identity ----------------------------------------------------
  // What the Home screen says above the fold. Kept here rather than in the
  // screen so that next year's build is a config edit, not a code edit.
  meetingName: 'ECVP 2026',
  societyName: 'European Conference on Visual Perception',
  // Left empty until confirmed: the programme data does not carry it, and a
  // wrong ordinal is worse than none. Home omits the line while it is blank.
  meetingNumber: '',
  venueName: 'Bournemouth International Centre',
  cityLong: 'Bournemouth, UK',
  dateRange: 'August 23 – 27, 2026',
  firstDate: '2026-08-23',
  lastDate: '2026-08-27',
  // Brand colour, used by every screen rather than hard-coded in each.
  accentColor: '#16324f',

  // --- Venue ---------------------------------------------------------------
  // Keys must match the `room` values in the data exactly. `location` is the
  // part only the venue knows and is omitted from the UI while empty. ECVP
  // posters carry no room at all, so they simply show without one.
  rooms: {
    'Tregonwell Hall': { label: 'Tregonwell Hall', location: '' },
    'Bayview Suite': { label: 'Bayview Suite', location: '' },
    'Purbeck Lounge': { label: 'Purbeck Lounge', location: '' },
    'Bournemouth International Centre': { label: 'Bournemouth International Centre', location: '' },
    'Pavilion': { label: 'Pavilion', location: '' },
    'Bournemouth Pier': { label: 'Bournemouth Pier', location: '' },
    'Russell Cotes Art Gallery & Museum (tbc)': { label: 'Russell Cotes Art Gallery & Museum', location: 'to be confirmed' },
  },
  // Floor plans, in order. Metro cannot resolve a require() built at runtime,
  // so each image is named here:
  //   { id: 'level-1', name: 'Level 1',
  //     image: require('../../assets/floors/level-1.png') }
  // While this is empty the Venue screen shows the room directory instead.
  floors: [],
  // Late changes worth interrupting the Home screen for — a moved room, a
  // cancelled session. Shown as an amber banner, newest first:
  //   { id: 'room-change-1', title: 'Room change', body: '…' }
  announcements: [],

  // --- Sharing -------------------------------------------------------------
  // Tags a share link so a code from a sibling app is rejected with a message
  // rather than half-read. Must be unique across the three apps.
  shareTag: 'ecvp26',
  // Only used where there is no window.location to read (the native build).
  shareBaseUrl: 'https://markwgreenlee.github.io/ecvp-2026-scheduler/',

  // --- Time ----------------------------------------------------------------
  // Times in the data are wall-clock times in this zone. Everything the app
  // shows or exports is reckoned here rather than in the device's zone, so a
  // phone still on home time is not misled.
  timeZone: 'Europe/London',
  // Fallback only, for platforms whose Intl cannot do timezone-aware
  // formatting. Daylight saving makes this wrong half the year, so it is a
  // last resort rather than the normal path: pick the offset in force during
  // the conference itself.
  fallbackUtcOffsetMinutes: 60,
  // Defensive default for an entry with no date. Every entry in the current
  // data has one, so this only guards a malformed export.
  fallbackDate: '2026-08-24',
  // Named in the live view, so nobody is told the clock is in another city.
  cityName: 'Bournemouth',

  // --- Programme shape -----------------------------------------------------
  // Order the filter chips appear in. Kinds present in the data but missing
  // here are appended alphabetically rather than hidden.
  kindOrder: ['keynote', 'symposium', 'talk', 'poster', 'social'],
  // Irregular plurals and anything that should not read as its raw field
  // value. Unlisted kinds are humanised automatically ('symposium_overview'
  // becomes 'Symposium overview' / 'Symposium overviews').
  kindLabels: {
    keynote: { one: 'Keynote', many: 'Keynotes' },
    symposium: { one: 'Symposium', many: 'Symposia' },
    talk: { one: 'Talk', many: 'Talks' },
    poster: { one: 'Poster', many: 'Posters' },
    social: { one: 'Social', many: 'Social' },
  },
  // Kinds whose calendar event spans the whole advertised block instead of a
  // single presentation slot.
  fullBlockKinds: ['social', 'keynote'],
  // Length of one presentation slot, used to close a session block when the
  // data gives no session_end.
  talkMinutes: 15,
  // Poster titles here are 'Poster Session 1 · Attention', and the seven topic
  // lines of one session are a single place to walk to, so the topic is
  // dropped for the live view. Conferences whose poster titles carry no
  // session prefix should return the title unchanged.
  posterSessionName: (title) => (title || '').split(' · ')[0] || 'Poster session',
  // Kinds that are really part of another kind. An aliased kind gets no filter
  // chip of its own and is matched by its target's chip, and its entries join
  // the target's session block. IMRF carries a separate 'symposium_overview'
  // record per symposium; without this it would get a chip nobody wants and
  // list every symposium twice in the live view. Cards keep their own badge,
  // so an overview still reads as one.
  kindAlias: {},

  // --- Calendar export -----------------------------------------------------
  icsFileName: 'ecvp-2026-schedule.ics',
  scheduleFileName: 'ecvp-2026-my-schedule.json',
  icsProductId: '-//ECVP 2026 Schedule Organizer//EN',
  // Makes event UIDs stable and unique, so re-importing updates events rather
  // than duplicating them, and two apps' events never collide.
  uidDomain: 'ecvp-2026-scheduler',

  // --- Local storage -------------------------------------------------------
  // All three apps are served from markwgreenlee.github.io, so they share one
  // localStorage. Without a prefix they overwrite each other's schedules:
  // opening VSS would wipe an ECVP schedule and vice versa.
  storagePrefix: 'ecvp-2026',
};

export default conference;
