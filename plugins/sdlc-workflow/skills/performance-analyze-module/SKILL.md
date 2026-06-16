---
name: performance-analyze-module
description: |
  Inspect source code to detect performance anti-patterns by examining bundle composition, API call patterns, component structure, and resource loading.
argument-hint: "[target-repository-path]"
---

# performance-analyze-module skill

Source code analysis to detect performance anti-patterns in a user-selected workflow. Examines bundle composition, API call patterns, render logic, and resource loading.

**Key Distinction:** This skill inspects source code. The `performance-plan-optimization` skill reads this analysis report and creates Jira tasks.

## Guardrails

- Creates files in `performance/analysis/` — does NOT modify source code
- Requires Performance Analysis Configuration with a selected workflow and baseline report
- Blocking step: Step 1 (target repository path, if not provided)
- Missing config → halt, suggest `performance-setup`. Missing baseline → halt, suggest `performance-baseline`
- Serena probe failure → do NOT halt; set `serena_mode = down`, continue with Grep
- Finding validation (Step 9) is mandatory. Precision over volume: 10 correct findings beats 50 with 40% noise
- Detection steps (5–8) may be delegated to subagents for parallelism. Validation (Step 9) may not — subagent output is input to validation, not input to the report
- When delegating detection steps, the parent agent must update `analysis-progress.json` with each subagent's results before proceeding to Step 9
- `findings-validation.json` must exist before the report is written

### Plugin Root Resolution

Every bash block that calls `perf-config.py` must begin with:

```bash
plugin_root=$(ls -d "${HOME}/.claude/plugins/cache/"*/sdlc-workflow/*/ 2>/dev/null \
  | sort -V | tail -1)
if [ -z "$plugin_root" ] || [ ! -d "$plugin_root" ]; then
  echo "❌ sdlc-workflow plugin not found"; exit 1
fi
```

## Step 1 – Determine Target Repository

Use the user-provided repository path, or the current working directory.

If `performance-config.json` exists, read `metadata.analysis_scope` and verify the repository matches:
- `backend-only`: backend indicators (Cargo.toml, pom.xml, requirements.txt, etc.)
- `frontend-only`: frontend indicators (package.json with frontend deps, framework config)
- `full-stack`/`full-stack-monorepo`: both sets of indicators

If config doesn't exist, skip validation.

## Step 2 – Verify Configuration and Selected Workflow

### Step 2.0 – Read Analysis Assumptions

Read `analysis_assumptions` from `performance-config.json`:

```bash
assumptions=$(python3 "$plugin_root/scripts/perf-config.py" get-section analysis_assumptions)
```

| Field | Variable | Default |
|---|---|---|
| `bandwidth_mbps` | `analysis_bandwidth_mbps` | 5 |
| `api_latency_ms` | `analysis_api_latency_ms` | 100 |
| `reflow_cost_ms` | `analysis_reflow_cost_ms` | 5 |
| `cache_hit_rate` | `analysis_cache_hit_rate` | 0.8 |
| `chain_depth` | `analysis_chain_depth` | 3 |
| `db_latency_ms` | `analysis_db_latency_ms` | 10 |

Validate each value (positive numbers, `cache_hit_rate` 0.0–1.0, `chain_depth` 1–5). Use defaults for invalid values with a warning.

### Step 2.1 – Check for Selected Workflow

Extract workflow name, entry point, key screens from config. If no workflow selected → halt: "Run `performance-baseline` first."

### Step 2.2 – Read Backend/Frontend Configuration

Read `metadata.backend_available`. If `true`: read backend config (name, path, framework, `serena_instance`, api_base_path) + frontend config if scope includes frontend. If `false`: log frontend-only mode; backend steps (6.B, 7) will be skipped. Serena availability is determined by live probe in Step 6.B, not here.

### Step 2.3 – Initialize Progress Checklist

Write `{analysis_dir}/analysis-progress.json` based on `(metric_type, backend_available)`:

| metric_type | backend_available | Steps → `pending` | Steps → `not_applicable` |
|---|---|---|---|
| `frontend` | any | 5.1-5.3, 6.1-6.9 | 6.B, 7.1-7.7, 7.6.1-7.6.6, 8.A-D, 8.F, 9.7 |
| `backend` | `true` | 6.B, 7.1-7.7, 7.6.1-7.6.6, 9.7 | 5.1-5.3, 6.1-6.9, 8.A-D, 8.F |
| `hybrid` | `true` | 5.1-5.3, 6.1-6.9, 6.B, 7.1-7.7, 7.6.1-7.6.6, 8.A-D, 8.F, 9.7 | (none) |
| `hybrid` | `false` | 5.1-5.3, 6.1-6.9 | 6.B, 7.1-7.7, 7.6.1-7.6.6, 8.A-D, 8.F, 9.7 |

Status values: `pending` (not yet run), `done` (completed — requires `findings` count, 0 = "no instances"), `skipped` (runtime scope guard excluded a step that could apply — requires `reason`), `not_applicable` (step does not apply to this `metric_type`/`backend_available` combo — use for all steps initialized as `not_applicable` in the table above), `optional_skipped` (user declined or prerequisites not met — requires `reason`). Use `not_applicable` (not `skipped`) for steps excluded by metric_type at initialization.

Optional step rules: Step 5.1 (no bundle stats found) → `done` with `findings: 0` (estimation fallback runs). Step 7.7 (service not running) → `optional_skipped`. Step 9.7 guard failure → `not_applicable`; user declines → `optional_skipped`.

At the end of each detection step (5.x, 6.x, 7.x, 8.x): update `analysis-progress.json` with the step's status and findings count.

## Step 3 – Verify Baseline Report Exists

Read `metadata.metric_type` to determine which baselines to check:
- `frontend`/`hybrid`: check `{baseline-directory}/baseline-report.md`
- `backend`/`hybrid`: check `{baseline-directory}/benchmark-results.json`

Halt if any required baseline is missing. Verify workflow name matches between baseline and config.

## Step 4 – Read Baseline Data

**Frontend baseline** (if metric_type includes frontend): Extract per-scenario metrics (LCP, FCP, DOM Interactive, Total Load Time), resource timing breakdown, aggregate metrics.

**Backend baseline** (if metric_type includes backend): Parse `benchmark-results.json` for per-endpoint metrics (response time percentiles, throughput, error rate, cache effectiveness).

## Step 5 – Analyze Bundle Composition

**Scope:** Skip if `metric_type = "backend"` (bundle composition is frontend-only). Proceed to Step 6.

### Step 5.1 – Locate Bundle Stats (Optional)

Check for webpack/vite bundle stats (`dist/stats.json`, `build/stats.json`, `.vite/stats.json`). If found, extract module names/sizes, third-party dependencies, code-split chunk boundaries.

### Step 5.2 – Identify Third-Party Libraries

From baseline resource timing, classify each JavaScript file as third-party (node_modules, vendor, CDN) or application code. Calculate size ratios. List top 10 by size.

### Step 5.3 – Module-Specific vs Shared Code Ratio

From bundle stats (or import pattern estimation), calculate the ratio of workflow-specific code to shared code.

## Anti-Pattern Severity Reference

All detection steps (6.x and 7.x) classify findings using this table. Each step says "classify per severity table" rather than restating thresholds.

| Anti-Pattern | High | Medium | Low |
|---|---|---|---|
| Over-Fetching (6.1) | >50% unused OR >100KB+30% | 25-50% unused | <25% unused |
| N+1 Frontend (6.2) | >10 iter sequential | 5-10 iter | <5 iter |
| Waterfall (6.3) | depth>5 OR >1000ms chain | depth 4-5 OR 500-1000ms | depth 3 OR <500ms |
| Render-Blocking (6.4) | load time >50% FCP OR >200KB | 25-50% FCP OR 100-200KB | <25% FCP OR <100KB |
| Unused Code (6.5) | >100KB or >10 imports | 50-100KB or 5-10 imports | <50KB or <5 imports |
| Re-Renders (6.6) | Critical path + DOM >3500ms | Critical path + DOM 2500-3500ms | Non-critical OR DOM <2500ms |
| Long Tasks (6.7) | >200ms or multiple >100ms | 100-200ms | 50-100ms |
| Layout Thrashing (6.8) | R/W in loops >10 iter | R/W in loops 5-10 iter | <5 iter or isolated |
| Missing Lazy Load (6.9) | Route >100KB eager OR >5 routes | 50-100KB OR 3-5 routes | <50KB OR <3 routes |
| N+1 Backend (7.3) | >10 sequential queries | 5-10 sequential | <5 or partial mitigation |
| Missing Pagination (7.4) | No pagination, >100 items | 50-100 items | <50 items |
| Missing Caching (7.5) | >100ms op, high traffic, static data | 20-100ms, medium traffic | <20ms or low traffic |
| Inefficient Queries (7.6) | SELECT * >10 cols >1000 rows | Unnecessary JOINs or >50% unused cols | Minor, <25% unused |
| Unused JOINs (7.6.1) | Large table (>10K rows) or 3+ unused | Medium table (1K-10K) | Small table (<1K) with indexes |
| Missing Indexes (7.6.4) | JOIN/WHERE on loop query (multiplier>1) | Range filter on large table | ORDER BY or small table |
| SQL Duplication (7.6.5) | Same CTE 3+ times or table scans | Same CTE 2 times | >50% overlap across 2 queries |
| Seq Scan (9.7) | >10K rows in loop query | 1K-10K rows or single query | <1K rows |
| Row Estimate Mismatch (9.7) | >100x mismatch | 10x-100x mismatch | <10x mismatch |
| Nested Loop on Large Table (9.7) | Inner scan >10K rows | Inner 1K-10K rows | Inner <1K rows |

**Impact formulas** (use throughout):
- Over-fetching: `(unused/total) × response_size ÷ (bandwidth_mbps × 125000)`
- N+1: `(iterations - 1) × api_latency_ms` (frontend) or `× db_latency_ms` (backend)
- Waterfall: `chain_time - (slowest × 1.2)`
- Layout thrashing: `(iterations - 1) × reflow_cost_ms`
- Caching: `operation_time × cache_hit_rate`

## Step 6 – Detect Frontend Anti-Patterns

**Scope:** Skip if `metric_type = "backend"` (jump to Step 6.B). Run for `frontend` or `hybrid`.

Impact estimates are heuristics for prioritization — verify after implementation.

### Step 6.1 – Over-Fetching Detection

Search workflow components for API calls (`fetch(`, `axios.get(`, `useQuery(`). For each endpoint, identify the response schema and grep for field usage in consuming components. Flag fields in the response that are never referenced.

Confidence: Low (grep cannot track destructuring, prop drilling, or dynamic access).

**Advisory drift check (hybrid only):** If `workflow.traced_api_endpoints` exists, compare endpoints discovered here against that list. Log as informational notes (not findings, not blocking):
- Endpoint in Step 6.1 but NOT in traced list → "API call `{url}` in `{file}` not in baseline trace — baseline may need refresh"
- Endpoint in traced list but NOT in Step 6.1 → "Traced API `{path}` not found in current source — may have been removed"

These are advisory only. Code changes between baseline and analysis are normal. Do not halt or create findings from drift.

### Step 6.2 – N+1 Query Detection (Frontend)

Search for loops (`.forEach(`, `.map(`, `for (`) with API calls (`fetch(`, `axios.`) within 10 lines. Check if `await` is inside the loop (sequential) vs `Promise.all` (parallel). Also check `useQuery`/`useQueries` calls without `staleTime` — default `0` causes refetch on every mount.

### Step 6.3 – Waterfall Loading Detection

From baseline resource timing, build a dependency graph. Identify chains of >3 sequential resources. Calculate waterfall depth and total chain time.

### Step 6.4 – Render-Blocking Resources Detection

Search HTML entry points for `<script src=` without `async`/`defer` and `<link rel="stylesheet"` without non-blocking attributes. Cross-reference blocking resource load times against FCP/LCP.

### Step 6.5 – Unused Code Detection

Extract all `import` statements from workflow components. Search for usage of each imported symbol in the file body. Flag imports never referenced. Estimate unused bundle size from stats or typical module sizes.

### Step 6.6 – Expensive Re-Render Detection

Identify component hierarchy in workflow routes. Search for missing memoization (React: `React.memo`, `useMemo`, `useCallback`; Vue: `computed`, `watch`). Flag components receiving complex props without memoization, inline functions as props, missing `key` in lists. Prioritize components in the critical render path.

### Step 6.7 – Long Task Detection

Check baseline for resource timing data. Grep for expensive patterns — synchronous loops over large datasets, JSON.parse of large payloads, DOM manipulation in loops, spread inside `.reduce()` (O(n²) memory: `[...prev,` patterns).

### Step 6.8 – Layout Thrashing Detection

Search for DOM read-write patterns: reading layout properties (`offsetWidth`, `getBoundingClientRect`) followed by writes (`style.width =`, `classList.add`) inside loops. Static analysis cannot determine execution ordering — only flag patterns where read-write appears inside a loop.

### Step 6.9 – Missing Lazy Loading Detection

Check route configuration for dynamic imports (React: `React.lazy`, Vue: `() => import(...)`, Next.js: `dynamic()`). Flag routes using static imports for large components. Estimate component sizes from bundle stats or file size.

## Step 6.B – Serena Availability Probe

Runs for `metric_type = "backend"` or `"hybrid"` when `backend_available = true`.

Read `serena_instance` from config. If non-empty, call `mcp__{serena_instance}__get_symbols_overview` with `relative_path="."`:
- Response received → `serena_mode = live`
- Error → `serena_mode = down`, log error
- No serena_instance → `serena_mode = not-configured`

`serena_mode` applies to all of Step 7. Use Serena when `live`, grep/Read otherwise.

## Step 7 – Backend Source Code Analysis

**Runs when `backend_available = true` and `metric_type` is `backend` or `hybrid`.**

**Endpoint source (scope-aware):** Step 7 does not run for `metric_type = "frontend"` (frontend-only skips backend analysis).
- `metric_type = "backend"`: Iterate endpoints from `performance-config.json` scenarios (populated by baseline's Step 3 backend discovery). Step 6.1 was skipped; config scenarios are the authoritative endpoint list.
- `metric_type = "hybrid"`: Iterate endpoints from `workflow.traced_api_endpoints` (populated by baseline Step 4.8 frontend-to-backend API tracing). These are the specific backend APIs that the selected frontend workflow calls. Fallback: if `traced_api_endpoints` is empty (backward compat with older configs), use config scenarios with `type: "backend"` instead.

For EACH endpoint from the source above:

### Tool Selection (applies to all Step 7.x sub-steps)

| serena_mode | Tool | Confidence |
|---|---|---|
| `live` | `mcp__{serena_instance}__find_symbol(...)` with `include_body=true` | High |
| `down` / `not-configured` | Grep across backend_path + Read tool | Medium |

### Step 7.1 – Locate Backend Handler

Search for handler by endpoint path fragment. Extract handler function name and file location. If not found, document limitation and skip to next endpoint.

### Step 7.2 – Extract Backend Response Schema

Read handler implementation and identify return type from function signature. Find and read the response struct/class definition. Extract ALL fields recursively including nested objects.

Document complete response schema:
```
Endpoint: GET /api/v2/products/:id
Response Type: ProductResponse
Fields: id, name, description, price, inventory{quantity, warehouse_location}, created_at, ...
```

### Step 7.3 – Detect Backend N+1 Queries

Read handler implementation. Search for query patterns inside loops:

| Framework | N+1 Pattern |
|---|---|
| Rust (sqlx) | `for item in items { query!(..., item.id).fetch_one(&pool).await }` |
| Rust (SeaORM) | `for item in items { Entity::find_by_id(item.id).one(&db).await? }` |
| Rust (Diesel) | `for item in items { table.find(item.id).first::<Model>(&conn)? }` |
| Java (JPA) | `for (Item item : items) { repository.findById(item.getId()) }` |
| Python (SQLAlchemy) | `for item in items: session.query(Model).filter(...).first()` |
| Node (TypeORM/Prisma) | `for (const item of items) { await db.model.findUnique({...}) }` |

**NOT N+1** (concurrent execution — do NOT flag):
- JS: `Promise.all([...])`, `Promise.allSettled([...])`
- Rust: `tokio::try_join!`, `join_all(futures)`, `buffer_unordered(n)`, `for_each_concurrent`, `FuturesUnordered`
- Java: `CompletableFuture.allOf(...)`, `.parallelStream()`
- Python: `asyncio.gather(...)`, `ThreadPoolExecutor.map(...)`

**Partial mitigation:** Sequential outer loop with concurrent inner calls — classify as N+1 with note about inner concurrency.

**Loop origin identification:** For each N+1 finding, identify the **outermost loop that drives the query multiplication** — not just the inner query call site. Record:
- `loop_function`: the function containing the loop (name, file, line)
- `loop_variable`: what is being iterated (e.g., `rows`, `items`, `matches`)
- `loop_source`: what produces the iteration set (e.g., "result of `load_graphs_query`", "parameter `rows: Vec<Row>`")
- `loop_nesting`: whether the N+1 query is in the outermost loop or a nested inner loop

Include this as `loop_origin` in the finding output. This distinguishes "the loop itself must be eliminated" from "only the inner query needs batching."

### Step 7.3.1 – Detect Pre-Fetchable Concurrent Query Patterns

Concurrent execution patterns (`buffer_unordered`, `Promise.all`, `asyncio.gather`, etc.) are correctly exempt from N+1 classification — they don't cause sequential latency stacking. However, they can still generate **O(N) DB queries** when each concurrent task makes per-item database calls. These are pre-fetch opportunities: the per-item queries could be replaced by a single batch pre-fetch before the concurrent processing starts.

**Detection:** This check runs as part of deep chain analysis (Step 7.6.2) when a concurrent iteration construct is encountered — it is placed here for classification context, but executes during Step 7.6.2's recursive tracing. For each concurrent iteration pattern found, check whether the concurrent body contains DB queries:

| Framework | Concurrent Per-Item Pattern |
|---|---|
| Rust | `stream::iter(items).map(async \|item\| { Entity::find().filter(...item...).one(conn).await }).buffer_unordered(n)` |
| Rust | `stream::iter(items).map(async \|item\| { resolve_something(item.id, conn).await }).buffer_unordered(n)` |
| JS | `Promise.all(items.map(async item => { await db.model.findOne({...item...}) }))` |
| Python | `asyncio.gather(*[fetch_one(item.id) for item in items])` |
| Java | `items.parallelStream().map(item -> repository.findById(item.getId()))` |

**Classification:** Flag as anti-pattern type `Pre-Fetchable Concurrent Queries` with severity based on the query count:
- High: >50 concurrent per-item queries (estimated from collection size × queries per item)
- Medium: 10-50 concurrent per-item queries
- Low: <10 concurrent per-item queries

**Finding output:** Include `prefetch_opportunity: true`, the concurrent construct (e.g., `buffer_unordered(self.concurrency)`), the per-item queries (function names and DB entities accessed), and the data source that produces the iteration set. This is consumed by plan-optimization to generate a pre-fetch mandate.

**Distinguish from fixed-set concurrency:** Do NOT flag concurrent execution over a **fixed, small set** of known operations (e.g., `tokio::try_join!(query_a, query_b, query_c)` or `Promise.all([fetchUser(), fetchProfile(), fetchSettings()])`). Only flag concurrent iteration over a **dynamic collection** whose size scales with input data.

### Step 7.4 – Detect Missing Pagination

Check if collection endpoints (`Vec<T>`, `List<T>`) have pagination parameters (`page`, `limit`, `offset`) and query methods (`.limit()`, `.offset()`, `setMaxResults()`).

### Step 7.5 – Detect Missing Caching

Identify expensive operations (DB queries for static data, external API calls, complex computations). Check for cache usage by framework:

| Framework | Cache Indicators |
|---|---|
| Rust | `moka`, `redis-rs`, `cached` crate, `Cache`, `lazy_static!` with HashMap |
| Java | `@Cacheable`, `Caffeine`, `Redis` |
| Python | `@lru_cache`, `@cached`, `Redis` |
| Node | `node-cache`, `Redis`, `memory-cache` |

### Step 7.6 – Detect Inefficient Queries

Extract SQL queries or ORM calls from handler. Flag `SELECT *` or equivalent. Cross-reference queried fields with response schema (Step 7.2). Check for missing indexes on WHERE/JOIN columns.

### Step 7.6.1 – Detect Unused Table Joins

For each query with JOINs:

1. **Extract** base table, joined tables, join type, join condition
2. **Check field usage** from joined tables: SELECT clause, WHERE/HAVING, handler code, response schema
3. **Classify:**
   - **UNUSED** — no fields from joined table used anywhere → remove JOIN
   - **FILTER-ONLY** — joined table used only in WHERE → replace with subquery/EXISTS
4. **Estimate impact:** INNER JOIN +10-30ms, LEFT JOIN +15-40ms, unindexed JOIN +50-500ms per request

### Step 7.6.2 – Deep Service Chain Analysis

Trace function calls from each handler into service methods, model builders, and utilities to detect anti-patterns hidden below the handler layer.

**Depth:** Use `analysis_chain_depth` (default 3) from config.

**For each handler**, initialize `call_graph = []`, `visited = {handler}`, `query_ledger = []`, `depth = 0`.

**Recursive tracing:** For each call site in function body, resolve the callee (`self.method` → same impl, `service.method` → resolve type, trait methods → concrete impl). Use Serena `find_symbol`/`find_declaration` when live, grep+Read otherwise.

For each resolved callee: check cycle/depth limit, read body, apply anti-pattern checks (N+1, unused JOINs, SELECT *, missing caching). Special cases:
- **Cache-guarded paths:** `.get(key)` + early return + `.insert(key, value)` on miss → annotate as `cache_gated: true`. Confirm it's a cache (type contains Cache/Lru/Ttl, known crate), not a dedup set
- **Conditional queries:** `Memo<T>`/`Option<T>` params where one branch triggers a query — check what caller passes
- **Model builders:** Always trace into `from_entity`/`from_row`/`from_model`/`new`
- Add queries to `query_ledger` with depth, loop multiplier, source. Recurse at `depth + 1`

**Persist Query Ledger:**

After building the query ledger, write `{analysis_dir}/query-ledger.json`. This structured artifact is consumed by Step 9.7 (live SQL analysis) and must exist before Step 9.7 runs.

Schema: `[{query_id, description, source_file, source_line, depth, loop_multiplier, orm_snippet, raw_sql, query_type, is_literal_sql}]`
- `is_literal_sql`: `true` for `query!()` macros, `@Query`, raw SQL strings. `false` for ORM builder chains.
- `query_type`: SELECT, INSERT, UPDATE, DELETE, or UNKNOWN.

**Outputs:** Call graph (tree format: `endpoint → service → model [file:line] ← N queries`) and query ledger table (per-query: description, source, depth, loop multiplier, conditional†, cache-gated‡, effective count; totals for all and warm-cache).

**Multiplier propagation:** Walk call_graph root→query; multiply by all loop multipliers on the path. **Estimated total DB latency:** `total_queries × db_latency_ms`.

**Zero-result check:** If a bulk fetch (`WHERE id IN (?)`) is keyed on IDs from a preceding query that can return zero results, check whether the fetch is guarded (`if ids.is_empty() { return }`) or fires unconditionally. Flag unconditional empty-set queries as wasted computation (Medium severity).

### Step 7.6.3 – Wasted Computation Detection

For each handler, compare fields accessed from the service call return value against the full return type. If handler uses <50% of returned fields and unused portion involves queries (from call graph), flag as wasted computation with the query cost.

### Step 7.6.4 – Missing Index Detection

Cross-reference WHERE/JOIN/ORDER BY columns from query_ledger against migration files. Build an index registry from `CREATE INDEX`, `.create_index()`, primary keys. Flag columns with no covering index.

**Table registry validation:** Also build a **table registry** from migration DDL (`CREATE TABLE` statements and `.create_table()` calls). Before flagging a missing index, confirm the target table exists in the table registry. If not found, record the gap in the finding's reason (e.g., "table `foo` not found in migration files — verify manually"). This feeds into Step 9.1-B check 5 which greps migration files for factual claims.

Tables from live EXPLAIN findings (Step 9.7.4) are inherently validated — the query executed successfully against the database.

### Step 7.6.5 – Inter-Query Duplication Detection

Collect raw SQL for all queries in each handler's ledger. Extract CTE names and subquery aliases. Flag CTEs/subqueries appearing in 2+ queries with identical or semantically equivalent SQL bodies. Estimate overhead: `(occurrences - 1) × db_latency_ms`.

### Step 7.6.6 – Cache Effectiveness Analysis

For endpoints with a confirmed cache AND baseline cache data: partition query_ledger into cache-gated vs cache-bypass queries. If `bypass_ratio > 0.5`, cache-bypass queries dominate — the cache delivers minimal improvement. List the anti-pattern findings producing bypass queries; these must be fixed before cache improvements are worthwhile.

### Step 7.7 – Backend Dynamic Performance Testing

**Runs automatically when:** backend service is running on configured port, test data manifest exists, `curl` is available. Otherwise skips gracefully.

Wrap API profiling in a shell function: benchmark each endpoint (cold + warm runs), measure percentiles, detect cache effectiveness. Compare current metrics against `benchmark-results.json` baseline if it exists. Regression thresholds: p95 > 50ms AND > 10% = regression.

## Step 8 – Cross-Reference Over-Fetching

For each endpoint from Step 6.1:

**A. Extract backend response fields** (from Step 7.2 schema — must be complete).

**B. Analyze frontend field usage** — grep for property accesses across frontend `src/`. Mark each field USED or UNUSED.

**C. Calculate waste:**
- Field-level: `unused / total × 100`
- If N+1: multiply by call count
- Payload: `(unused / total) × response_size × call_count`

**D. Severity:** Critical if N+1 (10+) with >50% over-fetching. High if single call >50%. Medium if 25-50%. Low if <25%.

### Step 8.F – Cross-Layer Computation Waste Detection

**Skip if:** `backend_available = false`, scope is backend-only or frontend-only, or no query_ledger exists.

Map response fields to their computation cost (queries from call graph). Cross-reference with frontend field usage. Sum query costs for frontend-unused fields. If unused fields account for >50% of total query cost, flag as cross-layer waste.

## Step 9 – Generate Workflow Analysis Report

### Step 9.0 – Pre-Report Completeness Gate

Read `{analysis_dir}/analysis-progress.json`. Verify:
1. No step has status `pending` — if any do, go back and complete them
2. Each `done` step has an explicit findings count (0 is valid)
3. No endpoints were silently dropped (compare analyzed endpoints vs config)
4. Query ledger was consumed by Steps 7.6.3-7.6.6 when it exists

Do not proceed to Step 9.1 until all checks pass.

### Step 9.1 – Finding Validation

**Mandatory.** Process all findings from Steps 5–8.

#### Step 9.1-A – Build Findings Inventory

Table with columns: #, Anti-Pattern, Step, File:Line, Detection Method, Evidence Excerpt, Original Confidence, Original Severity. Assign unique IDs (F1, F2, ...).

#### Step 9.1-B – Source Code Re-Verification

For each finding: re-read the source at the reported location (use the same tool as the detection method — do NOT use Serena for frontend findings). Verify the file exists, the code matches the evidence excerpt, and the pattern is locally present. Record PASS or FAILED with reason.

#### Step 9.1-B2 – Deep Analysis

**Mandatory for every finding with 9.1-B: PASS.** Pattern existence ≠ valid finding.

For each finding, apply these checks:

1. **Trace call chain** — Who calls this function? What bounds exist upstream? Is output reused downstream? If upstream bounds or downstream reuse invalidate the finding → FAILED: context invalidates pattern
2. **Question fix premise** — Does the recommended fix work for this technology/runtime?
   - PostgreSQL: one query per connection per transaction → `try_join!` on shared connection = zero parallelism
   - SeaORM `load_one` on `Vec<Model>` = batch query (single `WHERE id IN (...)`), NOT N+1
   - `serde_json` 128-level recursion limit → depth limits on deserialized data is dead code
   - If fix provides no benefit → FAILED: fix premise invalid
3. **Assess real-world impact** — Check actual cardinality, pagination limits, FK constraints. A query filtered by parent FK with bounded cardinality is NOT "unbounded." A table with <1000 rows doesn't need an index. If negligible → FAILED or downgrade to Low
4. **Challenge conclusion** — Construct the strongest counterargument. Common invalidators: data reused by multiple consumers, N is a small constant, function is linear despite length, extraction creates cross-module coupling, fire-and-forget is correct for telemetry
5. **Verify factual claims** — grep ALL migration files for claimed missing indexes. Trace full pipeline for claimed missing depth limits. Verify no FK/pagination constraint bounds a "unbounded" query

**False-positive risk factors by anti-pattern:**

| Anti-Pattern | Key Risk Factors |
|---|---|
| Over-Fetching | Field used via spread, passed to library, computed property access |
| N+1 | `Promise.all`/batch variant, fixed small set (<3), ORM `load_one`/`load_many` is batch |
| Waterfall | Cache-warm resources, unavoidable auth dependency |
| Unused Code | Dynamic import, reflection, shared library |
| Unused JOINs | JOIN for filtering (WHERE), ordering (ORDER BY), ORM lazy-loading |
| Missing Pagination | Known small table (<50 rows), admin-only endpoint |
| Missing Indexes | Small table (<1K rows), admin/ingestion path only, existing composite index covers it |
| Wasted Computation | Shared service method, unused fields are cheap (no queries) |
| Cross-Layer Waste | Fields needed for future feature, SEO/meta tags |

#### Step 9.1-C – Assign Confidence

Confidence = min(Detection Method, Evidence Strength) adjusted by false-positive risk. Base: High (Serena/raw SQL), Medium (grep + structural context, depth-0), Low (dynamic queries, depth>0, control flow ambiguity). Downgrade one level per unresolvable risk factor.

#### Step 9.1-D – Assign Severity

Apply the Anti-Pattern Severity Reference table using actual quantified values from detection. Recalculate if values changed during re-verification.

#### Step 9.1-E – Assign Implementation Timeline

`<1h` (single-line/config) · `1-4h` (single-file refactor) · `0.5-1d` (multi-file, one module) · `1-3d` (cross-module/API change) · `3-5d` (architectural) · `>5d` (major restructuring)

#### Step 9.1-F – Assign Disposition

| Disposition | Criteria |
|---|---|
| **Confirmed** | Passed 9.1-B and 9.1-B2, confidence ≥ Medium |
| **Confirmed (Low Confidence)** | Passed both, confidence = Low → report with "requires manual verification" flag |
| **Downgraded** | Passed both, but impact corrected downward |
| **Discarded** | Failed any check in 9.1-B or 9.1-B2 → exclude from report (log with reason) |

#### Step 9.1-G – Validation Summary

Produce summary table: Finding, Anti-Pattern, Disposition, Confidence, Severity, Timeline, Reason.

Include statistics: submitted, confirmed, low-confidence, downgraded, discarded (with percentages).

Only Confirmed, Confirmed (Low Confidence), and Downgraded findings proceed to the report.

#### Step 9.1-H – Persist Validation Artifact

Write `{analysis_dir}/findings-validation.json` with all findings (including discarded for audit trail). Set `validation_run: true` only after all validation steps complete. See [finding-validation.md](../performance/finding-validation.md) for schema.

### Step 9.2 – Report Location

Report path: `{analysis_dir}/workflow-analysis-report.md`.

### Step 9.3 – Report Structure

Read template from `${plugin_root}skills/performance/performance-analysis-report.template.md`. Populate with metrics/bundle/baseline from Steps 2–8 and findings exclusively from `findings-validation.json` (never raw detection output). Include frontend sections for `frontend`/`hybrid`, backend sections for `backend`/`hybrid`.

### Step 9.4 – Overall Performance Rating

Compare metrics against Optimization Targets: Excellent (all within), Good (1-2 slightly above, ≤20%), Needs Improvement (2-3 above, >20%), Poor (all above or any >50%). Hybrid: worst of frontend and backend.

### Step 9.5 – Prioritize Optimizations

Sort validated findings by estimated impact descending. Use query ledger totals as primary impact metric for backend optimizations.

**Cache-bypass priority:** Findings producing cache-bypass queries rank ABOVE cache improvements.

**Priority table:**

| Priority | Optimization | Confidence | Severity | Timeline | Prerequisite | Impact | Effort |
|---|---|---|---|---|---|---|---|
| 1 | {optimization} | {conf} | {sev} | {time} | {prereq or —} | {impact} | {effort} |

Prerequisites: use "Fix #N first" when an optimization delivers no benefit until another is applied. Prerequisite fixes must appear before dependent optimizations in the table.

**Strategic optimizations** (materialized views, background jobs, data model changes, ingestion pipeline changes) go in a separate table with S1, S2, ... numbering. For each, explain what scaling limit tactical fixes cannot address.

### Step 9.7 – Live SQL Analysis (Optional)

**Guard:** `backend_available = true` AND `metric_type` is `backend` or `hybrid` AND `{analysis_dir}/query-ledger.json` exists and is non-empty. Skip entirely when any guard condition is false.

#### Step 9.7.0 – Prompt User

Offer: (1) Automated — provide connection details, (2) Manual — receive EXPLAIN commands to run yourself, (3) Skip → proceed to Step 9.8. Warn: use dev/staging DB only.

#### Step 9.7.1 – Prepare Queries

Read `{analysis_dir}/query-ledger.json`. Only eligible queries proceed:

- `is_literal_sql = true` AND `query_type = "SELECT"` → EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
- Mutation queries (INSERT/UPDATE/DELETE) → EXPLAIN without ANALYZE only, or skip
- `is_literal_sql = false` or dynamic SQL → skip, document as Phase 1 limitation

Parameterize eligible queries with representative values from test data manifest or safe defaults.

#### Step 9.7.2 – Collect Connection Details (Automated Mode Only)

Prompt for PostgreSQL connection details. Verify connectivity. On failure: offer re-entry, switch to manual mode, or skip.

**Security:** Connection details held in session memory only — never written to any file or artifact.

#### Step 9.7.3 – Obtain EXPLAIN Results

**Automated:** Execute EXPLAIN on eligible queries with a 30-second statement timeout. Never execute mutation queries via EXPLAIN ANALYZE — use EXPLAIN without ANALYZE or skip. On timeout: prompt user to run the timed-out query manually and share the result, or skip that query. On other errors: record and continue.

**Manual:** Present numbered EXPLAIN commands for each eligible query (with source location and parameterized SQL). User executes on their database and shares results back. Accept partial results — analyze whatever is provided. Determine `detection_method` from whether output contains execution timing.

#### Step 9.7.4 – Analyze Bottlenecks

Parse EXPLAIN output for: sequential scans on large tables, missing indexes, nested loop joins on large inner relations, row estimate mismatches, sorts spilling to disk, high-cost nodes, hash batch overflow. Classify severity per the Anti-Pattern Severity Reference table.

#### Step 9.7.5 – Create and Validate Findings

Create findings with `detection_method: "EXPLAIN ANALYZE"` (or `"EXPLAIN"`), `step: "9.7.4"`, confidence: High. Include `explain_data` per [finding-validation.md](../performance/finding-validation.md) schema. Finding IDs continue the existing F-sequence.

Pass each finding through the Step 9.1 validation flow (9.1-B source re-verification, 9.1-B2 fix premise validation, 9.1-C–F confidence/severity/disposition assignment). Update `findings-validation.json`.

If Step 9.7 added any new Confirmed or Downgraded findings, re-run Step 9.5 to incorporate them into the priority table before proceeding to Step 9.8.

#### Step 9.7.6 – Heuristic vs Measured Comparison

Compare static estimates (`db_latency_ms` × effective query count) against measured execution times. Label clearly as "Heuristic Estimate vs Measured" with the formula — these are not comparable methodologies.

### Step 9.8 – Validate and Write Report

**Step 9.8-A:** Confirm `findings-validation.json` exists. Assemble report content (including Live SQL Analysis section if Step 9.7 was performed). Run validation checklist from [finding-validation.md](../performance/finding-validation.md). All rules must PASS.

**Step 9.8-B:** Only when 9.8-A shows all PASS: set `Validation Status: passed`, write to `{analysis_dir}/workflow-analysis-report.md`.

## Step 10 – Output Summary

```
✅ Performance analysis complete!

Workflow: {name}
Overall Rating: {rating}
Report: performance/analysis/workflow-analysis-report.md
Validation: {confirmed} confirmed, {downgraded} downgraded, {discarded} discarded

Key Findings:
- {finding-1}
- {finding-2}
- {finding-3}

Top Optimization: {top} — Impact: {impact}

{if Step 9.7 was performed}
Live SQL Analysis: {analyzed} queries analyzed, {skipped} skipped, {bottlenecks} bottlenecks found
Top bottleneck: {description} — {execution_time}ms
{end if}

Next: Run /sdlc-workflow:performance-plan-optimization to create Jira tasks
```

## Important Rules

- All detection must be based on actual code search results — never fabricate findings
- Impact estimates should be conservative; scope analysis to the selected workflow only
- Zero instances = report "No instances detected" — don't omit the step
- Detection failures → document in report limitations; validation gate (Step 9.8) still applies
- Live SQL credentials: session-only, NEVER written to any file/artifact. Use env vars for passwords — never CLI args
- Live SQL: NEVER execute mutation queries via EXPLAIN ANALYZE. Use EXPLAIN without ANALYZE, or skip
