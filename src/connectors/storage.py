""" Storage interface module """

import json
from pathlib import Path

STORAGE_PATH = Path(__file__).parent.parent.parent / "storage"


class Storage:
    """Storage interface for connectors"""

    def __init__(self):
        if not STORAGE_PATH.exists():
            STORAGE_PATH.mkdir()

    def write(self, data: dict, uuid: str):
        """Write data to storage"""
        item_path = STORAGE_PATH / f"{uuid}.json"
        with open(item_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(data))

    def read(self, uuid):
        """Read data from storage"""
        item_path = STORAGE_PATH / f"{uuid}.json"
        if not item_path.exists():
            return None
        with open(item_path, "r", encoding="utf-8") as f:
            return json.loads(f.read())

    def delete(self, uuid):
        """Delete data from storage"""
        item_path = STORAGE_PATH / f"{uuid}.json"
        if item_path.exists():
            item_path.unlink()
