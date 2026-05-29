import { useMemo } from "react";

import type { ShapePropsModel } from "../../graphics/models";
import type { DispatcherOutputModel } from "../models";

import { useSimulatorTheme } from "./useSimulatorTheme";

export const useSimulatorPositions = ({
  output,
}: UseSimulatorPositionsParamsModel) => {
  const { theme } = useSimulatorTheme();

  return useMemo(() => {
    if (!output) return [];

    const { requests, timestamps } = output;
    const elevators = timestamps[0]?.elevators;

    const elevatorX: Record<string, number> = {};
    if (timestamps.length > 0) {
      elevators.forEach((e, index) => {
        elevatorX[e.id] =
          index * theme.elevator.size + (index + 1) * theme.spacing;
      });
    }

    return timestamps.map((t) => {
      const { time } = t;
      const position: SimulatorPositionsModel = {
        elevators: {},
        passengers: {},
      };

      t.elevators.forEach((e) => {
        position.elevators[e.id] = {
          x: elevatorX[e.id],
          y: (e.floor - 1) * theme.floor.height,
          z: 0,
        };
      });

      const passengersQueue = requests
        .filter(
          (r) =>
            r.time_request <= time && (!r.time_pickup || time < r.time_pickup),
        )
        .sort((a, b) => a.time_request - b.time_request);

      const droppedOffQueue = requests
        .filter((r) => r.time_dropoff && time >= r.time_dropoff)
        .sort((a, b) => (a.time_dropoff || 0) - (b.time_dropoff || 0));

      requests.forEach((r) => {
        // not yet requested
        if (time < r.time_request) {
          position.passengers[r.passenger_id] = null;
          return;
        }

        const { elevator_id } = r;
        const elevatorPosition = elevator_id
          ? position.elevators[elevator_id]
          : null;

        // dropped off
        if (r.time_dropoff && time >= r.time_dropoff) {
          const floorDroppedOff = droppedOffQueue.filter(
            (w) => w.dropoff === r.dropoff,
          );
          const dropoffIndex = floorDroppedOff.findIndex(
            (w) => w.passenger_id === r.passenger_id,
          );
          const dropoffX =
            theme.elevator.size * elevators.length +
            (elevators.length + 1) * theme.spacing;
          position.passengers[r.passenger_id] = {
            x: dropoffX + dropoffIndex * theme.spacing,
            y: (r.dropoff - 1) * theme.floor.height,
            z: 0,
          };
          return;
        }

        // in elevator
        if (
          r.time_pickup &&
          time >= r.time_pickup &&
          time < (r.time_dropoff ?? Infinity) &&
          elevatorPosition
        ) {
          position.passengers[r.passenger_id] = { ...elevatorPosition };
          return;
        }

        // in queue
        const floorQueue = passengersQueue.filter((w) => w.pickup === r.pickup);
        const queueIndex = floorQueue.findIndex(
          (w) => w.passenger_id === r.passenger_id,
        );
        if (queueIndex !== -1) {
          position.passengers[r.passenger_id] = {
            x: -theme.spacing - queueIndex * theme.spacing,
            y: (r.pickup - 1) * theme.floor.height,
            z: 0,
          };
        } else {
          position.passengers[r.passenger_id] = null;
        }
      });

      return position;
    });
  }, [output, theme]);
};

export type UseSimulatorPositionsParamsModel = {
  output?: DispatcherOutputModel;
};

export type SimulatorPositionsModel = {
  elevators: Record<string, ShapePropsModel["position"] | null>;
  passengers: Record<string, ShapePropsModel["position"] | null>;
};
