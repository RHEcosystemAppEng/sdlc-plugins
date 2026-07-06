# Repository Impact Map — TC-9002: Improve search experience

## Ambiguities Identified

The feature description (TC-9002) contains several vague or underspecified requirements that require assumptions to plan actionable tasks. Each ambiguity is documented below with the assumption used for planning:

1. **"Search should be faster" — no performance targets.** The requirement states "currently too slow" but provides no baseline metrics (current latency, query volume, percentile targets). **Assumption:** "faster" means search queries should return results within 500ms at p95 for typical query patterns. The implementation will add database indexes and optimize query execution.

2. **"Results should be more relevant" — no relevance criteria defined.** No definition of what constitutes "relevant" vs "irrelevant" results, no ranking algorithm preference, no examples of bad results. **Assumption:** "relevant" means results are ranked using PostgreSQL full-text search ranking functions (ts_rank), with results matching more query terms scoring higher.

3. **"Add filters — some kind of filtering capability" — no filter specification.** No indication of which fields should be filterable, what filter operators are needed (exact match, range, multi-select), or how filters interact (AND vs OR). **Assumption:** minimum viable filters are entity type (SBOM, advisory, package) and a date range filter, leveraging the existing query builder helpers in `common/src/db/query.rs`.

4. **"Should be fast enough" (NFR) — no quantifiable target.** This non-functional requirement has no SLA, no latency threshold, no throughput target. **Assumption:** covered by the performance assumption in ambiguity #1 above.

5. **"Don't break existing functionality" (NFR) — no regression scope defined.** No specific backward compatibility guarantees, no list of critical workflows to preserve, no regression test requirements. **Assumption:** all existing search API response shapes are preserved; new parameters are additive (optional query parameters); existing integration tests in `tests/api/search.rs` continue to pass.

## Impact Map

```
trustify-backend:
  changes:
    - Add database migration with GIN indexes on full-text search columns to improve query performance
    - Optimize SearchService query execution to use indexed full-text search with ts_vector/ts_query
    - Implement relevance-based ranking for search results using PostgreSQL ts_rank scoring
    - Add filter query parameters to the search endpoint (entity type, date range)
    - Update search service to apply filter predicates using existing query builder helpers
    - Add integration tests for new search performance, ranking, and filtering behavior
```

## Excluded Requirements

| Requirement | Reason for Exclusion |
|---|---|
| Better UI — "Make it look nicer" (non-MVP) | Cannot be planned: no design mockups are available, and no frontend repository is in scope. The Repository Registry contains only `trustify-backend`. UI improvements require a frontend repository and Figma designs to decompose into actionable tasks. |

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified:
- No coordinated schema migrations — the search index migration (Task 1) is additive and does not break existing code if landed alone.
- No breaking API changes — all endpoint changes are additive (new optional query parameters); the existing `GET /api/v2/search` contract is preserved.
- No cross-cutting refactors — each task modifies a contained set of files within the search module.
- No tightly coupled components — each task delivers independently usable value (faster search, ranked results, filtered results).

All tasks target branch `main`.

## Inherited Field Propagation

| Field | Feature Value | Propagated to Tasks |
|---|---|---|
| Priority | Normal | Yes — `{"name": "Normal"}` included in `additional_fields` |
| Fix Versions | RHTPA 1.6.0 | Yes — `{"name": "RHTPA 1.6.0"}` included in `additional_fields` (no `fixVersion scope` configured in Jira Field Defaults; defaulting to "both") |
| Labels | ai-generated-jira | Yes — all tasks include `["ai-generated-jira"]` label |

## additional_fields for all created tasks

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Normal"},
  "fixVersions": [{"name": "RHTPA 1.6.0"}]
}
```
