# Performance Analysis Report

**Generated:** {iso-8601-timestamp}  
**Workflow:** {workflow-name}  
**Baseline Date:** {baseline-capture-date}

---

## Executive Summary

**Overall Performance Rating:** {rating} (Excellent / Good / Needs Improvement / Poor)

**Key Findings:**
- {summary-bullet-1}
- {summary-bullet-2}
- {summary-bullet-3}

**Top 3 Optimization Opportunities:**
1. {opportunity-1} — Estimated impact: {impact-1}
2. {opportunity-2} — Estimated impact: {impact-2}
3. {opportunity-3} — Estimated impact: {impact-3}

---

## Workflow Metrics

| Metric | Current (p95) | Target | Status |
|---|---|---|---|
| LCP (Largest Contentful Paint) | {lcp-p95} ms | 2500 ms | {status} |
| FCP (First Contentful Paint) | {fcp-p95} ms | 1800 ms | {status} |
| DOM Interactive | {domInteractive-p95} ms | 3500 ms | {status} |
| Total Load Time | {total-p95} ms | 4000 ms | {status} |

---

## Bundle Composition

**Total JavaScript Size:** {total-js-size} KB  
**Third-Party Libraries:** {third-party-size} KB ({third-party-percentage}%)  
**Application Code:** {application-code-size} KB ({application-code-percentage}%)

**Top Third-Party Libraries by Size:**

| Library | Size | Used In |
|---|---|---|
| {library-1} | {size-1} KB | {scenarios-1} |
| {library-2} | {size-2} KB | {scenarios-2} |
| ... | ... | ... |

---

## Anti-Pattern Analysis

### {Anti-Pattern-Name}

**Severity:** {High / Medium / Low}  
**Confidence:** {High (Serena MCP) / Medium (Grep — good pattern) / Low (Grep — requires manual verification)}  
**Instances Found:** {count}  
**Estimated Impact:** {quantified-impact}

**Description:**
{brief-explanation-of-anti-pattern}

**Detected Instances:**

1. **{file-path}:{line-number}**
   ```{language}
   {code-snippet}
   ```
   **Issue:** {specific-issue-description}
   **Recommended Fix:** {actionable-recommendation}
   **Verification Checklist:**
   - [ ] {verification-step-1 from detection step}
   - [ ] {verification-step-2 from detection step}

{... repeat for each anti-pattern ...}

---

## Backend Source Code Analysis

**Note:** This section is included only if backend repository is configured (`backend_available = true`). Otherwise, omit this section entirely.

**Backend Repository:** {backend-repo-name} ({backend-framework})  
**Analysis Coverage:** {endpoints-analyzed} endpoints analyzed  
**Serena Status:** {serena-instance-name or "Grep fallback"}

### Backend Anti-Patterns Detected

#### Database N+1 Queries

**Severity:** {High / Medium / Low}  
**Instances Found:** {count}  
**Estimated Latency Impact:** {(n_queries - 1) * 10ms}

**Detected Instances:**

1. **{handler-file-path}:{line-number}**
   ```{language}
   {code-snippet-showing-loop-with-queries}
   ```
   **Issue:** {count} queries executed sequentially in loop  
   **Recommended Fix:**
   - **SQL:** Use batch query: `SELECT * FROM table WHERE id IN (...)`
   - **SeaORM:** Use `.find()` with `filter(column.is_in(ids))` or `.find_with_related()` for eager loading
   - **Diesel:** Use `.filter(id.eq_any(ids))` for batch query
   - **JPA/Hibernate:** Use `@EntityGraph`, `JOIN FETCH` in JPQL, or `findAllById(ids)`
   - **SQLAlchemy:** Use `.filter(Model.id.in_(ids))` for batch query
   - **Django ORM:** Use `Model.objects.filter(id__in=ids)` or `.select_related()`

{... repeat for each N+1 instance ...}

#### Missing Pagination

**Severity:** {High / Medium / Low}  
**Instances Found:** {count}  
**Estimated Payload Waste:** {(total_items - 20) * avg_item_size}

**Detected Instances:**

1. **Endpoint:** GET {endpoint-path}
   **Handler:** {handler-file-path}  
   **Issue:** Returns {item-count} items without pagination  
   **Recommended Fix:** Add `page` and `limit` query parameters, implement `.limit()` and `.offset()` in query

{... repeat for each pagination issue ...}

#### Missing Caching

**Severity:** {High / Medium / Low}  
**Instances Found:** {count}  
**Estimated Latency Reduction:** {operation_time × analysis_cache_hit_rate}

**Detected Instances:**

1. **Endpoint:** GET {endpoint-path}
   **Handler:** {handler-file-path}  
   **Issue:** {expensive-operation-description} on every request (no cache detected)  
   **Data Change Frequency:** {static / slow-changing / fast-changing}  
   **Recommended Fix:** Implement cache layer (Redis, in-memory) with appropriate TTL

{... repeat for each caching issue ...}

#### Inefficient Queries

**Severity:** {High / Medium / Low}  
**Instances Found:** {count}  
**Estimated Impact:** 30-50% query time reduction

**Detected Instances:**

1. **Query:** {query-snippet}
   **Handler:** {handler-file-path}:{line-number}  
   **Issue:** SELECT * fetches {column-count} columns but only {used-count} used in response  
   **Recommended Fix:** Specify exact columns: `SELECT id, name, price FROM products WHERE ...`

{... repeat for each inefficient query ...}

#### Unused Table Joins

**Severity:** {Critical / High / Medium / Low}  
**Instances Found:** {count}  
**Estimated Impact:** {total_latency_saved}ms saved per request

**Description:** Database queries that JOIN tables but never access fields from the joined tables, wasting database CPU, I/O, and memory resources.

**Detected Instances:**

1. **Endpoint:** {endpoint_method} {endpoint_path}
   **Handler:** {handler-file-path}:{line-number}  
   **Query:**
   ```{language}
   {full_query_with_highlighted_join}
   ```
   **Unused Join:** `{joined_table}` (alias: `{alias}`)  
   **Reason:** No fields from `{joined_table}` accessed in SELECT, WHERE, or response schema  
   **Join Type:** {INNER/LEFT/RIGHT JOIN}  
   **Table Size:** {estimated_row_count} rows  
   **Index Status:** {Indexed/Not Indexed} on foreign key  
   **Estimated Overhead:** {overhead_ms}ms per query  
   **Call Frequency:** {single/N+1 with count calls}  
   **Total Impact:** {total_impact}ms per request  
   **Recommended Fix:**
   ```{language}
   {optimized_query_without_unused_join}
   ```

{... repeat for each unused join instance ...}

**Total Estimated Impact:** {sum_of_all_impacts}ms reduction across {count} endpoints

### Cross-Repository Over-Fetching Analysis

**Note:** This analysis cross-references backend response schemas with frontend field usage.

#### Per-Endpoint Analysis

##### Endpoint: GET {endpoint-path}

**Backend Handler:** {handler-file-path}  
**Response Type:** {ResponseStructName}  
**Total Fields:** {total-field-count}  
**Used by Frontend:** {used-field-count}  
**Unused Fields:** {unused-field-list}  
**Over-Fetching Percentage:** {waste-percentage}%  
**Call Pattern:** {Single call / N+1 (count calls)}  
**Payload Waste:** {waste-bytes} KB per request × {call-count if N+1} calls = {total-waste} KB  
**Recommendation:** {Create specialized DTO / Use GraphQL / Field projection}

{... repeat for each endpoint ...}

---

## Dynamic Performance Testing

**Note:** This section is included only if dynamic testing was executed (backend running + test data manifest exists).

**Status:** Service running on localhost:{port}  
**Methodology:** curl loop — cold-cache first request + {iterations} warm-cache requests for p50/p95/p99 percentiles  
**Iterations:** {iterations} requests per endpoint

### Endpoint Performance Metrics

{... for each endpoint in dynamic_results ...}

#### Endpoint: {endpoint_method} {endpoint_path}

**Test URL:** {test_url}

**Response Time (milliseconds)**:
| Metric | Value |
|---|---|
| p50 (Median) | {p50}ms |
| p95 | {p95}ms |
| p99 | {p99}ms |
| Mean | {mean}ms |

**Cache Effectiveness**:
- First request: {first_request_ms}ms (cache miss)
- Subsequent mean: {mean}ms (cache hits)
- Improvement: {cache_improvement_pct}% faster
- **Status**: {cache_status} ✅/⚠️

**Dynamic vs Static Comparison**:
| Source | Estimate | Notes |
|---|---|---|
| Static Analysis | **[Manual: See Backend Source Code Analysis section]** | Check N+1 query findings, estimated overhead |
| Dynamic Actual | {p95}ms (p95) | Measured with curl loop |
| Variance | **[Manual: Calculate]** | If >200ms: Database profiling needed |

**Recommendation**: Review static analysis estimates. If variance >200ms, database query optimization is critical priority.

{... end for each endpoint ...}

### Summary

**Total Endpoints Tested:** {count}  
**Cache-Effective Endpoints:** {count with "Effective" status}  
**Slow Endpoints (p95 > 500ms):** {count}  
**Recommended Actions:**
- Endpoints with >200ms variance: Profile with database query analyzer
- Minimal cache effectiveness: Review caching strategy
- Slow endpoints: Prioritize for optimization

---

## Recommended Optimizations

**Note:** Optimizations are categorized by layer (Frontend / Backend / Integration) when backend analysis is available.

Optimizations are prioritized by estimated impact (time or size savings).

| Priority | Optimization | Estimated Impact | Effort |
|---|---|---|---|
| 1 | {optimization-1} | {impact-1} | {effort-1} |
| 2 | {optimization-2} | {impact-2} | {effort-2} |
| 3 | {optimization-3} | {impact-3} | {effort-3} |
| ... | ... | ... | ... |

**Effort Legend:**
- **Low:** < 1 day of work
- **Medium:** 1-3 days of work
- **High:** > 3 days of work

---

## Next Steps

1. Review this report with the team and prioritize optimizations
2. Create optimization plan and Jira Epic/Tasks using `/sdlc-workflow:performance-plan-optimization`
3. After implementing optimizations, re-run `/sdlc-workflow:performance-baseline` to capture new baseline and measure improvements
