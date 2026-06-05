import pytest
from clockwords.solver.vocab import token_lists_12h, all_words
from clockwords.solver.score import (
    compile_patterns,
    construct_score,
    covered_times,
    word_presence_score,
)

# Module-level fixtures — expensive to build, shared across all tests
TOKEN_LISTS = token_lists_12h()
PATTERNS    = compile_patterns(TOKEN_LISTS)


class TestTokenLists12h:
    def test_exactly_720_keys(self):
        assert len(TOKEN_LISTS) == 720

    def test_keys_are_00_to_11(self):
        hours = {int(k[:2]) for k in TOKEN_LISTS}
        assert hours == set(range(12))

    def test_midnight_and_noon_share_key(self):
        # "00:00" must have both "midnight" and "noon" phrase options
        cores = {tuple(tl) for tl in TOKEN_LISTS["00:00"]}
        assert ("midnight",) in cores
        assert ("noon",)     in cores
        assert ("twelve",)   in cores   # shared between both hours

    def test_no_ampm_tokens(self):
        # "am" and "pm" must never appear — core phrases only
        all_tokens = {t for tl_list in TOKEN_LISTS.values() for tl in tl_list for t in tl}
        assert "am" not in all_tokens
        assert "pm" not in all_tokens


class TestWordPresenceScore:
    def test_empty_grid_is_zero(self):
        assert word_presence_score("", TOKEN_LISTS) == 0.0

    def test_junk_grid_is_zero(self):
        assert word_presence_score("zzz", TOKEN_LISTS) == 0.0

    def test_single_word_scores_positively(self):
        assert word_presence_score("one", TOKEN_LISTS) > 0

    def test_more_useful_words_score_higher(self):
        s_one  = word_presence_score("one",     TOKEN_LISTS)
        s_many = word_presence_score("tenoone", TOKEN_LISTS)
        assert s_many > s_one

    def test_scores_partial_phrases(self):
        # "pastone" has "past" and "one" but not a third word —
        # still scores higher than "one" alone
        assert word_presence_score("pastone", TOKEN_LISTS) > \
               word_presence_score("one",     TOKEN_LISTS)


class TestConstructScore:
    def test_empty_list_is_zero(self):
        assert construct_score([], TOKEN_LISTS) == 0.0

    def test_positive_for_real_words(self):
        for w in ["one", "noon", "past", "quarter"]:
            assert construct_score([w], TOKEN_LISTS) > 0

    def test_efficient_triplet_beats_single_word(self):
        # "tenoone" packs three useful words in 7 chars
        assert construct_score(["ten", "noon", "one"], TOKEN_LISTS) >= \
               construct_score(["ten"],               TOKEN_LISTS)


class TestCoveredTimes:
    def test_720_patterns_compiled(self):
        assert len(PATTERNS) == 720

    # --- individual word coverage (core-only matching) ---

    def test_noon_covers_0000(self):
        assert "00:00" in covered_times("noon", PATTERNS)

    def test_midnight_covers_0000(self):
        assert "00:00" in covered_times("midnight", PATTERNS)

    def test_twelve_covers_0000(self):
        assert "00:00" in covered_times("twelve", PATTERNS)

    def test_ten_covers_1000(self):
        # core phrase for 10:00 is just "ten"
        assert "10:00" in covered_times("ten", PATTERNS)

    def test_one_covers_0100(self):
        assert "01:00" in covered_times("one", PATTERNS)

    # --- tenoone covers three times ---

    def test_tenoone_covers_noon(self):
        assert "00:00" in covered_times("tenoone", PATTERNS)

    def test_tenoone_covers_ten_oclock(self):
        assert "10:00" in covered_times("tenoone", PATTERNS)

    def test_tenoone_covers_one_oclock(self):
        assert "01:00" in covered_times("tenoone", PATTERNS)

    def test_tenoone_does_not_cover_10_05(self):
        # 10:05 needs "five" (or "oh") — not in "tenoone"
        assert "10:05" not in covered_times("tenoone", PATTERNS)

    # --- ordering is enforced ---

    def test_words_must_appear_in_phrase_order(self):
        # "five past three" covers 03:05
        assert "03:05" in  covered_times("fivepastthree", PATTERNS)
        # reversed order does not
        assert "03:05" not in covered_times("threepastfive", PATTERNS)

    def test_words_must_be_contiguous(self):
        # letters present but not forming the word
        assert "10:00" not in covered_times("taebcn",  PATTERNS)
        assert "10:00" in     covered_times("ten",      PATTERNS)

    # --- multi-word phrases ---

    def test_quarter_past_three_covers_0315(self):
        assert "03:15" in covered_times("quarterpastthree", PATTERNS)

    def test_half_past_covers_x30(self):
        assert "02:30" in covered_times("halfpasttwo", PATTERNS)
