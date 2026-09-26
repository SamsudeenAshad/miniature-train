import assert from "node:assert/strict";
import { loadConfig } from "./config.ts";

const FALLBACK_URLS = ["/api/control", "/api/inference"];

// Network failure must fall back, never throw.
(globalThis as Record<string, unknown>).fetch = () => Promise.reject(new Error("down"));
const offline = await loadConfig();
assert.deepEqual([offline.controlApiUrl, offline.inferenceUrl], FALLBACK_URLS);

// Missing keys must fall back too.
(globalThis as Record<string, unknown>).fetch = () =>
  Promise.resolve({ ok: true, json: () => Promise.resolve({ controlApiUrl: 42 }) });
const partial = await loadConfig();
assert.deepEqual([partial.controlApiUrl, partial.inferenceUrl], FALLBACK_URLS);

// Healthy source is honored.
(globalThis as Record<string, unknown>).fetch = () =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve({ controlApiUrl: "/custom/control", inferenceUrl: "/custom/inference" }),
  });
const custom = await loadConfig();
assert.deepEqual([custom.controlApiUrl, custom.inferenceUrl], ["/custom/control", "/custom/inference"]);

console.log("config unit ok");
