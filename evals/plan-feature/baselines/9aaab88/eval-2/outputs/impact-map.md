# Impact Map: TC-9002 -- Improve Search Experience

## Workflow Mode

**Direct-to-main**: This feature targets a single repository (trustify-backend) with no atomicity constraints requiring coordinated deployment. Each task can be merged independently to `main`.

## Flagged Ambiguities

The feature description TC-9002 is intentionally vague and contains several ambiguities that must be resolved before or during implementation:

1. **"Search should be faster" -- No quantified performance targets.** The requirement says "currently too slow" but provides no baseline metrics (current latency) or target SLA (e.g., p95 < 200ms). Assumption pending clarification: we will target sub-500ms p95 response time for search queries and add query optimization without a specific benchmark until stakeholders provide one.

2. **"Results should be more relevant" -- No relevance criteria defined.** There is no specification of what "relevant" means -- no ranking algorithm, no scoring criteria, no examples of good vs. bad results. Assumption pending clarification: we will improve relevance by adding PostgreSQL full-text search ranking (ts_rank) to order results by match quality rather than insertion order.

3. **"Add filters" -- No filter types specified.** The requirement says "some kind of filtering capability" without defining which fields should be filterable, what filter operators to support, or which entity types filters apply to. Assumption pending clarification: we will add filters for entity type (SBOM, advisory, package), date range, and severity, based on the existing entity model fields.

4. **"Should be fast enough" -- Non-functional requirement is completely unquantified.** No latency target, throughput target, or definition of "fast enough." Assumption pending clarification: we will add caching and query optimization to improve performance without a specific SLA.

5. **"Don't break existing functionality" -- No regression test baseline specified.** No definition of what existing behavior must be preserved or how to verify it. Assumption pending clarification: we will preserve existing search API contract (GET /api/v2/search) and add new query parameters as optional/backward-compatible.

## Scope Exclusions

- **"Better UI" (Non-MVP)**: This requirement cannot be planned. No design mockups are provided, and no frontend repository is in scope (only trustify-backend is available). This item is excluded from the implementation plan entirely. It should be planned separately once a frontend repository and design specifications are available.

## Repository Impact

### trustify-backend

| Area | Files Impacted | Change Type |
|---|---|---|
| Search service | `modules/search/src/service/mod.rs` | Modify -- add full-text ranking and filter logic |
| Search endpoints | `modules/search/src/endpoints/mod.rs` | Modify -- add filter query parameters |
| Search filter model | `modules/search/src/model/mod.rs` | Create -- define filter and search result types |
| Query helpers | `common/src/db/query.rs` | Modify -- add full-text search query builder helpers |
| Search tests | `tests/api/search.rs` | Modify -- add filter and relevance test cases |

## Task Summary

| Task | Title | Dependencies |
|---|---|---|
| 1 | Define search filter model types | None |
| 2 | Add full-text search ranking to search service | Task 1 |
| 3 | Add filter parameters to search endpoint | Task 2 |
| 4 | Add search result caching | Task 3 |
| 5 | Add search integration tests | Task 3 |
