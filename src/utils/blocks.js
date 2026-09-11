import { toMinutes, fromMinutes, gapInMinutes } from './conferenceTime';

// "What's on now" works in blocks, not individual presentations: you walk to a
// room for a session, not for one 15-minute talk.
//
// Keynotes, socials and poster sessions carry a session_end in the data. Talk
// and symposium sessions do not, so a block's end is its last talk plus one
// slot — which reproduces the real timetable (10:30-12:00, 14:00-15:30,
// 17:00-18:30) and correctly makes the shorter symposia end early.
export const TALK_MINUTES = 15;

const startOf = (s) => s.time || s.session_start || '';

// Posters name a topic line per session ("Poster Session 1 · Attention"); for a
// live view those seven lines are one place to walk to, so collapse them.
const posterSessionName = (title) => (title || '').split(' · ')[0] || 'Poster Session';

const blockKeyFor = (s) => {
  if (s.kind === 'poster') {
    return `${s.date}|poster|${s.session_start}|${posterSessionName(s.session_title)}`;
  }
  if (s.kind === 'talk' || s.kind === 'symposium') {
    return `${s.date}|${s.kind}|${s.room || ''}|${s.session_title || ''}`;
  }
  return `${s.date}|${s.kind}|${startOf(s)}|${s.session_title || s.title}`;
};

export const buildBlocks = (sessions) => {
  const byKey = new Map();

  for (const s of sessions) {
    const key = blockKeyFor(s);
    if (!byKey.has(key)) {
      byKey.set(key, {
        key,
        kind: s.kind,
        date: s.date,
        day: s.day,
        room: s.room || '',
        title: s.kind === 'poster' ? posterSessionName(s.session_title) : (s.session_title || s.title),
        items: [],
      });
    }
    byKey.get(key).items.push(s);
  }

  const blocks = [];
  for (const block of byKey.values()) {
    block.items.sort((a, b) => {
      const t = (startOf(a) || '').localeCompare(startOf(b) || '');
      return t !== 0 ? t : String(a.id).localeCompare(String(b.id));
    });

    const first = block.items[0];
    const declaredEnd = toMinutes(first.session_end);
    const starts = block.items.map(i => toMinutes(startOf(i))).filter(v => v !== null);
    const start = starts.length ? Math.min(...starts) : toMinutes(first.session_start);

    block.startMinutes = start;
    block.endMinutes = declaredEnd !== null
      ? declaredEnd
      : (starts.length ? Math.max(...starts) + TALK_MINUTES : start + TALK_MINUTES);
    block.start = fromMinutes(block.startMinutes);
    block.end = fromMinutes(block.endMinutes);
    blocks.push(block);
  }

  blocks.sort((a, b) => {
    const d = a.date.localeCompare(b.date);
    if (d !== 0) return d;
    if (a.startMinutes !== b.startMinutes) return a.startMinutes - b.startMinutes;
    return (a.room || '').localeCompare(b.room || '');
  });
  return blocks;
};

// The presentation running at this moment inside a block. Poster sessions have
// no running item — every poster is up for the whole session.
export const currentItem = (block, minutes) => {
  if (block.kind === 'poster') return null;
  let found = null;
  for (const item of block.items) {
    const t = toMinutes(startOf(item));
    if (t !== null && t <= minutes) found = item; else break;
  }
  return found;
};

// now is { date, minutes } in conference time.
export const whatIsOn = (blocks, now) => {
  const live = [];
  const later = [];

  for (const block of blocks) {
    const offset = gapInMinutes(now, block.date, block.startMinutes);
    const endOffset = gapInMinutes(now, block.date, block.endMinutes);
    if (offset <= 0 && endOffset > 0) live.push(block);
    else if (offset > 0) later.push({ block, inMinutes: offset });
  }

  later.sort((a, b) => a.inMinutes - b.inMinutes);
  const soonest = later.length ? later[0].inMinutes : null;
  // Everything starting at the same moment is equally "next" — three parallel
  // rooms should all be listed, not just whichever sorted first.
  const next = soonest === null ? [] : later.filter(l => l.inMinutes === soonest);

  return {
    live,
    next: next.map(n => n.block),
    nextInMinutes: soonest,
    finished: live.length === 0 && later.length === 0,
  };
};

// Your own picks that start within the given window — what the reminder strip
// watches.
export const startingSoon = (selected, now, windowMinutes) => {
  const out = [];
  for (const s of selected) {
    const start = toMinutes(s.time || s.session_start);
    if (start === null) continue;
    const inMinutes = gapInMinutes(now, s.date, start);
    if (inMinutes >= 0 && inMinutes <= windowMinutes) out.push({ session: s, inMinutes });
  }
  out.sort((a, b) => a.inMinutes - b.inMinutes);
  return out;
};
