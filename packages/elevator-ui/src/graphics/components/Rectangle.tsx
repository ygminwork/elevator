import { Edges } from "@react-three/drei";
import { useFrame } from "@react-three/fiber";
import { useRef, useState } from "react";
import * as THREE from "three";

import type { ShapePropsModel } from "../models";

export const Rectangle = ({
  color,
  dimension,
  opacity = 1.0,
  position,
}: RectanglePropsModel) => {
  const ref = useRef<THREE.Mesh>(null);

  const getContainerPosition = ({
    dimension,
    position,
  }: ShapePropsModel): [number, number, number] => {
    return [
      (position?.x ?? 0) + (dimension?.width ?? 10) / 2,
      (position?.y ?? 0) + (dimension?.height ?? 10) / 2,
      -((position?.z ?? 0) + (dimension?.depth ?? 10) / 2),
    ];
  };
  const [target] = useState(() => new THREE.Vector3());
  const [initialPosition] = useState(() =>
    getContainerPosition({ dimension, position }),
  );

  useFrame((state, delta) => {
    if (!ref.current) return;
    target.set(...getContainerPosition({ dimension, position }));
    ref.current.position.lerp(target, 10 * delta);
  });

  return (
    <mesh ref={ref} position={initialPosition}>
      <boxGeometry
        args={[
          dimension?.width ?? 10,
          dimension?.height ?? 10,
          dimension?.depth ?? 10,
        ]}
      />
      <meshStandardMaterial
        color={color}
        transparent
        opacity={opacity}
        depthWrite={false}
      />
      <Edges color="black" lineWidth={0.5} />
    </mesh>
  );
};

export type RectanglePropsModel = ShapePropsModel & {
  opacity?: number;
  color?: string;
};
