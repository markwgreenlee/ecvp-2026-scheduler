// Everything time-related is reckoned in the conference's own timezone, not the
// phone's. An attendee whose clock is still on home time, or who never let the
// phone update it, should still be told the right thing — and the calendar
// export already anchors to the same zone.

export const CONFERENCE_TZ = 'Europe/London';

// Used only if the platform cannot do timezone-aware formatting. The whole
// programme sits inside British Summer Time, and ExportButton makes the same
// +01:00 assumption.
const FALLBACK_OFFSET_MINUTES = 60;

let formatter;
const getFormatter = () => {
  if (formatter !== undefined) return formatter;
  try {
    formatter = new Intl.DateTimeFormat('en-GB', {
      timeZone: CONFERENCE_TZ,
      year: 'numeric', month: '2-digit', day: '2-digit',
      hour: '2-digit', minute: '2-digit', hourCycle: 'h23',
    });
    // Prove it actually honours the timezone before trusting it.
    formatter.format(new Date());
  } catch (_) {
    formatter = null;
  }
  return formatter;
};

// -> { date: 'YYYY-MM-DD', time: 'HH:MM', minutes: <since midnight> }
export const conferenceNow = (instant = new Date()) => {
  const fmt = getFormatter();
  if (fmt) {
    const parts = {};
    for (const p of fmt.formatToParts(instant)) parts[p.type] = p.value;
    const hour = Number(parts.hour) % 24;
    const minute = Number(parts.minute);
    return {
      date: `${parts.year}-${parts.month}-${parts.day}`,
      time: `${String(hour).padStart(2, '0')}:${parts.minute}`,
      minutes: hour * 60 + minute,
    };
  }
  const shifted = new Date(instant.getTime() + FALLBACK_OFFSET_MINUTES * 60000);
  const iso = shifted.toISOString();
  return {
    date: iso.slice(0, 10),
    time: iso.slice(11, 16),
    minutes: shifted.getUTCHours() * 60 + shifted.getUTCMinutes(),
  };
};

export const toMinutes = (hhmm) => {
  if (!hhmm) return null;
  const [h, m] = hhmm.split(':').map(Number);
  if (Number.isNaN(h) || Number.isNaN(m)) return null;
  return h * 60 + m;
};

export const fromMinutes = (mins) => {
  const m = ((mins % 1440) + 1440) % 1440;
  return `${String(Math.floor(m / 60)).padStart(2, '0')}:${String(m % 60).padStart(2, '0')}`;
};

// Whole days between two YYYY-MM-DD dates, ignoring clocks entirely.
export const daysBetween = (fromDate, toDate) => {
  const a = Date.parse(`${fromDate}T00:00:00Z`);
  const b = Date.parse(`${toDate}T00:00:00Z`);
  if (Number.isNaN(a) || Number.isNaN(b)) return 0;
  return Math.round((b - a) / 86400000);
};

// Minutes from one (date, minutes) point to another.
export const gapInMinutes = (from, toDate, toMinutesOfDay) =>
  daysBetween(from.date, toDate) * 1440 + (toMinutesOfDay - from.minutes);

// "3 days", "1h 08m", "8 min", "now"
export const formatGap = (mins) => {
  if (mins <= 0) return 'now';
  if (mins < 60) return `${mins} min`;
  if (mins < 1440) {
    const h = Math.floor(mins / 60);
    return `${h}h ${String(mins % 60).padStart(2, '0')}m`;
  }
  const days = Math.round(mins / 1440);
  return days === 1 ? 'tomorrow' : `${days} days`;
};
