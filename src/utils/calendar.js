// Shared between the Google, Apple and .ics exports so the three agree on when
// an event starts and how long it runs.

// The whole programme sits in British Summer Time; the rest of the app makes
// the same assumption when it builds Date objects for the calendar.
export const CONFERENCE_UTC_OFFSET = '+01:00';

// Keynotes and socials run for their whole advertised block; everything else
// is a 15-minute slot.
const FULL_BLOCK_KINDS = ['social', 'keynote'];

export const getEventTimes = (session) => {
  const startStr = session.time || session.session_start || '09:00';
  const [sh, sm] = startStr.split(':').map(Number);
  let eh, em;
  if (FULL_BLOCK_KINDS.includes(session.kind) && session.session_end) {
    [eh, em] = session.session_end.split(':').map(Number);
  } else {
    const tot = sh * 60 + sm + 15;
    eh = Math.floor(tot / 60);
    em = tot % 60;
  }
  return [sh, sm, eh, em];
};

const pad2 = (n) => String(n).padStart(2, '0');

export const toTitleCase = (str) =>
  str.toLowerCase().replace(/\b\w/g, c => c.toUpperCase());

export const eventTitle = (session) =>
  session.room ? `[${toTitleCase(session.room)}] ${session.title}` : session.title;

const stamp = (date, h, m) => {
  const d = new Date(`${date}T${pad2(h)}:${pad2(m)}:00${CONFERENCE_UTC_OFFSET}`);
  return d.toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '');
};

// iCalendar escaping: backslash first, then the delimiters, then newlines.
const esc = (text) => String(text || '')
  .replace(/\\/g, '\\\\')
  .replace(/;/g, '\;')
  .replace(/,/g, '\\,')
  .replace(/\r?\n/g, '\\n');

// RFC 5545 caps a content line at 75 *octets*, not characters, and an abstract
// blows straight past it. Counting characters would let accented author names
// and en-dashes overflow the limit, and splitting mid-character would corrupt
// them outright, so measure UTF-8 width and never break inside one.
const utf8Width = (ch) => {
  const cp = ch.codePointAt(0);
  if (cp < 0x80) return 1;
  if (cp < 0x800) return 2;
  if (cp < 0x10000) return 3;
  return 4;
};

const fold = (line) => {
  const pieces = [];
  let current = '';
  let width = 0;
  let limit = 75;
  for (const ch of [...line]) {
    const w = utf8Width(ch);
    if (width + w > limit) {
      pieces.push(current);
      current = '';
      // A continuation line opens with a space, which counts toward the limit.
      width = 1;
      limit = 75;
    }
    current += ch;
    width += w;
  }
  pieces.push(current);
  return pieces.join('\r\n ');
};

export const buildIcs = (sessions, reminderMinutes) => {
  const now = new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '');
  const lines = [
    'BEGIN:VCALENDAR',
    'VERSION:2.0',
    'PRODID:-//ECVP 2026 Schedule Organizer//EN',
    'CALSCALE:GREGORIAN',
    'METHOD:PUBLISH',
  ];

  for (const s of sessions) {
    const date = s.date || '2026-08-24';
    const [sh, sm, eh, em] = getEventTimes(s);
    const authors = Array.isArray(s.authors) ? s.authors.join(', ') : (s.authors || '');
    lines.push(
      'BEGIN:VEVENT',
      fold(`UID:${s.id}@ecvp-2026-scheduler`),
      `DTSTAMP:${now}`,
      `DTSTART:${stamp(date, sh, sm)}`,
      `DTEND:${stamp(date, eh, em)}`,
      fold(`SUMMARY:${esc(eventTitle(s))}`),
      fold(`LOCATION:${esc(s.room || '')}`),
      fold(`DESCRIPTION:${esc(
        `Authors: ${authors}\n\nSession: ${s.session_title || ''}\n\nAbstract: ${s.abstract || ''}`
      )}`),
    );
    if (reminderMinutes > 0) {
      lines.push(
        'BEGIN:VALARM',
        `TRIGGER:-PT${reminderMinutes}M`,
        'ACTION:DISPLAY',
        fold(`DESCRIPTION:${esc(s.title)}`),
        'END:VALARM',
      );
    }
    lines.push('END:VEVENT');
  }

  lines.push('END:VCALENDAR');
  return lines.join('\r\n');
};
