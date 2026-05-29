from copy import deepcopy

import numpy as np

from dispatcher.dispatchers.base_dispatcher import BaseDispatcher
from elevator.schemas.elevator import Elevator
from passenger.schemas.passenger_request import PassengerRequest


class MarginalCostDispatcher(BaseDispatcher):
    name: str = "MarginalCost"

    def _cost(
        self,
        elevator: Elevator,
    ) -> float:
        cloned = deepcopy(elevator)
        all_requests = cloned.pickup_requests + cloned.dropoff_requests
        current_time = 0
        while cloned.is_busy():
            current_time += 1
            cloned.tick(current_time)
        return sum(
            (request.time_dropoff - request.time_request)
            for request in all_requests
            if request.time_dropoff is not None
        )

    def _marginal_cost(
        self,
        request: PassengerRequest,
        elevator: Elevator,
    ) -> float:
        current = self._cost(elevator)
        simulated = deepcopy(elevator)
        simulated.assign(deepcopy(request))
        return self._cost(simulated) - current

    def assign(
        self,
        requests: list[PassengerRequest],
    ) -> list[tuple[PassengerRequest, Elevator]]:
        elevators = self.elevators_available
        elevator_snapshots = list(map(deepcopy, elevators))
        return [
            (
                r,
                elevators[
                    np.argmin([self._marginal_cost(r, e) for e in elevator_snapshots])
                ],
            )
            for r in requests
        ]
