import statistics

import numpy as np
from pydantic import BaseModel, Field


class DispatcherStatistics(BaseModel):
    max: float = Field(description="maximum")
    mean: float = Field(description="average")
    min: float = Field(description="minimum")
    p1: float = Field(description="1st percentile")
    p10: float = Field(description="10th percentile")
    p25: float = Field(description="25th percentile")
    p50: float = Field(description="50th percentile")
    p75: float = Field(description="75th percentile")
    p90: float = Field(description="90th percentile")
    p99: float = Field(description="99th percentile")
    stddev: float = Field(description="standard deviation")
    jains_fairness_score: float = Field(description="Jain's fairness score")
    gini_fairness_score: float = Field(description="Gini fairness score")

    @staticmethod
    def from_values(
        values: list[float],
    ) -> "DispatcherStatistics":
        values = sorted(values)
        return DispatcherStatistics(
            mean=statistics.mean(values),
            stddev=statistics.pstdev(values),
            min=values[0],
            max=values[-1],
            **{f"p{p}": np.percentile(values, p) for p in [1, 10, 25, 50, 75, 90, 99]},
            gini_fairness_score=DispatcherStatistics.gini_fairness(values),
            jains_fairness_score=DispatcherStatistics.jains_fairness(values),
        )

    @staticmethod
    def gini_fairness(
        values: list[float],
    ) -> float:
        n = len(values)
        mean = statistics.mean(values)
        if n < 2 or mean < 0:
            return 0
        total = sum(abs(xi - xj) for xi in values for xj in values)
        return 1 - total / (2 * n**2 * mean)

    @staticmethod
    def jains_fairness(
        values: list[float],
    ) -> float:
        n = len(values)
        if n == 0:
            return 0.0
        denominator = n * sum(v**2 for v in values)
        if denominator == 0:
            return 0.0
        return (sum(values) ** 2) / denominator
