from pydantic import PrivateAttr

from dispatcher.dispatchers.base_dispatcher import BaseDispatcher
from elevator.schemas.elevator import Elevator
from passenger.schemas.passenger_request import PassengerRequest


class RoundRobinDispatcher(BaseDispatcher):
    name: str = "RoundRobin"

    _index: int = PrivateAttr(default=0)  # currently assigned elevator

    def assign(
        self,
        requests: list[PassengerRequest],
    ) -> list[tuple[PassengerRequest, Elevator]]:
        elevators = self.elevators_available
        result = []
        for request in requests:
            result.append((request, elevators[self._index % len(elevators)]))
            self._index += 1
        return result
