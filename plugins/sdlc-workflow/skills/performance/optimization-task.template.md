# Performance Optimization Task Template

This template extends the base `task-description-template.md` with performance-specific sections.

## Template

```
## Repository
<repository-name>

## Description
<What optimization this task achieves and why>

## Baseline Metrics

Current performance metrics before optimization (from baseline-report.md):

| Metric | Current (Baseline) | Unit |
|---|---|---|
| LCP (Largest Contentful Paint) | {baseline-lcp} | ms |
| FCP (First Contentful Paint) | {baseline-fcp} | ms |
| DOM Interactive (Time to Interactive) | {baseline-domInteractive} | ms |
| Total Load Time | {baseline-total} | ms |
(if analyze Step 5 produced bundle stats)
| Bundle Size | {baseline-bundle-size} | KB |
(end if)
(if metric-type is "backend" or "hybrid")
| Response Time (p95) | {baseline-response-time-p95} | ms |
| Throughput | {baseline-throughput} | req/s |
| Error Rate | {baseline-error-rate} | % |
| DB Query Time (p95) | {baseline-db-query-time-p95} | ms |
(end if)

## Target Metrics

Performance targets to achieve with this optimization:

| Metric | Target | Improvement | Unit |
|---|---|---|---|
| LCP (Largest Contentful Paint) | {target-lcp} | {lcp-improvement}% | ms |
| FCP (First Contentful Paint) | {target-fcp} | {fcp-improvement}% | ms |
| DOM Interactive (Time to Interactive) | {target-domInteractive} | {domInteractive-improvement}% | ms |
| Total Load Time | {target-total} | {total-improvement}% | ms |
(if analyze Step 5 produced bundle stats)
| Bundle Size | {target-bundle-size} | {bundle-improvement}% | KB |
(end if)
(if metric-type is "backend" or "hybrid")
| Response Time (p95) | {target-response-time-p95} | {response-time-improvement}% | ms |
| Throughput | {target-throughput} | {throughput-improvement}% | req/s |
| Error Rate | {target-error-rate} | {error-rate-improvement}% | % |
| DB Query Time (p95) | {target-db-query-time-p95} | {db-query-time-improvement}% | ms |
(end if)

## Files to Modify
- `path/to/file.ext` — <brief reason>

## Files to Create
- `path/to/new_file.ext` — <purpose>

## API Changes
- `GET /v2/endpoint` — NEW: <description>
- `PUT /v2/endpoint/{id}` — MODIFY: <what changes in request/response>

## Implementation Notes
<Specific guidance: patterns to follow, existing code to reuse,
key functions/structs/components to interact with.
Reference actual file paths and symbol names found during repository analysis.>

## Reuse Candidates
- `path/to/file.ext::symbol_name` — <what it does and how it relates to this task>

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Target metrics achieved (LCP ≤ {target-lcp}ms, FCP ≤ {target-fcp}ms)
- [ ] No performance regressions in non-target scenarios (< 5% degradation)

## Test Requirements
- [ ] Functional test description 1
- [ ] Functional test description 2

## Performance Test Requirements

- [ ] Re-run baseline capture for ALL scenarios (not just affected ones)
- [ ] Verify target scenario meets target metrics
- [ ] Verify non-target scenarios have no regressions (< 5% degradation in LCP, FCP, DOM Interactive, Total Load Time)
- [ ] Generate before/after comparison report
- [ ] If regression detected in non-target scenarios, prompt user for approval before committing

## Verification Commands
- `<command>` — <expected outcome>
- `node capture-baseline.mjs --config performance-config.json` — Should show improved metrics for target scenario

## Documentation Updates
- `path/to/doc.md` — <what content to add or revise>

## Dependencies
- Depends on: Task N — <task title> (if any)
```

## Database Migration Extension

When the task involves database migrations (Layer 2A with `db-migration` label), add these sections after Performance Test Requirements:

```
## Database Migration

### Migration Framework
{framework_name} (e.g., SeaORM Migration, Alembic, Flyway, TypeORM)

### Before/After SQL (Manual Verification)

#### Before (Current Query)
```sql
{original_query}
```

#### Before EXPLAIN (if live analysis was performed)
```
{explain_output_before}
```

#### After (Optimized Query)
```sql
{optimized_query}
```

### Migration Up/Down SQL (Manual Verification)

#### Up (Apply)
```sql
{migration_up_sql — e.g., CREATE INDEX CONCURRENTLY idx_table_col ON table(col);}
```

#### Down (Rollback)
```sql
{migration_down_sql — e.g., DROP INDEX IF EXISTS idx_table_col;}
```

**Note:** Manual verification SQL uses `CONCURRENTLY` for production safety. Framework migration scripts below do not, because most migration runners wrap in transactions where `CONCURRENTLY` is invalid.

### Migration Script (Source Code)

The framework-idiomatic migration that implement-task will write to the codebase:

```{language}
{generated_migration_code — e.g., SeaORM Migration struct, Alembic revision, Flyway SQL file}
```

### Safety Checks
- [ ] No column drops or data loss operations
- [ ] Rollback/down migration is non-destructive
- [ ] Migration follows CONVENTIONS.md patterns

### Manual Verification

Run against your database to verify improvement:
```sql
EXPLAIN ANALYZE {optimized_query};
```
Compare execution time with the Before EXPLAIN output above.

### Storage Impact

Before/after size queries for the affected table(s), dialect derived from Migration Framework.
```

## Database Migration Extension Rules

- **Migration Script** section is required for `db-migration` tasks
- **Before/After SQL** must show the exact SQL change for manual verification
- **Migration Up/Down SQL** must be runnable directly against the database
- **Rollback/Down** must be provided for every migration
- **Safety Checks** must be pre-verified before task creation (plan-optimization Step 5.5.6)
- **Manual Verification** command must be runnable directly by the developer
- Migration scripts must follow CONVENTIONS.md patterns. If CONVENTIONS.md documents migration naming, index naming, or file structure conventions, the script must match exactly
- **Storage Impact** is always included with before/after size queries for the affected table(s)

---

## Migration SQL Optimization Extension

When the task involves fixing existing migration SQL (Layer 2A with `migration-sql-optimization` label), add these sections after Performance Test Requirements:

```
## Migration SQL Fix

### Target Migration File
{migration_file_path} (line {start_line}–{end_line})

### Deployment Status
**CONFIRM BEFORE IMPLEMENTING:** Has this migration been applied to production/staging databases?
- If YES: Create a NEW corrective migration file that applies the optimized SQL (e.g., re-runs the backfill with the fix, replaces the function definition)
- If NO: Modify the existing migration file directly

### Before (Current Migration SQL)
```sql
{original_migration_sql}
```

### After (Corrected Migration SQL)
```sql
{corrected_migration_sql}
```

### Performance Impact
{explanation_of_improvement — e.g., "Adding ANALYZE before the backfill fixes a 170x row overestimate, reducing query plan cost from ~1.8B to ~21M"}

### Verification
```sql
{verification_query — e.g., EXPLAIN ANALYZE for planner estimates, timing comparison for function rewrites}
```

### Safety Checks
- [ ] Fix preserves semantic correctness (same data outcome after migration)
- [ ] Fix is idempotent if migration re-runs (ON CONFLICT handling preserved)
- [ ] No data loss operations introduced
- [ ] For function rewrites: new function produces identical output for all input patterns
```

## Migration SQL Optimization Extension Rules

- **Target Migration File** must point to the exact file and line range from the analysis finding
- **Deployment Status** check is mandatory — determines whether to modify existing migration or create a new corrective migration
- **Before/After SQL** must show the complete affected code section, not just a snippet
- **Verification** must include a runnable command the developer can use to confirm the fix
- Migration SQL optimization tasks are distinct from `db-migration` tasks (which create new DDL migrations)
- For PL/pgSQL function rewrites: the Before/After must show the complete function body, and verification must include a correctness check (both functions produce identical output) in addition to a timing comparison

---

## Rules

Follows all base template rules (from `shared/task-description-template.md`), plus:

- **Baseline Metrics** section is required — must reference actual baseline data
- **Target Metrics** section is required — targets must be realistic and measurable
- **Performance Test Requirements** section is required — defines regression testing criteria
- Omit non-applicable sections (API Changes, Files to Create, Documentation Updates, etc.) as per base template rules
- Target metrics should follow Google's Core Web Vitals "Good" thresholds unless application-specific requirements dictate otherwise:
  - LCP: ≤ 2.5s
  - FCP: ≤ 1.8s
  - DOM Interactive: ≤ 3.5s
- Improvement percentages help communicate expected impact clearly
- For query decomposition tasks (Cross-Table OR Filter, Load-All-Then-Search, or Inefficient Queries findings involving query splitting), **Test Requirements** MUST include equivalence tests (decomposed queries return the same result set as the original) and edge case tests (single-branch success, all-branch error path, cross-branch dedup)
