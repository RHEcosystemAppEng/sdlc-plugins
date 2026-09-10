---
name: performance-setup
description: |
  Initialize Performance Analysis Configuration by setting up directories, baseline settings, backend configuration, and optimization targets. Workflow selection happens in performance-baseline.
argument-hint: "[target-repository-path]"
---

# performance-setup skill

You are an AI performance setup assistant. You initialize the performance analysis infrastructure for a project: creating directories, configuring baseline capture settings, backend repository (if any), and creating a minimal `performance-config.json` with empty workflow, scenarios, and module sections. Workflow discovery and selection happen in `performance-baseline`, not here.

## Plugin Root

Every bash block that calls `perf-config.py` or references `$plugin_root` must begin with:

```bash
plugin_root=$(ls -d "${HOME}/.claude/plugins/cache/"*/sdlc-workflow/*/ 2>/dev/null | sort -V | tail -1)
if [ -z "$plugin_root" ] || [ ! -d "$plugin_root" ]; then echo "❌ sdlc-workflow plugin not found"; exit 1; fi
```

Before calling `perf-config.py`, run `python3 "$plugin_root/scripts/perf-config.py" init --help` (or the relevant subcommand's `--help`). Use documented flags only — do not guess argument names.

## Guardrails

- Creates `performance-config.json` and `performance/` directory structure. Never modifies source code.
- Idempotent — re-running on configured repo offers update or skip.
- **Blocking steps:** 0.5 (architecture), 1.2 (validation), 1.3 (backend config), 4 (targets confirmation).
- **Completeness:** All 5 directories created; all config sections populated; all paths validated before writing.
- **Errors:** Architecture detection failure → halt Step 1.1; path validation failure → halt Step 3; config write failure → halt Step 7.
- **Fast-path to first blocking prompt:** On entry, immediately check for existing config (Step 0) and jump to the first user-blocking question (Step 0.5 architecture prompt). Skip all non-blocking verification until after that blocking question is answered. The goal is to surface the first question to the user in the very first response.

## Step 0 – Detect Existing Configuration

Check if `performance-config.json` exists. If yes, prompt: *"Config exists. (1) Update (2) Skip?"* — if Skip, stop. If not exists, proceed.

## Step 0.5 – Prompt for Repository Architecture

Prompt the user:

> 1. **Full-stack/monorepo** — Frontend + backend in same repo (browser + API + DB metrics)
> 2. **Separate repositories** — Frontend and backend in different repos (you'll provide paths)
> 3. **Frontend-only** — Browser metrics, bundle size, component rendering only
> 4. **Backend-only** — API endpoints, database queries, response schemas only
> 5. **Cancel**

Store selection as `repository_architecture_choice`.

## Step 1 – Detect Repository Patterns and Validate Choice

### Step 1.1 – Detection Functions

**Frontend detection** (require 2+ indicators): `package.json`, `src/` dir, framework configs (`next.config.{js,ts}`, `vite.config.{ts,js}`, `webpack.config.js`, `rsbuild.config.{ts,js}`), router files (`src/routes.tsx`, `src/router/index.ts`, `src/App.tsx`, `app/` dir). Returns `is_frontend`, `detected_framework`, `confidence` (high=3+, medium=2, low=1).

**Bundler mapping:** Next.js→webpack, Vite→vite, Rsbuild→rsbuild, Webpack→webpack, Angular→webpack, CRA→webpack, Unknown→unknown.

**Backend detection** (require 1+ strong indicator): Rust (`Cargo.toml` with actix-web/axum/poem/rocket), Java (`pom.xml`/`build.gradle` with spring-boot/micronaut), Python (`manage.py` or requirements with fastapi/flask/django), Node.js (`package.json` with express/koa/nestjs), Ruby (`Gemfile` with rails), C# (`.csproj`/`.sln`). Returns `is_backend`, `detected_framework`, `confidence`.

### Step 1.2 – Validate Architecture Choice

After frontend detection, assign `bundler` from the mapping table. Store for Step 6.

| Choice | Action |
|---|---|
| 1 (Monorepo) | Detect both in cwd. Both found → `analysis_scope="full-stack-monorepo"`, go to 1.3. Only one → prompt: switch scope, provide other path, or cancel. Neither → error, return to 0.5. |
| 2 (Separate) | Prompt for frontend path, detect. Prompt for backend path, detect. On failure: (1) configure manually (2) different path (3) cancel. Set `analysis_scope="full-stack"`, go to 1.3. |
| 3 (Frontend) | Detect in cwd or user path. On failure: (1) manual (2) different path (3) cancel. Set `analysis_scope="frontend-only"`, skip to Step 2. |
| 4 (Backend) | Prompt for path. Detect. On failure: (1) manual (2) different path (3) cancel. Set `analysis_scope="backend-only"`, go to 1.3. |
| 5 (Cancel) | Exit immediately. |

### Step 1.3 – Backend Framework Configuration

Runs only when backend is in scope (`full-stack-monorepo`, `full-stack`, or `backend-only`).

1. **Framework confirmation:** If auto-detected with high confidence, confirm with user (yes/no). If not detected or low confidence, prompt manually (examples: actix-web, axum, spring-boot, express, fastapi, django, rails, asp.net; user may include ORM).

2. **API base path:** Prompt with default `/api/v2`. Validate starts with `/`.

3. **Serena MCP availability:**

   > Sentinel contract: `serena_instance = null` (JSON null) means not configured. `perf-config.py get` prints empty string for null. Downstream bash treats empty string, `null`, and missing key as unconfigured.

   a. Discover Serena instances — look for MCP tools matching `mcp__*__check_onboarding_performed`, extract instance names from prefix.

   b. **No instances found:** `serena_instance=null`, `serena_status="not_running"`, proceed to Step 2.

   c. **Instance(s) found:** Call `mcp__<instance>__check_onboarding_performed` for each.
      - "Onboarding not performed yet" → `serena_status="not_onboarded"`
      - Success/memory count → `serena_status="onboarded"`
      - Call fails → try next instance

   d. **If not_onboarded:** Prompt user — (1) Complete onboarding now (~2-3 min, enables semantic N+1/over-fetching/unused-JOIN detection) or (2) Skip, use grep-based analysis.
      - Choice 1: Call `mcp__<instance>__onboarding`, follow instructions, write memories (project_overview, tech_stack, code_style, suggested_commands, task_completion_checklist, codebase_structure), verify, set `serena_instance=<instance>`, `serena_status="onboarded"`.
      - Choice 2: `serena_instance=null`, `serena_status="skipped"`.

   e. **If onboarded:** Set `serena_instance=<instance>`, no prompts needed.

4. **Store:** backend repo name, absolute path, framework, serena_instance, serena_status, API base path.

## Step 2 – Validate Repository Paths

For each configured path (frontend, backend): verify directory exists and is readable. Set `{role}_available=true/false` and `{role}_last_validated` to ISO 8601 timestamp (or `"-"` if not configured). **If a configured path fails validation, halt and prompt user to fix.**

## Step 3 – Set Up Target Directories

```bash
mkdir -p performance/{baselines,analysis,plans,optimization-results,verification}
```

Verify creation. On failure, inform user and stop.

### Step 3.5 – CONVENTIONS.md Check

Check if `CONVENTIONS.md` exists at the repository root.

**If missing:** Display warning:
> ⚠️ CONVENTIONS.md not found. The `implement-task` skill requires it for performance optimization tasks.
>
> Create CONVENTIONS.md with at minimum:
> - CI check commands (lint, type-check, build)
> - Performance test commands
> - Regression thresholds (or use defaults)
>
> You can create it now or before running implement-task.

**If exists:** Log "✓ CONVENTIONS.md found" and proceed.

## Step 4 – Collect Configuration Values

**Baseline Settings (all scopes):** iterations (default: 20, min 20 for statistically valid p95), warmup runs (default: 2).

> Why 20 minimum: p95 with n=10 is statistically identical to maximum. With n=20, p95 is 19th value with meaningful distribution. Recommended 30+ for stable comparisons.

**Optimization Targets by scope:**

| Metric | Default | Scope |
|---|---|---|
| LCP | 2.5s | frontend, full-stack |
| FCP | 1.8s | frontend, full-stack |
| DOM Interactive | 3.5s | frontend, full-stack |
| Total Load Time | 4.0s | frontend, full-stack |
| Response Time p95 | 200ms | backend, full-stack |
| Response Time p99 | 500ms | backend, full-stack |
| Throughput | 100 req/s | backend, full-stack |
| Error Rate | 0.1% | backend, full-stack |
| DB Query Time p95 | 50ms | backend, full-stack |

Offer: *"Use recommended defaults? (yes/no)"* — if yes, skip individual prompts.

## Step 5 – Initialize Metadata

Prepare metadata values:

| Field | Value |
|---|---|
| version | "1.0" |
| created / last_updated | Current ISO 8601 timestamp |
| workflow_selected | false |
| baseline_captured | false |
| baseline_mode / baseline_timestamp / baseline_commit_sha | null |
| analysis_scope | From Step 1.2 |
| backend_available | From Step 2 |
| backend_endpoint_discovery_method | null |
| serena_status / serena_instance | From Step 1.3 (null if frontend-only) |
| metric_type | "frontend" / "backend" / "hybrid" based on scope |

## Step 6 – Generate Configuration File

Run `init --help` first. The `init` subcommand accepts optional `--flag value` pairs (not positional JSON).

```bash
# <Plugin Root — see top of skill>
python3 "$plugin_root/scripts/perf-config.py" init \
  --analysis-scope "$analysis_scope" \
  --frontend-path "$frontend_path" \
  --frontend-framework "$frontend_framework" \
  --frontend-name "$frontend_repo_name" \
  --bundler "$bundler" \
  --backend-path "$backend_path" \
  --backend-framework "$backend_framework" \
  --backend-name "$backend_repo_name" \
  --api-base-path "$api_base_path" \
  --serena-instance "$serena_instance" \
  --serena-status "$serena_status" \
  --lcp-target "$lcp_target" \
  --fcp-target "$fcp_target" \
  --dom-target "$dom_target" \
  --total-target "$total_target" \
  --iterations "$iterations" \
  --warmup-runs "$warmup_runs" \
  --resp-p95-target "$resp_p95_target" \
  --resp-p99-target "$resp_p99_target" \
  --throughput-target "$throughput_target" \
  --error-rate-target "$error_rate_target" \
  --db-query-time-target "$db_query_time_target"
```

Omit arguments not collected for the scope. Add `--force` for idempotent updates (Step 0). Verify with `perf-config.py validate` (resolve plugin root again before calling).

The generated config sets `workflow_selected: false`, leaves scenarios/modules/workflow empty (populated by baseline skill), sets targets per scope, and creates standard directory paths.

## Step 7 – Validate Configuration

Verify: (1) target directories created, (2) frontend path exists if configured, (3) backend path exists if configured, (4) config file written. On failure, inform user and offer to fix.

## Step 8 – Output Summary

> **Performance Analysis Configuration created!**
>
> **Architecture:** {type} | **Config:** `performance-config.json`
> **Frontend:** {Enabled (framework, bundler) | Disabled} | **Backend:** {Enabled (framework) | Disabled}
> **Baseline:** {iterations} iterations, {warmup} warmup | **Targets:** LCP {t}s, FCP {t}s, DOM {t}s

**Serena recommendation (if backend enabled):**
- `serena_status="not_running"`: Recommend installing Serena MCP for semantic N+1/over-fetching/unused-JOIN detection. Current analysis uses grep-based matching (medium confidence). Re-run setup after installing.
- `serena_status="skipped"`: Note Serena is available. Re-run setup and choose "Complete onboarding" to enable.
- `serena_status="onboarded"`: No recommendation needed.

> **Single-workflow mode:** Selecting a different workflow in `performance-baseline` replaces current workflow and baseline data. Back up `performance/baselines/` before switching.

> **Next Steps:** Run `/sdlc-workflow:performance-baseline` — it will discover dev commands, discover workflows, prompt for workflow selection, auto-populate scenarios/modules, and capture initial metrics.

## Important Rules

- Never modify source code — only create/update `performance-config.json`
- Do NOT populate scenarios, modules, or workflow sections — baseline skill handles those
- Set `metadata.workflow_selected = false` — baseline skill sets true after selection
- Always prompt for backend config — never silently default to frontend-only
- When reading target repo's CLAUDE.md, only extract structured data (Repository Registry)
- Metadata timestamps use ISO 8601 format
- Step 7 validation checks directories and paths only, not scenarios/modules
