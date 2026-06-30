# Repository Impact Map — TC-9002: Improve search experience

## Ambiguities Identified

The feature description (TC-9002) contains several ambiguities that must be clarified
before implementation can proceed with full confidence. The following ambiguities are
flagged for product owner / stakeholder clarification:

1. **"Search should be faster" — no quantitative performance target.** The feature says
   search is "currently too slow" but provides no measurable latency target (e.g.,
   p95 < 200ms). **Assumption (pending clarification):** target p95 search latency
   of < 500ms for typical queries, measured at the API response level.

2. **"Results should be more relevant" — no definition of relevance.** No ranking
   criteria, weighting factors, or relevance algorithm is specified. It is unclear
   whether relevance means full-text match quality, recency, severity weighting, or
   some combination. **Assumption (pending clarification):** improve relevance by
   implementing proper full-text search ranking using PostgreSQL `ts_rank` with
   weighted fields (title > description > metadata).

3. **"Add filters" — no filter specification.** The feature says "some kind of
   filtering capability" without defining which fields should be filterable or
   the UX pattern for applying filters. **Assumption (pending clarification):**
   add query-parameter-based filtering on entity type (SBOM, advisory, package),
   and leverage existing entity-specific fields (severity for advisories, license
   for packages) as secondary filters.

4. **"Should be fast enough" — unmeasurable NFR.** No performance budget, no load
   profile, no acceptable degradation threshold. **Assumption (pending clarification):**
   search performance should not regress beyond the target in ambiguity #1, and
   should handle concurrent usage patterns typical of the existing deployment.

5. **"Better UI" (non-MVP) — no design mockups or frontend repository.** This
   requirement is marked as non-MVP and cannot be planned without design mockups
   and access to a frontend repository. The Repository Registry in the project
   configuration contains only the backend repository (trustify-backend). This
   requirement is **excluded from the current plan scope**. It should be planned
   separately once a Figma design is available and a frontend repository is onboarded.

6. **"Don't break existing functionality" — no regression baseline.** No mention of
   existing test coverage, backward compatibility requirements for the search API
   contract, or migration strategy for existing search consumers. **Assumption
   (pending clarification):** the existing `GET /api/v2/search` endpoint contract
   must remain backward-compatible; new filter parameters are additive (optional
   query parameters).

## Workflow Mode Decision

**Selected mode: `direct-to-main`**

**Rationale:** No atomicity indicators are present. Each task can be merged independently
without leaving `main` in a broken state:
- The search performance optimization is self-contained within the search module.
- Filter support adds optional query parameters to an existing endpoint (backward-compatible).
- The database indexing migration can land independently and benefits queries immediately.
- No cross-repository dependencies exist (only trustify-backend is impacted).
- No coordinated schema migrations, breaking API changes, or tightly coupled feature
  components that require all-or-nothing delivery.

## Priority and fixVersions Propagation

- **Priority:** Normal (from feature TC-9002) — will be propagated to all created tasks.
- **fixVersions:** RHTPA 1.6.0 (from feature TC-9002) — will be propagated to all created
  tasks. (No `fixVersion scope` override found in Jira Configuration; defaulting to `"both"`,
  which includes task-level propagation.)

## Impact Map

```
trustify-backend:
  changes:
    - Add PostgreSQL full-text search indexes on searchable entity fields (SBOM name/description, advisory title/description, package name) via a new SeaORM migration
    - Refactor SearchService to use PostgreSQL tsvector/tsquery full-text search with ts_rank ranking instead of naive LIKE/ILIKE queries
    - Add filter query parameters (entity type, severity, license) to the GET /api/v2/search endpoint
    - Extend the search endpoint handler to parse and apply filter parameters using the existing query builder helpers
    - Add integration tests for search performance improvements, relevance ranking, and filter functionality
```
