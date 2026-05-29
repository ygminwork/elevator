from pydantic import BaseModel, Field

from elevator.schemas.elevator import Elevator


class DispatcherTimestamp(BaseModel):
    time: int = Field(
        description="current time",
        default=0,
    )
    elevators: list[Elevator] = Field(
        description="elevator states",
        default_factory=list,
    )
