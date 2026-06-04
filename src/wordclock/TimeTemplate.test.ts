import _ from 'lodash';
import {
  ClockfaceHourTT,
  ClockfaceMinuteTT,
  MinutesPastHourTT,
  MinutesTilHourTT,
  QuarterPastHourTT,
  QuarterTilHourTT,
  HalfPastHourTT,
  FractionHourTT,
  ALL_TEMPLATES,
} from './TimeTemplate';
import { TimePhrase } from './TimePhrase';

// ---------------------------------------------------------------------------
// ClockfaceHourTT
// ---------------------------------------------------------------------------
describe('ClockfaceHourTT', () => {
  const tt = new ClockfaceHourTT();
  const phrases = tt.generatePhrases();

  test('all phrases have min=0', () => {
    expect(phrases.every((p) => p.min === 0)).toBe(true);
  });

  test('produces "midnight" phrase at 0:00', () => {
    const midnights = phrases.filter((p) => p.hour === 0 && p.timewords === 'midnight');
    expect(midnights.length).toBeGreaterThan(0);
  });

  test('produces bare "three" phrase at 3:00', () => {
    expect(phrases.some((p) => p.hour === 3 && p.timewords === 'three')).toBe(true);
  });

  test("produces \"three o'clock\" phrase at 3:00", () => {
    expect(phrases.some((p) => p.hour === 3 && p.timewords === "three o'clock")).toBe(true);
  });

  test('produces "noon" at 12:00', () => {
    expect(phrases.some((p) => p.hour === 12 && p.timewords === 'noon')).toBe(true);
  });

  test('covers all 24 hours', () => {
    const hours = _.uniq(phrases.map((p) => p.hour));
    expect(hours.sort((a, b) => a - b)).toEqual(_.range(0, 24));
  });
});

// ---------------------------------------------------------------------------
// ClockfaceMinuteTT
// ---------------------------------------------------------------------------
describe('ClockfaceMinuteTT', () => {
  const tt = new ClockfaceMinuteTT();
  const phrases = tt.generatePhrases();

  test('no phrases have min=0', () => {
    expect(phrases.every((p) => p.min !== 0)).toBe(true);
  });

  test('"three oh seven" at 3:07', () => {
    expect(phrases.some((p) => p.hour === 3 && p.min === 7 && p.timewords === 'three oh seven')).toBe(true);
  });

  test('"three thirty" at 3:30', () => {
    expect(phrases.some((p) => p.hour === 3 && p.min === 30 && p.timewords === 'three thirty')).toBe(true);
  });

  test('"three half past" at 3:30', () => {
    expect(phrases.some((p) => p.hour === 3 && p.min === 30 && p.timewords === 'three half past')).toBe(true);
  });
});

// ---------------------------------------------------------------------------
// MinutesPastHourTT
// ---------------------------------------------------------------------------
describe('MinutesPastHourTT', () => {
  const tt = new MinutesPastHourTT();
  const phrases = tt.generatePhrases();

  test('"five past three" at 3:05', () => {
    expect(phrases.some((p) => p.hour === 3 && p.min === 5 && p.timewords === 'five past three')).toBe(true);
  });

  test('"a quarter past midnight" at 0:15', () => {
    expect(phrases.some((p) => p.hour === 0 && p.min === 15 && p.timewords === 'a quarter past midnight')).toBe(true);
  });

  test('"fifteen past midnight" at 0:15', () => {
    expect(phrases.some((p) => p.hour === 0 && p.min === 15 && p.timewords === 'fifteen past midnight')).toBe(true);
  });

  test('max minute is 30', () => {
    expect(phrases.every((p) => p.min <= 30)).toBe(true);
  });
});

// ---------------------------------------------------------------------------
// MinutesTilHourTT
// ---------------------------------------------------------------------------
describe('MinutesTilHourTT', () => {
  const tt = new MinutesTilHourTT();
  const phrases = tt.generatePhrases();

  test('"five til four" at 3:55', () => {
    expect(phrases.some((p) => p.hour === 3 && p.min === 55 && p.timewords === 'five til four')).toBe(true);
  });

  test('"a quarter til midnight" at 23:45', () => {
    expect(phrases.some((p) => p.hour === 23 && p.min === 45 && p.timewords === 'a quarter til midnight')).toBe(true);
  });

  test('"one til one" at 0:59 (1am - 1 min)', () => {
    expect(phrases.some((p) => p.hour === 0 && p.min === 59 && p.timewords === 'one til one')).toBe(true);
  });

  test('minutes are all in range 31..59', () => {
    expect(phrases.every((p) => p.min >= 31 && p.min <= 59)).toBe(true);
  });
});

// ---------------------------------------------------------------------------
// QuarterPastHourTT
// ---------------------------------------------------------------------------
describe('QuarterPastHourTT', () => {
  const tt = new QuarterPastHourTT();
  const phrases = tt.generatePhrases();

  test('all phrases have min=15', () => {
    expect(phrases.every((p) => p.min === 15)).toBe(true);
  });

  test('"quarter past midnight" at 0:15', () => {
    expect(phrases.some((p) => p.hour === 0 && p.timewords === 'quarter past midnight')).toBe(true);
  });

  test('"quarter past one" at 1:15', () => {
    expect(phrases.some((p) => p.hour === 1 && p.timewords === 'quarter past one')).toBe(true);
  });

  test('"quarter past noon" at 12:15', () => {
    expect(phrases.some((p) => p.hour === 12 && p.timewords === 'quarter past noon')).toBe(true);
  });

  test('covers all 24 hours', () => {
    const hours = _.uniq(phrases.map((p) => p.hour)).sort((a, b) => a - b);
    expect(hours).toEqual(_.range(0, 24));
  });
});

// ---------------------------------------------------------------------------
// QuarterTilHourTT
// ---------------------------------------------------------------------------
describe('QuarterTilHourTT', () => {
  const tt = new QuarterTilHourTT();
  const phrases = tt.generatePhrases();

  test('all phrases have min=45', () => {
    expect(phrases.every((p) => p.min === 45)).toBe(true);
  });

  test('"quarter til one" at 0:45', () => {
    expect(phrases.some((p) => p.hour === 0 && p.timewords === 'quarter til one')).toBe(true);
  });

  test('"quarter til midnight" at 23:45', () => {
    expect(phrases.some((p) => p.hour === 23 && p.timewords === 'quarter til midnight')).toBe(true);
  });
});

// ---------------------------------------------------------------------------
// HalfPastHourTT
// ---------------------------------------------------------------------------
describe('HalfPastHourTT', () => {
  const tt = new HalfPastHourTT();
  const phrases = tt.generatePhrases();

  test('all phrases have min=30', () => {
    expect(phrases.every((p) => p.min === 30)).toBe(true);
  });

  test('"half past three" at 3:30', () => {
    expect(phrases.some((p) => p.hour === 3 && p.timewords === 'half past three')).toBe(true);
  });

  test('"half past midnight" at 0:30', () => {
    expect(phrases.some((p) => p.hour === 0 && p.timewords === 'half past midnight')).toBe(true);
  });
});

// ---------------------------------------------------------------------------
// FractionHourTT
// ---------------------------------------------------------------------------
describe('FractionHourTT', () => {
  const tt = new FractionHourTT();
  const phrases = tt.generatePhrases();

  test('"three and a quarter" at 3:15', () => {
    expect(phrases.some((p) => p.hour === 3 && p.min === 15 && p.timewords === 'three and a quarter')).toBe(true);
  });

  test('"three and a half" at 3:30', () => {
    expect(phrases.some((p) => p.hour === 3 && p.min === 30 && p.timewords === 'three and a half')).toBe(true);
  });

  test('"midnight and three quarters" at 0:45', () => {
    expect(phrases.some((p) => p.hour === 0 && p.min === 45 && p.timewords === 'midnight and three quarters')).toBe(true);
  });
});

// ---------------------------------------------------------------------------
// ALL_TEMPLATES — global sanity checks
// ---------------------------------------------------------------------------
describe('ALL_TEMPLATES', () => {
  test('every minute 0..59 has at least one phrase for every hour 0..23', () => {
    const allPhrases = ALL_TEMPLATES.flatMap((t) => t.generatePhrases());
    const byKey = _.groupBy(allPhrases, (p) => p.timeKey);

    const missing: string[] = [];
    for (let h = 0; h <= 23; h++) {
      for (let m = 0; m <= 59; m++) {
        const key = `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`;
        if (!byKey[key] || byKey[key].length === 0) missing.push(key);
      }
    }
    expect(missing).toEqual([]);
  });

  test('every phrase has valid hour/min', () => {
    const allPhrases = ALL_TEMPLATES.flatMap((t) => t.generatePhrases());
    for (const p of allPhrases) {
      expect(p.hour).toBeGreaterThanOrEqual(0);
      expect(p.hour).toBeLessThanOrEqual(23);
      expect(p.min).toBeGreaterThanOrEqual(0);
      expect(p.min).toBeLessThanOrEqual(59);
    }
  });
});
