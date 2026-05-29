from pydantic import BaseModel, Field


class BuildingInput(BaseModel):
    n_capacity: int = Field(description="elevator capacity")
    n_elevators: int = Field(description="number of elevators")
    n_floors: int = Field(description="number of floors")


building_input_fixture = BuildingInput(
    n_capacity=5,
    n_elevators=5,
    n_floors=10,
)
