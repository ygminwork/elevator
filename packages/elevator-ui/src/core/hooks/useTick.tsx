import { useEffect, useCallback, useState, useRef } from "react";

export const useTick = (
  {
    defaultCount = 0,
    defaultSpeed = 1000,
    maxCount,
    onTick,
  }: UseTickParamsModel = {
    defaultCount: 0,
    defaultSpeed: 1000,
  },
) => {
  const [count, countSet] = useState<number>(defaultCount);
  const [speed, speedSet] = useState<number>(defaultSpeed);
  const [elapsed, elapsedSet] = useState<number>(0);
  const [isRunning, isRunningSet] = useState<boolean>(false);

  const onTickRef = useRef(onTick);
  const countRef = useRef(count);
  const elapsedRef = useRef(elapsed);

  useEffect(() => {
    onTickRef.current = onTick;
  }, [onTick]);

  useEffect(() => {
    if (!isRunning) return;

    const intervalId = setInterval(() => {
      const nextCount = countRef.current + 1;
      const nextElapsed = elapsedRef.current + speed;
      countRef.current = nextCount;
      elapsedRef.current = nextElapsed;
      onTickRef.current?.(nextCount);

      if (maxCount !== undefined && nextCount >= maxCount) {
        isRunningSet(false);
        clearInterval(intervalId);
        countSet(maxCount);
      } else {
        countSet(nextCount);
      }
      elapsedSet(nextElapsed);
    }, speed);

    return () => clearInterval(intervalId);
  }, [isRunning, speed, maxCount]);

  const start = useCallback(() => {
    if (maxCount !== undefined && countRef.current >= maxCount) return;
    isRunningSet(true);
  }, [maxCount]);

  const stop = useCallback(() => isRunningSet(false), []);

  const reset = useCallback(() => {
    countSet(0);
    elapsedSet(0);
    countRef.current = 0;
    elapsedRef.current = 0;
    isRunningSet(false);
  }, []);

  const setCount = useCallback((value: number | ((prev: number) => number)) => {
    countSet((prev) => {
      const next = typeof value === "function" ? value(prev) : value;
      countRef.current = next;
      return next;
    });
  }, []);

  return {
    count,
    elapsed,
    isRunning,
    reset,
    setCount,
    setSpeed: speedSet,
    speed,
    start,
    stop,
  };
};

export type UseTickParamsModel = {
  onTick?(count: number): void;
  defaultCount?: number;
  defaultSpeed?: number;
  maxCount?: number;
};
