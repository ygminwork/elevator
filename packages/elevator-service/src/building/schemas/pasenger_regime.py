from typing import Any

import numpy as np
from pydantic import BaseModel, Field, PrivateAttr

from building.schemas.building import Building
from building.schemas.passenger_flow import PassengerFlow


class PassengerRegime(BaseModel):
    name: str = Field(description="regime name")
    building: Building = Field(description="building")
    time_start: int = Field(description="start time (seconds)")
    time_end: int = Field(description="end time (seconds)")
    rate: float = Field(description="passenger rate", default=1.0)
    flows: list[PassengerFlow] = Field(
        description="passenger flows",
        default_factory=list,
    )

    _transition_matrix: np.ndarray[float] = PrivateAttr(
        default=np.array([])
    )  # source-destination transition matrix

    def model_post_init(self, __context: Any) -> None:
        flows, floors = self.flows, self.building.floors
        n = len(floors)
        if not flows:
            matrix = np.ones((n, n))
            np.fill_diagonal(matrix, 0.0)
        else:
            populations = np.array([f.population for f in floors])
            floor_types = np.array([f.floor_type for f in floors])
            flow_weights = np.array([f.weight for f in flows])

            flow_matrices = []
            for flow in flows:
                source_mask = np.isin(floor_types, flow.source_floor_types)
                destination_mask = np.isin(floor_types, flow.destination_floor_types)
                sources = np.where(source_mask, populations, 0.0)
                destinations = np.where(destination_mask, populations, 0.0)
                flow_matrix = sources[:, None] * destinations[None, :]
                np.fill_diagonal(flow_matrix, 0.0)
                flow_matrices.append(flow_matrix)

            flow_matrices = np.stack(flow_matrices)
            matrix = np.tensordot(flow_matrices, flow_weights, axes=(0, 0))

        total = np.sum(matrix, axis=1, keepdims=True)
        matrix = np.divide(matrix, total, out=np.zeros_like(matrix), where=total > 0)
        self._transition_matrix = matrix

    @property
    def transition_matrix(self) -> np.ndarray[float]:
        return self._transition_matrix
