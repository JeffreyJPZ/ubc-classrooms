import { AppProvider } from "./providers";
import { AppRouter } from "./routes";

export function App() {
  return (
    <AppProvider>
      <AppRouter/>
    </AppProvider>
  );
};
