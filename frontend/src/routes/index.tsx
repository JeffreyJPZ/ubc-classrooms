/**
 * Manages routing
 */
import { createBrowserRouter } from "react-router-dom"

import { publicRoutes } from "./public"

export function AppRouter() {
    const router = createBrowserRouter(publicRoutes);
    return (
        <>{router}</>
    );
};
