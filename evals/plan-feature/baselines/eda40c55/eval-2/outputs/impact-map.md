# Repository Impact Map — TC-9002: Improve search experience

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators identified. Each task (performance optimization, relevance scoring, filter parameters) can be merged independently without leaving `main` in a broken state. There are no coordinated schema migrations, breaking API changes, cross-cutting refactors, or tightly coupled components that require all-or-nothing delivery.

## Impact

```
trustify-backend:
  changes:
    - Optimize search query performance in SearchService (query plan improvements, database indexing)
    - Add caching configuration to search endpoint route builder
    - Implement relevance scoring/ranking for search results in SearchService
    - Add filter query parameters to GET /api/v2/search endpoint
    - Implement filter logic in SearchService using shared query builder helpers
    - Add database migration for search-related indexes
    - Update search integration tests for new filter parameters, relevance ordering, and performance
```

## Excluded Requirements

| Requirement | Reason for Exclusion |
|---|---|
| **Better UI** (non-MVP) | Cannot be planned: no frontend repository is available in the Repository Registry, and no design mockups or Figma URLs have been provided. UI improvements require a frontend repository and design specifications to decompose into actionable tasks. This requirement is explicitly excluded from scope. |

## Ambiguities Identified

The following ambiguities in the feature description require clarification from stakeholders before implementation details can be finalized. Tasks document assumptions where they fill in missing details.

1. **No performance target specified.** "Search should be faster" and "Should be fast enough" provide no baseline measurement or target SLA (e.g., current p95 latency, target p95 latency). Tasks assume database-level query optimization and caching are the primary levers, but without a target metric, acceptance criteria for "fast enough" cannot be objectively verified.

2. **No relevance criteria defined.** "Results should be more relevant" does not specify what relevance means to users — whether it is text-match proximity, recency, entity-type weighting, field-specific boosting, or a combination. The task assumes PostgreSQL full-text search ranking (ts_rank) as a starting point, pending clarification on the desired ranking behavior.

3. **Filter dimensions unspecified.** "Add filters — Some kind of filtering capability" does not specify which fields should be filterable (entity type, date range, severity, license, package name, etc.), what filter operators to support (exact match, range, multi-select), or how filters interact (AND vs OR). The task assumes a minimum viable set of filters (entity type, date range) pending stakeholder input.

4. **Search scope undefined.** The feature does not specify whether search improvements apply to all searchable entity types (SBOMs, advisories, packages) or a subset. The existing SearchService provides full-text search across entities, but it is unclear whether all entity types should receive equal optimization effort.

5. **"Don't break existing functionality" lacks criteria.** The non-functional requirement provides no regression test baseline, backward compatibility contract, or specific integration points to preserve. Tasks assume that existing GET /api/v2/search response shape and query parameters must remain backward compatible (additive changes only).

## Field Propagation

- **Priority:** Normal (inherited from TC-9002, will be propagated to all created tasks)
- **Fix Versions:** RHTPA 1.6.0 (inherited from TC-9002, will be propagated to all created tasks; no `fixVersion scope` setting found in Jira Configuration, defaulting to "both")
