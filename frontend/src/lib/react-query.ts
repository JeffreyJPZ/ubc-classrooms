import { QueryClient, QueryClientConfig } from "react-query";

export const queryConfig: QueryClientConfig = {
    defaultOptions: {
        queries: {
            refetchOnWindowFocus: false,
            retry: true,
            useErrorBoundary: true,
        },
    },
};

export const queryClient = new QueryClient(queryConfig);