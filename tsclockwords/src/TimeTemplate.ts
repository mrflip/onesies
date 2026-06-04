import { TimePhrase } from './TimePhrase';
import {
  hourWords,
  hourWordsWithSpecial,
  MINUTE_PAST_WORDS,
  MINUTE_CLOCKFACE_WORDS,
} from './timewords';

// ---------------------------------------------------------------------------
// Base class
// ---------------------------------------------------------------------------

export abstract class TimeTemplate {
  abstract readonly name: string;

  /** Return every TimePhrase this template can express. */
  abstract generatePhrases(): TimePhrase[];
}

// ---------------------------------------------------------------------------
// Helper: all (hour24, hourWord) pairs for hours 0..23
// ---------------------------------------------------------------------------

function allHours(includeSpecial = true): Array<{ h24: number; word: string }> {
  const out: Array<{ h24: number; word: string }> = [];
  for (let h = 0; h <= 23; h++) {
    const words = includeSpecial ? hourWordsWithSpecial(h) : hourWords(h);
    for (const word of words) {
      out.push({ h24: h, word });
    }
  }
  return out;
}

// ---------------------------------------------------------------------------
// "H o'clock / H sharp / bare H" — ClockfaceHourTT
// ---------------------------------------------------------------------------

/** "three", "three sharp", "three o'clock" (minute = 0) */
export class ClockfaceHourTT extends TimeTemplate {
  readonly name = 'ClockfaceHour';

  generatePhrases(): TimePhrase[] {
    const phrases: TimePhrase[] = [];
    for (const { h24, word: hWord } of allHours()) {
      for (const mWord of MINUTE_CLOCKFACE_WORDS[0]) {
        const timewords = mWord ? `${hWord} ${mWord}` : hWord;
        phrases.push(new TimePhrase(h24, 0, timewords));
      }
    }
    return phrases;
  }
}

// ---------------------------------------------------------------------------
// "H oh MM" / "H MM" — ClockfaceMinuteTT
// ---------------------------------------------------------------------------

/** "three oh seven", "three fifteen", "three thirty", etc. */
export class ClockfaceMinuteTT extends TimeTemplate {
  readonly name = 'ClockfaceMinute';

  generatePhrases(): TimePhrase[] {
    const phrases: TimePhrase[] = [];
    for (const { h24, word: hWord } of allHours()) {
      for (let m = 1; m <= 59; m++) {
        for (const mWord of MINUTE_CLOCKFACE_WORDS[m] ?? []) {
          phrases.push(new TimePhrase(h24, m, `${hWord} ${mWord}`));
        }
      }
    }
    return phrases;
  }
}

// ---------------------------------------------------------------------------
// "N past H" — MinutesPastHourTT
// ---------------------------------------------------------------------------

/** "five past three", "a quarter past midnight", "thirty past one" */
export class MinutesPastHourTT extends TimeTemplate {
  readonly name = 'MinutesPastHour';

  generatePhrases(): TimePhrase[] {
    const phrases: TimePhrase[] = [];
    for (const { h24, word: hWord } of allHours()) {
      for (let m = 1; m <= 39; m++) {
        for (const mWord of MINUTE_PAST_WORDS[m] ?? []) {
          phrases.push(new TimePhrase(h24, m, `${mWord} past ${hWord}`));
        }
      }
    }
    return phrases;
  }
}

// ---------------------------------------------------------------------------
// "N til H" — MinutesTilHourTT
// ---------------------------------------------------------------------------

/** "five til three", "a quarter til midnight", "ten til two" */
export class MinutesTilHourTT extends TimeTemplate {
  readonly name = 'MinutesTilHour';

  generatePhrases(): TimePhrase[] {
    const phrases: TimePhrase[] = [];
    for (const { h24, word: hWord } of allHours()) {
      for (let offset = 1; offset <= 39; offset++) {
        const min = (60 - offset) % 60;
        const actualH24 = (h24 - 1 + 24) % 24;
        for (const mWord of MINUTE_PAST_WORDS[offset] ?? []) {
          phrases.push(new TimePhrase(actualH24, min, `${mWord} til ${hWord}`));
        }
      }
    }
    return phrases;
  }
}

// ---------------------------------------------------------------------------
// "N to H" — MinutesToHourTT
// ---------------------------------------------------------------------------

/** "five to three", "a quarter to midnight", "ten to two" */
export class MinutesToHourTT extends TimeTemplate {
  readonly name = 'MinutesToHour';

  generatePhrases(): TimePhrase[] {
    const phrases: TimePhrase[] = [];
    for (const { h24, word: hWord } of allHours()) {
      for (let offset = 1; offset <= 39; offset++) {
        const min = (60 - offset) % 60;
        const actualH24 = (h24 - 1 + 24) % 24;
        for (const mWord of MINUTE_PAST_WORDS[offset] ?? []) {
          phrases.push(new TimePhrase(actualH24, min, `${mWord} to ${hWord}`));
        }
      }
    }
    return phrases;
  }
}

// ---------------------------------------------------------------------------
// "quarter past H" — QuarterPastHourTT
// ---------------------------------------------------------------------------

/** "quarter past one", "quarter past midnight", etc. */
export class QuarterPastHourTT extends TimeTemplate {
  readonly name = 'QuarterPastHour';

  generatePhrases(): TimePhrase[] {
    return allHours().map(({ h24, word }) => new TimePhrase(h24, 15, `quarter past ${word}`));
  }
}

// ---------------------------------------------------------------------------
// "quarter til H" — QuarterTilHourTT
// ---------------------------------------------------------------------------

export class QuarterTilHourTT extends TimeTemplate {
  readonly name = 'QuarterTilHour';

  generatePhrases(): TimePhrase[] {
    return allHours().map(({ h24, word }) => {
      const actualH24 = (h24 - 1 + 24) % 24;
      return new TimePhrase(actualH24, 45, `quarter til ${word}`);
    });
  }
}

// ---------------------------------------------------------------------------
// "quarter to H" — QuarterToHourTT
// ---------------------------------------------------------------------------

export class QuarterToHourTT extends TimeTemplate {
  readonly name = 'QuarterToHour';

  generatePhrases(): TimePhrase[] {
    return allHours().map(({ h24, word }) => {
      const actualH24 = (h24 - 1 + 24) % 24;
      return new TimePhrase(actualH24, 45, `quarter to ${word}`);
    });
  }
}

// ---------------------------------------------------------------------------
// "half past H" — HalfPastHourTT
// ---------------------------------------------------------------------------

export class HalfPastHourTT extends TimeTemplate {
  readonly name = 'HalfPastHour';

  generatePhrases(): TimePhrase[] {
    return allHours().map(({ h24, word }) => new TimePhrase(h24, 30, `half past ${word}`));
  }
}

// ---------------------------------------------------------------------------
// "and a quarter" / "and a half" — FractionHourTT
// ---------------------------------------------------------------------------

export class FractionHourTT extends TimeTemplate {
  readonly name = 'FractionHour';

  generatePhrases(): TimePhrase[] {
    const fractions: Array<{ min: number; fword: string }> = [
      { min: 15, fword: 'and a quarter' },
      { min: 30, fword: 'and a half' },
    ];
    const phrases: TimePhrase[] = [];
    for (const { h24, word } of allHours()) {
      for (const { min, fword } of fractions) {
        phrases.push(new TimePhrase(h24, min, `${word} ${fword}`));
      }
    }
    return phrases;
  }
}

// ---------------------------------------------------------------------------
// Registry of all templates
// ---------------------------------------------------------------------------

export const ALL_TEMPLATES: TimeTemplate[] = [
  new ClockfaceHourTT(),
  new ClockfaceMinuteTT(),
  new MinutesPastHourTT(),
  new MinutesTilHourTT(),
  new MinutesToHourTT(),
  new QuarterPastHourTT(),
  new QuarterTilHourTT(),
  new QuarterToHourTT(),
  new HalfPastHourTT(),
  new FractionHourTT(),
];
