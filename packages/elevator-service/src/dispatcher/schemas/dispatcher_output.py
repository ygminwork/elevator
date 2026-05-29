from pydantic import BaseModel, Field, computed_field

from dispatcher.schemas.dispatcher_statistics import DispatcherStatistics
from dispatcher.schemas.dispatcher_summary import DispatcherSummary
from dispatcher.schemas.dispatcher_timestamp import DispatcherTimestamp
from passenger.schemas.passenger import Passenger
from passenger.schemas.passenger_request import PassengerRequest


class DispatcherOutput(BaseModel):
    floors: int = Field(description="number of floors")
    requests: list[PassengerRequest] = Field(
        description="passenger requests",
        default_factory=list,
    )
    passengers: list[Passenger] = Field(
        description="passengers",
        default_factory=list,
    )
    timestamps: list[DispatcherTimestamp] = Field(
        description="timestamped history of elevators",
        default_factory=list,
    )

    @computed_field
    @property
    def summary(self) -> DispatcherSummary:
        requests: list[PassengerRequest] = [
            r
            for r in self.requests
            if r.time_pickup is not None and r.time_dropoff is not None
        ]
        if not requests:
            raise ValueError("no completed requests")

        n = len(requests)
        ideals = [abs(r.dropoff - r.pickup) for r in requests]
        actuals = [float(r.time_travel) for r in requests]

        total_ideal = sum(ideals)
        total_actual = sum(actuals)
        speed_score = total_ideal / total_actual if total_actual > 0 else 0.0

        times_wait = [float(r.time_wait) for r in requests]
        times_total = [float(r.time_total) for r in requests]
        detours = [actuals[i] / ideals[i] if ideals[i] > 0 else 0.0 for i in range(n)]

        timestamps = self.timestamps
        elevators = timestamps[-1].elevators
        utilized = sum(
            e1.occupancy
            for t1, t2 in zip(timestamps, timestamps[1:], strict=False)
            for e1, e2 in zip(t1.elevators, t2.elevators, strict=True)
            if e2.floor != e1.floor
        )
        total_capacity = sum(e.travel * e.capacity for e in elevators)
        efficiency_score = utilized / total_capacity if total_capacity > 0 else 0.0

        return DispatcherSummary(
            detour_statistics=DispatcherStatistics.from_values(detours),
            efficiency_score=efficiency_score,
            speed_score=speed_score,
            time_total_statistics=DispatcherStatistics.from_values(times_total),
            time_wait_statistics=DispatcherStatistics.from_values(times_wait),
        )
