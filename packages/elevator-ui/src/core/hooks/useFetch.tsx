import { useLoading } from "./useLoading";

export const useFetch = () => {
  const [, isLoadingSet] = useLoading();

  return {
    fetch: async <T,>(...[uri, options = {}]: FetchParamsModel): Promise<T> => {
      const headers = new Headers(options?.headers ?? {});
      if (!headers.has("Content-Type")) {
        headers.set("Content-Type", "application/json");
      }
      headers.set("Accept", "application/json");

      isLoadingSet(true);
      try {
        const response = await fetch(uri, {
          body: options.body ? JSON.stringify(options.body) : undefined,
          headers,
          method: options.method ?? "get",
        });
        if (!response.ok) {
          const errorBody = await response.json().catch(() => ({}));
          throw new Error(errorBody.detail || response.statusText);
        }
        return (await response.json()) as T;
      } catch (error) {
        console.error(error);
        throw error;
      } finally {
        isLoadingSet(false);
      }
    },
  };
};

export type FetchParamsModel = [
  uri: string,
  options?: {
    method?: "get" | "post";
    body?: Record<string, unknown>;
    headers?: HeadersInit;
  },
];
