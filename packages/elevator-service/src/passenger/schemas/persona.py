from pydantic import BaseModel, Field


class Persona(BaseModel):
    name: str = Field(description="persona name")
    weight: float = Field(description="persona weight", default=1.0)
    floor_levels: list[int] = Field(description="floor levels", default_factory=list)
    rate_travel: float = Field(description="travel rate", default=1.0)
