from __future__ import annotations

import re
from collections import defaultdict

from clockwords.menu import TIME_MENU
from clockwords.phrases import TimePhrase


def normalize(text: str) -> str:
    """Lowercase and strip non-alpha chars  (\"o'clock\" → \"oclock\")."""
    return re.sub(r"[^a-z]", "", text.lower())


def _core_tokens(p: TimePhrase) -> list[str]:
    return [t for w in p.core.split() if (t := normalize(w))]


def token_lists_12h() -> dict[str, list[list[str]]]:
    """Phrase token lists keyed by 12-hour position ("00:00"–"11:59").

    Hours fold modulo 12 so h=0 (midnight) and h=12 (noon) share key "00:00",
    pooling their distinct phrase options.  Tokens come from core only — no
    ampm — since a 12-hour clock face does not show am/pm in the letter grid.
    Each key's list is deduplicated by token tuple.
    """
    raw: dict[str, list[list[str]]] = defaultdict(list)
    seen: dict[str, set[tuple[str, ...]]] = defaultdict(set)

    for time_key, phrases in TIME_MENU.items():
        h, m = int(time_key[:2]), int(time_key[3:])
        key = f"{h % 12:02d}:{m:02d}"
        for p in phrases:
            tokens = _core_tokens(p)
            t = tuple(tokens)
            if t not in seen[key]:
                seen[key].add(t)
                raw[key].append(tokens)

    return dict(raw)


def all_words() -> list[str]:
    """Sorted list of every unique word token that appears in any 12h phrase."""
    words: set[str] = set()
    for tl_list in token_lists_12h().values():
        for tl in tl_list:
            words.update(tl)
    return sorted(words)
