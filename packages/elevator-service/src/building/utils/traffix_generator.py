from typing import Optional

import numpy as np
from pydantic import BaseModel, Field

from building.schemas.building import Building
from building.schemas.floor import FloorType
from building.schemas.pasenger_regime import PassengerRegime
from core.utils.uid import uid
from dispatcher.configs.global_config import global_config
from passenger.schemas.passenger_request import PassengerRequest
from passenger.schemas.persona import Persona


class TrafficGenerator(BaseModel):
    building: Building = Field(description="building")
    regimes: list[PassengerRegime] = Field(
        description="passenger regimes",
        default_factory=list,
    )
    personas: list[Persona] = Field(
        description="personas",
        default_factory=list,
    )
    time_start: int = Field(description="start time (seconds)", default=0)
    time_end: int = Field(description="end time (seconds)", default=0)
    random_seed: int = Field(description="random seed", default=42)

    def generate(
        self,
        n_population: int,
    ) -> list[PassengerRequest]:
        floors = self.building.floors
        n_floors = len(floors)
        if n_population <= 0 or not n_floors or not self.regimes:
            return []

        tick_seconds = global_config.tick_seconds
        rng = np.random.default_rng(self.random_seed)
        floor_levels = [f.level for f in floors]

        floor_population = np.zeros(n_floors, dtype=int)
        outside_population = n_population

        if self.personas:
            persona_names = [p.name for p in self.personas]
            persona_weights = np.array(
                [p.weight * p.rate_travel for p in self.personas], dtype=float
            )
            persona_probabilities = persona_weights / persona_weights.sum()
            persona_floor_masks: dict[str, Optional[np.ndarray]] = {
                p.name: (
                    np.array(
                        [1.0 if f.level in set(p.floor_levels) else 0.0 for f in floors]
                    )
                    if p.floor_levels
                    else None
                )
                for p in self.personas
            }
        else:
            persona_names = ["default"]
            persona_probabilities = np.array([1.0])
            persona_floor_masks = {"default": None}

        def get_regime(tick: int) -> Optional[PassengerRegime]:
            for r in self.regimes:
                if r.time_start <= tick < r.time_end:
                    return r
            return None

        def sample_dropoff(transition_matrix: np.ndarray, pickup_idx: int) -> int:
            row = transition_matrix[pickup_idx].copy()
            row_sum = row.sum()
            if row_sum > 0:
                row /= row_sum
            else:
                row = np.ones(n_floors)
                row[pickup_idx] = 0.0
                row /= row.sum()
            return int(rng.choice(n_floors, p=row))

        def sample_persona() -> str:
            return str(rng.choice(persona_names, p=persona_probabilities))

        requests: list[PassengerRequest] = []

        for tick in range(self.time_start, self.time_end, tick_seconds):
            regime = get_regime(tick)
            if regime is None:
                continue
            transition_matrix = regime.transition_matrix
            floor_types = np.array([f.floor_type for f in floors])
            if regime.flows:
                source_types = [
                    ft for flow in regime.flows for ft in flow.source_floor_types
                ]
                source_mask = np.isin(floor_types, source_types).astype(float)
            else:
                source_mask = np.ones(n_floors, dtype=float)

            lobby_mask = np.array(
                [1.0 if f.floor_type == FloorType.LOBBY else 0.0 for f in floors]
            )

            expected_trips = (
                regime.rate
                * (tick_seconds / 3600)
                * (outside_population + floor_population.sum())
            )

            n_trips = int(rng.poisson(expected_trips))
            if n_trips == 0:
                continue

            for _ in range(n_trips):
                on_floor_emission = floor_population.astype(float) * source_mask
                outside_emission = outside_population * lobby_mask * source_mask
                combined_emission = on_floor_emission + outside_emission
                total = combined_emission.sum()
                if total <= 0:
                    continue

                emission = combined_emission / total
                persona_name = sample_persona()
                mask = persona_floor_masks[persona_name]
                if mask is not None:
                    masked = emission * mask
                    masked_total = masked.sum()
                    emission = masked / masked_total if masked_total > 0 else emission

                pickup_idx = int(rng.choice(n_floors, p=emission))
                dropoff_idx = sample_dropoff(transition_matrix, pickup_idx)

                if pickup_idx == dropoff_idx:
                    continue

                pickup_level = floor_levels[pickup_idx]
                dropoff_level = floor_levels[dropoff_idx]

                if floor_population[pickup_idx] > 0:
                    floor_population[pickup_idx] -= 1
                else:
                    outside_population = max(0, outside_population - 1)
                floor_population[dropoff_idx] += 1
                requests.append(
                    PassengerRequest(
                        passenger_id=uid(persona_name),
                        pickup=pickup_level,
                        dropoff=dropoff_level,
                        time_request=tick // tick_seconds,
                    )
                )

        requests.sort(key=lambda r: r.time_request)
        return requests
