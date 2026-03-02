/**
 * Schafkopf Event Scheduler - Main Entry Point
 *
 * This application generates a WhatsApp poll with the next 10 weekdays
 * (Monday-Friday for the next 2 weeks) to schedule Schafkopf events.
 *
 * Usage:
 *   bun run scheduler
 */

import { loadConfig, getDefaultConfigPath } from './config';
import { SchafkopfScheduler } from './scheduler';

/**
 * Main function - entry point for the scheduler
 */
async function main() {
  console.log('=== Schafkopf Event Scheduler ===\n');

  try {
    // Load configuration
    const configPath = getDefaultConfigPath();
    console.log(`Loading configuration from: ${configPath}`);
    const config = loadConfig(configPath);
    console.log('Configuration loaded successfully\n');

    // Create and run scheduler
    const scheduler = new SchafkopfScheduler(config);
    const messageId = await scheduler.run();

    console.log(`\n✓ Success! Poll sent (Message ID: ${messageId})`);
    process.exit(0);

  } catch (error) {
    // Handle errors gracefully
    if (error instanceof Error) {
      console.error(`\n✗ Error: ${error.message}`);

      // Show stack trace in debug mode
      if (process.env.DEBUG) {
        console.error('\nStack trace:');
        console.error(error.stack);
      }
    } else {
      console.error(`\n✗ Unexpected error: ${String(error)}`);
    }

    process.exit(1);
  }
}

// Run the scheduler
main();
