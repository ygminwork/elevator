import pytest

from building.schemas.building import building_fixture
from core.utils.read_json import read_json
from core.utils.write_json import write_json
from dispatcher.dispatchers.linear_optimization_dispatcher import (
    LinearOptimizationDispatcher,
)
from dispatcher.dispatchers.marginal_cost_dispatcher import MarginalCostDispatcher
from dispatcher.dispatchers.nearest_dispatcher import NearestDispatcher
from dispatcher.dispatchers.round_robin_dispatcher import RoundRobinDispatcher
from passenger.schemas.passenger_request import PassengerRequest


@pytest.mark.asyncio
async def test_dispatcher():
    requests = read_json(pathname="data/requests.json", cls=list[PassengerRequest])

    algorithms = [
        RoundRobinDispatcher,
        NearestDispatcher,
        MarginalCostDispatcher,
        LinearOptimizationDispatcher,
    ]
    for algorithm in algorithms:
        dispatcher = algorithm(
            building=building_fixture,
            requests=requests,
        )
        output = await dispatcher.dispatch()
        write_json(
            pathname=f"stats/{dispatcher.name}.json",
            value=output.model_dump(mode="json"),
        )
