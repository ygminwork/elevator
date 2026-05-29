from pydantic import BaseModel, Field

from building.schemas.floor import FloorType


class PassengerFlow(BaseModel):
    weight: float = Field(description="passenger flow weight", default=1.0)
    source_floor_types: list[FloorType] = Field(
        description="source floor types",
        default_factory=list,
    )
    destination_floor_types: list[FloorType] = Field(
        description="destination floor types",
        default_factory=list,
    )
