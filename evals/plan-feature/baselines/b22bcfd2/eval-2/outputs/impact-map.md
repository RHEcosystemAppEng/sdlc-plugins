# Impact Map: TC-9002 — Improve Search Experience

## Ambiguities Identified

The feature description TC-9002 is underspecified. The following ambiguities must be resolved before implementation can be considered complete. Where necessary, assumptions are documented below and labeled as **assumptions pending clarification**.

1. **"Search should be faster" lacks measurable targets.** No current latency baseline is provided, and no target latency or throughput is specified. What does "too slow" mean quantitatively? Is the goal sub-200ms p95? Sub-500ms? Without a performance baseline and target, we cannot verify the requirement is met.
   - *Assumption pending clarification*: We assume the goal is to optimize query execution via database indexing and query restructuring, targeting sub-500ms p95 response time for typical search queries.

2. **"Results should be more relevant" has no relevance criteria.** There is no definition of what makes a search result "relevant." Is this about text-match ranking, recency weighting, entity-type prioritization, or user-specific context? No scoring model or ranking algorithm is specified.
   - *Assumption pending clarification*: We assume relevance means implementing text-match scoring using PostgreSQL full-text search ranking functions (ts_rank) so results are ordered by match quality rather than insertion order.

3. **"Add filters" does not specify which filters.** The requirement says "some kind of filtering capability" without specifying filterable fields. Should users filter by entity type (SBOM, advisory, package)? By date range? By severity? By package name or license?
   - *Assumption pending clarification*: We assume MVP filters include: entity type (sbom/advisory/package), date range (created_after/created_before), and severity (for advisories). These align with fields already present in the entity models.

4. **Non-functional requirement "should be fast enough" has no measurable threshold.** This duplicates the vagueness of requirement #1 without adding specificity. No SLA, percentile target, or benchmark is given.
   - *Assumption pending clarification*: We treat this as covered by the performance optimization in ambiguity #1 (sub-500ms p95 target).

5. **"Don't break existing functionality" lacks scope definition.** Does this mean strict API backward compatibility (same response schema)? Does it include maintaining existing query parameter behavior? Is there a regression test suite that defines "existing functionality"?
   - *Assumption pending clarification*: We assume this means the existing `GET /api/v2/search` endpoint must continue to accept its current query parameters and return results in the existing `PaginatedResults<T>` format. New filter parameters are additive (optional query params).

## Scope Exclusion

**"Better UI" (non-MVP) is excluded from this plan.** This requirement cannot be planned without:
- Design mockups or Figma specifications defining "better"
- A frontend repository (e.g., trustify-ui) — the only repository in scope is trustify-backend
- UX requirements specifying what visual or interaction improvements are expected

This requirement should be revisited in a separate feature once design assets and frontend repository access are available.

## Inherited Jira Fields

- **Priority**: Normal (inherited from TC-9002, propagated to all tasks via `additional_fields.priority`)
- **Fix Versions**: RHTPA 1.6.0 (inherited from TC-9002, propagated to all tasks via `additional_fields.fixVersions`)

## Summary Comment (Step 6c)

The following would be posted as a summary comment on feature issue TC-9002:

> **Plan Summary for TC-9002 — Improve Search Experience**
>
> 5 ambiguities were identified and documented with assumptions pending clarification. The non-MVP requirement "Better UI" was excluded from scope (requires design mockups and frontend repository).
>
> 4 tasks were created targeting trustify-backend with direct-to-main workflow.
>
> **Inherited fields propagated to all tasks:**
> - Priority: Normal (inherited from feature)
> - Fix Versions: RHTPA 1.6.0 (inherited from feature)
>
> **Tasks created:**
> 1. TC-9002-1: Optimize search query performance with database indexing
> 2. TC-9002-2: Implement search result relevance scoring
> 3. TC-9002-3: Add search filter parameters
> 4. TC-9002-4: Add search integration tests for new functionality

## Description Digest

After each task is created, a description digest comment is posted on the task issue. The digest is computed by re-fetching the task description from the Jira API and running `scripts/sha256-digest.py`. The comment format is:

```
[sdlc-workflow] Description digest: sha256-md:<64-char-hex>
```

For example:
```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f6...
```

(Actual digests are computed at task creation time from the API-fetched description content.)

## Impact by Repository

trustify-backend:
  changes:
    - Add GIN index on search-relevant columns for full-text search performance in a new database migration
    - Refactor `SearchService` in `modules/search/src/service/mod.rs` to use PostgreSQL `ts_rank` for relevance-scored result ordering
    - Extend `GET /api/v2/search` endpoint in `modules/search/src/endpoints/mod.rs` with optional filter query parameters: `entity_type`, `created_after`, `created_before`, `severity`
    - Add filter predicate logic to `common/src/db/query.rs` query builder helpers for the new search filter parameters
    - Add integration tests in `tests/api/search.rs` covering relevance scoring, filter combinations, and performance regression checks
    - Add new migration file under `migration/src/` for the full-text search GIN index
