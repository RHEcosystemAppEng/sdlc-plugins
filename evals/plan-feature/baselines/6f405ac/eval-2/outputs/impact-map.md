# Impact Map: TC-9002 — Improve Search Experience

## Workflow Mode

Direct-to-main — single repository (trustify-backend), no cross-repo coordination required.

## Scope

This plan covers the three MVP requirements from TC-9002:

1. **Search should be faster** — improve query performance via database indexing and caching
2. **Results should be more relevant** — add relevance scoring/ranking to the search service
3. **Add filters** — expose filtering parameters on the search API endpoint

### Excluded from Scope

- **Better UI** (non-MVP) — this is a backend repository with no frontend code. Planning UI improvements requires design mockups and access to a frontend repository, neither of which is available. This requirement cannot be planned without that context.

## Flagged Ambiguities

The feature description (TC-9002) contains several vague or missing requirements that must be clarified before implementation can be considered complete. The plan below documents assumptions made to fill gaps, but these should be validated with stakeholders.

### Ambiguity 1: No performance baseline or target for "faster"

The requirement says "search should be faster" and "currently too slow" but provides no quantitative data:
- What is the current p50/p95 search latency?
- What is the target latency?
- How many concurrent search requests does the system handle?

**Assumption (pending clarification):** The primary bottleneck is missing database indexes on searchable text columns. Adding full-text search indexes and response caching will address the "too slow" complaint. No specific latency SLA is enforced in this plan.

### Ambiguity 2: No definition of "relevant" results or ranking criteria

The requirement says "results should be more relevant" and "users complain about irrelevant results" but does not define:
- What makes a result relevant? (recency, text match quality, entity type priority?)
- Are there specific user complaints or examples of bad results?
- Should ranking be configurable per user or global?

**Assumption (pending clarification):** Relevance is defined as PostgreSQL full-text search rank (`ts_rank`) based on text match quality. Results are ordered by rank descending. No user-configurable ranking is implemented.

### Ambiguity 3: No specification for "add filters"

The requirement says "some kind of filtering capability" but does not specify:
- Which entity fields should be filterable? (type, severity, date range, license?)
- Should filters be AND or OR combined?
- Are filters applied before or after text search?
- What is the API contract for filter parameters?

**Assumption (pending clarification):** Filters are added for entity type (SBOM, advisory, package), severity (for advisories), and date range (created_at). Filters are combined with AND semantics and applied alongside the text search query. Filter parameters are passed as query string parameters on the existing `GET /api/v2/search` endpoint.

### Ambiguity 4: "Should be fast enough" is not a measurable NFR

The non-functional requirement "should be fast enough" has no threshold. No performance test or SLA gate is included in this plan. If a specific latency target is established, a follow-up task should add benchmark tests.

### Ambiguity 5: "Don't break existing functionality" — no regression test baseline

The NFR "don't break existing functionality" is addressed by maintaining backward compatibility on the search endpoint (new filter parameters are optional, default behavior is unchanged) and by extending existing integration tests. However, without a defined regression suite, this is best-effort.

## Impacted Files

### Modified

| File | Change | Task |
|---|---|---|
| `modules/search/src/service/mod.rs` | Add relevance scoring, filter logic, full-text search ranking | 2, 3 |
| `modules/search/src/endpoints/mod.rs` | Add filter query parameters, update route configuration with caching | 3, 4 |
| `modules/search/Cargo.toml` | Add dependencies if needed for full-text search support | 2 |
| `common/src/db/query.rs` | Add shared full-text search helpers and filter builder utilities | 2, 3 |
| `server/src/main.rs` | No changes expected — search module routes are already mounted | — |
| `tests/api/search.rs` | Extend with filter tests, relevance ordering tests, performance smoke tests | 5 |

### Created

| File | Purpose | Task |
|---|---|---|
| `migration/src/m0002_search_indexes/mod.rs` | Database migration for full-text search indexes on searchable columns | 1 |

## Task Dependency Order

```
Task 1 (DB indexes) ─────────────────────┐
                                          ├──> Task 5 (integration tests)
Task 2 (relevance scoring) ──────────────┤
                                          │
Task 3 (filters) ────────────────────────┤
                                          │
Task 4 (caching) ────────────────────────┘
```

Tasks 1-4 can be implemented in parallel but are logically ordered. Task 5 depends on all of them.

## Conventions Applied

All conventions from repo-backend.md Key Conventions apply since all tasks modify `.rs` files:

- Module pattern: `model/ + service/ + endpoints/`
- Error handling: `Result<T, AppError>` with `.context()`
- Response types: `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Query helpers: shared filtering via `common/src/db/query.rs`
- Testing: integration tests in `tests/api/` with real PostgreSQL
- Caching: `tower-http` caching middleware
