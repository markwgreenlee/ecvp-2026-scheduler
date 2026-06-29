/**
 * Environment configuration
 *
 * Public variables (prefixed with EXPO_PUBLIC_) are safe to use in client code.
 * Secret variables are only available on EAS servers and during builds.
 */

const config = {
  // Public app information
  appName: process.env.EXPO_PUBLIC_APP_NAME || 'ECVP 2026 Schedule Organizer',
  conferenceYear: process.env.EXPO_PUBLIC_CONFERENCE_YEAR || '2026',
  conferenceDates: process.env.EXPO_PUBLIC_CONFERENCE_DATES || 'August 23–27, 2026',
  conferenceLocation: process.env.EXPO_PUBLIC_CONFERENCE_LOCATION || 'Bournemouth, UK',
  totalPresentations: process.env.EXPO_PUBLIC_TOTAL_PRESENTATIONS || '618',

  // External links
  githubRepo: process.env.EXPO_PUBLIC_GITHUB_REPO || 'https://github.com/markwgreenlee/ecvp-2026-scheduler',
  conferenceWebsite: process.env.EXPO_PUBLIC_CONFERENCE_WEBSITE || 'https://ecvp2026.uk/',
};

export default config;
