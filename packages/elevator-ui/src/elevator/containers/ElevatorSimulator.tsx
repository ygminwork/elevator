import Button from "@mui/material/Button";
import _ from "lodash";
import { useMemo, useState } from "react";

import type { DispatcherOutputModel } from "../models";

import { Wrapper } from "../../core/components/Wrapper";
import { useFetch } from "../../core/hooks/useFetch";
import { useTick } from "../../core/hooks/useTick";
import { GraphicsContainer } from "../../graphics/containers/GraphicsContainer";
import { Elevator } from "../components/Elevator";
import { Floor } from "../components/Floor";
import { Passenger } from "../components/Passenger";
import { useSimulatorPositions } from "../hooks/useSimulatorPositions";
import { useSimulatorTheme } from "../hooks/useSimulatorTheme";

export const ElevatorSimulator = ({}: SimulatorPropsModel) => {
  const { theme } = useSimulatorTheme();
  const [output, outputSet] = useState<DispatcherOutputModel>();
  const [currentTime, currentTimeSet] = useState<number>(0);

  const positions = useSimulatorPositions({ output });

  const { start, stop } = useTick({
    maxCount: output?.timestamps?.length
      ? output.timestamps.length - 1
      : undefined,
    onTick: currentTimeSet,
  });

  const [elevators, passengers] = useMemo(() => {
    if (!output) return [[], []];
    const { requests, timestamps } = output;
    return [
      timestamps[0].elevators ?? [],
      [...new Set(requests.map((r) => r.passenger_id))],
    ];
  }, [output]);

  const containerPosition = useMemo(() => {
    if (!output) return { x: 0, y: 0, z: 0 };
    const height = output.floors * theme.floor.height;
    const width = theme.elevator.size * elevators.length;
    return { x: width * 1.5, y: height, z: height * 1.5 };
  }, [theme, output, elevators]);

  const { fetch } = useFetch();

  const handleClick = async () => {
    stop();
    const output = await fetch<DispatcherOutputModel>(
      "http://localhost:8000/api/elevator/dispatch",
      { method: "post" },
    );

    if (output.timestamps) {
      output.timestamps = output.timestamps.map((t) => ({
        ...t,
        elevators: t.elevators.map((e) => ({
          ...e,
          dropoffs: _.reduce(
            e.dropoff_ids,
            (r, v, k) => ({
              ...r,
              [k]: v
                .map((id) => output.requests.find((r) => r.id === id))
                .filter(Boolean),
            }),
            {},
          ),
          pickups: _.reduce(
            e.pickup_ids,
            (r, v, k) => ({
              ...r,
              [k]: v
                .map((id) => output.requests.find((r) => r.id === id))
                .filter(Boolean),
            }),
            {},
          ),
        })),
      }));
    }

    outputSet(output);
    start();
  };

  return (
    <Wrapper>
      <Button color="primary" variant="contained" onClick={handleClick}>
        Custom Color Button
      </Button>
      <>{currentTime}</>
      <Wrapper width={500} height={500} border mTop>
        {output ? (
          <GraphicsContainer position={containerPosition}>
            {Array.from({ length: output.floors }).map((_, i) => (
              <Floor key={i} level={i + 1} elevators={elevators} />
            ))}

            {elevators.map((e) => {
              const position = positions[currentTime].elevators[e.id];
              return (
                position && (
                  <Elevator
                    key={e.id}
                    id={e.id}
                    capacity={e.capacity}
                    position={position}
                  />
                )
              );
            })}

            {passengers.map((p) => {
              const position = positions[currentTime].passengers[p];
              const x = position?.x ?? 0;
              const z = position?.z ?? 0;
              return (
                position && (
                  <Passenger
                    key={p}
                    id={p}
                    position={position}
                    status={x < 0 ? "walking" : z > 0 ? "static" : "idle"}
                  />
                )
              );
            })}
          </GraphicsContainer>
        ) : (
          <>N/A</>
        )}
      </Wrapper>
    </Wrapper>
  );
};

export type SimulatorPropsModel = {};
