"""TimePhrase dataclass and render_time convenience function."""

from __future__ import annotations

from dataclasses import dataclass

from .timewords import ampm_label


@dataclass(frozen=True)
class TimePhrase:
    hour: int   # 0–23
    min: int    # 0–59
    timewords: str

    def __post_init__(self) -> None:
        if not 0 <= self.hour <= 23:
            raise ValueError(f"hour {self.hour} out of range 0–23")
        if not 0 <= self.min <= 59:
            raise ValueError(f"min {self.min} out of range 0–59")

    @property
    def ampm(self) -> str:
        return ampm_label(self.hour)

    @property
    def words(self) -> str:
        parts = [self.timewords, self.ampm]
        return " ".join(p for p in parts if p)

    @property
    def time_key(self) -> str:
        return f"{self.hour:02d}:{self.min:02d}"

    def __str__(self) -> str:
        return f'[{self.time_key}] "{self.words}"'


def render_time(hour: int, minute: int, timewords: str) -> TimePhrase:
    return TimePhrase(hour=hour, min=minute, timewords=timewords)
