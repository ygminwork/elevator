from collections import defaultdict

from pydantic import BaseModel, Field, PrivateAttr, computed_field

from core.utils.priority_queue import PriorityQueue, PriorityType
from core.utils.uid import uid
from dispatcher.configs.global_config import global_config
from elevator.constants import Direction
from passenger.schemas.passenger_request import PassengerRequest


class Elevator(BaseModel):
    capacity: int = Field(description="total capacity")
    id: str = Field(
        description="elevator id",
        default_factory=lambda: uid("elevator"),
    )
    floor: int = Field(
        description="current floor",
        default=1,
    )
    direction: Direction = Field(
        description="current direction",
        default=Direction.IDLE,
    )

    _is_open: bool = PrivateAttr(default=False)  # door is open
    _travel: int = PrivateAttr(default=0)  # travel counter
    _dwell: int = PrivateAttr(default=0)  # dwell count
    _occupancy: int = PrivateAttr(default=0)  # occupancy count
    _pickups: defaultdict[int, list[PassengerRequest]] = PrivateAttr(
        default_factory=lambda: defaultdict(list)
    )  # pickups by floor
    _dropoffs: defaultdict[int, list[PassengerRequest]] = PrivateAttr(
        default_factory=lambda: defaultdict(list)
    )  # dropoffs by floor
    _up_queue: PriorityQueue = PrivateAttr(
        default_factory=lambda: PriorityQueue(priority_type=PriorityType.MIN)
    )  # min heap for up queue
    _down_queue: PriorityQueue = PrivateAttr(
        default_factory=lambda: PriorityQueue(priority_type=PriorityType.MAX)
    )  # max heap for down queue

    @computed_field
    @property
    def occupancy(self) -> int:
        return self._occupancy

    @property
    def availibility(self) -> int:
        return self.capacity - self._occupancy

    @computed_field
    @property
    def is_open(self) -> bool:
        return self._is_open

    @computed_field
    @property
    def travel(self) -> int:
        return self._travel

    @computed_field
    @property
    def pickup_ids(self) -> dict[int, list[str]]:
        return {k: [request.id for request in r] for k, r in self._pickups.items()}

    @property
    def pickup_requests(self) -> list[PassengerRequest]:
        return [request for requests in self._pickups.values() for request in requests]

    @property
    def dropoff_requests(self) -> list[PassengerRequest]:
        return [request for requests in self._dropoffs.values() for request in requests]

    @computed_field
    @property
    def dropoff_ids(self) -> dict[int, list[str]]:
        return {k: [request.id for request in r] for k, r in self._dropoffs.items()}

    @computed_field
    @property
    def stops(self) -> list[int]:
        return self._up_queue.heap + [-f for f in self._down_queue.heap]

    def _push(self, target: int) -> None:
        current = self.floor

        if target > current:
            if target not in self._up_queue:
                self._up_queue.push(target)
            if self.direction == Direction.IDLE:
                self.direction = Direction.UP
        elif target < current:
            if target not in self._down_queue:
                self._down_queue.push(target)
            if self.direction == Direction.IDLE:
                self.direction = Direction.DOWN
        else:
            match self.direction:
                case Direction.UP:
                    if target not in self._down_queue:
                        self._down_queue.push(target)
                case Direction.DOWN:
                    if target not in self._up_queue:
                        self._up_queue.push(target)

    def assign(self, request: PassengerRequest) -> None:
        request.elevator_id = self.id
        current, pickup = self.floor, request.pickup
        self._pickups[pickup].append(request)
        if self.direction == Direction.IDLE and pickup == current:
            self.direction = request.direction
        else:
            self._push(pickup)

    def eta(
        self,
        request: PassengerRequest,
    ) -> float:
        direction_request, pickup, dropoff = (
            request.direction,
            request.pickup,
            request.dropoff,
        )
        direction_elevator, stops, current = (
            self.direction,
            self.stops,
            self.floor,
        )
        highest = max(stops + [current]) if stops else current
        lowest = min(stops + [current]) if stops else current

        routes: list[tuple[int, int]] = [(pickup, dropoff)]
        match direction_elevator:
            case Direction.IDLE:
                routes.append((current, pickup))
            case Direction.UP:
                if direction_request == Direction.UP and current <= pickup:
                    # Direct Path
                    routes.append((current, pickup))
                elif direction_request == Direction.DOWN:
                    # 1 turnaround
                    routes.extend([(current, highest), (pickup, highest)])
                else:
                    routes.extend(
                        [(current, highest), (lowest, highest), (lowest, pickup)]
                    )
                    # 2 turnarounds (passed)
            case Direction.DOWN:
                if direction_request == Direction.DOWN and current >= pickup:
                    # Direct Path
                    routes.append((pickup, current))
                elif direction_request == Direction.UP:
                    # 1 turnaround
                    routes.extend([(lowest, current), (lowest, pickup)])
                else:
                    # 2 turnarounds (passed)
                    routes.extend(
                        [(lowest, current), (lowest, highest), (pickup, highest)]
                    )
        total_cost = 0
        for route in routes:
            [low, high] = route
            dwell_tick = sum(global_config.dwell_tick for s in stops if low < s < high)
            total_cost += abs(high - low) + dwell_tick

        return total_cost

    def tick(self, time: int) -> None:
        current = self.floor

        # process dwelling
        if self._dwell:
            self._dwell -= 1
            return

        # process queues
        if self.direction == Direction.UP and self._up_queue.peek() == current:
            self._up_queue.pop()
        elif self.direction == Direction.DOWN and self._down_queue.peek() == current:
            self._down_queue.pop()

        self._is_open = False

        # process dropoffs
        if current in self._dropoffs:
            self._is_open = True
            dropoff_list = self._dropoffs.pop(current)
            for r in dropoff_list:
                r.time_dropoff = time
            self._occupancy -= len(dropoff_list)

        # process pickups
        if current in self._pickups:
            remaining = []

            for r in self._pickups[current]:
                is_same_direction = (
                    (self.direction == r.direction)
                    or (self.direction == Direction.UP and self._up_queue.is_empty())
                    or (
                        self.direction == Direction.DOWN and self._down_queue.is_empty()
                    )
                )

                if is_same_direction and self._occupancy < self.capacity:
                    self._is_open = True
                    r.time_pickup = time
                    self._dropoffs[r.dropoff].append(r)
                    self._push(r.dropoff)
                    self.direction = r.direction
                    self._occupancy += 1
                else:
                    remaining.append(r)

            if remaining:
                self._pickups[current] = remaining
                self._push(current)
            else:
                del self._pickups[current]

        # dwell cost
        if self._is_open and global_config.dwell_tick:
            self._dwell = global_config.dwell_tick
            return

        # determine next move
        match self.direction:
            case Direction.UP:
                if not self._up_queue.is_empty():
                    self.floor += 1
                elif not self._down_queue.is_empty():
                    self.direction = Direction.DOWN
                    self.floor -= 1
                else:
                    self.direction = Direction.IDLE
            case Direction.DOWN:
                if not self._down_queue.is_empty():
                    self.floor -= 1
                elif not self._up_queue.is_empty():
                    self.direction = Direction.UP
                    self.floor += 1
                else:
                    self.direction = Direction.IDLE

        if self.floor != current:
            self._travel += 1

    def is_busy(self) -> bool:
        return (
            not self._up_queue.is_empty()
            or not self._down_queue.is_empty()
            or bool(self._dropoffs)
            or bool(self._pickups)
        )
