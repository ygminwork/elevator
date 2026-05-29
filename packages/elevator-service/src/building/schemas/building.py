from collections import defaultdict

from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator

from building.schemas.building_input import building_input_fixture
from building.schemas.floor import Floor, FloorType
from core.utils.uid import uid
from elevator.schemas.elevator import Elevator


class Building(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    id: str = Field(
        description="building id",
        default_factory=lambda: uid("building"),
    )
    floors: list[Floor] = Field(
        description="floors in the building",
        default_factory=list,
    )
    elevators: list[Elevator] = Field(
        description="elevators in the building",
        default_factory=list,
    )
    populations: defaultdict[int, int] = Field(
        description="population per floor",
        default_factory=lambda: defaultdict(int),
    )

    @computed_field
    @property
    def n_floors(self) -> int:
        return len(self.floors)

    @field_validator("floors")
    @classmethod
    def validate_floors(cls, floors: list[Floor]) -> list[Floor]:
        if not floors:
            return []

        floors = sorted(floors, key=lambda f: f.level)
        levels = [f.level for f in floors]
        if len(set(levels)) != len(levels):
            raise ValueError("duplicate floor levels")
        if levels[-1] - levels[0] != len(levels) - 1:
            raise ValueError("non-consecutive floor levels")
        return floors


building_fixture = Building(
    floors=[
        Floor(level=1, floor_type=FloorType.LOBBY),
        Floor(level=2, floor_type=FloorType.OFFICE, population=80),
        Floor(level=3, floor_type=FloorType.OFFICE, population=70),
        Floor(level=4, floor_type=FloorType.OFFICE, population=60),
        Floor(level=5, floor_type=FloorType.CAFETERIA),
        Floor(level=6, floor_type=FloorType.OFFICE, population=50),
        Floor(level=7, floor_type=FloorType.OFFICE, population=40),
        Floor(level=8, floor_type=FloorType.OFFICE, population=30),
        Floor(level=9, floor_type=FloorType.OFFICE, population=20),
        Floor(level=10, floor_type=FloorType.OFFICE, population=10),
    ],
    elevators=[
        Elevator(capacity=building_input_fixture.n_capacity)
        for _ in range(building_input_fixture.n_elevators)
    ],
)
