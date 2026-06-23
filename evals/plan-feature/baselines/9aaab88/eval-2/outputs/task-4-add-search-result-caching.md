## Repository
trustify-backend

## Target Branch
main

## Description
Add caching for search results to improve search response time. The feature description says search is "currently too slow" and "should be faster." This task adds tower-http caching middleware to the search endpoint to reduce database query load for repeated searches.

**Assumption pending clarification**: "Search should be faster" is interpreted as adding HTTP-level caching since no specific performance target is given. The feature description provides no latency SLA (e.g., p95 < 200ms), so we add caching as a general performance improvement. Further optimization (database indexes, query tuning) may be needed after establishing baseline metrics.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` -- Add tower-http cache control headers to the search route builder; configure cache-control with appropriate max-age for search results

## Implementation Notes
The repository already uses `tower-http` caching middleware as noted in the Key Conventions. Follow the existing cache configuration pattern used in endpoint route builders.

Per CONVENTIONS.md §Caching: uses `tower-http` caching middleware; cache configuration in endpoint route builders.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Endpoint registration: each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` file scope.

Add cache-control headers to the search endpoint route in `modules/search/src/endpoints/mod.rs`. Use a short max-age (e.g., 60 seconds) since search results may change as new SBOMs and advisories are ingested. The cache should be scoped per query parameter combination to avoid returning stale filtered results.

## Dependencies
- Depends on: Task 3 -- Add filter parameters to search endpoint (caching should apply to the updated endpoint with filter support)

## Acceptance Criteria
- [ ] Search endpoint responses include Cache-Control headers with appropriate max-age
- [ ] Repeated identical search requests within the cache window do not re-query the database
- [ ] Different query parameter combinations are cached independently
- [ ] Cache does not interfere with filter parameter handling
- [ ] **Assumption pending clarification**: Cache duration (assumed 60s) matches stakeholder performance/freshness requirements
- [ ] **Assumption pending clarification**: HTTP-level caching is sufficient to meet the "faster search" requirement (no specific SLA provided)

## Test Requirements
- [ ] Integration test that search response includes Cache-Control header
- [ ] Integration test that different filter combinations produce independent cache entries

[sdlc-workflow] Description digest: sha256-md:50b7eaa606bfe699825c4c08359b03224c28d14607511435763a382f429dd32d
