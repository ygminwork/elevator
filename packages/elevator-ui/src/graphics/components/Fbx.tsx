import { useFBX, useAnimations } from "@react-three/drei";
import { useFrame } from "@react-three/fiber";
import { useEffect, useRef, useState, useMemo } from "react";
import * as THREE from "three";
import { SkeletonUtils } from "three-stdlib";

import type { ShapePropsModel } from "../models";

const FADE_DURATION = 0.5;

export const Fbx = ({
  animationState,
  color,
  pathname,
  position,
  scale = 0.01,
}: FbxPropsModel) => {
  const fbx = useFBX(pathname);
  const { cloned, materials } = useMemo(() => {
    const cloned = SkeletonUtils.clone(fbx);
    const materials: Array<THREE.MeshStandardMaterial> = [];
    cloned.traverse((child) => {
      if (child instanceof THREE.Mesh) {
        if (Array.isArray(child.material)) {
          child.material = child.material.map((mat) => {
            const matClone = mat.clone();
            if ("color" in matClone) materials.push(matClone);
            return matClone;
          });
        } else {
          child.material = child.material.clone();
          if ("color" in child.material) materials.push(child.material);
        }
      }
    });
    return { cloned, materials };
  }, [fbx]);

  const ref = useRef<THREE.Group>(null);
  const { actions, names } = useAnimations(fbx.animations, ref);
  const [target] = useState(() => new THREE.Vector3());

  useEffect(() => {
    if (!color) return;
    materials.forEach((v) => v.color.set(color));
  }, [materials, color]);

  useEffect(() => {
    const action = animationState ?? names[0];
    if (!actions?.[action]) return;
    actions[action].reset().fadeIn(FADE_DURATION).play();
    return () => {
      actions[action]?.fadeOut(FADE_DURATION);
    };
  }, [actions, animationState, names]);

  useFrame((state, delta) => {
    if (!ref.current) return;
    target.set(position?.x ?? 0, position?.y ?? 0, position?.z ?? 0);
    ref.current.position.lerp(target, 10 * delta);
  });

  return <primitive object={cloned} ref={ref} scale={scale} />;
};

export type FbxPropsModel = ShapePropsModel & {
  color?: string;
  pathname: string;
  animationState?: string;
  scale?: number;
};
