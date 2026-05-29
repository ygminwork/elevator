import uuid
from typing import Optional


def uid(prefix: Optional[str] = None) -> str:
    value = uuid.uuid4()
    return f"{prefix}-{value}" if prefix else str(value)
