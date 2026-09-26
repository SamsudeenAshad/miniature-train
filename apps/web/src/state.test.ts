import assert from "node:assert/strict";
import { canExecute, requireCtx } from "./state.ts";

assert.deepEqual(requireCtx({ project: "p", environment: "e" }), { project: "p", environment: "e" });
assert.throws(() => requireCtx({ project: "p" }), /context required/);
assert.equal(canExecute("abc", "abc"), true);
assert.equal(canExecute("abc", "def"), false);
assert.equal(canExecute(null, "abc"), false);
console.log("state unit ok");
