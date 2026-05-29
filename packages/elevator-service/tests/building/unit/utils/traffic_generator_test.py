import pytest

from building.schemas.building import building_fixture
from building.schemas.floor import FloorType
from building.schemas.pasenger_regime import PassengerRegime
from building.schemas.passenger_flow import PassengerFlow
from building.utils.traffix_generator import TrafficGenerator
from core.utils.write_json import write_json
from dispatcher.configs.global_config import global_config
from passenger.schemas.persona import Persona


@pytest.mark.asyncio
async def test_traffic_generator():
    personas = [
        Persona(
            name="executive",
            weight=0.5,
            rate_travel=0.25,
            floor_levels=[8, 9, 10],
        ),
        Persona(
            name="employee",
            weight=10.0,
            rate_travel=1.0,
        ),
        Persona(
            name="visitor",
            rate_travel=0.5,
            floor_levels=[1, 2, 3],
        ),
        Persona(
            name="courier",
            rate_travel=5.0,
        ),
    ]

    regimes = [
        PassengerRegime(
            name="morning rush",
            building=building_fixture,
            time_start=8 * 60 * 60,  # 8:00 AM
            time_end=9 * 60 * 60,  # 9:00 AM
            rate=0.8,
            flows=[
                PassengerFlow(
                    weight=5.0,
                    source_floor_types=[FloorType.LOBBY],
                    destination_floor_types=[FloorType.OFFICE],
                ),
                PassengerFlow(
                    weight=1.0,
                    source_floor_types=[FloorType.OFFICE],
                    destination_floor_types=[FloorType.OFFICE],
                ),
            ],
        ),
        PassengerRegime(
            name="mid morning rush",
            building=building_fixture,
            time_start=9 * 60 * 60,  # 9:00 AM
            time_end=12 * 60 * 60,  # 12:00 PM
            rate=0.1,
            flows=[
                PassengerFlow(
                    weight=2.0,
                    source_floor_types=[FloorType.LOBBY],
                    destination_floor_types=[FloorType.OFFICE],
                ),
                PassengerFlow(
                    weight=1.0,
                    source_floor_types=[FloorType.OFFICE],
                    destination_floor_types=[FloorType.OFFICE],
                ),
            ],
        ),
        PassengerRegime(
            name="lunch rush",
            building=building_fixture,
            time_start=12 * 60 * 60,  # 12:00 PM
            time_end=14.5 * 60 * 60,  # 1:30 PM
            rate=0.5,
            flows=[
                PassengerFlow(
                    weight=4.0,
                    source_floor_types=[FloorType.OFFICE],
                    destination_floor_types=[FloorType.CAFETERIA],
                ),
                PassengerFlow(
                    weight=2.0,
                    source_floor_types=[FloorType.OFFICE],
                    destination_floor_types=[FloorType.LOBBY],
                ),
                PassengerFlow(
                    weight=1.0,
                    source_floor_types=[FloorType.CAFETERIA],
                    destination_floor_types=[FloorType.OFFICE],
                ),
            ],
        ),
        PassengerRegime(
            name="post lunch",
            building=building_fixture,
            time_start=14.5 * 60 * 60,  # 1:30 PM
            time_end=15 * 60 * 60,  # 3:00 PM
            rate=0.4,
            flows=[
                PassengerFlow(
                    weight=2.0,
                    source_floor_types=[FloorType.CAFETERIA],
                    destination_floor_types=[FloorType.OFFICE],
                ),
                PassengerFlow(
                    weight=1.0,
                    source_floor_types=[FloorType.LOBBY],
                    destination_floor_types=[FloorType.OFFICE],
                ),
            ],
        ),
        PassengerRegime(
            name="afternoon",
            building=building_fixture,
            time_start=15 * 60 * 60,  # 3:00 PM
            time_end=17 * 60 * 60,  # 5:00 PM
            rate=0.1,
            flows=[
                PassengerFlow(
                    weight=3.0,
                    source_floor_types=[FloorType.OFFICE],
                    destination_floor_types=[FloorType.OFFICE],
                ),
                PassengerFlow(
                    weight=1.0,
                    source_floor_types=[FloorType.LOBBY],
                    destination_floor_types=[FloorType.OFFICE],
                ),
            ],
        ),
        PassengerRegime(
            name="evening rush",
            building=building_fixture,
            time_start=17 * 60 * 60,  # 5:00 PM
            time_end=19 * 60 * 60,  # 7:00 PM
            rate=0.8,
            flows=[
                PassengerFlow(
                    weight=5.0,
                    source_floor_types=[FloorType.OFFICE],
                    destination_floor_types=[FloorType.LOBBY],
                ),
                PassengerFlow(
                    weight=0.5,
                    source_floor_types=[FloorType.LOBBY],
                    destination_floor_types=[FloorType.OFFICE],
                ),
            ],
        ),
        PassengerRegime(
            name="late evening",
            building=building_fixture,
            time_start=19 * 60 * 60,  # 7:00 PM
            time_end=24 * 60 * 60,  # 12:00 AM
            rate=0.1,
            flows=[
                PassengerFlow(
                    source_floor_types=[FloorType.OFFICE],
                    destination_floor_types=[FloorType.LOBBY],
                ),
            ],
        ),
    ]

    generator = TrafficGenerator(
        building=building_fixture,
        regimes=regimes,
        personas=personas,
        random_seed=42,
        time_start=6 * 60 * 60,  # 6:00 AM
        time_end=24 * 60 * 60,  # 12:00 AM
    )

    n_population = global_config.n_population
    requests = generator.generate(n_population=n_population)
    assert len(requests) >= n_population

    write_json(
        pathname="data/requests.json",
        value=[r.model_dump(mode="json") for r in requests],
    )
