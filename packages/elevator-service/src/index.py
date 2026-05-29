from elevator.dispatchers.eta_dispatcher import EtaDispatcher

from building.schemas.building import Building
from building.schemas.floor import Floor
from elevator.schemas.elevator import Elevator

n_floors = 10

building = Building(
    floors=[Floor(level=i) for i in range(1, n_floors + 1)],
    elevators=[
        Elevator(capacity=5),
    ],
)

requests = [
    (0, "passenger1", 1, 9),
    (5, "passenger2", 5, 1),
    (10, "passenger3", 3, 8),
]

dispatcher = EtaDispatcher(
    building=building,
    requests=requests,
)

dispatcher.dispatch()
