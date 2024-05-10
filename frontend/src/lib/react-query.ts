import { QueryClient, QueryClientConfig } from "react-query";

const config: QueryClientConfig = {
    defaultOptions: {
        queries: {
            refetchOnWindowFocus: false,
            retry: true,
            useErrorBoundary: true,
        },
    },
};

export const queryClient = new QueryClient(config)