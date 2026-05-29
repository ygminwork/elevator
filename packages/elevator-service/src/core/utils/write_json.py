import json
from pathlib import Path

from core.utils.get_root import get_root
from dispatcher.configs.global_config import global_config


def write_json(
    pathname: str,
    value: str,
) -> None:
    fullpath = get_root() / global_config.outdir / pathname
    fullpath = Path(fullpath)
    fullpath.parent.mkdir(parents=True, exist_ok=True)
    fullpath = f"{fullpath.with_suffix('')}.json"
    with open(fullpath, "w") as f:
        json.dump(value, f, indent=2)
