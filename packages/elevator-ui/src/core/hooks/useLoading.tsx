import { createContext, useContext } from "react";

export const LoadingContext = createContext<
  [isLoading: boolean, isLoadingSet: (value: boolean) => void]
>([false, () => {}]);

export const useLoading = () => useContext(LoadingContext);
