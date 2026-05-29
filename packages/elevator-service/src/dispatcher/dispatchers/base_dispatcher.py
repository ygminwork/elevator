from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any, Optional, Tuple

from pydantic import BaseModel, Field, PrivateAttr

from building.schemas.building import Building
from dispatcher.schemas.dispatcher_output import DispatcherOutput
from dispatcher.schemas.dispatcher_timestamp import DispatcherTimestamp
from elevator.schemas.elevator import Elevator
from passenger.schemas.passenger import Passenger
from passenger.schemas.passenger_request import PassengerRequest


class BaseDispatcher(BaseModel, ABC):
    """
    Base class for dispatchers
    """

    building: Building = Field(description="building")
    _requests: list[PassengerRequest] = PrivateAttr(
        default_factory=list
    )  # all requests

    def __init__(
        self,
        requests: Optional[list[PassengerRequest | Tuple]] = None,
        **kwargs: dict[str, Any],
    ):
        super().__init__(**kwargs)
        _requests: list[PassengerRequest] = []
        if requests:
            if isinstance(requests[0], Tuple):
                _requests = list(map(PassengerRequest.deserialize, requests))
            else:
                _requests = requests
        _requests.sort(key=lambda x: x.time_request)
        self._requests = _requests

    @property
    def elevators_available(self) -> list[Elevator]:
        return [e for e in self.building.elevators if e.availibility > 0]

    @abstractmethod
    def assign(
        self,
        requests: list[PassengerRequest],
    ) -> list[tuple[PassengerRequest, Elevator]]:
        raise NotImplementedError

    async def dispatch(self) -> DispatcherOutput:
        current_time = 0
        elevators = self.building.elevators
        requests_all = self._requests
        requests_queue = list(requests_all)
        passengers = list(
            map(lambda v: Passenger(id=v), set([r.passenger_id for r in requests_all]))
        )
        output = DispatcherOutput(
            floors=self.building.n_floors,
            passengers=passengers,
            requests=requests_all,
            timestamps=[
                DispatcherTimestamp(
                    time=current_time,
                    elevators=deepcopy(elevators),
                )
            ],
        )

        while requests_queue or any(e.is_busy() for e in elevators):
            current_time += 1

            requests_current: list[PassengerRequest] = []
            while requests_queue and requests_queue[0].time_request <= current_time:
                requests_current.append(requests_queue.pop(0))

            if requests_current and self.elevators_available:
                for r, e in self.assign(requests_current):
                    e.assign(r)

            for e in elevators:
                e.tick(current_time)

            output.timestamps.append(
                DispatcherTimestamp(
                    time=current_time,
                    elevators=deepcopy(elevators),
                )
            )

        return output
