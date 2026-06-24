# Impact Map — TC-9002: Improve Search Experience

## Feature Summary

Improve the search experience in trustify-backend by making search faster, returning more relevant results, and adding filtering capabilities.

## Ambiguities and Open Questions

The feature description (TC-9002) is deliberately vague in several areas. The following ambiguities MUST be resolved with the product owner before implementation is finalized:

### Ambiguity 1: No Performance Targets for "Search should be faster"

The requirement states search is "currently too slow" and the NFR says "should be fast enough," but provides no measurable targets. Questions:
- What is the current p50/p95 search latency?
- What is the acceptable target latency (e.g., < 200ms p95)?
- Under what load conditions should this target be met?
- **Assumption (pending clarification):** We assume the goal is to add database indexing and optimize query construction to reduce latency. We will add query-level logging to establish a baseline, but cannot validate "fast enough" without concrete targets.

### Ambiguity 2: No Definition of "More Relevant Results"

The requirement says users complain about irrelevant results but does not define relevance criteria. Questions:
- What ranking factors should be used (recency, severity, text match quality, popularity)?
- Should exact matches rank higher than partial matches?
- Is there a desired scoring algorithm or weighting scheme?
- Which entity types are most important in search results (SBOMs, advisories, packages)?
- **Assumption (pending clarification):** We assume relevance means implementing proper full-text search ranking using PostgreSQL `ts_rank` with weighted fields (title/name weighted higher than description), with exact matches ranked above partial matches.

### Ambiguity 3: "Add Filters" Is Completely Unspecified

The requirement says "some kind of filtering capability" without specifying:
- Which fields should be filterable (severity, date range, entity type, license, package name)?
- What filter types are needed (exact match, range, multi-select, free text)?
- Should filters be combinable (AND/OR logic)?
- Should filters apply to all searchable entities or only specific ones?
- **Assumption (pending clarification):** We assume filters for entity type (SBOM, advisory, package), date range (created/modified), and severity (for advisories). Filters will use AND logic and be passed as query parameters.

### Ambiguity 4: "Better UI" Cannot Be Planned

The "Better UI" requirement is marked non-MVP, and this is a backend-only repository (trustify-backend). There is no frontend repository in scope, no design mockups referenced, and no UI specifications provided. This requirement is **excluded from this plan entirely**. If a frontend repository exists, a separate feature plan should be created for it once design mockups are available.

### Ambiguity 5: NFR "Don't Break Existing Functionality" Lacks Specificity

"Don't break existing functionality" is standard practice but provides no guidance on:
- Is there a specific regression test suite that must pass?
- Are there API contracts or OpenAPI specs that must remain backward-compatible?
- **Assumption (pending clarification):** We assume all existing endpoint contracts must be preserved (backward-compatible additions only) and all existing tests in `tests/api/search.rs` must continue to pass.

## Scope

### In Scope (MVP)

| Requirement | Mapped Tasks |
|---|---|
| Search should be faster | Task 1 (indexing), Task 2 (query optimization) |
| Results should be more relevant | Task 3 (full-text search ranking) |
| Add filters | Task 4 (filter parameters), Task 5 (integration tests) |

### Out of Scope

| Requirement | Reason |
|---|---|
| Better UI (non-MVP) | No frontend repository in scope; no design mockups available. Cannot be planned for a backend-only repository. |

## Repository Impact

### trustify-backend

| Area | Files Affected | Nature of Change |
|---|---|---|
| Database migrations | `migration/src/` | New migration for search indexes |
| Search module | `modules/search/src/service/mod.rs`, `modules/search/src/endpoints/mod.rs` | Query optimization, ranking, filter support |
| Common query helpers | `common/src/db/query.rs` | Extended filter/sort helpers |
| Entity definitions | `entity/src/sbom.rs`, `entity/src/advisory.rs`, `entity/src/package.rs` | Index annotations |
| Integration tests | `tests/api/search.rs` | New and updated search tests |

## Task Dependency Graph

```
Task 1 (DB indexes)
    └──> Task 2 (Query optimization)
              └──> Task 3 (Relevance ranking)
                        └──> Task 5 (Integration tests)
Task 4 (Filter support) ──> Task 5 (Integration tests)
```

## Assumptions Summary

All assumptions below are **pending clarification** from the product owner:

1. Performance target is "reduce search latency via indexing and query optimization" (no specific ms target)
2. Relevance is defined as PostgreSQL `ts_rank` with weighted fields (name/title > description)
3. Filters cover: entity type, date range, and advisory severity
4. Filters use AND-combination logic via query parameters
5. All existing API contracts and tests must be preserved (backward compatibility)
6. Search covers all three entity types: SBOMs, advisories, and packages
