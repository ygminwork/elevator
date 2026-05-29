import { useMemo } from "react";

import type { ElevatorPropsModel } from "./Elevator";

import { Plane } from "../../graphics/components/Plane";
import { useSimulatorTheme } from "../hooks/useSimulatorTheme";

export const Floor = ({ elevators, level = 1 }: FloorPropsModel) => {
  const { theme } = useSimulatorTheme();
  const { height, width, z } = useMemo(() => {
    return {
      height: theme.elevator.size,
      width:
        theme.elevator.size * elevators.length +
        (elevators.length + 1) * theme.spacing +
        theme.floor.padding * 2,
      z: (level - 1) * theme.floor.height,
    };
  }, [theme, elevators, level]);
  return (
    <Plane
      opacity={theme.floor.opacity}
      color={theme.floor.color}
      dimension={{ height, width }}
      position={{ x: -theme.floor.padding, y: 0, z }}
    />
  );
};

export type FloorPropsModel = {
  elevators: Array<ElevatorPropsModel>;
  level?: number;
};
