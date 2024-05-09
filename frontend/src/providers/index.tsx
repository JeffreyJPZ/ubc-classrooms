/*
 * Error handling and fallbacks for app
 */
import { Suspense } from "react"
import { ErrorBoundary } from "react-error-boundary"

type ErrorFallbackProps = {
    error: Error
    resetErrorBoundary: () => void
}

function ErrorFallback({ error, resetErrorBoundary }: ErrorFallbackProps) {
    return (
        <div>
            <h1>Something went wrong:</h1>
            <pre>{error.message}</pre>
            <button onClick={resetErrorBoundary}>Refresh</button>
        </div>
    );
}

type AppProviderProps = {
    children: React.ReactNode
}

export function AppProvider({ children }: AppProviderProps) {

    return (
        <Suspense fallback={<div>Loading...</div>}>
            <ErrorBoundary FallbackComponent={ErrorFallback}>
                {children}
            </ErrorBoundary>
        </Suspense>
    );
}