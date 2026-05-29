import _ from "lodash";

export const cleanObject = (
  value: Record<string, unknown>,
): Record<string, unknown> => _.omitBy(value, _.isNil);
