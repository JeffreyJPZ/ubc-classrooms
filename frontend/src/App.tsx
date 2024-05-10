import { AppProvider } from "./providers/app";
import { AppRouter } from "./routes/app";

export function App() {
  return (
    <AppProvider>
      <AppRouter/>
    </AppProvider>
  );
};
