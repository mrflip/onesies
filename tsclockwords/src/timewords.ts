/** Cardinal hour words: index 0 = "twelve" (used for 12 o'clock), index 1..12 = one..twelve */
export const HOUR_WORDS: Record<number, string[]> = {
  0:  ['twelve'],
  1:  ['one'],
  2:  ['two'],
  3:  ['three'],
  4:  ['four'],
  5:  ['five'],
  6:  ['six'],
  7:  ['seven'],
  8:  ['eight'],
  9:  ['nine'],
  10: ['ten'],
  11: ['eleven'],
  12: ['twelve'],
};

/**
 * Special names for the top-of-hour anchors.
 * hour 0 → midnight, hour 12 → noon (each extends the normal "twelve").
 */
export const SPECIAL_HOUR_NAMES: Record<number, string[]> = {
  0:  ['midnight'],
  12: ['noon'],
};

/** All names for an hour (1-12), NOT including midnight/noon. */
export function hourWords(h: number): string[] {
  const h12 = ((h - 1 + 12) % 12) + 1; // 1-12
  return HOUR_WORDS[h12] ?? [String(h12)];
}

/** All names for an hour including special ones (midnight/noon). */
export function hourWordsWithSpecial(h: number): string[] {
  const base = hourWords(h);
  const special = SPECIAL_HOUR_NAMES[h] ?? SPECIAL_HOUR_NAMES[h % 12];
  return special ? [...base, ...special] : base;
}

/**
 * Spoken forms for a minute offset used in "X past" / "X til" / "X to" contexts.
 * Extends to 39 so phrases like "thirty past" and "twenty nine til" are covered.
 */
export const MINUTE_PAST_WORDS: Record<number, string[]> = {
  1:  ['one'],
  2:  ['two'],
  3:  ['three'],
  4:  ['four'],
  5:  ['five'],
  6:  ['six'],
  7:  ['seven'],
  8:  ['eight'],
  9:  ['nine'],
  10: ['ten'],
  11: ['eleven'],
  12: ['twelve'],
  13: ['thirteen'],
  14: ['fourteen'],
  15: ['a quarter', 'fifteen'],
  16: ['sixteen'],
  17: ['seventeen'],
  18: ['eighteen'],
  19: ['nineteen'],
  20: ['twenty'],
  21: ['twenty one'],
  22: ['twenty two'],
  23: ['twenty three'],
  24: ['twenty four'],
  25: ['twenty five'],
  26: ['twenty six'],
  27: ['twenty seven'],
  28: ['twenty eight'],
  29: ['twenty nine'],
  30: ['thirty'],
  31: ['thirty one'],
  32: ['thirty two'],
  33: ['thirty three'],
  34: ['thirty four'],
  35: ['thirty five'],
  36: ['thirty six'],
  37: ['thirty seven'],
  38: ['thirty eight'],
  39: ['thirty nine'],
};

/**
 * Spoken forms for a minute value used in "H:MM" / "H oh MM" style.
 * Minute 0 can be "sharp" / "" (empty string = bare hour).
 */
export const MINUTE_CLOCKFACE_WORDS: Record<number, string[]> = {
  0:  ['', 'sharp', "o'clock"],
  1:  ['oh one'],
  2:  ['oh two'],
  3:  ['oh three'],
  4:  ['oh four'],
  5:  ['oh five'],
  6:  ['oh six'],
  7:  ['oh seven'],
  8:  ['oh eight'],
  9:  ['oh nine'],
  10: ['ten'],
  11: ['eleven'],
  12: ['twelve'],
  13: ['thirteen'],
  14: ['fourteen'],
  15: ['fifteen'],
  16: ['sixteen'],
  17: ['seventeen'],
  18: ['eighteen'],
  19: ['nineteen'],
  20: ['twenty'],
  21: ['twenty one'],
  22: ['twenty two'],
  23: ['twenty three'],
  24: ['twenty four'],
  25: ['twenty five'],
  26: ['twenty six'],
  27: ['twenty seven'],
  28: ['twenty eight'],
  29: ['twenty nine'],
  30: ['thirty'],
  31: ['thirty one'],
  32: ['thirty two'],
  33: ['thirty three'],
  34: ['thirty four'],
  35: ['thirty five'],
  36: ['thirty six'],
  37: ['thirty seven'],
  38: ['thirty eight'],
  39: ['thirty nine'],
  40: ['forty'],
  41: ['forty one'],
  42: ['forty two'],
  43: ['forty three'],
  44: ['forty four'],
  45: ['forty five'],
  46: ['forty six'],
  47: ['forty seven'],
  48: ['forty eight'],
  49: ['forty nine'],
  50: ['fifty'],
  51: ['fifty one'],
  52: ['fifty two'],
  53: ['fifty three'],
  54: ['fifty four'],
  55: ['fifty five'],
  56: ['fifty six'],
  57: ['fifty seven'],
  58: ['fifty eight'],
  59: ['fifty nine'],
};

/** am/pm label for a 24-hour value 0..23 */
export function ampmLabel(hour24: number): string {
  if (hour24 === 0 || hour24 === 12) return '';
  return hour24 < 12 ? 'am' : 'pm';
}
