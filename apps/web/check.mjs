import { readFileSync } from "node:fs";

// UI checks without a browser: contract screens/states + approval/execution separation.
const contract = JSON.parse(readFileSync(new URL("./state-contract.json", import.meta.url), "utf-8"));
const state = readFileSync(new URL("./src/state.ts", import.meta.url), "utf-8");
const app = readFileSync(new URL("./src/App.tsx", import.meta.url), "utf-8");

for (const s of ["overview", "incident", "action", "audit"]) {
  if (!contract.screens.includes(s)) throw new Error(`contract missing screen ${s}`);
  if (!state.includes(`"${s}"`)) throw new Error(`state missing screen ${s}`);
}
const stateScreens = [...state.matchAll(/"(overview|data|training|runs|model|monitoring|incident|action|audit|settings)"/g)].map((m) => m[1]);
for (const s of contract.screens) {
  if (!stateScreens.includes(s)) throw new Error(`state SCREENS missing contract screen ${s}`);
}
if (!app.includes("SCREENS")) throw new Error("App must render SCREENS");
if (!app.includes("loadConfig")) throw new Error("App must use the backend config loader");
for (const st of ["loading", "empty", "denied", "disconnected", "partial", "stale"]) {
  if (!contract.states.includes(st)) throw new Error(`contract missing state ${st}`);
}
if (!contract.rules.approval_separate_from_execution) throw new Error("approval/execution must be separate");
const config = readFileSync(new URL("./src/config.ts", import.meta.url), "utf-8");
if (!config.includes("FALLBACK")) throw new Error("config must define safe fallback");
const publicConfig = JSON.parse(readFileSync(new URL("./public/config.json", import.meta.url), "utf-8"));
for (const k of ["controlApiUrl", "inferenceUrl"]) {
  if (typeof publicConfig[k] !== "string") throw new Error(`public config missing ${k}`);
}
for (const f of ["./nginx.conf", "./nginx.compose.conf"]) {
  const conf = readFileSync(new URL(f, import.meta.url), "utf-8");
  for (const route of ["/api/control/", "/api/inference/"]) {
    if (!conf.includes(route)) throw new Error(`${f} missing route ${route}`);
  }
}
console.log("web checks ok");
