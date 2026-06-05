"""Write a dictionary to a line-oriented KV-JSON format.

Each line is valid TSV and the whole file is valid JSON:
  first line:  {"  key  :  <json_value>
  other lines: ,   key  :  <json_value>
  last line:   }
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def dump_kv_json(data: dict[str, Any], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for i, (key, val) in enumerate(data.items()):
            prefix = "{" if i == 0 else ","
            f.write(f"{prefix}\t{json.dumps(key)}\t:\t{json.dumps(val)}\n")
        f.write("}\n")
