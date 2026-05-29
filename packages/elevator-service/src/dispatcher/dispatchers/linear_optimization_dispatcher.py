from typing import ClassVar

import numpy as np
import pulp

from core.utils.logger import logger
from dispatcher.dispatchers.base_dispatcher import BaseDispatcher
from dispatcher.dispatchers.marginal_cost_dispatcher import MarginalCostDispatcher
from elevator.schemas.elevator import Elevator
from passenger.schemas.passenger_request import PassengerRequest


class LinearOptimizationDispatcher(BaseDispatcher):
    name: str = "LinearOptimization"
    fallback_dispatcher: ClassVar[type[BaseDispatcher]] = MarginalCostDispatcher

    def _fallback(
        self,
        requests: list[PassengerRequest],
        elevators: list[Elevator],
    ) -> dict[PassengerRequest, Elevator]:
        dispatcher = self.fallback_dispatcher(building=self.building)
        return dispatcher.assign(requests)

    def assign(
        self,
        requests: list[PassengerRequest],
    ) -> list[tuple[PassengerRequest, Elevator]]:
        elevators = self.elevators_available
        if len(requests) == 1:
            return self._fallback(requests, elevators)

        n_requests, n_elevators = len(requests), len(elevators)
        cost_matrix = np.array([[e.eta(r) for e in elevators] for r in requests])

        problem = pulp.LpProblem("LinearOptimization", pulp.LpMinimize)
        x = np.array(
            pulp.LpVariable.matrix(
                "x",
                (range(n_requests), range(n_elevators)),
                cat="Binary",
            )
        ).reshape(n_requests, n_elevators)

        problem += pulp.lpSum(cost_matrix * x)
        for i in range(n_requests):
            problem += pulp.lpSum(x[i]) == 1

        for j, elevator in enumerate(elevators):
            problem += pulp.lpSum(x[:, j]) <= elevator.availibility

        problem.solve()
        if pulp.LpStatus[problem.status] == "Optimal":
            assignments = np.vectorize(pulp.value)(x) > 0.5
            return [
                (requests[i], elevators[j])
                for i, j in zip(*np.where(assignments), strict=True)
            ]

        logger.warning(
            "linear optimization failed, falling back to %s",
            self.fallback_dispatcher,
        )
        return self._fallback(requests, elevators)
