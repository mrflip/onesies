"""Unit tests for the clockwords Python package."""

import pytest

from clockwords.phrases import TimePhrase
from clockwords.timewords import ampm_label, hour_words, hour_words_with_special
from clockwords.templates import (
    ClockfaceHourTT,
    HalfPastHourTT,
    MinutesPastHourTT,
    MinutesToHourTT,
    QuarterPastHourTT,
)
from clockwords.menu import phrases_for, TIME_MENU


# ---------------------------------------------------------------------------
# TimePhrase basics
# ---------------------------------------------------------------------------

class TestTimePhrase:
    def test_full_joins_core_and_ampm(self):
        p = TimePhrase(hour=3, min=15, core="quarter past three")
        assert p.full == "quarter past three am"

    def test_no_ampm_at_noon(self):
        p = TimePhrase(hour=12, min=0, core="noon")
        assert p.ampm == ""
        assert p.full == "noon"

    def test_no_ampm_at_midnight(self):
        p = TimePhrase(hour=0, min=0, core="midnight")
        assert p.ampm == ""

    def test_pm_label_afternoon(self):
        p = TimePhrase(hour=15, min=30, core="half past three")
        assert p.ampm == "pm"

    def test_time_key_format(self):
        assert TimePhrase(9, 5, "nine oh five").time_key == "09:05"

    def test_invalid_hour_raises(self):
        with pytest.raises(ValueError):
            TimePhrase(hour=24, min=0, core="bad")

    def test_invalid_min_raises(self):
        with pytest.raises(ValueError):
            TimePhrase(hour=1, min=60, core="bad")

    def test_str_format(self):
        p = TimePhrase(3, 15, "quarter past three")
        assert str(p) == '[03:15] "quarter past three am"'


# ---------------------------------------------------------------------------
# timewords vocabulary helpers
# ---------------------------------------------------------------------------

class TestTimewords:
    def test_hour_words_maps_h24_to_12h(self):
        assert "three" in hour_words(3)
        assert "three" in hour_words(15)

    def test_hour_words_no_special(self):
        assert "midnight" not in hour_words(0)
        assert "noon" not in hour_words(12)

    def test_hour_words_with_special_includes_midnight(self):
        assert "midnight" in hour_words_with_special(0)

    def test_hour_words_with_special_includes_noon(self):
        assert "noon" in hour_words_with_special(12)

    @pytest.mark.parametrize("h,expected", [
        (0, ""), (12, ""), (6, "am"), (18, "pm"),
    ])
    def test_ampm_label(self, h, expected):
        assert ampm_label(h) == expected


# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

class TestTemplates:
    def test_clockface_hour_generates_bare_hour(self):
        phrases = ClockfaceHourTT().generate_phrases()
        timewords_set = {p.core for p in phrases}
        assert "three" in timewords_set

    def test_clockface_hour_generates_oclock(self):
        phrases = ClockfaceHourTT().generate_phrases()
        timewords_set = {p.core for p in phrases}
        assert "three o'clock" in timewords_set

    def test_clockface_hour_all_at_minute_zero(self):
        phrases = ClockfaceHourTT().generate_phrases()
        assert all(p.min == 0 for p in phrases)

    def test_half_past_generates_correct_phrases(self):
        phrases = HalfPastHourTT().generate_phrases()
        timewords_set = {p.core for p in phrases}
        assert "half past three" in timewords_set
        assert "half past midnight" in timewords_set

    def test_half_past_all_at_minute_30(self):
        phrases = HalfPastHourTT().generate_phrases()
        assert all(p.min == 30 for p in phrases)

    def test_minutes_past_coverage(self):
        phrases = MinutesPastHourTT().generate_phrases()
        timewords_set = {p.core for p in phrases}
        assert "five past three" in timewords_set
        assert "a quarter past midnight" in timewords_set

    def test_minutes_to_hour(self):
        phrases = MinutesToHourTT().generate_phrases()
        timewords_set = {p.core for p in phrases}
        assert "five to four" in timewords_set

    def test_quarter_past_hour(self):
        phrases = QuarterPastHourTT().generate_phrases()
        assert all(p.min == 15 for p in phrases)
        timewords_set = {p.core for p in phrases}
        assert "quarter past one" in timewords_set


# ---------------------------------------------------------------------------
# TimeMenu
# ---------------------------------------------------------------------------

class TestTimeMenu:
    def test_all_1440_minutes_covered(self):
        assert len(TIME_MENU) == 24 * 60

    def test_phrases_for_3_15_includes_quarter_past(self):
        results = phrases_for(3, 15)
        words_set = {p.core for p in results}
        assert "quarter past three" in words_set

    def test_phrases_for_sorted_by_length(self):
        results = phrases_for(3, 0)
        lengths = [len(p.full) for p in results]
        assert lengths == sorted(lengths)

    def test_phrases_for_midnight_includes_midnight(self):
        results = phrases_for(0, 0)
        words_set = {p.core for p in results}
        assert "midnight" in words_set
