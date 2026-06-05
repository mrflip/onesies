from __future__ import annotations

from .score import construct_score


def greedy_seed(
    start: list[str],
    vocab: list[str],
    token_lists: dict[str, list[list[str]]],
    max_words: int = 12,
) -> list[str]:
    """Append words from *vocab* one at a time, each step picking the word that
    most improves construct_score (word_presence / smushed_length).

    Stops at *max_words* or when no remaining vocab word improves the score.
    Words already in the current list are never re-added.
    """
    words = list(start)
    used = set(words)
    current_score = construct_score(words, token_lists)

    for _ in range(max_words - len(start)):
        best_word: str | None = None
        best_score = current_score

        for w in vocab:
            if w in used:
                continue
            s = construct_score(words + [w], token_lists)
            if s > best_score:
                best_score = s
                best_word = w

        if best_word is None:
            break

        words.append(best_word)
        used.add(best_word)
        current_score = best_score

    return words
