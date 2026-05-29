import type { ShapePropsModel } from "../models";

export const Plane = ({
  color,
  dimension,
  isHorizontal = true,
  opacity = 1.0,
  position,
}: PlanePropsModel) => {
  const getContainerPosition = ({
    dimension,
    position,
  }: ShapePropsModel): [number, number, number] => {
    return [
      (position?.x ?? 0) + (dimension?.width ?? 10) / 2,
      position?.z ?? 0,
      -((position?.y ?? 0) + (dimension?.height ?? 10) / 2),
    ];
  };
  return (
    <mesh
      position={getContainerPosition({ dimension, position })}
      rotation={isHorizontal ? [-Math.PI / 2, 0, 0] : undefined}
    >
      <planeGeometry args={[dimension?.width ?? 10, dimension?.height ?? 10]} />
      <meshStandardMaterial
        color={color}
        transparent
        opacity={opacity}
        depthWrite={false}
      />
    </mesh>
  );
};

export type PlanePropsModel = ShapePropsModel & {
  color: string;
  opacity?: number;
  isHorizontal?: boolean;
};
