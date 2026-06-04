import _ from 'lodash';
import { TimePhrase } from './TimePhrase';
import { ALL_TEMPLATES } from './TimeTemplate';

/**
 * All phrases grouped by "HH:MM" key.
 *
 * Example:
 *   TimeMenu["03:15"] → [
 *     TimePhrase { hour:3, min:15, timewords:"quarter past three" },
 *     TimePhrase { hour:3, min:15, timewords:"three fifteen" },
 *     TimePhrase { hour:3, min:15, timewords:"three and a quarter" },
 *     ...
 *   ]
 */
export type TimeMenu = Record<string, TimePhrase[]>;

function buildTimeMenu(): TimeMenu {
  const allPhrases = ALL_TEMPLATES.flatMap((t) => t.generatePhrases());
  return _.groupBy(allPhrases, (p) => p.timeKey);
}

export const TIME_MENU: TimeMenu = buildTimeMenu();

/** Return phrases for a specific 24-hour time, sorted by word length. */
export function phrasesFor(hour: number, min: number): TimePhrase[] {
  const key = `${String(hour).padStart(2, '0')}:${String(min).padStart(2, '0')}`;
  return _.sortBy(TIME_MENU[key] ?? [], (p) => p.words.length);
}

/** Summary: how many distinct phrases exist per minute, sorted descending. */
export function coverageSummary(): Array<{ timeKey: string; count: number }> {
  return _.chain(TIME_MENU)
    .map((phrases, timeKey) => ({ timeKey, count: phrases.length }))
    .sortBy('timeKey')
    .value();
}
