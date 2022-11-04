from datetime import datetime
import json
from typing import Any, Dict


def save_in_json(path: str, data: Any):
    now = datetime.now().strftime("%d%m%Y_%H:%M:%S")
    with open(f"{path}/{now}.json", "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)