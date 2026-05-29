import type { ShapePropsModel } from "../../graphics/models";

import { Rectangle } from "../../graphics/components/Rectangle";
import { useSimulatorTheme } from "../hooks/useSimulatorTheme";

export const Elevator = ({ capacity, position }: ElevatorPropsModel) => {
  const { theme } = useSimulatorTheme();
  return (
    <Rectangle
      color={theme.elevator.color}
      dimension={{
        depth: theme.floor.height,
        height: theme.elevator.size,
        width: theme.elevator.size,
      }}
      position={position}
      opacity={theme.elevator.opacity}
    />
  );
};

export type ElevatorPropsModel = {
  id: string;
  capacity: number;
  position?: ShapePropsModel["position"];
};
