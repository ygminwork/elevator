from typing import Any, Optional, Tuple

from pydantic import BaseModel, Field, computed_field

from core.utils.uid import uid
from elevator.constants import Direction


class PassengerRequest(BaseModel):
    id: str = Field(
        description="request id",
        default_factory=lambda: uid("request"),
    )
    passenger_id: str = Field(description="passenger id")
    pickup: int = Field(description="pickup floor")
    dropoff: int = Field(description="dropoff floor")
    time_request: int = Field(description="request time")
    time_pickup: Optional[int] = Field(description="pickup time", default=None)
    time_dropoff: Optional[int] = Field(description="dropoff time", default=None)
    elevator_id: Optional[str] = Field(description="assigned elevator", default=None)

    @computed_field
    @property
    def time_wait(self) -> Optional[int]:
        if self.time_pickup is None:
            return None
        return self.time_pickup - self.time_request

    @computed_field
    @property
    def time_travel(self) -> Optional[int]:
        if self.time_pickup is None or self.time_dropoff is None:
            return None
        return self.time_dropoff - self.time_pickup

    @computed_field
    @property
    def time_total(self) -> Optional[int]:
        if self.time_dropoff is None:
            return None
        return self.time_dropoff - self.time_request

    @computed_field
    @property
    def direction(self) -> Direction:
        pickup, dropoff = self.pickup, self.dropoff
        if dropoff < pickup:
            return Direction.DOWN
        elif dropoff > pickup:
            return Direction.UP
        return Direction.IDLE

    @staticmethod
    def deserialize(data: Tuple[Any, Any, Any, Any]) -> "PassengerRequest":
        try:
            [time, id, source, dest] = data
            return PassengerRequest(
                time_request=int(time),
                passenger_id=str(id),
                pickup=int(source),
                dropoff=int(dest),
            )
        except Exception as e:
            print(e)
            raise TypeError("Invalid request data") from e

    def serialize(self) -> Tuple[int, str, int, int]:
        return [
            self.time_request,
            self.passenger_id,
            self.pickup,
            self.dropoff,
        ]
