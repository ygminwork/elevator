from pydantic import BaseModel, Field

from core.utils.uid import uid


class Passenger(BaseModel):
    id: str = Field(
        description="passenger id",
        default_factory=lambda: uid("passenger"),
    )
