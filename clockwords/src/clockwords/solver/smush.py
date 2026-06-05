from __future__ import annotations


def max_overlap(a: str, b: str) -> int:
    """Length of the longest suffix of *a* that is also a prefix of *b*."""
    limit = min(len(a), len(b))
    for n in range(limit, 0, -1):
        if a[-n:] == b[:n]:
            return n
    return 0


def smush(words: list[str]) -> str:
    """Concatenate *words* with maximum pairwise overlap at each join.

    Overlap is computed between the full accumulated string and the next word,
    so boundary effects compound: ["ten","noon","one"] → "tenoone".
    """
    if not words:
        return ""
    acc = words[0]
    for w in words[1:]:
        acc += w[max_overlap(acc, w):]
    return acc
