"""TimeTemplate subclasses: each generates a family of TimePhrase objects."""

from __future__ import annotations

from abc import ABC, abstractmethod
from itertools import product

from .phrases import TimePhrase
from .timewords import (
    MINUTE_CLOCKFACE_WORDS,
    MINUTE_PAST_WORDS,
    hour_words,
    hour_words_with_special,
)


def _all_hours(include_special: bool = True) -> list[tuple[int, str]]:
    """Return (h24, word) pairs for all hours 0–23."""
    pairs: list[tuple[int, str]] = []
    for h in range(24):
        words = hour_words_with_special(h) if include_special else hour_words(h)
        pairs.extend((h, w) for w in words)
    return pairs


class TimeTemplate(ABC):
    name: str

    @abstractmethod
    def generate_phrases(self) -> list[TimePhrase]:
        ...


class ClockfaceHourTT(TimeTemplate):
    name = "ClockfaceHour"

    def generate_phrases(self) -> list[TimePhrase]:
        phrases = []
        for h24, h_word in _all_hours():
            for m_word in MINUTE_CLOCKFACE_WORDS[0]:
                core = f"{h_word} {m_word}".strip() if m_word else h_word
                phrases.append(TimePhrase(h24, 0, core))
        return phrases


class ClockfaceMinuteTT(TimeTemplate):
    name = "ClockfaceMinute"

    def generate_phrases(self) -> list[TimePhrase]:
        phrases = []
        for (h24, h_word), m in product(_all_hours(), range(1, 60)):
            for m_word in MINUTE_CLOCKFACE_WORDS.get(m, []):
                phrases.append(TimePhrase(h24, m, f"{h_word} {m_word}"))
        return phrases


class MinutesPastHourTT(TimeTemplate):
    name = "MinutesPastHour"

    def generate_phrases(self) -> list[TimePhrase]:
        phrases = []
        for (h24, h_word), m in product(_all_hours(), range(1, 40)):
            for m_word in MINUTE_PAST_WORDS.get(m, []):
                phrases.append(TimePhrase(h24, m, f"{m_word} past {h_word}"))
        return phrases


class MinutesTilHourTT(TimeTemplate):
    name = "MinutesTilHour"

    def generate_phrases(self) -> list[TimePhrase]:
        phrases = []
        for (h24, h_word), offset in product(_all_hours(), range(1, 40)):
            minute = (60 - offset) % 60
            actual_h24 = (h24 - 1) % 24
            for m_word in MINUTE_PAST_WORDS.get(offset, []):
                phrases.append(TimePhrase(actual_h24, minute, f"{m_word} til {h_word}"))
        return phrases


class MinutesToHourTT(TimeTemplate):
    name = "MinutesToHour"

    def generate_phrases(self) -> list[TimePhrase]:
        phrases = []
        for (h24, h_word), offset in product(_all_hours(), range(1, 40)):
            minute = (60 - offset) % 60
            actual_h24 = (h24 - 1) % 24
            for m_word in MINUTE_PAST_WORDS.get(offset, []):
                phrases.append(TimePhrase(actual_h24, minute, f"{m_word} to {h_word}"))
        return phrases


class QuarterPastHourTT(TimeTemplate):
    name = "QuarterPastHour"

    def generate_phrases(self) -> list[TimePhrase]:
        return [TimePhrase(h24, 15, f"quarter past {word}") for h24, word in _all_hours()]


class QuarterTilHourTT(TimeTemplate):
    name = "QuarterTilHour"

    def generate_phrases(self) -> list[TimePhrase]:
        return [TimePhrase((h24 - 1) % 24, 45, f"quarter til {word}") for h24, word in _all_hours()]


class QuarterToHourTT(TimeTemplate):
    name = "QuarterToHour"

    def generate_phrases(self) -> list[TimePhrase]:
        return [TimePhrase((h24 - 1) % 24, 45, f"quarter to {word}") for h24, word in _all_hours()]


class HalfPastHourTT(TimeTemplate):
    name = "HalfPastHour"

    def generate_phrases(self) -> list[TimePhrase]:
        return [TimePhrase(h24, 30, f"half past {word}") for h24, word in _all_hours()]


class FractionHourTT(TimeTemplate):
    name = "FractionHour"

    def generate_phrases(self) -> list[TimePhrase]:
        fractions = [(15, "and a quarter"), (30, "and a half")]
        return [
            TimePhrase(h24, minute, f"{word} {fword}")
            for h24, word in _all_hours()
            for minute, fword in fractions
        ]


ALL_TEMPLATES: list[TimeTemplate] = [
    ClockfaceHourTT(),
    ClockfaceMinuteTT(),
    MinutesPastHourTT(),
    MinutesTilHourTT(),
    MinutesToHourTT(),
    QuarterPastHourTT(),
    QuarterTilHourTT(),
    QuarterToHourTT(),
    HalfPastHourTT(),
    FractionHourTT(),
]
