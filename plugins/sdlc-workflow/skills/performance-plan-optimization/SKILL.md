---
name: performance-plan-optimization
description: |
  Read analysis reports and generate structured optimization plan with Jira Epic and Tasks. Primarily organizes findings from performance-analyze-module; limited source inspection in Step 5 for impact analysis.
argument-hint: "[target-repository-path]"
---

# performance-plan-optimization skill

You are an AI optimization planning assistant. You generate a structured optimization plan by **reading** module-level analysis reports (created by `performance-analyze-module`), grouping optimization recommendations into logical tasks, creating Jira Epic and Tasks, and producing an optimization-plan.md document.

**Key Distinction:** This skill primarily reads analysis reports and creates Jira tasks. Limited source code inspection occurs in Step 5 (cross-functional impact analysis) for scope and effort estimation.

### Plugin Root Resolution

Every bash block that references `$plugin_root` must begin with:

```bash
plugin_root=$(ls -d "${HOME}/.claude/plugins/cache/"*/sdlc-workflow/*/ 2>/dev/null | sort -V | tail -1)
if [ -z "$plugin_root" ] || [ ! -d "$plugin_root" ]; then echo "❌ sdlc-workflow plugin not found"; exit 1; fi
```

## Guardrails

- Creates files in `performance/plans/` only -- does NOT modify source code
- Requires an existing `workflow-analysis-report.md` from analyze-module
- All RECOMMEND and CAUTION optimizations get Jira tasks (none silently skipped)
- All cross-functional impacts documented in Epic description
- Plan document saved locally even if Jira operations fail

**Blocking steps:** Step 4 zero-findings decision | Step 8 Epic credential confirmation | Step 9 per-task credential confirmation

**Error handling:** Missing report -> halt at Step 3, run analyze-module | Jira MCP unavailable -> REST fallback per `shared/jira-rest-fallback.md` | Jira credential failure -> retry once, then halt

## Step 1 -- Determine Target Repository

Use user-provided path or current working directory. Verify repository type matches `metadata.analysis_scope` in `performance-config.json`.

## Step 2 -- Verify Performance Configuration

Read `performance-config.json`. Stop if missing. Extract: selected workflow name, target directories (plans directory location).

## Step 3 -- Resolve Analysis Report Path

Extract `analysis_dir` from config `directories.analysis`. Construct path: `{analysis_dir}/workflow-analysis-report.md`.

## Step 4 -- Read and Parse Analysis Report

Read `metadata.metric_type` from config to determine which anti-pattern sections to parse.

Read the analysis report. Validate in order:

1. **Report exists** -- if not, halt: run `/sdlc-workflow:performance-analyze-module` first
2. **Anti-Pattern Analysis section present** -- if not, halt: report incomplete, re-run analyze-module
3. **Validation artifact exists** -- read `{analysis_dir}/findings-validation.json`; if missing, halt: re-run analyze-module
4. **Run validation checklist** -- apply rules A1-A7 and R1-R5 from [Finding Validation](../performance/finding-validation.md) against artifact + report. Accept schema_version `"1.0"` or `"1.1"`. Output checklist table. If any rule FAIL, halt
5. **Reject unvalidated** -- if report header shows `Validation Status: not validated`, halt
6. **Zero actionable findings:**

   | Condition | Action |
   |---|---|
   | `submitted == 0` | Offer: (1) empty-state Epic, or (2) cancel and re-run |
   | `submitted > 0`, zero Confirmed + Downgraded | Halt: all discarded, point to artifact |
   | One or more Confirmed/Downgraded | Proceed to Step 5 |

Parse findings using artifact dispositions -- Jira tasks only for Confirmed or Downgraded IDs.

**Extract from validated report:** workflow metrics (name, current/target values, rating), anti-pattern findings (name, severity, instances, estimated impact, code locations, fixes), prioritized optimizations (sorted by impact with effort estimates).

## Step 5 -- Cross-Functional Impact Analysis

Analyze potential impact of each optimization on other functionalities before task grouping.

**Scaling:** If >15 findings, full analysis on top 10 by impact. Remainder noted as "Cross-functional impact not analyzed -- manual review recommended."

### Step 5.1 -- Identify Affected Code Modules

Use Serena MCP first for symbol/reference discovery; fall back to Grep if unavailable. Always record which method was used and confidence level.

For each optimization target:
- Find references to affected component/function
- Store: file paths, line numbers, usage context
- Classify scope: Isolated (0 files) | Low (1-2) | Medium (3-5) | High (6+)

### Step 5.2 -- Assess Cross-Functional Impact

For each optimization with scope >= Low:

**Count affected workflows** by searching for workflow entry points (route/page components) that import affected code. Cross-reference with workflows in config.

**Classify severity:** None | Low (1-2 workflows) | Medium (3-4) | High (5-10) | Critical (all workflows or core infrastructure)

**Identify risk factors:**

| Risk Factor | Examples |
|---|---|
| Breaking Change | API contract change, removed parameter |
| Behavioral Change | Caching changes data freshness, retry logic changes |
| Performance Trade-off | Caching reduces latency but increases memory |
| Cosmetic Change | Layout shifts, animation timing |
| Infrastructure Change | Adding Redis, new service dependency |

### Step 5.3 -- Decision Framework

Apply rules in order to determine each optimization's disposition:

| Rule | Condition | Decision |
|---|---|---|
| 1 | Scope = Isolated AND Severity = None | RECOMMEND |
| 2 | Benefit >= 20% AND Scope <= Medium AND Severity <= Medium | RECOMMEND |
| 3 | Benefit 10-20% AND Scope <= Low AND Severity <= Medium | CAUTION |
| 4 | Benefit >= 20% AND Scope = Medium AND Severity = High | CAUTION |
| 5 | Benefit >= 20% AND Scope = High AND Severity = Critical | CONDITIONAL |
| 6 | Benefit < 10% AND Severity >= High | DEFER |
| 7 | Risk includes Infrastructure Change AND infra not deployed | CONDITIONAL |
| 8 | Benefit < 5% AND Scope >= Medium | REJECT |
| 9 | Default | DEFER |

**Decision outcomes:**

- **RECOMMEND** -- create Jira task, standard process
- **CAUTION** (RECOMMEND WITH CAUTION) -- create Jira task + safeguards: feature flag for gradual rollout, regression testing for affected workflows, staging validation, rollback plan, rollback trigger (any Core Web Vital degrades >10% OR error rate >2%)
- **CONDITIONAL** -- document requirements, do NOT create task yet (prerequisites not met)
- **DEFER** -- document for future review, do NOT create task (risk > benefit currently)
- **REJECT** -- document reasoning, do NOT create task (risk far outweighs benefit)

Every decision must include transparent rationale based on this framework.

### Step 5.4 -- Document Impact Analysis

For each optimization, document: performance benefit (quantified), impact scope/severity, detection method + confidence, affected components and workflows, risk factors, decision + rationale, required safeguards (if CAUTION), prerequisites (if CONDITIONAL), conditions for reconsideration (if DEFER), alternatives (if REJECT).

**Impact calculation formulas (use as applicable):**
- Bundle size reduction: `size_reduction_kb / (bandwidth_mbps * 125) * 1000` ms
- N+1 fix: `(n_queries - 1) * db_latency_ms` (default 10ms)
- Deep service chain N+1: use effective query count from call graph
- Missing index: assume 80-95% reduction for affected query
- Wasted computation: `(wasted_fields / total_fields) * avg_service_latency_ms`
- Caching: `operation_time * cache_hit_rate`
- Over-fetching fix: `(unused_fields / total_fields) * response_size_kb`

Store all impact analysis data for Steps 5.5-9.

### Step 5.5 -- Database Migration Script Generation (New Migrations)

**Guard:** Runs when any RECOMMEND or CAUTION finding has anti-pattern type in: Missing Index, Sequential Scan, Nested Loop, Row Estimate Mismatch, Unused JOINs, Inefficient Queries, SQL Duplication. Key off anti-pattern type, not step numbers — covers findings from both static analysis (Steps 7.6, 7.6.1, 7.6.4, 7.6.5) and live analysis (Step 9.7.4).

**Skip when:** no database-related findings exist among RECOMMEND/CAUTION dispositions.

#### Step 5.5.1 -- Read CONVENTIONS.md

**Mandatory.** Read the target repository's `CONVENTIONS.md`. If CONVENTIONS.md is missing, halt with: "CONVENTIONS.md is required for database migration planning. Document migration patterns (naming, index naming, file structure, FK index policy) before proceeding."

Extract migration-related conventions: naming patterns, file structure, index naming, transaction handling, FK index policy, rollback requirements. Scan 2-3 existing migration files in the repository to validate conventions match practice.

Any migration pattern found in existing files but NOT documented in CONVENTIONS.md → flag as a recommended convention addition in the plan output.

#### Step 5.5.2 -- Detect Migration Framework

Read `repositories.backend.framework` from config. Map to migration tool and path pattern:

| Framework | Migration Tool | Path Pattern |
|---|---|---|
| Rust (SeaORM) | SeaORM Migration | `migration/src/m{YYYYMMDD}_{HHMMSS}_{name}.rs` |
| Rust (Diesel) | Diesel | `migrations/{date}_{name}/up.sql` + `down.sql` |
| Rust (sqlx) | sqlx migrate | `migrations/{timestamp}_{name}.sql` |
| Python (Django) | Django | `{app}/migrations/{NNNN}_{name}.py` |
| Python (SQLAlchemy) | Alembic | `alembic/versions/{rev}_{name}.py` |
| Java (Spring) | Flyway | `src/main/resources/db/migration/V{N}__{name}.sql` |
| Node (TypeORM) | TypeORM | `src/migration/{timestamp}-{name}.ts` |
| Node (Prisma) | Prisma | `prisma/migrations/{timestamp}_{name}/migration.sql` |

If the detected framework is not in the table, default to raw SQL migration files and document the limitation.

#### Step 5.5.3 -- Generate Manual Verification Artifacts

For each database finding, produce raw SQL artifacts the user can run directly against their database:

- **Before SQL** — the current query, with its EXPLAIN ANALYZE output if live analysis (Step 9.7) was performed
- **After SQL** — the optimized query for manual `EXPLAIN ANALYZE` verification
- **Migration up SQL** — the DDL change (e.g., `CREATE INDEX CONCURRENTLY ...` for production use)
- **Migration down SQL** — the rollback DDL (e.g., `DROP INDEX IF EXISTS ...`)

Manual verification SQL recommends `CREATE INDEX CONCURRENTLY` for production safety. Framework migration scripts (Step 5.5.4) do not use CONCURRENTLY because most migration runners wrap in transactions where CONCURRENTLY is invalid.

- **Storage impact queries** — for each migration, include before/after size queries so the user can measure storage cost:
  - Queries must show: total relation size, table data size, total index size, and per-index size breakdown.
  - Derive SQL dialect from the migration framework detected in Step 5.5.2 (e.g., PostgreSQL for SeaORM/Diesel/sqlx, MySQL for TypeORM with MySQL). Example for PostgreSQL: `pg_total_relation_size()`, `pg_relation_size()`, `pg_indexes_size()`, `pg_stat_user_indexes`.
  - If the finding's reason mentions the table was not found in migration files, prepend a warning: "Confirm table name before running — table not found in migration DDL."

#### Step 5.5.4 -- Generate Framework Migration Script

Produce the migration in the framework's idiomatic format, following CONVENTIONS.md patterns from Step 5.5.1. This is the source code that implement-task will write to the codebase.

Include before/after comments referencing the raw SQL from Step 5.5.3.

#### Step 5.5.5 -- Present to User

For each migration, present both layers:

1. **Manual verification block:** Before SQL + EXPLAIN output, After SQL, Migration up/down SQL (with CONCURRENTLY), and verification command (`EXPLAIN ANALYZE {optimized_query}`)
2. **Source code block:** Framework migration script that implement-task will apply
3. **Storage impact block:** Before/after size queries for the affected table(s)

#### Step 5.5.6 -- Safety Checks

Verify for each migration:
- No column drops or data loss operations (DELETE, TRUNCATE, ALTER COLUMN DROP)
- Rollback/down migration is non-destructive
- Migration follows CONVENTIONS.md patterns

### Step 5.6 -- Migration SQL Optimization Handling (Existing Migrations)

**Guard:** Runs when any RECOMMEND or CAUTION finding has anti-pattern type in: Missing Statistics Refresh, Non-Materialized CTE Re-evaluation, Uniform Processing of Partitionable Data, Expensive PL/pgSQL Function Pattern. Key off anti-pattern type — these come from analyze-module Steps 7.8.1-7.8.4.

**Skip when:** no migration-SQL-optimization findings exist among RECOMMEND/CAUTION dispositions.

**Key distinction from Step 5.5:** Step 5.5 generates NEW migration files (e.g., CREATE INDEX for a missing index). Step 5.6 generates patches to EXISTING migration files (e.g., adding ANALYZE before a backfill, materializing a CTE, rewriting a PL/pgSQL function). The implementation approach differs: Step 5.5 produces a complete new migration script; Step 5.6 produces before/after diffs of existing files.

#### Step 5.6.1 -- Read Existing Migration File

For each migration SQL optimization finding, locate and read the specific migration file containing the anti-pattern. The finding's `file` field from `findings-validation.json` provides the path. Verify the file exists and the evidence excerpt matches.

#### Step 5.6.2 -- Generate Fix Artifacts

For each finding, produce:

- **Before SQL** — the current migration code (exact excerpt from the file)
- **After SQL** — the corrected migration code with the anti-pattern resolved
- **Explanation** — why the change improves performance, with estimated impact
- **Verification SQL** — a runnable command to confirm the fix works

Fix patterns by anti-pattern type:

| Anti-Pattern | Fix Pattern | Verification |
|---|---|---|
| Missing Statistics Refresh | Insert `ANALYZE {table};` before the backfill DML | `EXPLAIN ANALYZE {backfill_query}` — verify planner row estimates are within 10x of actual |
| Non-Materialized CTE | Add `MATERIALIZED` keyword to CTE definition | `EXPLAIN {query}` — verify CTE appears as "CTE Scan" (not inlined) |
| Uniform Processing | Split query into two passes: one for rows matching the partition predicate (with JOIN + function), one for the rest (direct insert without JOIN/function) | Run both passes and verify combined result matches original single-pass result |
| Expensive PL/pgSQL Pattern | Replace `regexp_replace()` with boundary-aware `replace()` calls; eliminate per-row queries with batch operations | Timing comparison: `\timing` + `SELECT expand_fn_old(...)` vs `SELECT expand_fn_new(...)` on representative data |

#### Step 5.6.3 -- Safety Checks

Verify for each fix:
- Fix preserves the migration's semantic correctness (same data outcome after migration completes)
- Fix is idempotent if the migration is re-run (ON CONFLICT handling preserved)
- No data loss operations introduced
- For function rewrites: verify the new function produces identical output for all input patterns (boundary cases, edge cases, NULL handling)

## Step 6 -- Group Optimizations into Logical Tasks

Group only **RECOMMEND** and **CAUTION** optimizations into tasks. CONDITIONAL/DEFER/REJECT are documented in the plan but do NOT become Jira tasks.

**If all filtered out:** Create Epic with summary note, document deferred items, skip to Step 11.

### Task Grouping by Layer + Type

**Layer 1 -- Frontend:** 1A Bundle Size (splitting, tree shaking, lazy loading) | 1B Render (memoization, virtual scrolling, layout thrashing) | 1C Resource (async/defer scripts, parallel loading, image optimization)

**Layer 2 -- Backend** (when configured): 2A Query (N+1, deep chain N+1, pagination, indexes, query rewrites) | 2B Response (over-fetching, wasted computation, caching)

Database migration findings (Missing Index, Sequential Scan, Unused JOINs, Inefficient Queries, SQL Duplication) are grouped under Layer 2A with the `db-migration` label in addition to `performance-optimization`. Index-related findings go into one migration task; query rewrite findings go into a separate task. Each migration task includes the generated migration script (from Step 5.5.4) in Implementation Notes and the manual verification artifacts (from Step 5.5.3) in the Database Migration extension section.

Migration SQL optimization findings (Missing Statistics Refresh, Non-Materialized CTE Re-evaluation, Uniform Processing of Partitionable Data, Expensive PL/pgSQL Function Pattern) are grouped under Layer 2A with the `migration-sql-optimization` label in addition to `performance-optimization`. These are distinct from `db-migration` tasks — they fix EXISTING migration files rather than generating new ones. Group by migration file: findings in the same migration file go into one task. Each task includes the before/after SQL (from Step 5.6.2) in Implementation Notes and the verification commands in the Migration SQL Optimization extension section.

**Strategic materialization promotion:** When the analysis report's Strategic Optimizations section (S1, S2, ...) identifies a materialized view, denormalized table, or pre-computed column that would eliminate a join chain appearing in 2+ N+1/query findings (cross-reference by finding ID in the analysis report's prioritized findings table, e.g., F1, F2, ...), promote it to a **separate db-migration task** under Layer 2A with the `db-migration` label. The task description must include: the target table schema (columns, types, constraints), the source query being materialized, the migration script (up/down) generated via Step 5.5, and which findings it resolves (by ID). This task should be sequenced before the N+1 fix tasks that depend on it, since the materialized table simplifies those fixes.

**Layer 3 -- Integration:** 3A API Communication (batch calls, parallel fetching, client-side caching)

### Task Structure

Each task includes: summary ("{Category}: {Description}"), description, files to modify, baseline/target metrics, acceptance criteria, performance test requirements, dependencies.

### N+1 Loop Elimination Mandate

When a task addresses an N+1 or sequential-loop finding, the task's Implementation Notes MUST:

1. **Identify the outermost iteration boundary** — the specific loop (`for`/`while`/`.map`), its location (function, file, line), and the data source it iterates over. If `loop_origin` is present in the finding (from analyze-module Step 7.3), use it directly. If `loop_origin` is not available (older analysis runs), inspect the finding's code location and trace outward to the enclosing loop using Serena or Grep.
2. **State explicitly:** "This loop must be eliminated or replaced with a batch operation that processes all items together. Adding batch helpers inside the loop body while retaining the sequential loop is insufficient — it reduces per-iteration cost but preserves the O(N) sequential query pattern."
3. **Specify the batch entry point** — which function should accept all items at once and process them in bulk (e.g., "Replace `for matched in rows { resolve_sbom_cpe(matched, ...) }` with a single `batch_resolve_sbom_cpes(rows, ...)` call").

This ensures implement-task understands that the loop itself is the optimization target, not just the code inside it.

### Pre-Fetch Mandate for Concurrent Per-Item Queries

When a task addresses a `Pre-Fetchable Concurrent Queries` finding (from analyze-module Step 7.3.1), the task's Implementation Notes MUST:

1. **Identify the data accessed per-item** — which DB entities or queries are called inside the concurrent body, and what keys they use (e.g., `sbom_id`, `node_id`, `checksum_value`).
2. **Design a pre-fetch cache** — specify a cache struct that holds the pre-fetched data (e.g., `HashMap<(Uuid, String), Vec<Model>>`). The cache should be:
   - Built once before the concurrent processing starts (immutable after construction — no locks during concurrent reads)
   - Scoped to the request lifetime (dropped at end of request, no TTL management)
   - Populated via batch queries (1-3 queries total, not per-item)
3. **Specify the integration point** — where the pre-fetch call should be inserted (before the concurrent iteration starts), how the cache should be passed to the concurrent body (e.g., `Arc<Cache>` cloned per task), and how per-item code should use the cache (cache-first with DB fallback for cache misses).
4. **State explicitly:** "The per-item DB queries inside the concurrent iteration must be replaced with cache lookups. The concurrent structure itself (`buffer_unordered`, `Promise.all`, etc.) should be preserved — only the DB calls inside it should be eliminated."

### Query Restructuring Mandate

When a task addresses a `Cross-Table OR Filter` (7.6.7), `Load-All-Then-Search` (7.6.8), or `Inefficient Queries` (7.6) finding that involves decomposing a single query with cross-table OR/ILIKE conditions into per-entity queries, the task's Implementation Notes MUST:

1. **Document the original query pattern** — the single query with cross-table OR conditions, which tables are joined, and why the optimizer abandons indexes (e.g., OR across LEFT JOINed tables forces sequential scan).
2. **Specify the decomposed pattern** — how many per-entity branches, and what each branch's join/filter scope is (e.g., "node branch: base table only, no joins; cpe branch: base table → cpe_ref → cpe; purl branch: base table → purl_ref → qualified_purl").
3. **Define the result merging strategy** — for subquery paths: UNION DISTINCT via query builder folding; for materialized paths: in-application sort + dedup on the composite key.
4. **State the equivalence constraint explicitly:** "The decomposed queries MUST return the same result set as the original single query for both bare queries (e.g., `q=openssl`) and field-qualified queries (e.g., `q=name~openssl`). Field-qualified queries must route to the correct single branch without behavioral change. Verify equivalence with the repository's existing integration test harness."
5. **Specify edge case handling** — each branch applies the filter to its column set; branches whose columns do not match the query fields fail filter parsing and are silently excluded. When all branches fail, the original combined column set must be used to produce the user-facing error message. When at least one branch succeeds but returns zero rows, the result is empty (not an error).

### Migration SQL Fix Mandate

When a task addresses a migration SQL optimization finding (from analyze-module Steps 7.8.1-7.8.4), the task's Implementation Notes MUST:

1. **Identify the exact migration file and line range** — the specific `.sql` or `.rs` migration file, the DML statement(s) or function definition affected, and the line numbers from the analysis finding.
2. **Show before/after SQL** — the exact current code and the corrected code from Step 5.6.2. For PL/pgSQL function rewrites, show the complete function body before and after.
3. **State the deployment status constraint explicitly:** "This migration file may have already been applied to production databases. The fix must be delivered as a NEW migration file that corrects the data state and replaces the function definition, OR as a modification to the existing migration file if it has not yet been deployed. Confirm deployment status before implementation."
4. **Specify verification:** For Missing Statistics Refresh fixes, provide `EXPLAIN ANALYZE` commands to verify the planner uses correct row estimates after ANALYZE. For CTE materialization fixes, provide `EXPLAIN` to verify single CTE evaluation. For function rewrites, provide a timing comparison query (old function vs new function on representative data). For query splits, provide a result-equivalence check query.

### Task Sequencing

1. Quick wins first (low effort, high impact)
2. Dependencies (tasks that unblock others)
3. Risk (low-risk before high-risk)

## Step 7 -- Generate Optimization Plan Document

### Step 7.1 -- Location

Read plans directory from config `directories.plans`. Filename: `optimization-plan.md`.

### Step 7.2 -- Populate Template

Read the plan template from `$plugin_root/skills/performance/performance-plan.template.md` and populate with calculated values from Steps 5-6.

### Step 7.3 -- Calculate Expected Impact

Based on `metric_type`: sum estimated improvements across all optimizations, calculate percentage reduction, use conservative (lower bound) estimates. Summed impact is a rough upper bound — individual improvements are not necessarily additive. Present as "estimated up to X improvement" not "will save X."

### Step 7.4 -- Calculate Total Effort

Low = 0.5 day | Medium = 2 days | High = 5 days. Sum across all tasks.

### Step 7.5 -- Write Plan

Write to `{plans-directory}/optimization-plan.md`.

## Step 8 -- Create Jira Epic

### Step 8.1 -- Epic Content

**Summary:** `Performance Optimization: {workflow-name}`

**Description** includes: workflow name, current/target rating, executive summary (task count, total effort, expected impact by metric_type), risk profile (total evaluated, tasks created, deferred/rejected counts, risk distribution), task sequence list.

Footer: `_This Epic was AI-generated by sdlc-workflow/performance-plan-optimization v{version}._`

### Step 8.2 -- Create Epic via Jira

**Attempt MCP first:**

```
mcp__atlassian__createJiraIssue(
  project_key, summary, description, issue_type="Epic",
  labels=["ai-generated-jira", "performance-optimization", workflow-name]
)
```

**If MCP fails**, prompt user with standard fallback (see `shared/jira-access-strategy.md`):
1. Yes -- use REST API via `python3 "$plugin_root/scripts/jira-client.py" create_issue ...`
2. No -- skip Jira, save plan locally, skip to Step 11
3. Retry -- retry MCP once

### Step 8.3 -- Capture Epic Key

Store Epic key (e.g., `TC-5001`) for task creation and linking.

## Step 9 -- Create Jira Tasks

For each grouped task from Step 6:

### Step 9.1 -- Task Description

Read the task template from `$plugin_root/skills/performance/optimization-task.template.md` and populate with: repository, description, files to modify, baseline/target metrics (by metric_type), implementation notes, cross-functional impact assessment (decision, scope, severity, detection method, confidence, affected workflows/components, risk factors, safeguards if CAUTION, testing requirements), acceptance criteria, performance test requirements, dependencies.

**Query safety constraints from CONVENTIONS.md:** When generating Implementation Notes for tasks that involve batch queries or dynamic SQL, search the target repository's `CONVENTIONS.md` for documented query safety patterns:
- Parameter limit handling (e.g., PostgreSQL's 65535 bind parameter limit)
- Chunking utilities (e.g., `chunked_with`, `batch_execute`)
- Preferred SQL patterns for bulk operations (e.g., `UNNEST` arrays vs inline `VALUES` clauses vs `Condition::any()` chains)

If CONVENTIONS.md documents a utility for parameter-safe batching (e.g., `trustify_common::db::chunk::chunked_with`), reference it by path in the Implementation Notes and state: "All batch queries MUST use `{utility}` or an equivalent parameter-safe pattern. Do not generate unbounded parameter lists (inline `VALUES` with 2*N params or `Condition::any()` with N compound filters) — these will hit PostgreSQL's 65535 parameter limit at scale."

**Target Metrics scoping:** When populating the Target Metrics section of each task, include ONLY the metrics that the specific optimization is expected to affect:
- Bundle size tasks: only frontend size metrics (bundle size, transfer size)
- N+1 query tasks: only backend response time metrics (p95, p99)
- Render optimization tasks: only DOM Interactive, LCP
- Cross-layer tasks: both frontend and backend metrics

Do NOT copy all workflow-level metrics into every task.

**Unit conversion:** `optimization_targets` stores frontend metrics in seconds; reports and Jira tasks use milliseconds. Multiply by 1000 when populating task Baseline/Target Metrics from config values.

### Step 9.2 -- Create Task via Jira

**MCP first**, same fallback flow as Epic (Step 8.2).

```
mcp__atlassian__createJiraIssue(
  project_key, summary, description, issue_type="Task",
  labels=["ai-generated-jira", "performance-optimization", workflow-name, layer, category]
)
```

**Labels:** layer = "frontend" | "backend" | "integration". Category = "bundle-size" | "render-optimization" | "resource-optimization" | "query-optimization" | "response-optimization" | "api-communication" | "db-migration" | "migration-sql-optimization".

For `db-migration` tasks: include both `performance-optimization` and `db-migration` labels. The `performance-optimization` label maintains Epic grouping; the `db-migration` label enables task type detection in implement-task and verify-pr.

For `migration-sql-optimization` tasks: include both `performance-optimization` and `migration-sql-optimization` labels. The `performance-optimization` label maintains Epic grouping; the `migration-sql-optimization` label distinguishes "fix existing migration SQL" from "create new migration" (`db-migration`). These tasks fix performance anti-patterns in existing migration files (backfill queries, PL/pgSQL functions) rather than generating new DDL migrations.

### Step 9.3 -- Set Epic as Parent

Set Epic as parent using Jira hierarchy (not issue links):

**At creation time (preferred):** pass `parent=<epic-key>` in `createJiraIssue`.

**After creation (fallback):** `mcp__atlassian__editJiraIssue(issue_key, fields={"parent": {"key": epic-key}})`.

**REST fallback:** `python3 "$plugin_root/scripts/jira-client.py" update_issue {task-key} --fields-json '{"parent": {"key": "{epic-key}"}}'`

**Legacy Jira:** fall back to `customfield_10014` (Epic Link) if parent field unsupported.

### Step 9.4 -- Link Task Dependencies

For tasks with dependencies, create "Blocks" links:

```
mcp__atlassian__createIssueLink(inward=prerequisite-key, outward=dependent-key, type="Blocks")
```

REST fallback: `python3 "$plugin_root/scripts/jira-client.py" create_link --inward {key} --outward {key} --link-type "Blocks"`

## Step 10 -- Post Plan as Epic Comment

Read `{plans-directory}/optimization-plan.md` and post as comment on the Epic.

**MCP:** `mcp__atlassian__addCommentToJiraIssue(epic-key, plan-content)`

**REST fallback:** `python3 "$plugin_root/scripts/jira-client.py" add_comment {epic-key} --comment-md "{content}"`

Append footer: `_This comment was AI-generated by sdlc-workflow/performance-plan-optimization v{version}._`

## Step 11 -- Output Summary

Report to the user:

> **Optimization plan created successfully!**
>
> **Workflow:** {workflow-name}
> **Expected Impact:** {metric improvements by metric_type}
> **Plan:** `performance/plans/optimization-plan.md`
> **Epic:** {epic-key} -- "Performance Optimization: {workflow-name}"
> **Tasks:** {task-count} tasks (list each key + summary)
> **Effort:** {total-effort-days} days
>
> **Next Steps:**
> 1. Review plan and tasks with your team
> 2. Implement: `/sdlc-workflow:implement-task {task-key}` (performance sections auto-detected)
> 3. After each task's PR merges to the target branch, re-baseline on the target branch: `/sdlc-workflow:performance-baseline`

If Jira was skipped, adjust: note plan saved locally, Jira not created.

> ⚠️ **Before implementing:** Ensure CONVENTIONS.md exists in the target repository with CI check commands and performance test commands. implement-task will halt without it.

## Important Rules

- Never modify source code -- only planning artifacts and Jira issues
- Always verify analysis report exists before proceeding
- Group optimizations into logical tasks with clear boundaries (not one task per finding)
- Task sequencing must follow dependencies (quick wins first)
- All Jira issues include `ai-generated-jira` label
- Use conservative effort estimates (upper bound)
- Impact analysis (Step 5) is mandatory before task grouping
- Use Serena MCP first for code analysis, Grep fallback; always document which method used
- Only RECOMMEND and CAUTION become Jira tasks; CONDITIONAL/DEFER/REJECT documented in plan with rationale
- If all optimizations deferred/rejected, create Epic with summary, document in plan
- If impact analysis fails for an optimization, default to DEFER with "Manual review required"
- Deferred/rejected optimizations must include conditions for reconsideration
