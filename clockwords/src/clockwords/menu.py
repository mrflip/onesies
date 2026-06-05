"""TimeMenu: all phrases grouped by time key, with lookup helpers."""

from __future__ import annotations

from collections import defaultdict

from .phrases import TimePhrase
from .templates import ALL_TEMPLATES

TimeMenu = dict[str, list[TimePhrase]]


def build_time_menu() -> TimeMenu:
    menu: TimeMenu = defaultdict(list)
    for template in ALL_TEMPLATES:
        for phrase in template.generate_phrases():
            menu[phrase.time_key].append(phrase)
    return dict(menu)


TIME_MENU: TimeMenu = build_time_menu()


def phrases_for(hour: int, minute: int) -> list[TimePhrase]:
    key = f"{hour:02d}:{minute:02d}"
    return sorted(TIME_MENU.get(key, []), key=lambda p: len(p.full))


def coverage_summary() -> list[dict[str, object]]:
    return sorted(
        [{"time_key": k, "count": len(v)} for k, v in TIME_MENU.items()],
        key=lambda x: x["time_key"],
    )
