/**
 * Date utility functions for the Schafkopf Scheduler
 * Handles date calculations, weekday filtering, and formatting
 */

/**
 * Checks if a date is a weekday (Monday-Friday)
 * @param date - The date to check
 * @returns true if the date is a weekday, false otherwise
 */
export function isWeekday(date: Date): boolean {
  const day = date.getDay();
  // 0 = Sunday, 6 = Saturday
  return day !== 0 && day !== 6;
}

/**
 * Gets the next N weekdays starting from next Monday
 * Automatically skips weekends
 *
 * @param count - Number of weekdays to return
 * @param startDate - Optional start date (defaults to today)
 * @param timezone - Timezone for date calculations (e.g., 'Europe/Berlin')
 * @returns Array of Date objects representing the next N weekdays
 */
export function getNextWeekdays(
  count: number,
  startDate?: Date,
  timezone: string = 'Europe/Berlin'
): Date[] {
  const weekdays: Date[] = [];

  // Start from today by default
  const current = startDate || new Date();

  // Convert to the specified timezone
  // Note: We create a date in the target timezone to handle DST correctly
  const startInTimezone = new Date(
    current.toLocaleString('en-US', { timeZone: timezone })
  );

  // Calculate days until next Monday
  // getDay() returns: 0 = Sunday, 1 = Monday, 2 = Tuesday, ..., 6 = Saturday
  const dayOfWeek = startInTimezone.getDay();

  // Calculate days to add to get to next Monday:
  // - If today is Monday (1): add 7 days to get next Monday
  // - If today is Tuesday (2): add 6 days to get next Monday
  // - If today is Wednesday (3): add 5 days to get next Monday
  // - If today is Thursday (4): add 4 days to get next Monday
  // - If today is Friday (5): add 3 days to get next Monday
  // - If today is Saturday (6): add 2 days to get next Monday
  // - If today is Sunday (0): add 1 day to get next Monday
  const daysUntilNextMonday = dayOfWeek === 0 ? 1 : (8 - dayOfWeek);

  startInTimezone.setDate(startInTimezone.getDate() + daysUntilNextMonday);
  startInTimezone.setHours(0, 0, 0, 0); // Reset to midnight

  let currentDate = new Date(startInTimezone);

  // Collect weekdays until we have enough
  while (weekdays.length < count) {
    if (isWeekday(currentDate)) {
      weekdays.push(new Date(currentDate));
    }

    // Move to next day
    currentDate.setDate(currentDate.getDate() + 1);
  }

  return weekdays;
}

/**
 * Formats a date for poll display
 * Format: "Mon 06.01" (short weekday + DD.MM)
 * Uses German locale for weekday names
 *
 * @param date - The date to format
 * @param timezone - Timezone for formatting (e.g., 'Europe/Berlin')
 * @returns Formatted date string
 */
export function formatDateForPoll(date: Date, timezone: string = 'Europe/Berlin'): string {
  // Get German short weekday name (Mon, Die, Mit, Don, Fre)
  const weekday = date.toLocaleDateString('de-DE', {
    weekday: 'short',
    timeZone: timezone,
  });

  // Capitalize first letter and remove period if present
  const weekdayCapitalized = weekday.charAt(0).toUpperCase() + weekday.slice(1).replace('.', '');

  // Get day and month with leading zeros
  const day = date.toLocaleDateString('de-DE', {
    day: '2-digit',
    timeZone: timezone,
  });

  const month = date.toLocaleDateString('de-DE', {
    month: '2-digit',
    timeZone: timezone,
  });

  return `${weekdayCapitalized} ${day}.${month}`;
}

/**
 * Generates formatted date strings for the next N weekdays starting from next Monday
 *
 * @param count - Number of weekdays to generate
 * @param startDate - Optional start date (defaults to today)
 * @param timezone - Timezone for date calculations (e.g., 'Europe/Berlin')
 * @returns Array of formatted date strings
 */
export function generatePollOptions(
  count: number,
  startDate?: Date,
  timezone: string = 'Europe/Berlin'
): string[] {
  const weekdays = getNextWeekdays(count, startDate, timezone);
  return weekdays.map(date => formatDateForPoll(date, timezone));
}
