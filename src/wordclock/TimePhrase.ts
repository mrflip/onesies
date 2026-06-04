import { ampmLabel } from './timewords';

/**
 * A single human-readable description of a moment in time.
 *
 * `hour`      – 24-hour value 0..23
 * `min`       – 0..59
 * `timewords` – the core phrase, e.g. "quarter past one", "half past midnight"
 *
 * The `.ampm` getter returns "am" / "pm" / "" depending on the hour.
 * The `.words` getter joins timewords + ampm (space-separated, trimmed).
 */
export class TimePhrase {
  readonly hour: number;
  readonly min: number;
  readonly timewords: string;

  constructor(hour: number, min: number, timewords: string) {
    if (hour < 0 || hour > 23) throw new RangeError(`hour ${hour} out of range`);
    if (min < 0 || min > 59) throw new RangeError(`min ${min} out of range`);
    this.hour = hour;
    this.min = min;
    this.timewords = timewords;
  }

  get ampm(): string {
    return ampmLabel(this.hour);
  }

  get words(): string {
    return [this.timewords, this.ampm].filter(Boolean).join(' ');
  }

  /** Sortable key for grouping: "HH:MM" */
  get timeKey(): string {
    return `${String(this.hour).padStart(2, '0')}:${String(this.min).padStart(2, '0')}`;
  }

  toString(): string {
    return `[${this.timeKey}] "${this.words}"`;
  }
}
