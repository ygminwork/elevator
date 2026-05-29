import type { ShapePropsModel } from "../../graphics/models";

import { Fbx } from "../../graphics/components/Fbx";

export const Passenger = ({
  id,
  position,
  status = "static",
}: PassengerPropsModel) => {
  return (
    <Fbx
      animationState={
        status === "walking"
          ? "Armature|Walk"
          : status === "idle"
            ? "Armature|Idle"
            : "Static Pose"
      }
      pathname="src/assets/passenger.fbx"
      position={position}
    />
  );
};

export type PassengerPropsModel = {
  status?: "static" | "walking" | "idle";
  id: string;
  position: ShapePropsModel["position"];
};
