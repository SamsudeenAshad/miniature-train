export const SCREENS = ["overview", "data", "training", "runs", "model", "monitoring", "incident", "action", "audit", "settings"] as const;
export type Screen = (typeof SCREENS)[number];

export interface Ctx {
  project: string;
  environment: string;
}

export function requireCtx(ctx: Partial<Ctx>): Ctx {
  if (!ctx.project || !ctx.environment) throw new Error("project/environment context required");
  return ctx as Ctx;
}

/** Approval and execution controls are separate; execution needs an approved plan hash. */
export function canExecute(approvedPlanHash: string | null, executionPlanHash: string): boolean {
  return !!approvedPlanHash && approvedPlanHash === executionPlanHash;
}
