from dataclasses import dataclass
from typing import Dict
import json
from pathlib import Path

@dataclass
class EditorConfig:
    command: str
    file_associations: Dict[str, str]
    uti_associations: Dict[str, str]


def load_config(path: Path) -> EditorConfig:
    raw = json.loads(path.read_text())

    return EditorConfig(
        command=raw["command"],
        file_associations={
            ext.lower(): lang
            for ext, lang in raw.get("extensions_devIconFoldername", {}).items()
        },
        uti_associations={
            uti: lang
            for uti, lang in raw.get("utis_devIconFoldername", {}).items()
        },
    )
