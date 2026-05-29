import Backdrop from "@mui/material/Backdrop";
import CircularProgress from "@mui/material/CircularProgress";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useIsFetching, useIsMutating } from "@tanstack/react-query";

import type { WrapperPropsModel } from "../../core/components/Wrapper";

const queryClient = new QueryClient();

const LoadingBackdrop = () => {
  const isFetching = useIsFetching();
  const isMutating = useIsMutating();
  return (
    <Backdrop
      sx={(theme) => ({ color: "#fff", zIndex: theme.zIndex.drawer + 1 })}
      open={!!isFetching || !!isMutating}
    >
      <CircularProgress color="inherit" />
    </Backdrop>
  );
};

export const QueryProvider = ({ children }: QueryProviderPropsModel) => {
  return (
    <QueryClientProvider client={queryClient}>
      <LoadingBackdrop />
      {children}
    </QueryClientProvider>
  );
};

export type QueryProviderPropsModel = WrapperPropsModel;
