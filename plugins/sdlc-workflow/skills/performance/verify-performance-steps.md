# verify-pr: Performance & Migration Verification Steps

Referenced extension of the `verify-pr` skill. The orchestrator loads this file and
executes these steps **only** when `task_type` is `performance` or `db-migration`
(set in verify-pr Step 1 "Task Type Detection"). Standard tasks never read this file.

Resolve any `${CLAUDE_PLUGIN_ROOT}` token and `perf-config.py`/`perf-benchmark.sh`
paths exactly as described in verify-pr's "Resolving this skill's own files" section —
always from the delivered plugin, never a repo-relative path.

`db-migration` inherits all `performance` steps (4.5, 4.6, 4.7, 10) **plus** Step 4.8.

## CONVENTIONS.md precondition (Step 4b)

Applied during verify-pr Step 4b for `performance` / `db-migration` tasks. CONVENTIONS.md
is **mandatory**. If the file does not exist at the repository root, halt immediately:

> "Performance optimization verification requires CONVENTIONS.md with at minimum: CI check commands, performance test commands, and regression thresholds. Create it before proceeding."

**Stop execution immediately.** Do not proceed with any subsequent steps.

If CONVENTIONS.md exists, extract any "Performance Thresholds" or "Regression Limits"
section for use in Step 4.6 (drift detection thresholds).

## Step 4.5 – Read Implementation Results (Performance Tasks Only)

**If `task_type = standard`:** Skip to Step 5.

Find the optimization result report in `performance/optimization-results/{jira_key}-*.md` (most recent by timestamp). Read and extract: jira_key, timestamp, branch, commit_sha, baseline_commit_sha, capture_mode, capture_target, capture_base_url, status, and before/after metrics by metric_type (frontend: LCP, FCP, DOM Interactive; backend: Response Time p95/p99, Throughput, Error Rate).

If report not found, check the PR description for a before/after table as fallback. If neither source has results, record "Implementation results not found" and proceed.

## Step 4.6 – Environmental Drift Detection (Performance Tasks Only)

**If `task_type = standard`:** Skip to Step 5.

**Environment mismatch check (run before re-run prompt):** Read `metadata.capture_target` from config (null → treat as `localhost`). Compare against `capture_target` from the optimization result report (Step 4.5). If they differ → record `Environment Match: MISMATCH` for the report. Skip numeric drift thresholds for frontend metrics — "Baseline used {config target}, implementation used {report target} — metrics not comparable." This check runs even if the user skips re-run.

Prompt user: (1) Re-run baseline now (recommended), (2) Skip and rely on implementation results.

**If re-run:** Read `metadata.baseline_mode`, `metadata.capture_target`, `metadata.capture_base_url`, `dev_environment.frontend.port`, `dev_environment.backend.port`, `baseline_settings.iterations` from `performance-config.json`. Use same capture mode as original baseline.

Copy `capture-baseline.template.mjs` from plugin cache to baseline directory (always fresh copy).

**Frontend/hybrid:** Read `capture_target` (null/missing → `localhost`).
- **`localhost`:** use `--port` from `dev_environment.frontend.port`
- **`hosted`:** read `capture_base_url` (halt if null/empty — "Re-run `/sdlc-workflow:performance-baseline` or `perf-config.py set metadata.capture_base_url <url>`."). Prompt for auth (`--storage-state` or `--user`/`--pass`) and `--insecure`.

Construct command mirroring performance-baseline Step 9.3 — absolute `--config` path, auth flag mutual exclusivity, `BASELINE_PASS` env var. Playwright leg follows `capture_target`; backend leg always uses `perf-benchmark.sh` + `dev_environment.backend.port`.

Verification failed → display script diagnostics, halt. Do not retry.

**Backend/hybrid:** Use `perf-benchmark.sh`:
```bash
plugin_root=$(ls -d "${HOME}/.claude/plugins/cache/"*/sdlc-workflow/*/ 2>/dev/null | sort -V | tail -1)
"$plugin_root/scripts/perf-benchmark.sh" \
  --port "$(python3 "$plugin_root/scripts/perf-config.py" get dev_environment.backend.port)" \
  --iterations "$(python3 "$plugin_root/scripts/perf-config.py" get baseline_settings.iterations)" \
  --manifest performance/test-data/manifest.json \
  --output "$(python3 "$plugin_root/scripts/perf-config.py" get directories.verification)/benchmark-results-verify.json"
```

Compare re-run results against implementation results.

**Drift thresholds (both gates must be exceeded to flag):**

Check CONVENTIONS.md first — if it defines a "Performance Thresholds" or "Regression Limits" section with custom thresholds (extracted in Step 4b), use those values. Otherwise use these defaults:

| Category | Relative | Absolute |
|---|---|---|
| Frontend time | >5% | >50ms |
| Frontend size | >5% | >10KB |
| Backend response time | >10% | >50ms |
| Backend throughput | >20% decrease | — |
| Backend error rate | — | >1% increase |

If significant drift found, flag for investigation with a comparison table. Record findings for report.

## Step 4.7 – Validate Target Achievement (Performance Tasks Only)

**If `task_type = standard`:** Skip to Step 5.

Evaluate ONLY the metrics listed in the task's **Target Metrics** section. Metrics not listed in the task are not evaluated — they belong to other tasks in the same Epic.

Compare current metrics (from Step 4.5 or 4.6) against the listed target metrics from the Jira task.

**Check for acknowledged regression:** If the optimization result report (Step 4.5) has `status: regression_acknowledged`, classify as **Partial Success** (WARN), not Regression (FAIL). Note in details: "Regression was acknowledged during implementation — see regression report for context."

- **Full Success:** All listed targets met → PASS
- **Partial Success:** Progress toward target >20% (calculated as `(baseline - current) / (baseline - target) × 100`) but not all targets met → WARN
- **Insufficient Improvement:** Progress <20% and targets not met → FAIL
- **Regression:** Any listed metric worse than baseline (and NOT `regression_acknowledged`) → FAIL

## Step 4.8 – Migration Safety Verification (Database Migration Tasks Only)

**If `task_type` is not `db-migration`:** Skip to Step 5.

**Scope:** Code-level verification only — DDL inspection, convention compliance, intent comparison. Live database execution (EXPLAIN, running migrations) is out of scope. Manual verification SQL in the task description is for the developer to run independently.

### Step 4.8.1 – Identify Migration Files

Filter the PR diff for migration files matching known framework path patterns:
- `migration/src/m*.rs` (SeaORM)
- `migrations/*/up.sql`, `migrations/*/down.sql` (Diesel)
- `migrations/*.sql` (sqlx)
- `alembic/versions/*.py` (Alembic)
- `**/migrations/*.py` (Django)
- `src/main/resources/db/migration/V*__*.sql` (Flyway)
- `prisma/migrations/*/migration.sql` (Prisma)
- `src/migration/*-*.ts` (TypeORM)

If no migration files found in the diff, record "Migration Safety: N/A — no migration files in diff" and proceed.

### Step 4.8.2 – Destructive DDL Scan

For each migration file, scan for destructive operations:

| Pattern | Result |
|---|---|
| `DROP TABLE`, `DROP COLUMN`, `DELETE FROM`, `TRUNCATE` | FAIL — blocks merge |
| `ALTER COLUMN ... DROP NOT NULL`, `ALTER COLUMN ... TYPE` | WARN — flag for review |
| `CREATE INDEX` without `CONCURRENTLY` | PASS — framework migrations run in transactions where CONCURRENTLY is invalid. Informational note: "For manual production rollout, use CONCURRENTLY." |
| `CREATE INDEX CONCURRENTLY` | PASS |
| `DROP INDEX` in rollback/down migration only | PASS |

### Step 4.8.3 – Verify Rollback Exists

Check that each migration has a corresponding rollback:
- SeaORM: `down()` method in the migration struct
- Diesel: `down.sql` alongside `up.sql`
- Alembic: `downgrade()` function
- Flyway: WARN — Flyway does not natively support rollback
- TypeORM: `down()` method
- Django: auto-generated rollback (PASS unless manual migration)

### Step 4.8.4 – DDL Intent Comparison

If the task description contains a **Database Migration** section with **Before/After SQL**, compare the planned DDL operations against the actual PR diff. Compare **intent** — what DDL operations are performed (create index on which table/column, rewrite which query) — not verbatim SQL, since implement-task may adapt scripts per CONVENTIONS.md.

### Step 4.8.5 – CONVENTIONS.md Compliance

Read CONVENTIONS.md migration-related sections. Verify:
- Migration file naming matches documented convention
- Index naming follows documented pattern
- Migration structure matches established patterns (scan 2-3 existing migrations as reference)
- FK index policy compliance if documented

Flag convention violations as code change requests (same upgrade behavior as the Style/Conventions sub-agent — e.g., "N migrations use X pattern; CONVENTIONS.md §Y documents this").

### Step 4.8 Verdict

Record overall Migration Safety result:
- **PASS**: No destructive DDL, rollback exists, conventions followed
- **WARN**: Non-blocking issues (Flyway rollback, non-CONCURRENTLY index)
- **FAIL**: Destructive DDL detected — blocks merge

## Step 8 report additions (Performance & Migration)

When generating the Step 8 report, include these rows in the report table (and their
"Verdict source mapping" entries) only for the relevant task type:

| Report Row | Result values | Source |
|---|---|---|
| Target Achievement | PASS/WARN/FAIL/N/A (performance tasks only) | Orchestrator (Step 4.7) |
| Environment Match | MATCH/MISMATCH/N/A (performance tasks only) | Orchestrator (Step 4.6) |
| Baseline Re-run | PASS/WARN/SKIPPED/N/A (performance tasks only) | Orchestrator (Step 4.6) |
| Migration Safety | PASS/WARN/FAIL/N/A (db-migration tasks only) | Orchestrator (Step 4.8) |

**Performance tasks (`task_type = performance`):** Additionally include a "Performance Results" section after the report table with the before/after comparison table from Step 4.5/4.6, achievement status from Step 4.7, and recommendations.

**Performance report affects Overall:** Target Achievement PASS/WARN/FAIL counts toward Overall result. Baseline Re-run and Environment Match are informational (do not affect Overall). Environment MISMATCH skips numeric drift thresholds — note "metrics not comparable" in the Baseline Re-run details.

## Step 10 – Update Optimization Result Report (Performance Tasks Only)

**If `task_type = standard`:** Skip this step.

If the optimization result report was found in Step 4.5, update it with verification results.

### Step 10.1 – Determine Status

Map Overall Result: PASS → `verified`, WARN (partial success) → `verified_with_warnings`, FAIL → `verification_failed`.

### Step 10.2 – Update Report Metadata

Confirm `report_file` exists. Update metadata frontmatter: set `status`, `verification_timestamp`, `verification_result`.

### Step 10.3 – Append Verification Section

Append to report: Verification Results section with timestamp, overall result, acceptance criteria summary, review feedback summary, CI status, target achievement, and recommendations.

### Step 10.4 – Update Latest Metrics in Config

**Only when** Overall Result is PASS or WARN (confirmed improvement). Skip on FAIL.

Use `perf-config.py set` to update `.latest` fields for each metric based on `metric_type`:
- Frontend/hybrid: lcp, fcp, dom_interactive, total_load_time
- Backend/hybrid: response_time_p95, response_time_p99, throughput, error_rate
- Always: `metadata.last_updated` to current UTC timestamp

Plugin root resolution for bash blocks:
```bash
plugin_root=$(ls -d "${HOME}/.claude/plugins/cache/"*/sdlc-workflow/*/ 2>/dev/null | sort -V | tail -1)
if [ -z "$plugin_root" ] || [ ! -d "$plugin_root" ]; then echo "❌ sdlc-workflow plugin not found"; exit 1; fi
```
