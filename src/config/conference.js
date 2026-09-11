/**
 * Conference configuration
 *
 * Everything that differs between the ECVP, VSS and IMRF builds of this app.
 * The modules under src/utils/ read from here and are otherwise identical
 * across the three repositories, so porting a fix means copying the utils
 * and editing only this file.
 */

const conference = {
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
  // Kinds that are really part of another kind's session block. IMRF carries a
  // separate 'symposium_overview' record per symposium, which would otherwise
  // list every symposium twice in the live view.
  blockKindAlias: {},

  // --- Calendar export -----------------------------------------------------
  icsFileName: 'ecvp-2026-schedule.ics',
  icsProductId: '-//ECVP 2026 Schedule Organizer//EN',
  // Makes event UIDs stable and unique, so re-importing updates events rather
  // than duplicating them, and two apps' events never collide.
  uidDomain: 'ecvp-2026-scheduler',
};

export default conference;
