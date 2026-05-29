from pydantic import BaseModel, Field

from dispatcher.schemas.dispatcher_statistics import DispatcherStatistics


class DispatcherSummary(BaseModel):
    time_wait_statistics: DispatcherStatistics = Field(
        description="wait time statistics",
    )
    time_total_statistics: DispatcherStatistics = Field(
        description="total time statistics",
    )
    detour_statistics: DispatcherStatistics = Field(
        description="detour statistics",
    )
    speed_score: float = Field(description="speed score")
    efficiency_score: float = Field(description="efficiency score")
