# Follow-up: Propagate hosted mode to implement-task and verify-pr

## Context

`performance-baseline` records `metadata.capture_target` ("localhost"|"hosted") and `metadata.capture_base_url` after capture. Neither `implement-task` Step 9-Perf.1 nor `verify-pr` Step 4.6 reads these fields — both hardcode `dev_environment.port`. Re-captures against a hosted environment will fail or produce incomparable metrics.

Auth credentials are never stored in config. For hosted re-captures, prompt the user at capture time.

`capture_target` and `capture_mode` (cold-start) are orthogonal — target is where, mode is how.

No script changes needed — this is skill-definition only. No changes to Step 9-Perf.0 (freshness check).

## implement-task — Step 9-Perf.1

### Current

Copy `capture-baseline.template.mjs` to baseline directory. Read `dev_environment.port`. Run with port and mode.

### Change

Read `metadata.capture_target` before `dev_environment.port` — hosted path does not use port for Playwright.

- **null/missing/`localhost`:** use `--port` from `dev_environment.port` (backward compatible with pre-hosted configs)
- **`hosted`:** read `metadata.capture_base_url`. If null/empty → halt: "Re-run `/sdlc-workflow:performance-baseline` or set URL via `perf-config.py set metadata.capture_base_url <url>`." If present → **blocking prompt**: show configured target (hosted at `{url}`) vs available environment; user chooses:
  - **Continue** — use hosted target, prompt for auth and `--insecure`
  - **Switch to localhost** — use `--port` from `dev_environment.port` for this capture only. Do NOT overwrite `metadata.capture_target` in config without explicit user consent. Warn: "Comparison is against a hosted baseline — metrics may not be comparable."
  - **Cancel**

For command construction, mirror performance-baseline Step 9.1 — absolute `--config` path, `--storage-state`/`--user`/`--pass` mutual exclusivity, omit auth flags for public hosted apps, `BASELINE_PASS` env var.

For `metric_type=hybrid`: Playwright leg follows `capture_target` logic above. Backend leg always uses `perf-benchmark.sh` + `dev_environment.port` (unchanged).

Add to Step 9-Perf.1 error handling: verification failed → display script diagnostics, halt. Do not retry.

### implement-task — Step 9-Perf.5

Add `capture_target` and `capture_base_url` (URL only, never credentials) to the optimization result report populate list, alongside `capture_mode`. Update the template section reference.

### Scope

Frontend Playwright capture only — backend `perf-benchmark.sh` unchanged.

## verify-pr — Step 4.5

### Current

Extract from optimization result report: `jira_key`, `timestamp`, `branch`, `commit_sha`, `baseline_commit_sha`, `capture_mode`, `status`, ...

### Change

Add `capture_target` and `capture_base_url` to the extraction list.

## verify-pr — Step 4.6

### Current

Read `metadata.baseline_mode`, `dev_environment.port`, `baseline_settings.iterations`. Frontend/hybrid: "Run Playwright capture (same as baseline Step 9.1)."

### Change

**Environment mismatch check — run before the optional re-run prompt.** Compare three values:
- `metadata.capture_target` from config (what baseline used)
- `capture_target` from optimization result report (what implementation used)
- Current re-run target (what verify-pr would use)

If any differ → record `Environment Match: MISMATCH` in the drift report. Skip numeric drift threshold comparisons for mismatched environments — metrics are not comparable. This check runs even if the user skips re-run, so "baseline was hosted, implementation used localhost" is always flagged.

Add `Environment Match` row to the verification report table (alongside `Baseline Re-run`).

**Script copy:** Always copy `capture-baseline.template.mjs` from plugin cache before re-run. Do not reuse an existing copy — it may predate hosted mode.

**Frontend capture command:**
- **`capture_target` null/missing/`localhost`:** use `--port` from `dev_environment.port`
- **`hosted`:** read `capture_base_url` (halt if null/empty — same remediation as implement-task). Prompt for auth and `--insecure`. Construct command mirroring baseline Step 9.1.

For `metric_type=hybrid`: Playwright leg follows `capture_target` logic. Backend leg always uses `perf-benchmark.sh` + `dev_environment.port` (unchanged).

Add to error handling: verification failed → display script diagnostics, halt. Do not retry.

### Scope

Frontend Playwright capture only — backend `perf-benchmark.sh` unchanged.

## optimization-result.template.md

Add `capture_target` and `capture_base_url` (URL only, never credentials) to the report template alongside `capture_mode`. Both Step 9-Perf.5 (write) and Step 4.5 (read) reference this template.

## Verification iteration

Built into `capture-baseline.mjs` — halts before measurement on failure. Both skills handle the exit code and display stderr. No duplicate verification logic needed.

## perf-config.py reads

Document in both skills: `get metadata.capture_target`, `get metadata.capture_base_url`.

## Skipped

- **Version bump:** Not included — bump plugin version at release time, not per-follow-up.

## Files to modify

1. `plugins/sdlc-workflow/skills/implement-task/SKILL.md` — Step 9-Perf.1, Step 9-Perf.5
2. `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` — Step 4.5, Step 4.6
3. `plugins/sdlc-workflow/skills/performance/optimization-result.template.md` — add `capture_target`, `capture_base_url` fields
