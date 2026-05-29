from enum import StrEnum

from pydantic import BaseModel, Field

from core.utils.uid import uid


class FloorType(StrEnum):
    GENERAL = "general"
    LOBBY = "lobby"
    CAFETERIA = "cafeteria"
    OFFICE = "office"


class Floor(BaseModel):
    id: str = Field(
        description="floor id",
        default_factory=lambda: uid("floor"),
    )
    level: int = Field(description="floor level")
    floor_type: FloorType = Field(description="floor type", default=FloorType.GENERAL)
    population: int = Field(description="population", default=0)
