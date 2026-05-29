# app/routers/users.py
import asyncio

from fastapi import APIRouter

from building.schemas.building import Building
from building.schemas.floor import Floor
from dispatcher.dispatchers.linear_optimization_dispatcher import (
    LinearOptimizationDispatcher,
)
from dispatcher.schemas.dispatcher_output import DispatcherOutput
from elevator.schemas.elevator import Elevator

dispatcher_api = APIRouter(prefix="/api/dispatcher")


@dispatcher_api.post(
    "/dispatch",
    response_model=DispatcherOutput,
)
async def dispatch():
    n_floors = 10
    building = Building(
        floors=[Floor(level=i) for i in range(1, n_floors + 1)],
        elevators=[
            Elevator(capacity=5),
            Elevator(capacity=5),
        ],
    )
    requests = [
        (0, "passenger1", 1, 9),
        (3, "passenger2", 5, 1),
        (10, "passenger3", 3, 8),
    ]
    dispatcher = LinearOptimizationDispatcher(
        building=building,
        requests=requests,
    )
    await asyncio.sleep(1)
    return await dispatcher.dispatch()
