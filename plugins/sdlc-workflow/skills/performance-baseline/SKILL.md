---
name: performance-baseline
description: |
  Discover workflows from the codebase, prompt user to select a target workflow, auto-populate configuration, then capture performance baseline metrics via browser automation and generate a baseline report.
argument-hint: "[target-repository-path]"
---

# performance-baseline skill

Discovers user workflows from the codebase, prompts user to select a target, auto-populates configuration, captures baseline metrics (browser automation for frontend, HTTP benchmarking for backend), and generates a baseline report.

## Guardrails

- Creates files in `performance/baselines/` — does NOT modify source code
- Requires Performance Analysis Configuration (run `performance-setup` first)
- Blocking steps: Step 4.4 (workflow selection), Step 8.3 (script review), Step 8.4.B4.3 (test data confirmation)
- If config missing → halt with remediation. If script error → halt with actionable error message
- **Fast-path to first blocking prompt:** On entry, immediately read `performance-config.json` and evaluate which step contains the first user-blocking question. Skip all non-blocking verification (repo type checks, file existence probes, Serena probes) until after that blocking question is answered. The goal is to surface the first question to the user in the very first response.
- Credentials passed via CLI args or `BASELINE_PASS` env var only — never written to config files or disk
- Verification iteration runs before measurement; halts on failure with actionable diagnostics
- Hosted mode (`--base-url`) applies to frontend Playwright capture only; backend `perf-benchmark.sh` is unchanged

### Plugin Root Resolution

Every bash block that calls `perf-config.py` must begin with:

```bash
plugin_root=$(ls -d "${HOME}/.claude/plugins/cache/"*/sdlc-workflow/*/ 2>/dev/null \
  | sort -V | tail -1)
if [ -z "$plugin_root" ] || [ ! -d "$plugin_root" ]; then
  echo "❌ sdlc-workflow plugin not found"; exit 1
fi
```

### perf-config.py CLI (read help before use)

**Do not guess argument syntax.** Before the first `perf-config.py` invocation in this skill run, and again before each subcommand you have not used yet, run its `--help` and follow the documented positional arguments:

```bash
python3 "$plugin_root/scripts/perf-config.py" --help
python3 "$plugin_root/scripts/perf-config.py" set-json --help
python3 "$plugin_root/scripts/perf-config.py" set --help
```

Global option: `--config PATH` (default: `performance-config.json`). Subcommands use **positional** arguments — there are no `--dotpath` or `--value` flags.

| Subcommand | Syntax | Use for |
|---|---|---|
| `set-json` | `set-json <dotpath> <json_value>` | Arrays/objects: `scenarios`, `modules`, `workflow`, `dev_environment` |
| `set` | `set <dotpath> <value>` | Scalars: `metadata.workflow_selected`, `metadata.baseline_captured`, `dev_environment.frontend.port` |
| `get` | `get <dotpath>` | Read a single value |
| `get-section` | `get-section <section>` | Dump a top-level section as JSON |
| `validate` | `validate` | Verify config after writes |

**`set-json` pitfalls:** The second argument is a JSON **string** (object or array), not a file path. Wrong: `set-json --dotpath scenarios --json '...'`. Right: `set-json scenarios '[...]'`. For multi-line JSON, use a quoted heredoc: `set-json scenarios "$(cat <<'EOF' ... EOF)"`.

After Step 4.7 writes, run `validate` and confirm with `get-section` on `workflow`, `scenarios`, and `modules`.

### Tool Selection (Serena / Grep)

`serena_mode` is set once by a Serena probe (call `get_symbols_overview` with `relative_path="."`). Use Serena when `live`, grep/Read otherwise.

| serena_mode | Tool | Confidence |
|---|---|---|
| `live` | `mcp__{serena_instance}__find_symbol(...)` | High |
| `down` / `not-configured` | Grep + Read | Medium |

## Step 1 – Determine Target Repository

Use the user-provided path, or the current working directory. Verify it contains appropriate project indicators for the configured `analysis_scope`.

## Step 2 – Verify Performance Configuration

Read `performance-config.json`. Verify config exists (halt if missing). Initialize `stored_mode = null`, `baseline_already_captured = false`.

### Step 2.0 – Check if Workflow Selection Required

Read `metadata.workflow_selected`:
- **false:** Proceed to Step 2.0.5 (scope check), then workflow discovery (Steps 3 or 4)
- **true:** Validate that `workflow.name`, `workflow.entry_point`, and `workflow.key_screens` are non-null and non-empty. If any are missing, prompt user to either reset `workflow_selected` to false (re-discover) or enter workflow details manually. Do NOT proceed with null workflow data.

### Step 2.0.5 – Check Analysis Scope

Read `metadata.analysis_scope`:
- `backend-only` → Step 3 (backend endpoint discovery)
- `frontend-only` → Step 4.1 (frontend route discovery)
- `full-stack` / `full-stack-monorepo` → Step 4.1 (frontend route discovery), then Step 4.8 (frontend-to-backend API tracing)

### Step 2.1 – Read Selected Workflow

Extract workflow name, entry point, key screens, complexity. Store for baseline capture. Skip to Step 2.2.

### Step 2.2 – Read Baseline Mode from Metadata

Extract `metadata.baseline_mode` → `stored_mode` and `metadata.baseline_captured` → `baseline_already_captured`.

## Step 3 – Backend API Endpoint Discovery

**Runs ONLY if `analysis_scope = "backend-only"` AND `workflow_selected = false`.**

### Step 3.0 – Serena Availability Probe

Read `serena_instance` from backend config. Run the Serena probe to set `serena_mode`.

### Step 3.1 – Locate API Route Definitions

Search backend codebase for API endpoint definitions using framework-specific patterns.

**Serena path:** For each endpoint module file, call `find_symbol` with `include_kinds=[12]`, `include_body=true`. Extract HTTP method, path, handler name, file.

**Grep path:** Run one grep per framework with `-A 3` context lines:

| Framework | Grep pattern |
|---|---|
| actix-web (Rust) | `'#\[get\|#\[post\|#\[put\|#\[delete'` |
| axum (Rust) | `'\.route("'` |
| Spring Boot (Java) | `'@GetMapping\|@PostMapping\|@PutMapping'` |
| FastAPI (Python) | `'@app\.get\|@router\.\(get\|post\)'` |
| Express (Node) | `'router\.\(get\|post\)\|app\.\(get\|post\)'` |

Parse grep output in-context — do NOT write to /tmp or shell variables.

**Output as in-context table:**

| # | HTTP Method | Path Pattern | Handler | File | Impact | Discovery Method |
|---|---|---|---|---|---|---|

**Coverage self-check:** List files scanned, compare against `find` results for the framework extension. Scan any missing files before proceeding. Verify raw result count matches table row count.

### Step 3.1.1 – Validate Endpoint Safety

For each handler, count references (Serena `find_referencing_symbols` or grep). Classify: <5 refs = Low, 5-10 = Medium, >10 = High impact.

### Step 3.2 – Group Endpoints into Workflows

Group by resource prefix (primary), controller/file (secondary), or OpenAPI tags (tertiary). Present ALL workflows. Estimate complexity: 1-2 endpoints = Simple, 3-4 = Moderate, 5+ = Complex.

**Verify grouping completeness:** Count table rows from Step 3.1 vs endpoints in groups. If mismatch, redo grouping. After 2 retries, prompt user.

### Step 3.3 – Present Workflows and Prompt Selection

Display ALL discovered workflows in numbered table with name, entry endpoint, key endpoints, complexity, impact. Prompt: "Enter the number of the workflow to optimize (1-N):"

### Step 3.4 – Auto-Populate Scenarios

**GET endpoints only** → create scenario entry with name derived from method+path, endpoint path, description.

**POST/PUT/DELETE endpoints** → do NOT create a scenario. Mutating endpoints risk side effects on test data and require sample request bodies. Record them in the in-context table for reference but exclude from the scenarios array written in Step 4.7.

### Step 3.5 – Discover Modules

For each handler file in selected workflow, extract functions/methods (Serena `get_symbols_overview` or grep for function signatures).

### Step 3.6 – Stage Config Changes

Collect scenarios, modules, workflow, metadata updates. Do NOT write config yet — deferred to Step 4.7.

## Step 4 – Frontend Workflow Discovery

### Step 4.1 – Find Router Configuration

**Skip if `workflow_selected = true`.**

Find router files with `find` (patterns: `*routes*.ts*`, `*router*.ts*`, `App.ts*`). Cross-check with framework-specific grep. Ensure all router files are identified.

### Step 4.2 – Extract Route Definitions

**Skip if `workflow_selected = true`.**

Read router files (Serena `get_symbols_overview` + `find_symbol`, or Read/Grep with `-A 2`). Extract route path, component, lazy-load status. Output as in-context table with row count.

### Step 4.3 – Infer Workflows from Routes

**Skip if `workflow_selected = true`.**

Group routes by: path prefix, list-to-detail patterns, feature directory, upload/action patterns. Standalone routes become single-route workflows. Estimate complexity. **Verify completeness** (table row count vs grouped count).

### Step 4.4 – Present Workflows and Prompt Selection

**Skip if `workflow_selected = true`.**

Display ALL workflows in numbered table. Prompt selection. Store workflow details.

### Step 4.5 – Auto-Populate Scenarios

**Skip if `workflow_selected = true`.**

Generate scenario per route: name derived from path, URL, description.

**Dynamic segment substitution:** For routes with dynamic segments (`:id`, `:slug`, etc.), substitute with real values from the test data manifest (generated in Step 8.4.B4, if available) or from sample IDs discovered during backend endpoint probing. If no manifest or sample data is available, prompt the user for representative values.

After auto-population, scan all scenario URLs for unresolved `:param` segments. If any remain, list them and prompt the user before proceeding — do not proceed to capture with unresolved segments.

### Step 4.6 – Discover Modules

**Skip if `workflow_selected = true`.**

Find lazy-loaded components for each route. Extract module entry points and names.

### Step 4.7 – Consolidated Config Write

Run `set-json --help` and `set --help` first (see **perf-config.py CLI** above). Write all staged changes to `performance-config.json` via `perf-config.py`:

1. `set-json scenarios` — JSON array from Step 4.5 (or Step 3.4 for backend-only)
2. `set-json modules` — JSON array from Step 4.6 (or Step 3.5 for backend-only)
3. `set-json workflow` — JSON object with `name`, `entry_point`, `key_screens`, `complexity`, `selected_on`
4. `set metadata.workflow_selected true`
5. `set metadata.backend_endpoint_discovery_method` — `"serena"`, `"grep"`, or discovery method used

Example (replace staged values; keep JSON on one line or use a heredoc):

```bash
python3 "$plugin_root/scripts/perf-config.py" set-json scenarios '[{"name":"list-packages","url":"/packages","description":"Package listing"}]'
python3 "$plugin_root/scripts/perf-config.py" set-json modules '[{"name":"PackagesPage","entry_point":"src/pages/Packages.tsx"}]'
python3 "$plugin_root/scripts/perf-config.py" set-json workflow '{"name":"package-listing","entry_point":"/packages","key_screens":["/packages"],"complexity":"Moderate","selected_on":"2026-06-05T12:00:00Z"}'
python3 "$plugin_root/scripts/perf-config.py" set metadata.workflow_selected true
python3 "$plugin_root/scripts/perf-config.py" set metadata.backend_endpoint_discovery_method grep
python3 "$plugin_root/scripts/perf-config.py" validate
```

If a command fails, re-run that subcommand's `--help` — do not pause waiting for user input to debug syntax.

### Step 4.8 – Trace Backend API Calls from Selected Workflow

**Runs ONLY when `analysis_scope` is `full-stack` or `full-stack-monorepo` AND `workflow_selected` was just set to true (fresh selection in this run, not a re-run with existing workflow).**

Purpose: Identify which backend API endpoints the selected frontend workflow's components actually call. These become the backend scenarios for hybrid baseline capture.

**Best-effort trace:** Follows one level of local imports from module entry points. Barrel files (`index.ts` re-exports), monorepo cross-package imports (`@myorg/api-client`), and deeply abstracted API clients (3+ import levels) may not be traced. User edits at the confirmation step (Step 4.8.6) are expected for non-trivial codebases.

#### Step 4.8.1 – Locate Workflow Component Files

From the `modules` array (just written in Step 4.7), resolve file paths for each module's `entry_point`. Then find locally-imported files:

1. Read each module's `entry_point` file.
2. Extract import statements to find local files imported by each entry point (ignore `node_modules` imports).
3. For `@/` or `~/` path aliases, read `tsconfig.json` `compilerOptions.paths` or `vite.config.ts` `resolve.alias` to resolve.
4. Build `workflow_files` list = entry point files + their locally-imported files.

#### Step 4.8.2 – Extract API Call URLs

Search `workflow_files` for API call patterns (single pass):

```
grep -rn "fetch(\|axios\.\|useQuery\|useSWR\|useMutation\|api\.\(get\|post\|put\|delete\|patch\)" <workflow_files>
```

For each match, extract URL string:

| URL form | Extraction | Example |
|---|---|---|
| String literal | Direct | `fetch('/api/v2/packages')` → `/api/v2/packages` |
| Template literal | Static prefix + dynamic marker | `` fetch(`/api/v2/packages/${id}`) `` → `/api/v2/packages/:id` |
| Variable | Trace one level to assignment; skip with note if unresolvable | `fetch(apiUrl)` |

Infer HTTP method from the pattern: `axios.get` → GET, `axios.post` → POST, `useMutation` → POST (default), plain `fetch` with no options or `method: 'GET'` → GET, `fetch` with `method: 'POST'` → POST.

**Output as in-context table:**

| # | HTTP Method | API Path | Dynamic | Source File:Line |
|---|---|---|---|---|

If zero API calls found: warn user, offer to manually enter endpoints or skip backend.

#### Step 4.8.3 – Resolve and Verify Against Backend Routes

1. Read `repositories.backend.api_base_path` from config (e.g., `/api/v2`).
2. For each discovered API path, normalize (prepend `api_base_path` if the path does not already start with it).
3. If the frontend uses environment variables for the base URL (e.g., `process.env.API_URL`), check `.env` or `.env.local` to resolve.
4. Verify each endpoint exists in the backend codebase using the same framework-specific grep patterns from Step 3.1 (`#[get|`, `@GetMapping`, `@app.get`, `router.get`, etc.).
5. Mark each endpoint as `verified: true` or `verified: false`. Record the backend handler file and function name for verified endpoints.

**Output as in-context table:**

| # | Frontend API Path | Resolved Backend Path | HTTP Method | Handler | Backend File | Verified |
|---|---|---|---|---|---|---|

#### Step 4.8.4 – Generate Backend Scenarios

**GET endpoints only** → create scenario entry:
```json
{"name": "api-get-packages", "url": "/api/v2/packages", "description": "API called by {workflow_name}", "type": "backend"}
```

**POST/PUT/DELETE endpoints** → record in `traced_api_endpoints` metadata but do NOT create a scenario. Mutating endpoints are traced for analyze-module coverage but not benchmarked — measuring POST/PUT requires sample request bodies and risks side effects on test data.

Dynamic segments stay as-is (e.g., `/api/v2/packages/:id`) — resolved during Step 8.4.B4 manifest generation.

#### Step 4.8.5 – Write to Config

1. Read current `scenarios` (frontend routes from Step 4.5). Tag each with `"type": "frontend"`.
2. Append backend scenarios from Step 4.8.4 (already tagged `"type": "backend"`).
3. Write merged array:
   ```bash
   python3 "$plugin_root/scripts/perf-config.py" set-json scenarios '[{"name":"list-packages","url":"/packages","description":"Package listing","type":"frontend"},{"name":"api-get-packages","url":"/api/v2/packages","description":"API called by package-listing","type":"backend"}]'
   ```
4. Write traced endpoints (all methods, including POST/PUT/DELETE):
   ```bash
   python3 "$plugin_root/scripts/perf-config.py" set-json workflow.traced_api_endpoints '[{"path":"/api/v2/packages","method":"GET","frontend_source":"src/pages/Packages.tsx:42","backend_handler":"src/handlers/packages.rs:get_packages","verified":true}]'
   ```
5. Set discovery method:
   ```bash
   python3 "$plugin_root/scripts/perf-config.py" set metadata.backend_endpoint_discovery_method frontend-trace
   ```
6. Validate:
   ```bash
   python3 "$plugin_root/scripts/perf-config.py" validate
   ```

#### Step 4.8.6 – Present Summary and Confirm

Display tracing results:

```
API Tracing Results for workflow "{name}":
- Frontend routes: {N}
- Backend API endpoints traced: {M}
  - GET (will measure): {G}
  - POST/PUT/DELETE (trace only): {P}
  - Verified against backend routes: {V}
  - Unverified: {U}

| # | Endpoint | Method | Frontend Source | Verified | Measurement |
|---|---|---|---|---|---|
| 1 | /api/v2/packages | GET | Packages.tsx:42 | Yes | Benchmark |
| 2 | /api/v2/packages/:id | GET | PackageDetail.tsx:18 | Yes | Benchmark |
| 3 | /api/v2/packages/:id/vulnerabilities | POST | PackageDetail.tsx:55 | Yes | Trace only |
```

**Blocking prompt:** "Continue with these backend API endpoints for measurement? (yes / edit / skip backend)"

- **yes** → proceed to Step 5
- **edit** → allow adding/removing endpoints (user can manually add POST/PUT with payloads)
- **skip backend** → remove `type: "backend"` scenarios from config, set `analysis_scope` → `frontend-only`, `metric_type` → `frontend`. This is the intended escape hatch.

## Step 5 – Discover Test Data

### Step 5.0 – Check Analysis Scope

- `frontend-only` → Step 5.3 (prompt)
- `backend-only` / `full-stack` → Step 5.0.5

### Step 5.0.5 – Serena Probe (if not already set)

Run probe if `serena_mode` was not set in Step 3.0 (happens for full-stack scope).

### Step 5.1 – Extract Workflow-Specific Scope

Read workflow name and endpoint URLs from config. Resolve module directory. Discovery must be workflow-specific.

For `full-stack` / `full-stack-monorepo`: read `workflow.traced_api_endpoints` to scope test data discovery to traced GET endpoints only.

### Step 5.2 – Discover List Endpoints

**backend-only:** Find GET endpoints without path parameters in `workflow_module_path` (Serena `find_symbol` or grep). Cross-reference against workflow endpoints. Store as `list_endpoints`.

**full-stack / full-stack-monorepo:** Restrict to GET endpoints in `workflow.traced_api_endpoints` that have no dynamic segments (no `:id`, `:slug`, etc.). These are the list endpoints that provide sample IDs for dynamic segment resolution in other traced endpoints.

**Dynamic segment resolution rules:**
1. GET endpoints with no dynamic segments → direct manifest entry (`test_url` = path)
2. GET endpoints with dynamic segments (`:id`, `:slug`) → find a corresponding list endpoint in `traced_api_endpoints` (e.g., `/api/v2/packages` provides IDs for `/api/v2/packages/:id`). Curl the list endpoint, extract sample IDs from response JSON (first 3 items). If no matching list endpoint exists, prompt user for sample values.
3. POST/PUT/DELETE → not in manifest (traced for analysis only, per Step 4.8.4)

### Step 5.3 – Frontend-Only Test Data Prompt

Prompt user to confirm test data availability for the workflow. If no → halt. If yes → proceed.

## Step 6 – Select Baseline Capture Mode

### Step 6.0 – Check for Existing Mode

If `stored_mode` is set (from Step 2.2): offer to use stored mode, reset, or cancel. If null (first run): proceed to Step 6.1.

### Step 6.1 – Mode Selection

Baseline uses **cold-start mode** (direct navigation, empty cache, fresh browser context per iteration). Inform user.

### Step 6.2 – Read Baseline Settings

Read `baseline_settings.iterations` (must be ≥ 20 for valid p95) and `warmup_runs` from config. Warn if iterations < 20.

## Step 7 – Check for Existing Baseline

Check for `{baseline-directory}/baseline-report.md`. If exists: offer Replace or Cancel. If replacing, read old metrics for comparison in Step 10.3. If not exists: set `old_metrics = null`.

## Step 8 – Prepare Capture Script

### Step 8.1 – Locate and Copy Template

Verify `capture-baseline.template.mjs` exists in plugin cache. Copy to `{baseline-directory}/capture-baseline.mjs`.

### Step 8.1.5 – Verify Playwright

**Skip if backend-only.** ESM imports resolve relative to the script file, not CWD. If `{baseline-directory}/node_modules/@playwright/test` is missing:

1. Read `repositories.frontend.path` from config
2. If `{frontend_path}/node_modules/@playwright/test` exists → `ln -sf "{frontend_path}/node_modules" "{baseline-directory}/node_modules"`
3. Else → halt: `npm install @playwright/test`

Verify Chromium binary is installed. Halt if missing with `npx playwright install chromium`.

### Step 8.3 – Script Review Prompt

Explain: Playwright browser automation, Web Performance APIs, verification pass before measurement, localhost (default) or hosted (`--base-url`) with `--storage-state` (SSO/Keycloak) or `--user`/`--pass` (simple forms). Offer user review. **Blocking step.**

### Step 8.3.5 – Application Startup

Prompt user:
1. **Already running** — provide URL(s) manually
2. **Auto-discovery** — discover and start commands automatically
3. **Hosted environment** — remote URL, not localhost
4. **Exit** — cancel

**If "Already running":** For each component in `analysis_scope`:

| Component | Default Port |
|---|---|
| Frontend | 3000 |
| Backend | 8080 |

Prompt for URL (default or custom). Verify port is listening (`nc -z localhost {port}`). If fails → halt. If succeeds → store URL/port, skip to Step 9.

**If "Hosted environment":** Prompt for base URL, auth method (`--storage-state <path>` for SSO/Keycloak — generate via `npx playwright codegen --save-storage=auth.json <url>`, or `--user`/`--pass` for simple forms, or none), and whether `--insecure` is needed. Verify reachable with `curl -ksI`. Store as in-memory variables — never write credentials to config. Skip to Step 9.

**If "Auto-discovery":** Proceed to Step 8.4.

### Step 8.4 – Dev Command Discovery (Auto-Discovery Only)

For each component required by `analysis_scope` (backend first for full-stack):

#### Step 8.4.1 – Check if Command Already Configured

Check the component-specific sub-key: `dev_environment.backend` for backend, `dev_environment.frontend` for frontend. If that sub-key has `command_approved: true` → skip this component to Start step.

**Backward compatibility:** If `dev_environment` is a flat object (has `command` at top level, no `frontend`/`backend` sub-keys), treat it as the single component matching `analysis_scope`. If scope is hybrid and config is flat → halt: "Re-run `/performance-setup` to update config for hybrid scope."

#### Step 8.4.2 – Discover, Approve, and Save Command

**Command discovery (first-match-wins):**

| Priority | Frontend Source | Backend Source |
|---|---|---|
| 1 | `package.json` scripts: `dev`, `start:dev`, `start` | README/CONTRIBUTING: first `cargo run`/`mvn`/`uvicorn`/`npm start` line |
| 2 | README/CONTRIBUTING: first `npm run` line | `Cargo.toml` `[[bin]]` → `cargo run --bin {name}` |
| 3 | Makefile: `dev`/`start`/`run` target | `pom.xml` → `./mvnw spring-boot:run` |
| 4 | Framework config presence → `npm run dev` | `build.gradle` → `./gradlew bootRun` |
| 5 | Ask user | `manage.py`/`pyproject.toml` → `python manage.py runserver`/`uvicorn` |
| 6 | — | `package.json` scripts → `npm run start` |
| 7 | — | Ask user |

**Port discovery (first-match-wins):** command flags → `.env` files → framework config → framework default (frontend: 3000, backend: 8080).

**Approval prompt:** Show discovered command, source, port. User: approve / modify / exit.

**Save:** Write to the component-specific sub-key (`dev_environment.frontend` or `dev_environment.backend`):

```bash
python3 "$plugin_root/scripts/perf-config.py" set-json dev_environment.frontend '{"command":"npm run dev","source":"package.json","port":3000,"command_approved":true,"last_validated":"2026-06-05T12:00:00Z"}'
```

Or scalars: `set dev_environment.frontend.command "npm run dev"`, `set dev_environment.frontend.port 3000`, `set dev_environment.frontend.command_approved true`.

#### Step 8.4.3 – Start and Verify

Start in background. Check port with `nc -z localhost {port}` every 2s for up to 60s. On timeout: offer extend 30s or abort.

#### Step 8.4.B4 – Query and Confirm Test Data (Backend)

If `manifest.json` doesn't exist, build it. **Endpoint source depends on scope:**

**backend-only:** Discover list endpoints generically (grep backend codebase), curl each to extract sample IDs, generate manifest.

**full-stack / full-stack-monorepo:** Build manifest from `type: "backend"` scenarios only (these were traced from the frontend workflow in Step 4.8). Do NOT run generic list endpoint discovery. For each `type: "backend"` scenario:
1. URL has no dynamic segments → add to manifest directly: `{"test_url": "<url>", "parameters": {}}`
2. URL has dynamic segments (`:id`, `:slug`) → substitute with sample IDs from Step 5.2 test data. If no sample IDs, prompt user.
3. Verify each manifest endpoint: `curl -s -o /dev/null -w "%{http_code}" http://localhost:{port}{test_url}`. Flag non-200 responses.

Display verification table:

| Endpoint | Status | Time | Sample |
|---|---|---|---|

Flag SLOW (>5s), TIMEOUT, AUTH ERROR, NOT FOUND endpoints. Prompt: yes / edit / abort.

**Full-stack: backend first, 5s initialization delay, then frontend.**

## Step 9 – Execute Baseline Capture

### Step 9.0 – Pre-Capture Validation

Validate `workflow.name`, `workflow.entry_point`, and `workflow.key_screens` are non-null and non-empty. Halt if any are missing.

### Step 9.1 – Config Validation

Run `validate --phase baseline` before any capture. This catches missing scenarios, invalid ports, and missing base URLs before a 2-minute capture run fails.

```bash
python3 "$plugin_root/scripts/perf-config.py" validate --phase baseline
```

If validation fails, halt and report the errors — do not proceed to capture.

### Step 9.2 – Scope-Based Capture

Branch based on `analysis_scope`. Follow exactly ONE path:

**Frontend-only:** Run Playwright capture (Steps 9.3–9.5).

**Backend-only:** Run `perf-benchmark.sh` with `dev_environment.backend.port`, iterations, manifest path. Output: `{baseline-dir}/benchmark-results.json`.

**Full-stack / full-stack-monorepo (hybrid):**
1. Verify backend still running and manifest exists
2. Verify manifest contains only endpoints from `workflow.traced_api_endpoints` (filter out any extra endpoints)
3. Run Playwright frontend capture (Steps 9.3–9.5) → `baseline-report-frontend.json`. The capture script automatically filters to `type !== 'backend'` scenarios.
4. Run `perf-benchmark.sh` with `dev_environment.backend.port` → `benchmark-results.json`
5. Merge into hybrid `baseline-report.md` with frontend metrics, backend metrics, and API Correlation sections (see Step 10.3)
6. Update metadata: `baseline_mode: "hybrid"`

### Step 9.3 – Construct Playwright Command (Frontend/Hybrid)

Auto-detect `performance-config.json` by walking up directory tree. Always use the absolute config path.

**Localhost:**
```
node {baseline-directory}/capture-baseline.mjs --config "$config_path" --port {dev_environment.frontend.port}
```

**Hosted:** Include only the args the user provided in Step 8.3.5. Omit `--user`/`--pass` if not provided, omit `--insecure` if not needed.
```
node {baseline-directory}/capture-baseline.mjs --config "$config_path" --base-url "{base_url}" [--storage-state "{path}"] [--user "{user}" --pass "{pass}"] [--insecure]
```

### Step 9.4 – Execute and Handle Errors

Run capture script. Handle errors:
- Verification failed → display failed checks from script output; do NOT retry measurement
- Connection refused → application not running
- Playwright not found → install instructions
- Invalid URLs → review config
- Missing metrics → check browser console
- Other → display error and halt

### Step 9.5 – Parse JSON Output

Parse script JSON output: scenarios (metrics per scenario), aggregate metrics, config.

## Step 10 – Generate Baseline Report

### Step 10.1 – Report Structure

Read `baseline-report.template.md` from plugin cache.

### Step 10.2 – Filter Scenarios by Workflow

Match scenario URLs against selected workflow's key screens. Halt if no matches.

### Step 10.3 – Populate Template

**Frontend metrics** (from `capture-baseline.mjs` JSON output — all modes except backend-only):
Replace placeholders: metadata (timestamp, repo, iterations), per-scenario metrics (LCP, FCP, DOM Interactive, Total Load Time), resource timing breakdown (top 10 by duration), ASCII waterfall per scenario. For the summary table, compute mean-of-scenario-p95s from per-scenario data (capture JSON has no cross-scenario aggregate).

**Backend metrics** (from `benchmark-results.json` — backend-only and hybrid):
Read the benchmark output JSON: `{"endpoints": {"<path>": {"p50_ms", "p95_ms", "p99_ms", "mean_ms", "cold_ms", "warm_cache_mean_ms", "cache_effectiveness_pct"}}, "aggregate": {...}}`. Per-endpoint: populate backend metrics table with response time percentiles and cache effectiveness. Aggregate: compute mean across all endpoint p95s for the summary table.

**API Correlation section** (hybrid only, when `workflow.traced_api_endpoints` is non-empty):
1. For each frontend scenario (route), look up which `traced_api_endpoints` have `frontend_source` files belonging to that route's module.
2. Cross-reference with Playwright resource timing: extract Fetch/XHR entries from the capture output that match traced API paths. These represent actual in-page API wait time.
3. If resource timing fetch data is available → use those durations for the "In-Page Fetch Time" column.
4. If resource timing fetch data is unavailable (e.g., deferred fetches not captured during cold-start) → use `perf-benchmark.sh` p95 as "Isolated API p95" with a disclaimer.
5. Do NOT compute "API % of Load" as a simple ratio — APIs may run in parallel, and page load includes rendering, fonts, JS parse. Present as a correlation table, not a causation table.

**If re-baseline:** Include comparison table with old vs new p95 deltas.

### Step 10.4 – Write Report

Write to `{baseline-directory}/baseline-report.md`.

### Step 10.5 – Update Configuration

Run `set --help` if not already run this session. Update metadata and optimization targets with `set` (scalars only — use captured values from Step 10):

```bash
python3 "$plugin_root/scripts/perf-config.py" set metadata.baseline_captured true
python3 "$plugin_root/scripts/perf-config.py" set metadata.baseline_mode cold-start
python3 "$plugin_root/scripts/perf-config.py" set metadata.baseline_timestamp "2026-06-05T12:00:00Z"
python3 "$plugin_root/scripts/perf-config.py" set metadata.baseline_commit_sha "<git-sha>"
python3 "$plugin_root/scripts/perf-config.py" set metadata.capture_target hosted  # or "localhost"
python3 "$plugin_root/scripts/perf-config.py" set metadata.capture_base_url "{base_url}"  # null for localhost
# Compute summary p95: mean of per-scenario p95 values (ms), then divide by 1000 for seconds
# First baseline: set optimization_targets.frontend.lcp.baseline AND .latest (repeat per metric)
# Re-baseline: update .latest only, preserve original .baseline
python3 "$plugin_root/scripts/perf-config.py" validate
```

- **First baseline:** Set both `baseline` and `latest` to captured p95 values (convert ms→seconds: divide by 1000)
- **Re-baseline:** Update only `latest`, preserve original `baseline`
- **Unit conversion:** Capture JSON emits ms; `optimization_targets.frontend.*` stores seconds. Always divide by 1000 before writing.

## Step 11 – Output Summary

```
✅ Baseline captured successfully!

Workflow: {name}
Scenarios: {count}
Report: performance/baselines/baseline-report.md

Key Metrics:
- LCP: {mean}ms (p95: {p95}ms)
- FCP: {mean}ms (p95: {p95}ms)
- DOM Interactive: {mean}ms (p95: {p95}ms)
- Total Load Time: {mean}ms (p95: {p95}ms)

{threshold-warnings}

Next: Run /sdlc-workflow:performance-analyze-module
```

## Important Rules

- Before any `perf-config.py` subcommand, run that subcommand's `--help` — never guess flags or argument order
- Never modify source code — only create measurement artifacts
- Each Bash invocation is isolated — re-derive values from config at each block
- Never skip steps or produce partial output
- Never auto-answer blocking prompts
- URLs are localhost-only by default; remote URLs require explicit `--base-url` (Step 8.3.5 option 3)
- Hosted mode applies to frontend Playwright capture only; backend `perf-benchmark.sh` is unchanged
- Credentials never persisted to config files — pass via CLI args or `BASELINE_PASS` env var
- `--insecure` is opt-in, not automatic with `--base-url`
- Filter scenarios to selected workflow only
- Generate ASCII waterfall visualization per scenario
- Include comparison section with deltas when re-baselining
