from __future__ import annotations

import re

from .smush import smush


def word_presence_score(
    grid: str,
    token_lists: dict[str, list[list[str]]],
) -> float:
    """Construct-phase score: sum over all 12h times of the maximum fraction of
    phrase-words that appear anywhere in *grid* as contiguous substrings.

    Word order is NOT checked here — that is the job of the regex scorer.
    This is a fast heuristic that rewards grids containing useful building
    blocks even before any full phrase is assembled.
    """
    total = 0.0
    for phrases in token_lists.values():
        best = 0.0
        for tokens in phrases:
            if not tokens:
                continue
            frac = sum(1 for t in tokens if t in grid) / len(tokens)
            if frac > best:
                best = frac
                if best == 1.0:
                    break  # can't do better for this time
        total += best
    return total


def construct_score(
    words: list[str],
    token_lists: dict[str, list[list[str]]],
) -> float:
    """word_presence_score / smushed_length — rewards coverage per letter."""
    grid = smush(words)
    if not grid:
        return 0.0
    return word_presence_score(grid, token_lists) / len(grid)


def compile_patterns(
    token_lists: dict[str, list[list[str]]],
) -> dict[str, re.Pattern[str]]:
    """One compiled regex per 12h time key.

    Matches when any of the time's phrase options has all its words present
    as contiguous substrings in left-to-right order.
    """
    patterns: dict[str, re.Pattern[str]] = {}
    for time_key, phrases in token_lists.items():
        alts = [
            ".*".join(re.escape(t) for t in tokens)
            for tokens in phrases
            if tokens
        ]
        if alts:
            patterns[time_key] = re.compile("|".join(f"(?:{a})" for a in alts))
    return patterns


def covered_times(
    grid: str,
    patterns: dict[str, re.Pattern[str]],
) -> set[str]:
    """Return the set of 12h time keys fully covered by *grid*."""
    return {tk for tk, pat in patterns.items() if pat.search(grid)}
