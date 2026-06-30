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
| `frontend` | any | 5.1-5.3, 6.1-6.9 | 6.B, 7.1-7.7, 7.3.2, 7.4.1, 7.6.1-7.6.8, 7.6.4.1, 7.8.1-7.8.4, 8.A-D, 8.F, 9.7 |
| `backend` | `true` | 6.B, 7.1-7.7, 7.3.2, 7.4.1, 7.6.1-7.6.8, 7.6.4.1, 7.8.1-7.8.4, 9.7 | 5.1-5.3, 6.1-6.9, 8.A-D, 8.F |
| `hybrid` | `true` | 5.1-5.3, 6.1-6.9, 6.B, 7.1-7.7, 7.3.2, 7.4.1, 7.6.1-7.6.8, 7.6.4.1, 7.8.1-7.8.4, 8.A-D, 8.F, 9.7 | (none) |
| `hybrid` | `false` | 5.1-5.3, 6.1-6.9 | 6.B, 7.1-7.7, 7.3.2, 7.4.1, 7.6.1-7.6.8, 7.6.4.1, 7.8.1-7.8.4, 8.A-D, 8.F, 9.7 |

Status values: `pending` (not yet run), `done` (completed — requires `findings` count, 0 = "no instances"), `skipped` (runtime scope guard excluded a step that could apply — requires `reason`), `not_applicable` (step does not apply to this `metric_type`/`backend_available` combo — use for all steps initialized as `not_applicable` in the table above), `optional_skipped` (user declined or prerequisites not met — requires `reason`). Use `not_applicable` (not `skipped`) for steps excluded by metric_type at initialization.

Optional step rules: Step 5.1 (no bundle stats found) → `done` with `findings: 0` (estimation fallback runs). Step 7.7 (service not running) → `optional_skipped`. Step 7.8 (no DML-containing migration files found) → all 7.8.x sub-steps set to `skipped` with reason "no DML-containing migration files found." Step 9.7 guard failure → `not_applicable`; user declines → `optional_skipped`.

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
| Unbounded Iteration (7.3.2) | No guard + DB queries with multiplier > 1 per iteration | No guard + single DB query per iteration | Guard exists but generous (> 1000) |
| Cross-Table OR (7.6.7) | OR spans 3+ LEFT JOINed entities on likely-large tables | OR spans 2 LEFT JOINed entities | Small reference tables only |
| Load-All-Then-Search (7.6.8) | Simple search criteria, known at query time, user-facing | Partially known criteria | Bounded data or reused collection |
| Late Pagination (7.4.1) | Unbounded load + post-load slice | Bounded load + post-load slice | Small collection or admin-only |
| Redundant Indexes (7.6.4.1) | Exact duplicate on junction/relationship table | Exact duplicate on regular table | Exact duplicate on small table |
| Recursive CTE Risk (7.6.2) | Junction table, no depth limit | Junction table, depth limit present | Entity table or tight limit (< 10) |
| Missing Statistics Refresh (7.8.1) | Backfill on >1M rows or 3+ table JOIN | Backfill on 2 tables or with function | Simple single-table INSERT...SELECT |
| Non-Materialized CTE (7.8.2) | CTE with function call, 3+ references | CTE with function, 2 references | CTE with simple aggregate, 2 references |
| Uniform Processing (7.8.3) | >1M rows, <10% need processing | Medium table, <50% need processing | Skip ratio unclear |
| Expensive PL/pgSQL Pattern (7.8.4) | Dynamic regexp in loop on >10K rows | Dynamic regexp unclear N, or EXECUTE in loop | RAISE NOTICE in loop or small-N |

**Impact formulas** (use throughout):
- Over-fetching: `(unused/total) × response_size ÷ (bandwidth_mbps × 125000)`
- N+1: `(iterations - 1) × api_latency_ms` (frontend) or `× db_latency_ms` (backend)
- Waterfall: `chain_time - (slowest × 1.2)`
- Layout thrashing: `(iterations - 1) × reflow_cost_ms`
- Caching: `operation_time × cache_hit_rate`
- Cross-Table OR: heuristic only — "Actual impact depends on table sizes (verify with EXPLAIN in Step 9.7)." Do not produce numeric `impact_ms`

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

### Step 7.3.2 – Detect Unbounded Query-Driving Iteration

Detects loops iterating a query result set of unknown/unbounded size where each iteration triggers DB queries, with no `.take(N)`, `if len > MAX`, or LIMIT guard.

**Detection:** Find loops (`for item in collection`) where `collection` is a query result (Vec from `.all()`, `.fetch_all()`, etc.) and the loop body calls DB queries (direct or via function calls). Check for size guards before the loop.

| Framework | Unbounded Iteration Pattern |
|---|---|
| Rust (SeaORM) | `let items = Entity::find().all(conn).await?; for item in items { OtherEntity::find_by_id(item.ref_id).one(conn).await? }` |
| Rust (sqlx) | `let rows = query!(...).fetch_all(&pool).await?; for row in rows { query!(..., row.id).fetch_one(&pool).await? }` |
| Java (JPA) | `List<Item> items = repo.findAll(); for (Item i : items) { repo2.findById(i.getRefId()) }` |
| Python (SQLAlchemy) | `items = session.query(Model).all(); for item in items: session.query(Other).get(item.ref_id)` |
| Node (TypeORM) | `const items = await repo.find(); for (const i of items) { await repo2.findOne(i.refId) }` |

**NOT unbounded:** Loop has `.take(N)` or `[..N]` before iteration, or an `if collection.len() > MAX { return Err(...) }` guard, or collection comes from a query with explicit `.limit()`.

**Severity:** Classify per severity table.

**Finding output:** Include `loop_source` (what produces the unbounded collection), `guard_check` (present/absent/generous), `query_count_per_iteration`.

### Step 7.4 – Detect Missing Pagination

Check if collection endpoints (`Vec<T>`, `List<T>`) have pagination parameters (`page`, `limit`, `offset`) and query methods (`.limit()`, `.offset()`, `setMaxResults()`).

### Step 7.4.1 – Late Pagination Detection

If pagination parameters are found (Step 7.4), trace where they are consumed. If they flow into a post-load slicing operation (`paginate_array()`, `[offset..offset+limit]`, `.skip(n).take(n)` on an in-memory collection) rather than into the SQL query (`.limit()`, `.offset()`, `LIMIT $1 OFFSET $2`), flag as "Late Pagination."

| Framework | Late Pagination Pattern |
|---|---|
| Rust | `let all = service.load_all(conn).await?; paginated.paginate_array(&all)` |
| Java | `List<T> all = service.findAll(); return all.subList(offset, offset + limit)` |
| Python | `all_items = service.get_all(); return all_items[offset:offset+limit]` |
| Node | `const all = await service.findAll(); return all.slice(offset, offset + limit)` |

**NOT late pagination:** Pagination parameters flow into `.limit()`, `.offset()`, or `LIMIT $1 OFFSET $2` in the SQL query itself.

**Evidence:** Identify both (a) the pagination parameter source and (b) the consumption point. Report the gap: "Pagination exists at API layer but is applied after loading N items into memory."

**Severity:** Classify per severity table.

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

**Auto-extension on pure delegation:** When the depth limit is reached on a function that consists entirely of delegating to another function — i.e., it calls a single other function and returns its result without transformation (e.g., `self.inner.method(args)`, `self.0.method(args)`) — extend the depth limit by 1 for that call path. Apply recursively up to `chain_depth + 3` (hard cap). This ensures deeply layered architectures (common in Rust with inner/outer service patterns) don't hide the actual query site. **Delegation indicators:** Function body has ≤ 3 statements, the last of which is a return/tail-call to another method. No loops, no conditionals branching to different query paths.

**For each handler**, initialize `call_graph = []`, `visited = {handler}`, `query_ledger = []`, `depth = 0`.

**Recursive tracing:** For each call site in function body, resolve the callee (`self.method` → same impl, `service.method` → resolve type, trait methods → concrete impl). Use Serena `find_symbol`/`find_declaration` when live, grep+Read otherwise.

For each resolved callee: check cycle/depth limit, read body, apply anti-pattern checks (N+1, unused JOINs, SELECT *, missing caching). Special cases:
- **Cache-guarded paths:** `.get(key)` + early return + `.insert(key, value)` on miss → annotate as `cache_gated: true`. Confirm it's a cache (type contains Cache/Lru/Ttl, known crate), not a dedup set
- **Conditional queries:** `Memo<T>`/`Option<T>` params where one branch triggers a query — check what caller passes
- **Model builders:** Always trace into `from_entity`/`from_row`/`from_model`/`new`
- Add queries to `query_ledger` with depth, loop multiplier, source. Recurse at `depth + 1`

**Persist Query Ledger:**

After building the query ledger, write `{analysis_dir}/query-ledger.json`. This structured artifact is consumed by Step 9.7 (live SQL analysis) and must exist before Step 9.7 runs.

Schema: `[{query_id, description, source_file, source_line, depth, loop_multiplier, orm_snippet, raw_sql, query_type, is_literal_sql, is_recursive_cte, target_table, depth_limit, table_pattern}]`
- `is_literal_sql`: `true` for `query!()` macros, `@Query`, raw SQL strings. `false` for ORM builder chains.
- `query_type`: SELECT, INSERT, UPDATE, DELETE, or UNKNOWN.
- `is_recursive_cte`: `true` when raw SQL contains `WITH RECURSIVE`. Default `false`.
- `target_table`: The table referenced in the recursive CTE's base case (e.g., `package_relates_to_package`). Only set when `is_recursive_cte: true`.
- `depth_limit`: The depth limit extracted from the SQL (e.g., `100` from `WHERE depth < 100`), or `"none"` if no limit found. Only set when `is_recursive_cte: true`.
- `table_pattern`: `"junction"` if the target table appears to be a junction/relationship table (compound PK with 2+ FK columns, or table name containing `relates`, `relationship`, `edge`, `link`, `closure`), otherwise `"entity"`. Only set when `is_recursive_cte: true`.

**Recursive CTE risk flagging:** When `is_recursive_cte: true`, flag as a scale risk finding with anti-pattern type `Recursive CTE Risk`. Classify severity per the severity table. Include `target_table`, `depth_limit`, and `table_pattern` in the finding output.

**Outputs:** Call graph (tree format: `endpoint → service → model [file:line] ← N queries`) and query ledger table (per-query: description, source, depth, loop multiplier, conditional†, cache-gated‡, effective count; totals for all and warm-cache).

**Multiplier propagation:** Walk call_graph root→query; multiply by all loop multipliers on the path. **Estimated total DB latency:** `total_queries × db_latency_ms`.

**Zero-result check:** If a bulk fetch (`WHERE id IN (?)`) is keyed on IDs from a preceding query that can return zero results, check whether the fetch is guarded (`if ids.is_empty() { return }`) or fires unconditionally. Flag unconditional empty-set queries as wasted computation (Medium severity).

### Step 7.6.3 – Wasted Computation Detection

For each handler, compare fields accessed from the service call return value against the full return type. If handler uses <50% of returned fields and unused portion involves queries (from call graph), flag as wasted computation with the query cost.

### Step 7.6.4 – Missing Index Detection

Cross-reference WHERE/JOIN/ORDER BY columns from query_ledger against migration files. Build an index registry from `CREATE INDEX`, `.create_index()`, primary keys. Flag columns with no covering index.

**Table registry validation:** Also build a **table registry** from migration DDL (`CREATE TABLE` statements and `.create_table()` calls). Before flagging a missing index, confirm the target table exists in the table registry. If not found, record the gap in the finding's reason (e.g., "table `foo` not found in migration files — verify manually"). This feeds into Step 9.1-B check 5 which greps migration files for factual claims.

Tables from live EXPLAIN findings (Step 9.7.4) are inherently validated — the query executed successfully against the database.

### Step 7.6.4.1 – Redundant Index Detection

After building the index registry (Step 7.6.4), compare all index entries for the same table. Flag as redundant when:

1. Two indexes have **identical column sets** (regardless of name)
2. A non-PK index duplicates the primary key columns exactly

**NOT redundant (do not flag):**
- A shorter single-column index that is a prefix of a multi-column index. The shorter index can be legitimately faster for queries filtering only on that column (smaller index, index-only scans). Only flag prefix indexes as redundant when the query ledger shows zero queries that use the shorter index without also using the additional columns of the longer one.
- Indexes with different column orderings (different leading columns serve different query patterns).

**Severity:** Classify per severity table. Base severity on table pattern: junction/relationship tables (compound FK columns) are likely large, regular entity tables are medium, small reference/lookup tables are low.

### Step 7.6.5 – Inter-Query Duplication Detection

Collect raw SQL for all queries in each handler's ledger. Extract CTE names and subquery aliases. Flag CTEs/subqueries appearing in 2+ queries with identical or semantically equivalent SQL bodies. Estimate overhead: `(occurrences - 1) × db_latency_ms`.

### Step 7.6.6 – Cache Effectiveness Analysis

For endpoints with a confirmed cache AND baseline cache data: partition query_ledger into cache-gated vs cache-bypass queries. If `bypass_ratio > 0.5`, cache-bypass queries dominate — the cache delivers minimal improvement. List the anti-pattern findings producing bypass queries; these must be fixed before cache improvements are worthwhile.

### Step 7.6.7 – Detect Cross-Table OR Filter Patterns

Detects ORM query builders that compose filter expressions across multiple LEFT JOINed entities, producing OR conditions that span tables and defeat index usage.

**Detection:** Find ORM filter-composition calls that register columns from multiple entities. For each:

1. Identify the entities whose columns are registered (e.g., `Entity.columns().add_columns(OtherEntity.columns())`)
2. Check if those entities are joined via LEFT JOIN in the query builder
3. If a bare-value filter (no field qualifier) generates ILIKE/OR across ALL registered columns, including columns from LEFT JOINed tables → flag

| Framework | Cross-Table OR Pattern |
|---|---|
| Rust (SeaORM) | `.columns().add_columns(other::Entity.columns())` with `.filtering_with(query, columns)` where query has no field qualifier |
| Rust (Diesel) | `.or_filter()` spanning columns from `.left_join()` tables |
| Java (JPA) | `CriteriaBuilder.or()` with predicates from joined entities |
| Python (SQLAlchemy) | `or_()` with columns from `.outerjoin()` tables |
| Node (TypeORM) | `Or()` conditions spanning `leftJoinAndSelect()` relations |

**NOT cross-table OR:** OR conditions within a single table. OR conditions on INNER JOINed tables (optimizer can handle these better). Explicit field-qualified filters (`q=name~openssl`) targeting a single entity.

**Severity:** Classify per severity table. Infer table size from data model: junction/relationship tables (compound FK columns) are likely large. Reference/lookup tables with simple PKs are likely small.

**Impact estimate:** Label as heuristic: "Estimated overhead: High — cross-table OR on LEFT JOINed tables typically forces sequential scan, defeating indexes. Actual impact depends on table sizes (verify with EXPLAIN in Step 9.7)." Do not produce a numeric `impact_ms` — this anti-pattern's cost is data-volume-dependent and cannot be estimated from source code alone.

### Step 7.6.8 – Detect Load-All-Then-Search

Detects patterns where all data for a key is loaded into memory and then searched/filtered for a specific subset, when the search criteria are known at query time and could be pushed to the database.

**Detection:** Find functions that:

1. Execute a query with only a parent-key filter (`WHERE parent_id = $1`) loading all children
2. Collect results into a Vec/HashMap/collection
3. Then search/filter that collection for items matching criteria that were available before the query

The anti-pattern is: the search criteria exist at the call site, but the query doesn't include them.

**Key distinction — what IS and IS NOT this anti-pattern:**
- **IS:** Load all products for a category → iterate to find products matching a user's search term. The search term was known before the query; it should be a WHERE clause.
- **IS NOT:** Load all nodes for an SBOM → build a dependency graph → traverse the graph to find ancestors. Graph traversal requires the full structure; the traversal operation itself can't be expressed as a SQL WHERE clause.

| Framework | Load-All-Then-Search Pattern |
|---|---|
| Rust (SeaORM/sqlx) | `Entity::find().filter(Column::ParentId.eq(id)).all(conn)` → `.iter().find(\|x\| x.name == search_term)` |
| Java (JPA) | `findByParentId(id)` → `stream().filter(x -> x.getName().equals(term))` |
| Python (SQLAlchemy) | `session.query(M).filter_by(parent=id).all()` → `[x for x in results if x.name == term]` |

**False-positive guards:**
1. If the in-memory structure is used for graph/tree traversal (petgraph operations, BFS/DFS, recursive walks) → **discard**. The full structure is necessary for traversal.
2. If the loaded data set is used by multiple downstream consumers with different filter criteria → **downgrade to Low**. Pre-loading avoids N separate queries.
3. If the filter criteria require application logic not expressible in SQL (regex, custom comparators, cross-record calculations) → **discard**.

**Severity:** Classify per severity table.

### Step 7.7 – Backend Dynamic Performance Testing

**Runs automatically when:** backend service is running on configured port, test data manifest exists, `curl` is available. Otherwise skips gracefully.

Wrap API profiling in a shell function: benchmark each endpoint (cold + warm runs), measure percentiles, detect cache effectiveness. Compare current metrics against `benchmark-results.json` baseline if it exists. Regression thresholds: p95 > 50ms AND > 10% = regression.

### Step 7.8 – Migration SQL Analysis

**Scope:** Runs when `backend_available = true` and `metric_type` is `backend` or `hybrid`. Scans migration files for performance anti-patterns in backfill/DML queries.

**Migration file discovery:** Reuse the migration path discovered by Step 7.6.4 (same directory used for index/table registry). If Step 7.6.4 was skipped or found no migration files, attempt discovery using the framework-to-path mapping (Cargo.toml → `migration/`, pom.xml → `src/main/resources/db/migration/`, requirements.txt → `migrations/` or `alembic/`, package.json → `src/migration/` or `prisma/migrations/`). If no migration files found, mark all 7.8.x sub-steps as `skipped` with reason "no migration files found."

**Scope filter:** Only analyze migration files containing DML statements (INSERT, UPDATE, DELETE) or PL/pgSQL function definitions (CREATE FUNCTION, CREATE OR REPLACE FUNCTION). Skip pure DDL-only migrations (CREATE TABLE, CREATE INDEX, ALTER TABLE ADD COLUMN). Build a **function registry** from all CREATE [OR REPLACE] FUNCTION statements across migration files — this is needed by Steps 7.8.3 and 7.8.4 when the function is defined in a different file than the one calling it.

**Scope independence:** Unlike Steps 7.1–7.6 (which analyze only the selected workflow's endpoints), Step 7.8 scans ALL DML-containing migration files in the backend codebase — not just those related to the selected workflow's runtime API endpoints. Migration anti-patterns affect deployment performance, ingestion pipelines, and data consistency regardless of which API workflow was selected for analysis.

**scope_context assignment:** Tag each migration finding with a `scope_context` field determined by tracing where the affected code is called from:

| scope_context | Condition | Example |
|---|---|---|
| `"runtime"` | Function/query is called by endpoint handlers at request time | Function referenced in `modules/fundamental/src/*/endpoints/` |
| `"ingestion"` | Function/query is called during data ingestion | Function referenced in `modules/ingestor/` or ingestion pipeline code |
| `"migration"` | Function/query runs only within migration SQL files — no references in any application source code (grep all `modules/`, `src/`, application crates excluding `migration/`) | Backfill INSERT that is never re-executed after migration |
| `"shared"` | Function is referenced from BOTH migration SQL AND application source code (any combination of runtime/ingestion callers) | Function defined in migration, called from both ingestor and endpoint handler |

**Caller search scope:** Search ALL application source code (`modules/`, `src/`, and any other application crates), excluding `migration/` itself. Do not limit the search to a single module — a function defined in a migration file may be called from any application crate.

**Assignment rules:**
1. For **named functions** (CREATE FUNCTION): grep application source for the function name. If found in any application source → `"ingestion"` or `"runtime"` based on the caller's location. If found in both endpoint handlers and ingestion code → `"shared"`. If found only in other migration SQL → `"migration"`.
2. For **inline SQL patterns** (CTEs, INSERT...SELECT without a named function): these are self-contained within the migration file. Default to `"migration"` unless the migration is designed to be re-run periodically (check for idempotency guards like `ON CONFLICT`, `WHERE NOT EXISTS`). Idempotent migrations that run during deployment → `"migration"`. One-time backfills → `"migration"`.
3. When uncertain, default to `"ingestion"` (over-report rather than suppress).

Do NOT suppress findings based on scope_context. All contexts produce valid findings. The scope_context is used by plan-optimization (Step 5) for prioritization, not for filtering.

**Backward compatibility:** Findings from prior analysis runs that lack `scope_context` should be treated as `scope_context = "unknown"` by downstream steps.

#### Step 7.8.1 – Missing Statistics Refresh

Detect bulk INSERT...SELECT or UPDATE...FROM operations that write to or read from tables without a preceding ANALYZE statement in the same migration file.

**Detection:** For each migration file containing INSERT...SELECT or UPDATE...FROM:

1. Extract the target table (INSERT INTO) and source tables (FROM/JOIN in the SELECT)
2. Check whether `ANALYZE {table};` appears before the DML statement in the same file for any of the involved tables
3. Flag when: the DML operates on a table that was just created or bulk-loaded in a prior migration step, AND no ANALYZE precedes the DML

| Pattern | Example |
|---|---|
| Missing ANALYZE before backfill | `CREATE TABLE new_table (...); INSERT INTO new_table SELECT ... FROM large_table;` — no `ANALYZE large_table;` or `ANALYZE new_table;` before the INSERT |
| Missing ANALYZE between steps | Step 1 bulk-inserts into `dict_table`, Step 2 JOINs `dict_table` — no `ANALYZE dict_table;` between steps |

**NOT missing ANALYZE (do not flag):**
- Small reference table inserts (INSERT INTO ... VALUES (...), ...) with fewer than 100 literal rows
- Migrations that only CREATE TABLE + CREATE INDEX (no DML)
- INSERT...SELECT where the source query has explicit LIMIT < 1000

**Severity:** Classify per severity table.

**Finding output:** Include `scope_context` per Step 7.8 Scope independence. For inline SQL patterns (INSERT...SELECT, CTE), default to `"migration"`. If the migration contains idempotency guards (ON CONFLICT, WHERE NOT EXISTS) suggesting periodic re-execution during deployments, note this in the finding but keep `scope_context = "migration"`.

#### Step 7.8.2 – Non-Materialized CTE Re-evaluation

Detect CTEs in migration DML that contain expensive operations AND are referenced multiple times in the outer query without the MATERIALIZED keyword.

**Detection:** For each CTE in migration SQL (`WITH ... AS (...)`):

1. Parse CTE name and body
2. Check if CTE body contains expensive operations: function calls (including PL/pgSQL functions from the function registry), JOINs, subqueries, aggregate functions (GROUP BY, array_agg, etc.)
3. Count references to the CTE name in the outer query (SELECT, INSERT, UPDATE statements after the CTE definition)
4. Flag when: reference count >= 2 AND CTE body is expensive AND no MATERIALIZED keyword

**PostgreSQL version context:** PostgreSQL 12+ may inline CTEs when they are non-recursive and referenced once. For CTEs referenced multiple times, the planner MAY still inline them (evaluating the body at each reference site). The MATERIALIZED keyword forces a single evaluation. Prior to PostgreSQL 12, all CTEs were implicitly materialized.

| Pattern | Example |
|---|---|
| Non-materialized CTE with function call, used in INSERT + md5 JOIN | `WITH expansions AS (SELECT expand_fn(col, mappings) AS expanded ...) INSERT INTO target SELECT e.sbom_id, el.id FROM expansions e JOIN dict el ON el.hash = md5(e.expanded)` — function evaluated once for the SELECT, again for the md5 JOIN |
| Non-materialized CTE referenced in two INSERTs | `WITH cte AS (SELECT ... FROM a JOIN b ...) INSERT INTO t1 ... FROM cte; INSERT INTO t2 ... FROM cte;` |

**NOT a problem (do not flag):**
- CTE referenced exactly once in the outer query
- CTE body is a simple SELECT from a single table with no function calls or JOINs
- CTE already has MATERIALIZED keyword
- Recursive CTEs (`WITH RECURSIVE`) — these are always materialized by PostgreSQL

**Severity:** Classify per severity table.

**Finding output:** Include `scope_context` per Step 7.8 Scope independence. For inline SQL patterns (INSERT...SELECT, CTE), default to `"migration"`. If the migration contains idempotency guards (ON CONFLICT, WHERE NOT EXISTS) suggesting periodic re-execution during deployments, note this in the finding but keep `scope_context = "migration"`.

#### Step 7.8.3 – Uniform Processing of Partitionable Data

Detect queries that apply an expensive operation to all rows when a filterable predicate could partition the work, allowing most rows to skip the expensive path.

**Detection scope:** Limited to specific high-confidence patterns to minimize false positives.

**Pattern 1 — Function call with early-exit guard:** For each migration DML that calls a PL/pgSQL function:

1. Read the function body (from CREATE FUNCTION in the same or earlier migration file, or from the function registry built during Step 7.8 initialization)
2. Check if the function contains an early-exit guard: `IF POSITION('X' IN param) = 0 THEN RETURN param; END IF;` or `IF param !~ 'pattern' THEN RETURN param; END IF;` or `IF param NOT LIKE '%pattern%' THEN RETURN param; END IF;`
3. Check if the calling query applies the function to all rows without filtering by the guard condition
4. Flag when: function has early-exit guard AND calling query processes all rows AND the guard condition could be used as a WHERE clause to skip the majority of rows

| Pattern | Example |
|---|---|
| Unconditional function application | `INSERT INTO target SELECT id, expand_fn(text, mappings) FROM source LEFT JOIN mapping_table ...;` where `expand_fn` returns input unchanged for rows without 'LicenseRef-' (early-exit guard) |
| LEFT JOIN + function on all rows | `INSERT INTO target SELECT src.id, expand_fn(src.text, lim.data) FROM src LEFT JOIN (SELECT ... FROM mappings GROUP BY sbom_id) lim ON ...;` where expand_fn has early-exit and the LEFT JOIN is only consumed by the function |

**Pattern 2 — CASE-expressible partitioning:** For each migration DML with a LEFT JOIN + function call:

1. Check if the LEFT JOIN is only needed by the function call (i.e., the JOIN's fields are only consumed by the function, not by the INSERT/UPDATE target columns directly)
2. If so, the query could be split: rows matching the guard condition go through the expensive path, the rest skip the JOIN and function entirely

**False-positive guards:**
1. If the function has no early-exit guard (every row needs processing) → **discard**. Without evidence that rows are skippable, uniform processing may be correct.
2. If the calling query already has a WHERE clause filtering to the relevant subset → **discard**. The query is already partitioned.
3. If the function modifies every row differently (no skip-able subset; guard checks a different concern than the expensive path) → **discard**.
4. If the function's early-exit guard percentage is unclear (no way to estimate skip ratio from code alone) → **downgrade to Low Confidence**. Route to "Candidates for Manual Review" in the report.
5. If the query is inside a transaction that already filters upstream (e.g., a temp table was populated with only matching rows) → **discard**. The upstream filter serves the same purpose as a WHERE clause.

**Confidence:** Low by default — this pattern requires understanding function semantics. Upgrade to Medium only when the early-exit guard uses a simple string predicate (POSITION/LIKE) that maps directly to a SQL WHERE clause.

**Severity:** Classify per severity table.

**Finding output:** Include `scope_context` per Step 7.8 Scope independence. For named PL/pgSQL functions, grep all application source code (excluding `migration/`) for the function name to determine caller context. A function defined in migration SQL that is referenced from application source code (e.g., `modules/ingestor/`) is NOT a "migration-only" function — it runs at ingestion time and its performance matters beyond the initial migration.

#### Step 7.8.4 – Expensive PL/pgSQL Function Patterns

Detect known slow patterns inside CREATE [OR REPLACE] FUNCTION definitions found in migration files.

**Detection:** For each PL/pgSQL function in migration SQL (from the function registry):

1. **Dynamic regexp in loop:** `regexp_replace(text, '\m' || variable || '...', replacement, 'g')` inside a FOREACH or FOR loop — the regex is recompiled on every iteration because it includes a concatenated variable. Flag when the concatenation uses a loop variable.
   - **Fix indicator:** If the pattern uses word boundaries (`\m`, `\M`, `(?![...])`) for delimiter matching in a known-delimiter context (SPDX expressions, CSV, space-delimited tokens), `replace()` with boundary-aware splitting would work — enumerate all valid boundary pairs instead of compiling a regex.

2. **Dynamic SQL in loops:** `EXECUTE 'SELECT ...' || variable` or `EXECUTE format('...', variable)` inside a LOOP — dynamic SQL prevents plan caching across iterations.

3. **Per-row database queries inside functions:** `SELECT ... INTO variable FROM table WHERE id = loop_var` inside a LOOP within a function body — this is the PL/pgSQL equivalent of N+1.

4. **Unnecessary RAISE NOTICE in hot paths:** `RAISE NOTICE` inside a LOOP that processes data rows — logging overhead per row (I/O + string formatting).

| Pattern | Example |
|---|---|
| Dynamic regexp in loop | `FOREACH mapping IN ARRAY mappings LOOP result := regexp_replace(result, '\m' \|\| mapping.license_id \|\| '(?![a-zA-Z0-9.-])', mapping.name, 'g'); END LOOP;` |
| EXECUTE in loop | `FOR r IN SELECT * FROM t LOOP EXECUTE format('INSERT INTO %I VALUES ...', r.name); END LOOP;` |
| Per-row query in function | `FOR r IN SELECT * FROM parent LOOP SELECT count(*) INTO cnt FROM child WHERE parent_id = r.id; END LOOP;` |

**NOT expensive (do not flag):**
- `regexp_replace` with a static (literal) pattern — the regex is compiled once
- EXECUTE outside a loop (one-time dynamic SQL)
- RAISE NOTICE outside a loop (diagnostic, not hot path)
- A loop with a small fixed-size input (e.g., `FOREACH mapping IN ARRAY mappings` where `mappings` has bounded cardinality < 10 from the calling context)

**Severity:** Classify per severity table.

**Finding output:** Include `scope_context` per Step 7.8 Scope independence. For named PL/pgSQL functions, grep all application source code (excluding `migration/`) for the function name to determine caller context. A function defined in migration SQL that is referenced from application source code (e.g., `modules/ingestor/`) is NOT a "migration-only" function — it runs at ingestion time and its performance matters beyond the initial migration.

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
| Missing Statistics Refresh (7.8.1) | Small table (<1K rows), single INSERT...VALUES (not INSERT...SELECT), migration is re-run idempotent |
| Non-Materialized CTE (7.8.2) | CTE referenced once (planner won't inline), PostgreSQL < 12 (CTEs always materialized), CTE body is trivial (no JOINs/functions) |
| Uniform Processing (7.8.3) | Function has no early-exit guard, upstream transaction already filters, query has WHERE clause partitioning, skip ratio unclear |
| Expensive PL/pgSQL Pattern (7.8.4) | Regex pattern is static literal (compiled once), loop bound is small constant (<10), scope_context confirmed as "migration" after full caller trace (no references in application source outside migration/) |

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

For migration findings (Step 7.8.x), include a **Migration & Ingestion Performance** section after the Backend Anti-Patterns section. Group findings by `scope_context`. Each finding must note its scope so readers understand whether it affects API response time, ingestion throughput, or deployment speed. Findings with `scope_context = "unknown"` (from prior runs without scope tagging) go into a separate "Unscoped Migration Findings" subsection.

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
