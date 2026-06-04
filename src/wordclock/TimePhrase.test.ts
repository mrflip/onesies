import { TimePhrase } from './TimePhrase';

describe('TimePhrase', () => {
  test('midnight has blank ampm', () => {
    const p = new TimePhrase(0, 0, 'midnight');
    expect(p.ampm).toBe('');
    expect(p.words).toBe('midnight');
  });

  test('noon has blank ampm', () => {
    const p = new TimePhrase(12, 0, 'noon');
    expect(p.ampm).toBe('');
    expect(p.words).toBe('noon');
  });

  test('hour 12 "twelve" has blank ampm', () => {
    const p = new TimePhrase(12, 0, 'twelve');
    expect(p.ampm).toBe('');
    expect(p.words).toBe('twelve');
  });

  test('am hours get "am"', () => {
    const p = new TimePhrase(3, 15, 'quarter past three');
    expect(p.ampm).toBe('am');
    expect(p.words).toBe('quarter past three am');
  });

  test('pm hours get "pm"', () => {
    const p = new TimePhrase(15, 30, 'half past three');
    expect(p.ampm).toBe('pm');
    expect(p.words).toBe('half past three pm');
  });

  test('timeKey is zero-padded HH:MM', () => {
    expect(new TimePhrase(3, 5, 'x').timeKey).toBe('03:05');
    expect(new TimePhrase(23, 59, 'x').timeKey).toBe('23:59');
  });

  test('rejects invalid hour', () => {
    expect(() => new TimePhrase(24, 0, 'x')).toThrow(RangeError);
  });

  test('rejects invalid minute', () => {
    expect(() => new TimePhrase(1, 60, 'x')).toThrow(RangeError);
  });
});
