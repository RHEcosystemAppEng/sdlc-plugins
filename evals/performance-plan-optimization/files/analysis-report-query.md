<!-- SYNTHETIC TEST DATA — DO NOT USE IN PRODUCTION -->

# Performance Analysis Report

**Generated:** 2026-06-15T12:00:00Z
**Workflow:** component-search
**Baseline Date:** 2026-06-15T10:00:00Z
**Validation Artifact:** `performance/analysis/findings-validation.json`
**Validation Status:** passed

---

## Workflow Metrics

| Metric | Current (p95) | Target | Status |
|---|---|---|---|
| Response Time (p95) | 35000 ms | 2000 ms | Poor |
| Response Time (p99) | 60000 ms | 5000 ms | Poor |
| Throughput | 2 req/s | 50 req/s | Poor |
| Error Rate | 0.5% | 0.1% | Needs Improvement |
| DB Query Time (p95) | 30000 ms | 1000 ms | Poor |

---

## Finding Validation Summary

**Validation Step:** Step 9.1 re-verified all findings against source code before report generation.

| # | Finding | Anti-Pattern | Step | Disposition | Confidence | Severity | Timeline | Notes |
|---|---|---|---|---|---|---|---|---|
| F1 | Cross-table OR filter defeats GIN index on sbom_node.name | Cross-Table OR Filter | 7.6.7 | Confirmed | High | High | 1-3 days | Bare-value filter generates ILIKE OR across 3 LEFT JOINed entities |
| F2 | Pagination applied after loading all results into memory | Late Pagination | 7.4.1 | Confirmed | High | High | 1-3 days | paginate_array() after full materialization |
| F3 | Unbounded loop with 2 DB queries per iteration | Unbounded Query-Driving Iteration | 7.3.2 | Confirmed | High | High | 1-3 days | No size guard on query result, 2N queries |
| F4 | Duplicate btree index on sbom_node(sbom_id, node_id) | Redundant Database Indexes | 7.6.4.1 | Confirmed | High | Medium | 1-4 hours | 52 GB redundant index identical to PK |
| F5 | Recursive CTE on 383M-row junction table with depth 50 | Recursive CTE Risk | 7.6.2 | Downgraded | Medium | Medium | 1-3 days | Depth limit exists but generous |

**Validation Statistics:**
- Findings submitted: 5
- Confirmed: 4 (80%)
- Confirmed (Low Confidence): 0 (0%)
- Downgraded: 1 (20%)
- Discarded: 0 (0%)

---

## Anti-Pattern Analysis

### Cross-Table OR Filter

**Severity:** High
**Confidence:** High (Grep — ORM filter composition analysis)
**Instances Found:** 1
**Estimated Impact:** Estimated overhead: High — cross-table OR on LEFT JOINed tables typically forces sequential scan, defeating indexes. Actual impact depends on table sizes (verify with EXPLAIN).

**Description:**
The search handler registers columns from three entities (sbom_node, cpe, qualified_purl) via `q_columns()` and applies a bare-value filter via `filtering_with()`. When `q=openssl` is used without a field qualifier, the filter generates ILIKE OR conditions across ALL string columns from ALL registered entities, including LEFT JOINed tables. PostgreSQL abandons the 12 GB GIN trigram index on `sbom_node.name` because OR spans LEFT JOINed entities, falling back to sequential scans of `sbom_node` (38 GB) and `sbom_package` (31 GB).

**Detected Instances:**

1. **src/handlers/search.rs:31**
   **Finding ID:** F1
   ```rust
   let search_subquery = sbom_node::Entity::find()
       .join(JoinType::Join, sbom_node::Relation::Package.def())
       .join(JoinType::LeftJoin, sbom_package::Relation::Purl.def())
       .join(JoinType::LeftJoin, sbom_package::Relation::Cpe.def())
       .join(JoinType::LeftJoin, sbom_package_cpe_ref::Relation::Cpe.def())
       .join(JoinType::LeftJoin, sbom_package_purl_ref::Relation::Purl.def())
       .select_only()
       .column(sbom_node::Column::SbomId)
       .filtering_with(query.q.clone(), q_columns())?
       .distinct()
       .into_query();
   ```
   **Issue:** `q_columns()` registers columns from sbom_node + cpe + qualified_purl. Bare `q=openssl` produces: `WHERE sbom_node.name ILIKE '%openssl%' OR cpe.vendor ILIKE '%openssl%' OR cpe.product ILIKE '%openssl%' OR ...` across LEFT JOINed tables. Optimizer cannot use GIN index when OR includes columns from different tables.
   **Recommended Fix:** Split into per-entity queries — one per column set (sbom_node, cpe, qualified_purl) — each using its optimal index. Merge results via UNION DISTINCT or in-application dedup.
   **Verification Checklist:**
   - [ ] Verify split queries return same result set as original
   - [ ] Verify EXPLAIN shows index scan (not seq scan) after fix
   **Validation Status:** Confirmed
   **Confidence:** High
   **Severity:** High
   **Timeline:** 1-3 days

---

### Late Pagination

**Severity:** High
**Confidence:** High (Grep — pagination flow analysis)
**Instances Found:** 1
**Estimated Impact:** Estimated up to 90% reduction in memory usage and response time for paginated requests

**Description:**
The component listing endpoint accepts pagination parameters (offset, limit) but applies them via `paginate_array()` after loading and enriching ALL components into memory. All rows are fetched, per-row queries executed, and results collected before slicing to the requested page.

**Detected Instances:**

1. **src/handlers/components.rs:52**
   **Finding ID:** F2
   ```rust
   let result = paginate_array(&enriched, paginated.offset, paginated.limit);
   ```
   **Issue:** Pagination applied post-load. All components loaded and enriched (2 queries per component) before slicing.
   **Recommended Fix:** Push LIMIT/OFFSET into the initial query. Load only the requested page of components before enrichment.
   **Validation Status:** Confirmed
   **Confidence:** High
   **Severity:** High
   **Timeline:** 1-3 days

---

### Unbounded Query-Driving Iteration

**Severity:** High
**Confidence:** High (Grep — loop and query analysis)
**Instances Found:** 1
**Estimated Impact:** N x 20ms per request, where N is unbounded (could be thousands)

**Description:**
The component listing handler loads all active components without a size guard and iterates each one, executing 2 DB queries per iteration (detail lookup + vendor filter).

**Detected Instances:**

1. **src/handlers/components.rs:32**
   **Finding ID:** F3
   ```rust
   for component in &all_components {
       let details = component_detail::Entity::find_by_id(component.id)
           .one(db.get_ref()).await?;
       let vendors = vendor::Entity::find()
           .filter(vendor::Column::ComponentId.eq(component.id))
           .all(db.get_ref()).await?;
       // ...
   }
   ```
   **Loop Source:** `component::Entity::find().filter(...).all(db)` — unbounded query result
   **Guard Check:** absent — no `.take(N)` or `if len > MAX`
   **Query Count Per Iteration:** 2
   **Recommended Fix:** Add a size guard and batch the per-item queries.
   **Validation Status:** Confirmed
   **Confidence:** High
   **Severity:** High
   **Timeline:** 1-3 days

---

### Redundant Database Indexes

**Severity:** Medium
**Confidence:** High (Grep — migration file analysis)
**Instances Found:** 1
**Estimated Impact:** 52 GB disk savings, improved buffer cache efficiency

**Description:**
The `sbom_node` table has a btree index `idx_sbom_node_sbom_id_node_id` on `(sbom_id, node_id)` that is identical to the primary key `sbom_node_pkey` on the same columns. The duplicate wastes 52 GB of disk and competes for buffer cache space.

**Detected Instances:**

1. **Table:** `sbom_node`
   **Duplicate Index:** `idx_sbom_node_sbom_id_node_id (sbom_id, node_id)`
   **Primary Key:** `sbom_node_pkey (sbom_id, node_id)`
   **Index Source:** `migration/m002_add_indexes.rs:8`
   **Finding ID:** F4
   **Estimated Impact:** 52 GB disk savings
   **Recommended Fix:**
   ```sql
   DROP INDEX IF EXISTS idx_sbom_node_sbom_id_node_id;
   ```
   **Validation Status:** Confirmed
   **Confidence:** High
   **Severity:** Medium
   **Timeline:** 1-4 hours

---

## Backend Source Code Analysis

**Backend Repository:** analysis-api (actix-web)
**Analysis Coverage:** 2 endpoints analyzed
**Serena Status:** Grep fallback

### Backend Anti-Patterns Detected

See findings F1–F5 above for all backend anti-patterns.

### Recursive CTE Risk

**Severity:** Medium
**Confidence:** Medium (Grep — SQL analysis)
**Instances Found:** 1
**Estimated Impact:** Scale risk — performance degrades proportionally with table size

**Description:**
A recursive CTE walks the `item_relates_to_item` junction table (383M rows) for ancestor resolution. Depth limit is 50, which prevents runaway recursion but is generous for a junction table where each level can fan out significantly.

**Detected Instances:**

1. **src/handlers/ancestor_walker.rs:15**
   **Finding ID:** F5
   ```sql
   WITH RECURSIVE ancestors AS (
       SELECT child_id, parent_id, 1 AS depth
       FROM item_relates_to_item WHERE child_id = $1
       UNION ALL
       SELECT r.child_id, r.parent_id, a.depth + 1
       FROM item_relates_to_item r JOIN ancestors a ON r.child_id = a.parent_id
       WHERE a.depth < 50
   )
   SELECT * FROM ancestors;
   ```
   **Target Table:** `item_relates_to_item` (junction, 383M rows)
   **Depth Limit:** 50
   **Table Pattern:** junction
   **Recommended Fix:** Reduce depth limit to 10-20, or pre-compute transitive closure for hot paths.
   **Validation Status:** Downgraded (from High to Medium — depth limit exists)
   **Confidence:** Medium
   **Severity:** Medium
   **Timeline:** 1-3 days

---

## Recommended Optimizations

### Tactical Optimizations

| Priority | Optimization | Confidence | Severity | Timeline | Prerequisite | Estimated Impact | Effort |
|---|---|---|---|---|---|---|---|
| 1 | F1: Split cross-table OR into per-entity queries | High | High | 1-3 days | None | Eliminates 69 GB sequential scan | High |
| 2 | F2: Push pagination into SQL query | High | High | 1-3 days | F3 | Estimated up to 90% memory reduction | Medium |
| 3 | F3: Add size guard and batch per-item queries | High | High | 1-3 days | None | Eliminates 2N sequential queries | Medium |
| 4 | F4: Drop redundant index | High | Medium | 1-4 hours | None | 52 GB disk + buffer cache savings | Low |
| 5 | F5: Reduce recursive CTE depth limit | Medium | Medium | 1-3 days | None | Scale risk mitigation | Medium |

### Strategic / Architectural Optimizations

No strategic optimizations identified — tactical fixes address the primary bottlenecks.

---

## Executive Summary

**Overall Performance Rating:** Poor

**Key Findings:**
- Cross-table OR filter defeats GIN trigram index, forcing 69 GB sequential scan on bare queries
- Pagination applied after full materialization — all rows loaded and enriched before slicing
- Unbounded iteration executes 2N DB queries with no size guard
- Redundant 52 GB index wastes buffer cache space

**Top 3 Optimization Opportunities:**
1. Cross-Table OR fix (F1) — eliminates 69 GB sequential scan per bare query
2. Late Pagination fix (F2) — estimated up to 90% memory reduction
3. Unbounded Iteration fix (F3) — eliminates 2N sequential query pattern

---

## Next Steps

1. Review this report with the team and prioritize optimizations
2. Create optimization plan and Jira Epic/Tasks using `/sdlc-workflow:performance-plan-optimization`
3. After implementing optimizations, re-run `/sdlc-workflow:performance-baseline` to capture new baseline and measure improvements
