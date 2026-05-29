import { useState } from "react";

import type { WrapperPropsModel } from "../../core/components/Wrapper";

import {
  SIMULATOR_THEME,
  SimulatorThemeContext,
} from "../hooks/useSimulatorTheme";

export const ElevatorSimulatorThemeProvider = ({
  children,
}: WrapperPropsModel) => {
  const [theme, themeSet] = useState(SIMULATOR_THEME);
  return (
    <SimulatorThemeContext.Provider value={{ theme: theme, themeSet }}>
      {children}
    </SimulatorThemeContext.Provider>
  );
};
