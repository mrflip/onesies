"""Dump TIME_MENU to tmp/TimeMenu.kv.json in line-oriented KV-JSON format."""

from pathlib import Path
from clockwords.menu import TIME_MENU
from clockwords.kv_json import dump_kv_json

output = Path(__file__).parents[1] / "tmp" / "TimeMenu.kv.json"

data = {
    time_key: [
        {"hour": p.hour, "min": p.min, "timewords": p.timewords, "words": p.words}
        for p in phrases
    ]
    for time_key, phrases in sorted(TIME_MENU.items())
}

dump_kv_json(data, output)
print(f"Wrote {len(data)} entries to {output}")
