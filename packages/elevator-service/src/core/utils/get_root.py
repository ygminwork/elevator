from pathlib import Path


def get_root(marker: str = "README.md"):
    current_path = Path(__file__).resolve()
    for parent in current_path.parents:
        if (parent / marker).exists():
            return parent
    return current_path.parent
