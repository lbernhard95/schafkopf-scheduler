import { WhatsAppClient } from '../../index';
import type { SchedulerConfig } from './config';
import { generatePollOptions } from './date-utils';
import { Logger } from '../../core/logger';

/**
 * Main Schafkopf Scheduler class
 * Handles the business logic for generating and sending event polls
 */
export class SchafkopfScheduler {
  private config: SchedulerConfig;
  private client: WhatsAppClient;
  private logger: Logger;

  constructor(config: SchedulerConfig) {
    this.config = config;
    this.logger = new Logger(config.whatsapp.logLevel);

    // Initialize WhatsApp client with config
    this.client = new WhatsAppClient({
      authDir: config.whatsapp.authDir,
      logLevel: config.whatsapp.logLevel,
    });
  }

  /**
   * Runs the scheduler: generates poll and sends it via WhatsApp
   * @returns Message ID of the sent poll
   */
  async run(): Promise<string> {
    try {
      this.logger.info('Starting Schafkopf Scheduler...');

      // Generate poll options (next N weekdays)
      const pollOptions = this.generatePollOptions();
      this.logger.info(`Generated ${pollOptions.length} poll options: ${pollOptions.join(', ')}`);

      // Send the poll
      const messageId = await this.sendPoll(pollOptions);

      this.logger.info(`Poll sent successfully (Message ID: ${messageId})`);

      return messageId;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      this.logger.error(`Scheduler failed: ${errorMessage}`);
      throw error;
    } finally {
      // Always disconnect gracefully
      await this.disconnect();
    }
  }

  /**
   * Generates poll options based on configuration
   * @returns Array of formatted date strings for poll options
   */
  private generatePollOptions(): string[] {
    this.logger.debug('Generating poll options...');

    const options = generatePollOptions(
      this.config.scheduler.weekdaysCount,
      undefined, // Start from tomorrow
      this.config.scheduler.timezone
    );

    return options;
  }

  /**
   * Sends the poll via WhatsApp
   * @param pollOptions - Array of poll option strings
   * @returns Message ID of the sent poll
   */
  private async sendPoll(pollOptions: string[]): Promise<string> {
    // Resolve recipient name to JID
    this.logger.info(`Resolving recipient name: "${this.config.scheduler.recipientName}"...`);
    const recipientJid = await this.client.resolveRecipient(this.config.scheduler.recipientName);

    this.logger.info(`Sending poll to ${recipientJid}...`);

    const messageId = await this.client.sendPoll(
      recipientJid,
      this.config.scheduler.pollTitle,
      pollOptions,
      pollOptions.length // Allow selecting all options (multi-select)
    );

    return messageId;
  }

  /**
   * Disconnects the WhatsApp client gracefully
   */
  async disconnect(): Promise<void> {
    this.logger.debug('Disconnecting WhatsApp client...');
    await this.client.disconnect();
  }
}
