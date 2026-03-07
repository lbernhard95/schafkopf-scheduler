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
    recipientName: string; // Changed from 'recipient' to 'recipientName' for clarity
    timezone: string;
    weekdaysCount: number;
  };
}

/**
 * Hardcoded configuration for Schafkopf Scheduler
 * All values are defined here instead of loading from a file
 */
export function getConfig(): SchedulerConfig {
  const isLambda = !!(
    process.env.AWS_EXECUTION_ENV ||
    process.env.AWS_LAMBDA_FUNCTION_NAME ||
    process.env.LAMBDA_TASK_ROOT
  );

  return {
    whatsapp: {
      // Directory where WhatsApp authentication data is stored
      // NOTE: Auth is always synced with S3 (bucket: whatsapp-scheduler-082113759242)
      // Local dev uses ./tmp/auth, Lambda uses /tmp/auth
      authDir: isLambda ? '/tmp/auth' : './tmp/auth',

      // Logging level: silent | error | warn | info | debug
      logLevel: 'info',
    },
    scheduler: {
      // Title of the poll message
      pollTitle: 'Next Schafkopf Event Poll',

      // Recipient name (group or contact)
      // This will be resolved dynamically to the correct JID
      // The match is exact but case-insensitive and emoji-independent
      // Examples:
      //   - 'AT Schafkopf' matches 'AT Schafkopf 🪙'
      //   - 'John Doe' matches individual contact named 'John Doe'
      recipientName: isLambda ? 'AT Schafkopf' : 'Wheatley',

      // Timezone for date calculations
      timezone: 'Europe/Berlin',

      // Number of weekdays to include in the poll (default: 10 = 2 weeks of weekdays)
      weekdaysCount: 10,
    },
  };
}
