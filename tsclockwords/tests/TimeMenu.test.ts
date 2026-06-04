import _ from 'lodash';
import { TIME_MENU, phrasesFor, coverageSummary } from '../src/TimeMenu';

describe('TIME_MENU', () => {
  test('has entries for all 1440 minutes in a day', () => {
    expect(Object.keys(TIME_MENU).length).toBe(24 * 60);
  });

  test('3:15 includes "quarter past three am"', () => {
    const words = phrasesFor(3, 15).map((p) => p.words);
    expect(words).toContain('quarter past three am');
  });

  test('3:15 includes "three fifteen am"', () => {
    const words = phrasesFor(3, 15).map((p) => p.words);
    expect(words).toContain('three fifteen am');
  });

  test('3:15 includes "three and a quarter am"', () => {
    const words = phrasesFor(3, 15).map((p) => p.words);
    expect(words).toContain('three and a quarter am');
  });

  test('3:55 includes "five to four am"', () => {
    const words = phrasesFor(3, 55).map((p) => p.words);
    expect(words).toContain('five to four am');
  });

  test('3:55 includes "five til four am"', () => {
    const words = phrasesFor(3, 55).map((p) => p.words);
    expect(words).toContain('five til four am');
  });

  test('0:00 includes "midnight" (no ampm suffix)', () => {
    const words = phrasesFor(0, 0).map((p) => p.words);
    expect(words).toContain('midnight');
  });

  test('0:00 includes "midnight sharp" (no ampm suffix)', () => {
    const words = phrasesFor(0, 0).map((p) => p.words);
    expect(words).toContain('midnight sharp');
  });

  test('0:00 does NOT include "midnight exactly"', () => {
    const words = phrasesFor(0, 0).map((p) => p.words);
    expect(words).not.toContain('midnight exactly');
  });

  test('12:00 includes "noon" (no ampm suffix)', () => {
    const words = phrasesFor(12, 0).map((p) => p.words);
    expect(words).toContain('noon');
  });

  test('phrasesFor returns sorted by word length', () => {
    const phrases = phrasesFor(3, 30);
    const lengths = phrases.map((p) => p.words.length);
    for (let i = 1; i < lengths.length; i++) {
      expect(lengths[i]).toBeGreaterThanOrEqual(lengths[i - 1]);
    }
  });

  test('every time slot has at least 2 phrases', () => {
    const under = Object.entries(TIME_MENU).filter(([, ps]) => ps.length < 2);
    expect(under).toEqual([]);
  });
});

describe('coverageSummary', () => {
  test('returns 1440 entries', () => {
    expect(coverageSummary().length).toBe(24 * 60);
  });

  test('is sorted by timeKey', () => {
    const summary = coverageSummary();
    for (let i = 1; i < summary.length; i++) {
      expect(summary[i].timeKey >= summary[i - 1].timeKey).toBe(true);
    }
  });
});
