/**
 * Manages routing
 */
import { RouterProvider, createBrowserRouter } from "react-router-dom";

import { publicRoutes } from "./public";

const router = createBrowserRouter(publicRoutes);

export function AppRouter() {
    return (
        <RouterProvider router={router} />
    );
};
