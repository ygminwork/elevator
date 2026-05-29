import type { WrapperPropsModel } from "./components/Wrapper";

export type FormControlPropsModel<T> = WrapperPropsModel & {
  defaultValue: T;
  onChange?(value: T): void;
  value?: T;
  label?: string;
};
