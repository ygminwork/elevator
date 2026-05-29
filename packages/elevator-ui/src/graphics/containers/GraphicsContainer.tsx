import { Canvas } from "@react-three/fiber";

import type { ShapePropsModel } from "../models";

import { type WrapperPropsModel } from "../../core/components/Wrapper";

export const GraphicsContainer = ({
  children,
  position,
}: GraphicsContainerPropsModel) => {
  const positions: [number, number, number] = [
    position?.x ?? 10,
    position?.y ?? 10,
    position?.z ?? 10,
  ];
  return (
    <Canvas camera={{ position: positions, zoom: 1 }}>
      <ambientLight intensity={0.5} />
      <directionalLight position={positions} />
      <group position={[0, 0, 0]}>{children}</group>
    </Canvas>
  );
};

export type GraphicsContainerPropsModel = WrapperPropsModel &
  Pick<ShapePropsModel, "position">;
