import { useState } from "react";
import { SCREENS, requireCtx, type Screen } from "./state";

export default function App() {
  const [screen, setScreen] = useState<Screen>("overview");
  const ctx = requireCtx({ project: "demo", environment: "staging" });
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
    </main>
  );
}
