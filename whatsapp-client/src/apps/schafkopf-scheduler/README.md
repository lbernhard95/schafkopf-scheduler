# Schafkopf Event Scheduler

A WhatsApp-based event scheduler that automatically generates polls with the next 10 weekdays (Monday-Friday) for scheduling Schafkopf events.

## Features

- **Automatic Weekday Selection**: Generates the next 10 weekdays (Mon-Fri), automatically skipping weekends
- **German Date Formatting**: Displays dates in the format "Mon 06.01" with German weekday names
- **Europe/Berlin Timezone**: All date calculations respect German timezone and DST
- **Multi-Select Polls**: Allows participants to select multiple available dates
- **YAML Configuration**: Easy-to-edit configuration file for customization

## Usage

### Quick Start

1. **Configure the recipient** in `config/schafkopf-scheduler.yaml`:
   ```yaml
   scheduler:
     recipient: "4917657753775"  # Your phone number or group JID
   ```

2. **Run the scheduler**:
   ```bash
   bun run scheduler
   ```

3. **Check WhatsApp** - The poll should arrive with the title "Next Schafkopf Event Poll" and 10 date options!

### Configuration

Edit `config/schafkopf-scheduler.yaml`:

```yaml
whatsapp:
  authDir: "./auth"              # WhatsApp auth directory
  logLevel: "info"               # silent | error | warn | info | debug

scheduler:
  pollTitle: "Next Schafkopf Event Poll"
  recipient: "4917657753775"     # Phone number or group JID
  timezone: "Europe/Berlin"      # Timezone for date calculations
  weekdaysCount: 10              # Number of weekdays (default: 10)
```

## Architecture

### File Structure

```
src/apps/schafkopf-scheduler/
├── index.ts          # Main entry point
├── config.ts         # Configuration loading & validation
├── scheduler.ts      # Main scheduler logic
└── date-utils.ts     # Date calculation & formatting utilities

config/
└── schafkopf-scheduler.yaml  # Configuration file
```

### How It Works

1. **Loads Configuration**: Reads YAML config and validates required fields
2. **Calculates Dates**: Starting from tomorrow, finds the next N weekdays (skips Sat/Sun)
3. **Formats Dates**: Converts to German format ("Di 03.03", "Mi 04.03", etc.)
4. **Connects to WhatsApp**: Establishes secure connection using saved credentials
5. **Sends Poll**: Creates multi-select poll with all date options
6. **Disconnects**: Gracefully closes connection after 2-second delivery wait

### Date Utilities

The `date-utils.ts` module provides:

- `isWeekday(date)` - Checks if a date is Monday-Friday
- `getNextWeekdays(count, startDate?, timezone?)` - Gets next N weekdays
- `formatDateForPoll(date, timezone?)` - Formats date as "Mon 06.01"
- `generatePollOptions(count, startDate?, timezone?)` - Complete date generation

## Examples

### Example Output

```bash
$ bun run scheduler
=== Schafkopf Event Scheduler ===

Loading configuration from: config/schafkopf-scheduler.yaml
Configuration loaded successfully

[INFO] Starting Schafkopf Scheduler...
[INFO] Generated 10 poll options: Di 03.03, Mi 04.03, Do 05.03, Fr 06.03, Mo 09.03, Di 10.03, Mi 11.03, Do 12.03, Fr 13.03, Mo 16.03
[INFO] Sending poll to 4917657753775...
[INFO] Poll sent successfully (Message ID: 3EB0C0D458D30A642E3BFB)

✓ Success! Poll sent (Message ID: 3EB0C0D458D30A642E3BFB)
```

### Example Poll

**Title**: Next Schafkopf Event Poll

**Options** (all selectable):
- Di 03.03
- Mi 04.03
- Do 05.03
- Fr 06.03
- Mo 09.03
- Di 10.03
- Mi 11.03
- Do 12.03
- Fr 13.03
- Mo 16.03

## Future Enhancements

- **Group Support**: Send polls directly to WhatsApp groups
- **Cron Scheduling**: Automatically run on a schedule (e.g., every Monday at 9am)
- **Response Collection**: Gather and analyze poll responses
- **Calendar Integration**: Export results to calendar apps
- **Reminder Messages**: Send follow-up reminders before events
- **Multiple Profiles**: Support different scheduler configurations

## Troubleshooting

### Configuration Errors

If you see `Configuration validation failed`, check:
- `scheduler.recipient` is set and not empty
- `scheduler.weekdaysCount` is between 1 and 20
- `whatsapp.logLevel` is one of: silent, error, warn, info, debug

### Connection Issues

If WhatsApp connection fails:
- Ensure `auth/` directory exists with valid credentials
- Check internet connectivity
- Try scanning QR code again if authentication expired

### Debug Mode

Enable detailed logging:
```bash
DEBUG=1 bun run scheduler
```

Or set log level in config:
```yaml
whatsapp:
  logLevel: "debug"
```

## Dependencies

- **@whiskeysockets/baileys** - WhatsApp Web API
- **js-yaml** - YAML configuration parsing
- **qrcode-terminal** - QR code display for authentication

Built with Bun runtime for TypeScript.
