# Repository Impact Map — TC-9002: Improve search experience

## Impact Map

```
trustify-backend:
  changes:
    - Optimize SearchService full-text search query execution for improved response times (modules/search/src/service/mod.rs)
    - Add or optimize shared query builder helpers for search performance (common/src/db/query.rs)
    - Implement relevance scoring logic in SearchService to rank results by match quality (modules/search/src/service/mod.rs)
    - Create search result model types with relevance score field (modules/search/src/model/)
    - Add filter query parameters to search endpoint handler (modules/search/src/endpoints/mod.rs)
    - Implement filter application logic in SearchService (modules/search/src/service/mod.rs)
    - Extend shared query builder with filter predicate support (common/src/db/query.rs)
    - Create search filter parameter types (modules/search/src/model/)
    - Add integration tests for search performance, relevance, and filtering (tests/api/search.rs)
```

## Excluded Requirements

| Requirement | MVP? | Reason for Exclusion |
|---|---|---|
| Better UI — "Make it look nicer" | No | No frontend repository exists in the Repository Registry. The target repository (trustify-backend) is a Rust backend service with no UI layer. A frontend repository would need to be added to the Registry before this requirement can be planned. |

## Ambiguity Notes

The following MVP requirements are plannable but contain significant ambiguity that
may require clarification during implementation:

| Requirement | Ambiguity | Recommendation |
|---|---|---|
| Search should be faster | No performance baseline or target defined (e.g., current p95 latency, target latency). NFR "Should be fast enough" is not quantifiable. | Define measurable performance targets before implementation (e.g., "p95 latency < 200ms for queries under 1000 results"). |
| Results should be more relevant | No relevance criteria, scoring model, or ranking factors specified. "Doesn't return useful results" is subjective. | Define what constitutes a "relevant" result — field weighting, exact vs partial match priority, recency bias, entity type boosting. |
| Add filters | No specific filter fields, entity types, or filter behavior defined. "Some kind of filtering capability" is underspecified. | Specify which fields are filterable (entity type, date range, severity, package name) and the expected filter behavior (AND/OR semantics, range vs exact match). |

## Workflow Mode Decision

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified:
- No coordinated schema migrations across tasks
- No breaking API changes — filter additions extend the existing API without modifying the current contract
- No cross-cutting refactors — each improvement (performance, relevance, filtering) is independent
- No tightly coupled frontend/backend changes — this is a backend-only feature

Each search improvement can be delivered and merged independently without leaving `main` in a broken state.

## Epic Grouping (by-sub-feature)

| Epic | Summary | Tasks |
|---|---|---|
| Epic 1 | TC-9002: Search Quality | Task 1 (performance), Task 2 (relevance) |
| Epic 2 | TC-9002: Search Filtering | Task 3 (filtering) |

## Task Creation Log

### Inherited Field Values

All tasks and epics inherit the following from Feature TC-9002:
- **Priority**: `{"name": "Normal"}` — Feature priority is "Normal" (not "Undefined"), so it is propagated
- **Fix Versions**: `[{"name": "RHTPA 1.6.0"}]` — Feature has non-empty fixVersions; no `fixVersion scope` setting in Jira Field Defaults (defaults to "both"), so versions are propagated to tasks

### Epic additional_fields

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Normal"},
  "fixVersions": [{"name": "RHTPA 1.6.0"}]
}
```

Parent field for both epics: `{"parent": {"key": "TC-9002"}}`

### Task additional_fields

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Normal"},
  "fixVersions": [{"name": "RHTPA 1.6.0"}]
}
```

Parent field for each task: set to its assigned Epic key (Task 1, 2 -> Epic 1 key; Task 3 -> Epic 2 key).

### Issue Links

**Feature "incorporates" links** (Feature -> Epics, since Epics are available):
- TC-9002 incorporates Epic 1 (TC-9002: Search Quality)
- TC-9002 incorporates Epic 2 (TC-9002: Search Filtering)

**Task dependency links**: None — all tasks are independent.
