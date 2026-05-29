import { createContext, useContext } from "react";

import type { SimulatorThemeModel } from "../models";

export const SIMULATOR_THEME: SimulatorThemeModel = {
  elevator: {
    color: "#3A225D",
    opacity: 0.5,
    size: 5,
  },

  floor: {
    color: "#1e293b",
    height: 5,
    opacity: 0.2,
    padding: 20,
  },

  spacing: 2,
};

export const SimulatorThemeContext = createContext<{
  theme: SimulatorThemeModel;
  themeSet(theme: SimulatorThemeModel): void;
}>({
  theme: SIMULATOR_THEME,
  themeSet: () => {},
});

export const useSimulatorTheme = () => useContext(SimulatorThemeContext);
