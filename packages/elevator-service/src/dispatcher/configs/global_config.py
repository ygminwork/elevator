from pydantic import BaseModel, Field


class GlobalConfig(BaseModel):
    dwell_tick: int = Field(description="dwell cost (in ticks)")
    tick_seconds: int = Field(description="seconds per tick")
    outdir: str = Field(description="output directory")
    n_population: int = Field(description="number of passengers")


global_config = GlobalConfig(
    dwell_tick=1,
    outdir="outputs",
    tick_seconds=10 * 60,  # 10 minutes
    n_population=50,
)
