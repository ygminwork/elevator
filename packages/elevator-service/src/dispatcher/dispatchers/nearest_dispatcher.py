from dispatcher.dispatchers.base_dispatcher import BaseDispatcher
from elevator.schemas.elevator import Elevator
from passenger.schemas.passenger_request import PassengerRequest


class NearestDispatcher(BaseDispatcher):
    name: str = "Nearest"

    def assign(
        self,
        requests: list[PassengerRequest],
    ) -> list[tuple[PassengerRequest, Elevator]]:
        elevators = self.elevators_available
        return [(r, min(elevators, key=lambda e: e.eta(r))) for r in requests]
