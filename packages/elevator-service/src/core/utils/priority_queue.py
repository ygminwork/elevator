import heapq
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, PrivateAttr


class PriorityType(Enum):
    MIN = -1
    MAX = 1


class PriorityQueue(BaseModel):
    priority_type: PriorityType = Field(
        description="min / max queue",
        default=PriorityType.MIN,
    )
    _heap: list[float] = PrivateAttr(default_factory=list)  # queue elements
    _values: set[float] = PrivateAttr(default_factory=set)  # present values

    def push(self, value: float) -> None:
        if value not in self._values:
            self._values.add(value)
            if self.priority_type == PriorityType.MAX:
                value *= -1
            heapq.heappush(self._heap, value)

    def pop(self) -> Optional[float]:
        if self.is_empty():
            return None
        value = heapq.heappop(self._heap)
        if self.priority_type == PriorityType.MAX:
            value *= -1
        self._values.remove(value)
        return value

    def peek(self) -> Optional[float]:
        if self.is_empty():
            return None
        value = self._heap[0]
        if self.priority_type == PriorityType.MAX:
            value *= -1
        return value

    def is_empty(self) -> bool:
        return len(self._heap) == 0

    def clear(self) -> None:
        self._heap = []
        self._values = set()

    @property
    def heap(self) -> list[float]:
        return self._heap

    def __len__(self) -> int:
        return len(self._heap)

    def __contains__(self, value: float) -> bool:
        return value in self._values
