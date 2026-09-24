export interface BackendConfig {
  controlApiUrl: string;
  inferenceUrl: string;
}

const FALLBACK: BackendConfig = {
  controlApiUrl: "/api/control",
  inferenceUrl: "/api/inference",
};

export async function loadConfig(): Promise<BackendConfig> {
  try {
    const res = await fetch("/config.json");
    if (!res.ok) return FALLBACK;
    const body = await res.json();
    if (typeof body.controlApiUrl !== "string" || typeof body.inferenceUrl !== "string") return FALLBACK;
    return body as BackendConfig;
  } catch {
    return FALLBACK;
  }
}
