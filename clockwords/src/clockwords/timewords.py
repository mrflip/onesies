"""Vocabulary tables and helpers for clock-word phrase generation."""

from __future__ import annotations

HOUR_WORDS: dict[int, list[str]] = {
    0:  ["twelve"],
    1:  ["one"],
    2:  ["two"],
    3:  ["three"],
    4:  ["four"],
    5:  ["five"],
    6:  ["six"],
    7:  ["seven"],
    8:  ["eight"],
    9:  ["nine"],
    10: ["ten"],
    11: ["eleven"],
    12: ["twelve"],
}

SPECIAL_HOUR_NAMES: dict[int, list[str]] = {
    0:  ["midnight"],
    12: ["noon"],
}

MINUTE_PAST_WORDS: dict[int, list[str]] = {
    1:  ["one"],
    2:  ["two"],
    3:  ["three"],
    4:  ["four"],
    5:  ["five"],
    6:  ["six"],
    7:  ["seven"],
    8:  ["eight"],
    9:  ["nine"],
    10: ["ten"],
    11: ["eleven"],
    12: ["twelve"],
    13: ["thirteen"],
    14: ["fourteen"],
    15: ["a quarter", "fifteen"],
    16: ["sixteen"],
    17: ["seventeen"],
    18: ["eighteen"],
    19: ["nineteen"],
    20: ["twenty"],
    21: ["twenty one"],
    22: ["twenty two"],
    23: ["twenty three"],
    24: ["twenty four"],
    25: ["twenty five"],
    26: ["twenty six"],
    27: ["twenty seven"],
    28: ["twenty eight"],
    29: ["twenty nine"],
    30: ["thirty"],
    31: ["thirty one"],
    32: ["thirty two"],
    33: ["thirty three"],
    34: ["thirty four"],
    35: ["thirty five"],
    36: ["thirty six"],
    37: ["thirty seven"],
    38: ["thirty eight"],
    39: ["thirty nine"],
}

MINUTE_CLOCKFACE_WORDS: dict[int, list[str]] = {
    0:  ["", "sharp", "o'clock"],
    1:  ["oh one"],
    2:  ["oh two"],
    3:  ["oh three"],
    4:  ["oh four"],
    5:  ["oh five"],
    6:  ["oh six"],
    7:  ["oh seven"],
    8:  ["oh eight"],
    9:  ["oh nine"],
    10: ["ten"],
    11: ["eleven"],
    12: ["twelve"],
    13: ["thirteen"],
    14: ["fourteen"],
    15: ["fifteen"],
    16: ["sixteen"],
    17: ["seventeen"],
    18: ["eighteen"],
    19: ["nineteen"],
    20: ["twenty"],
    21: ["twenty one"],
    22: ["twenty two"],
    23: ["twenty three"],
    24: ["twenty four"],
    25: ["twenty five"],
    26: ["twenty six"],
    27: ["twenty seven"],
    28: ["twenty eight"],
    29: ["twenty nine"],
    30: ["thirty"],
    31: ["thirty one"],
    32: ["thirty two"],
    33: ["thirty three"],
    34: ["thirty four"],
    35: ["thirty five"],
    36: ["thirty six"],
    37: ["thirty seven"],
    38: ["thirty eight"],
    39: ["thirty nine"],
    40: ["forty"],
    41: ["forty one"],
    42: ["forty two"],
    43: ["forty three"],
    44: ["forty four"],
    45: ["forty five"],
    46: ["forty six"],
    47: ["forty seven"],
    48: ["forty eight"],
    49: ["forty nine"],
    50: ["fifty"],
    51: ["fifty one"],
    52: ["fifty two"],
    53: ["fifty three"],
    54: ["fifty four"],
    55: ["fifty five"],
    56: ["fifty six"],
    57: ["fifty seven"],
    58: ["fifty eight"],
    59: ["fifty nine"],
}


def hour_words(h: int) -> list[str]:
    """All word forms for hour h (0–23), excluding midnight/noon."""
    h12 = (h - 1) % 12 + 1
    return HOUR_WORDS.get(h12, [str(h12)])


def hour_words_with_special(h: int) -> list[str]:
    """All word forms including midnight/noon where applicable."""
    base = hour_words(h)
    special = SPECIAL_HOUR_NAMES.get(h, SPECIAL_HOUR_NAMES.get(h % 12, []))
    return base + special if special else base


def ampm_label(hour24: int) -> str:
    if hour24 in (0, 12):
        return ""
    return "am" if hour24 < 12 else "pm"
