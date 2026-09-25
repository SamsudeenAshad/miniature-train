import { useEffect, useState } from "react";
import { loadConfig, type BackendConfig } from "./config";
import { SCREENS, requireCtx, type Screen } from "./state";

export default function App() {
  const [screen, setScreen] = useState<Screen>("overview");
  const [backend, setBackend] = useState<BackendConfig | null>(null);
  const ctx = requireCtx({ project: "demo", environment: "staging" });
  useEffect(() => {
    loadConfig().then(setBackend);
  }, []);
  return (
    <main>
      <header>
        {ctx.project} / {ctx.environment}
      </header>
      <nav>
        {SCREENS.map((s) => (
          <button key={s} onClick={() => setScreen(s)} aria-pressed={s === screen}>
            {s}
          </button>
        ))}
      </nav>
      <section aria-live="polite">screen: {screen}</section>
      <footer>{backend ? `api: ${backend.controlApiUrl}` : "api: loading…"}</footer>
    </main>
  );
}
