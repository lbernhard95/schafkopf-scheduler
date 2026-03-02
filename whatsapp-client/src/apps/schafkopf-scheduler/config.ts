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

      // Recipient in WhatsApp JID format (must include domain)
      // Two formats are supported:
      // 1. Individual chat: "PHONE_NUMBER@s.whatsapp.net" (e.g., "4917657753775@s.whatsapp.net")
      // 2. Group chat: "GROUP_ID@g.us" (e.g., "HbgNlG0Ftnf6ZWH7WTETCn@g.us")
      // Note: Phone numbers should include country code without + prefix
      recipient: 'HbgNlG0Ftnf6ZWH7WTETCn@g.us',
      // Timezone for date calculations
      timezone: 'Europe/Berlin',

      // Number of weekdays to include in the poll (default: 10 = 2 weeks of weekdays)
      weekdaysCount: 10,
    },
  };
}
