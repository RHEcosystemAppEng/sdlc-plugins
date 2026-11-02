## Repository
release-verifier

## Target Branch
main

## Description
Add end-to-end integration tests for the gated verification flow covering the full pipeline: PR lookup → tracker search → issue state check → verify or skip. Tests exercise the happy path, the skip path, and critically the fail-closed path where the gateway returns an empty result from an unauthenticated source.

## Files to Modify
- `tests/gate/test_resolve_issue.py` — add integration-level tests that exercise the full gate pipeline with mocked tracker responses
- `tests/tracker/test_client.py` — add integration tests for the auth probe and search under various gateway conditions

## Implementation Notes
- Focus on three key scenarios:
  1. **Happy path:** PR has a linked issue in "Ready for Verification" → verification runs
  2. **Legitimate skip:** PR has no linked issue, auth probe succeeds → skip with log
  3. **Fail-closed path:** PR has no linked issue, auth probe fails (gateway returns empty to unauthenticated request) → gate exits non-zero
- Mock the tracker gateway responses at the HTTP level (not at the function level) to exercise the full client → gate pipeline.
- Verify that `scripts/pre-verify.sh` correctly propagates exit codes from all three scenarios.
- Per docs/constraints.md §5 (Code Change Rules): tests only, no production code changes.

## Acceptance Criteria
- [ ] Integration test covers the happy path (linked issue in correct state → verification runs)
- [ ] Integration test covers the legitimate skip path (no linked issue, authenticated → skip)
- [ ] Integration test covers the fail-closed path (no linked issue, unauthenticated/degraded → non-zero exit)
- [ ] Integration test verifies `pre-verify.sh` exit code propagation for all three scenarios

## Test Requirements
- [ ] End-to-end test: mock gateway returns a matching issue in "Ready for Verification" state → verify `resolve_gated_issue` returns the issue and verification proceeds
- [ ] End-to-end test: mock gateway returns `[]` for search, `200` for auth probe → verify `resolve_gated_issue` returns `None` (skip)
- [ ] End-to-end test: mock gateway returns `[]` for search, auth probe fails → verify `resolve_gated_issue` raises error (fail-closed)
- [ ] Shell integration test: run `pre-verify.sh` with mocked gateway in degraded state → verify non-zero exit and error message

## Dependencies
- Depends on: Task 2 — Fail-closed gate
- Depends on: Task 3 — Gate verification flow
