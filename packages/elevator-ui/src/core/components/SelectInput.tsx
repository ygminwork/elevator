import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import Select from "@mui/material/Select";

import type { FormControlPropsModel } from "../models";

import { useControlledValue } from "../hooks/useControlledValue";
import { Wrapper } from "./Wrapper";

export const SelectInput = <T,>({
  defaultValue,
  label,
  onChange,
  options,
  value,
  ...props
}: SelectPropsModel<T>) => {
  const [valueControlled, valueControlledSet] = useControlledValue<T>({
    defaultValue,
    onChange,
    value,
  });
  return (
    <Wrapper {...props}>
      <FormControl fullWidth>
        <InputLabel id={label}>{label}</InputLabel>
        <Select
          labelId={label}
          value={valueControlled}
          label={label}
          onChange={(e) => valueControlledSet(e.target.value as T)}
        >
          {options?.map((option) => (
            <MenuItem
              key={`${option}`}
              value={option as string}
            >{`${option}`}</MenuItem>
          ))}
        </Select>
      </FormControl>
    </Wrapper>
  );
};

export type SelectPropsModel<T> = FormControlPropsModel<T> & {
  options?: Array<T>;
};
