/**
 * Configuration interface for Schafkopf Scheduler
 */
export interface SchedulerConfig {
  whatsapp: {
    authDir: string;
    logLevel: 'silent' | 'error' | 'warn' | 'info' | 'debug';
  };
  scheduler: {
    pollTitle: string;
    recipient: string;
    timezone: string;
    weekdaysCount: number;
  };
}

/**
 * Hardcoded configuration for Schafkopf Scheduler
 * All values are defined here instead of loading from a file
 */
export function getConfig(): SchedulerConfig {
  return {
    whatsapp: {
      // Directory where WhatsApp authentication data is stored
      // NOTE: Auth is always synced with S3 (bucket: whatsapp-scheduler-082113759242)
      // Local dev uses ./tmp/auth, Lambda uses /tmp/auth
      authDir: './tmp/auth',

      // Logging level: silent | error | warn | info | debug
      logLevel: 'info',
    },
    scheduler: {
      // Title of the poll message
      pollTitle: 'Next Schafkopf Event Poll',

      // Recipient phone number (without country code prefix like +)
      // Later this can be changed to a group JID (e.g., "group-id@g.us")
      recipient: '4917657753775',

      // Timezone for date calculations
      timezone: 'Europe/Berlin',

      // Number of weekdays to include in the poll (default: 10 = 2 weeks of weekdays)
      weekdaysCount: 10,
    },
  };
}
