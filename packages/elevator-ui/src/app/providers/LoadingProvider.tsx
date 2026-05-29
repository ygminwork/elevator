import Backdrop from "@mui/material/Backdrop";
import CircularProgress from "@mui/material/CircularProgress";
import { useState } from "react";

import type { WrapperPropsModel } from "../../core/components/Wrapper";

import { LoadingContext } from "../../core/hooks/useLoading";

export const LoadingProvider = ({ children }: WrapperPropsModel) => {
  const [isLoading, isLoadingSet] = useState<boolean>(false);
  return (
    <LoadingContext.Provider value={[isLoading, isLoadingSet]}>
      {children}
      <Backdrop
        sx={(theme) => ({ color: "#fff", zIndex: theme.zIndex.drawer + 1 })}
        open={isLoading}
      >
        <CircularProgress color="inherit" />
      </Backdrop>
    </LoadingContext.Provider>
  );
};
