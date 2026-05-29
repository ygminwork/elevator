import { createTheme, ThemeProvider } from "@mui/material/styles";

import type { WrapperPropsModel } from "../../core/components/Wrapper";

import { LoadingProvider } from "../providers/LoadingProvider";

const theme = createTheme({
  palette: {
    primary: {
      main: "#3A225D",
    },
    secondary: {
      main: "#F7D54E",
    },
  },
});

export const AppContainer = ({ children }: AppContainerPropsModel) => {
  return (
    <ThemeProvider theme={theme}>
      <LoadingProvider>{children}</LoadingProvider>
    </ThemeProvider>
  );
};

export type AppContainerPropsModel = WrapperPropsModel;
