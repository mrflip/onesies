from clockwords.solver.greedy import greedy_seed
from clockwords.solver.score import compile_patterns, construct_score, covered_times
from clockwords.solver.smush import smush
from clockwords.solver.vocab import all_words, token_lists_12h

TOKEN_LISTS = token_lists_12h()
VOCAB       = all_words()
PATTERNS    = compile_patterns(TOKEN_LISTS)


class TestGreedySeed:
    def test_expands_from_single_start(self):
        result = greedy_seed(["ten"], VOCAB, TOKEN_LISTS, max_words=6)
        assert len(result) > 1

    def test_preserves_start_word(self):
        result = greedy_seed(["noon"], VOCAB, TOKEN_LISTS, max_words=6)
        assert "noon" in result

    def test_no_duplicate_words(self):
        result = greedy_seed(["past"], VOCAB, TOKEN_LISTS, max_words=8)
        assert len(result) == len(set(result))

    def test_all_words_from_vocab(self):
        result = greedy_seed(["one"], VOCAB, TOKEN_LISTS, max_words=6)
        assert all(w in VOCAB for w in result)

    def test_score_does_not_decrease(self):
        start  = ["ten"]
        result = greedy_seed(start, VOCAB, TOKEN_LISTS, max_words=8)
        assert construct_score(result, TOKEN_LISTS) >= construct_score(start, TOKEN_LISTS)

    def test_covers_more_times_than_start(self):
        start_times  = covered_times(smush(["ten"]),               PATTERNS)
        result       = greedy_seed(["ten"], VOCAB, TOKEN_LISTS, max_words=8)
        result_times = covered_times(smush(result),                PATTERNS)
        assert len(result_times) >= len(start_times)

    def test_smushed_length_is_sublinear_in_word_count(self):
        # Good smushing should give noticeable compression
        result = greedy_seed(["ten"], VOCAB, TOKEN_LISTS, max_words=8)
        grid = smush(result)
        avg_word_len = sum(len(w) for w in result) / len(result)
        assert len(grid) < len(result) * avg_word_len  # at least some overlap

    def test_empty_start_still_works(self):
        # Greedy from scratch: no start word, so max_words cap still applies
        result = greedy_seed([], VOCAB, TOKEN_LISTS, max_words=4)
        assert len(result) <= 4
