#!/usr/bin/env python
"""Show greedy seeds from various starting words so you can sanity-check them."""

from clockwords.solver.greedy import greedy_seed
from clockwords.solver.score import compile_patterns, construct_score, covered_times
from clockwords.solver.smush import smush
from clockwords.solver.vocab import all_words, token_lists_12h

TOKEN_LISTS = token_lists_12h()
VOCAB       = all_words()
PATTERNS    = compile_patterns(TOKEN_LISTS)

STARTS = ["ten", "noon", "past", "quarter", "one", "twenty", "half"]
MAX_WORDS = 10

print(f"Vocabulary ({len(VOCAB)} words): {VOCAB}\n")

for start_word in STARTS:
    words = greedy_seed([start_word], VOCAB, TOKEN_LISTS, max_words=MAX_WORDS)
    grid  = smush(words)
    times = covered_times(grid, PATTERNS)
    score = construct_score(words, TOKEN_LISTS)

    print(f"seed={start_word!r}")
    print(f"  words  : {words}")
    print(f"  grid   : {grid!r}  (len={len(grid)})")
    print(f"  covered: {len(times)}/720 times")
    print(f"  score  : {score:.4f}")
    if times:
        sample = sorted(times)[:8]
        print(f"  sample : {sample}")
    print()
