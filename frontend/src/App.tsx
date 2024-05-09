import { AppProvider } from "./providers";
import { AppRouter } from "./routes";

export function App() {
  <AppProvider>
    <AppRouter/>
  </AppProvider>
};
