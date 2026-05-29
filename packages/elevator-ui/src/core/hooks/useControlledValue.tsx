import { useState } from "react";

import type { FormControlPropsModel } from "../models";

export type UseControlledValuePropsModel<T> = Pick<
  FormControlPropsModel<T>,
  "defaultValue" | "onChange" | "value"
>;

export const useControlledValue = <T,>({
  defaultValue,
  onChange,
  value,
}: UseControlledValuePropsModel<T>): [T, (value: T) => void] => {
  const [valueControlled, valueControlledSet] = useState<T>(defaultValue);
  return [value ?? valueControlled, onChange ?? valueControlledSet];
};
