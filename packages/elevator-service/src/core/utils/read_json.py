import json
from typing import Type, TypeVar

from pydantic import TypeAdapter, ValidationError

from core.utils.get_root import get_root
from dispatcher.configs.global_config import global_config

T = TypeVar("T")


def read_json(pathname: str, cls: Type[T]) -> T:
    pathname = get_root() / global_config.outdir / pathname
    with open(pathname, "r") as f:
        value = json.load(f)
    try:
        return TypeAdapter(cls).validate_python(value)
    except ValidationError as e:
        raise TypeError(f"invalid type: {e}") from e
