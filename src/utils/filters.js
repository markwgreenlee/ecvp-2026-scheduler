// Day and type chips are derived from the data rather than hard-coded, so the
// same screens work for VSS and IMRF, which run on different days and need not
// carry every presentation type.

const KIND_ORDER = ['keynote', 'symposium', 'talk', 'poster', 'social'];

const KIND_LABELS = {
  keynote: 'Keynotes',
  symposium: 'Symposia',
  talk: 'Talks',
  poster: 'Posters',
  social: 'Social',
};

export const kindLabel = (kind) =>
  KIND_LABELS[kind] || kind.charAt(0).toUpperCase() + kind.slice(1) + 's';

// Day names in calendar order, ordered by each day's ISO date rather than by a
// fixed Sunday-first list.
export const daysInOrder = (sessions) => {
  const dateOf = new Map();
  for (const s of sessions) {
    if (s.day && !dateOf.has(s.day)) dateOf.set(s.day, s.date || '');
  }
  return [...dateOf.entries()]
    .sort((a, b) => a[1].localeCompare(b[1]))
    .map(([day]) => day);
};

export const kindsInOrder = (sessions) => {
  const present = new Set(sessions.map(s => s.kind).filter(Boolean));
  return [
    ...KIND_ORDER.filter(k => present.has(k)),
    ...[...present].filter(k => !KIND_ORDER.includes(k)).sort(),
  ];
};

export const matchesFilters = (session, day, kind) =>
  (!day || session.day === day) && (!kind || session.kind === kind);
