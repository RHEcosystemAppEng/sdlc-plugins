## Repository
trustify-backend

## Target Branch
main

## Priority
Major

## Fix Versions
RHTPA 1.5.0

## Description
Execute performance benchmarks for the advisory severity aggregation endpoint feature (TC-9001). Validate that API response times are within acceptable thresholds under load, no memory leaks are detected during sustained usage, and database query performance does not degrade with increased data volume. The endpoint must meet the p95 < 200ms target for SBOMs with up to 500 advisories.

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load (p95 < 200ms for SBOMs with up to 500 advisories)
- [ ] No memory leaks detected during sustained usage of the advisory-summary endpoint
- [ ] Database query performance does not degrade with increased data volume
- [ ] Cached responses return within expected latency (significantly faster than uncached)
- [ ] Aggregation query performs efficiently with large advisory datasets

## Test Requirements
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Dependencies
- Depends on: Task 1 — Create advisory severity summary model
- Depends on: Task 2 — Implement advisory severity aggregation service method
- Depends on: Task 3 — Add advisory-summary endpoint with caching
- Depends on: Task 4 — Add cache invalidation for advisory summary on ingestion
- Depends on: Task 5 — Add integration tests for advisory-summary endpoint
