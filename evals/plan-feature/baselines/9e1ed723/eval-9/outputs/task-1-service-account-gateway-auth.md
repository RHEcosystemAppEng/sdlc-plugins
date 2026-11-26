# Task 1 — Authenticate tracker calls with the service-account token via the gateway

**Summary:** TC-9008: Authenticate tracker calls with service-account token via API gateway
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9008)
**Fix Versions:** (omitted — TC-9008 has none)
**Parent:** none (Feature → Task hierarchy; Feature "Incorporates" this task)

## Repository
release-verifier

## Target Branch
main

## Description
TC-9008 moves tracker access from a personal token to a new service-account token, sent through the tracker API gateway. This task changes how the tracker client builds credentials and where it sends requests, so that every tracker call (including `search_issues`) goes through the gateway with the service-account token. The personal token is no longer used.

This task covers the requirement "Authenticate tracker calls with the service-account token via the gateway" and the acceptance criterion "Tracker calls use the service-account token through the gateway."

## Files to Modify
- `src/tracker/auth.py` — build the `Authorization` header from the service-account token instead of the personal token
- `src/tracker/client.py` — send requests to the tracker API gateway base URL using the header from `auth.py`
- `tests/tracker/test_client.py` — add tests for the service-account header and gateway routing

## Implementation Notes
- `src/tracker/auth.py` currently builds the tracker `Authorization` header from the configured token. Change it to read the service-account token setting, replacing the personal token, and keep the existing header-building function as the single source of the header. Confirm the exact configuration key name against the current token configuration read in `auth.py`.
- If the service-account token is missing or empty, fail at header-build time with a clear error and do not send an unauthenticated request. An empty token is a cause of the fail-open path documented in TC-9008's Known Risks (the gateway answers unauthenticated requests with a successful empty result).
- `src/tracker/client.py` must get its base URL and headers only from the gateway configuration and `auth.py`. Remove any direct-to-tracker host or personal-token fallback so a request can't silently go out unauthenticated.
- Keep the existing `search_issues(jql)` signature unchanged. Task 2 changes its failure behaviour, and Task 3 consumes it.
- Constraints (docs/constraints.md):
  - §2.1–2.3: commits reference TC-9008's task key in the footer, follow Conventional Commits, and include an `Assisted-by:` trailer.
  - §3.1–3.3: branch is named after the task Jira key, the PR link is posted to Jira, and `gh pr create --base main`.
  - §5.1–5.4: change only the listed files, inspect code before modifying it, follow these notes, and reuse the existing header builder rather than duplicating it.

## Reuse Candidates
- `src/tracker/auth.py` (existing `Authorization` header builder) — extend it to source the service-account token rather than writing a new auth helper
- `src/tracker/client.py::search_issues` — existing request path; reuse its HTTP plumbing and only change the credential and base-URL source

## Acceptance Criteria
- [ ] Every tracker request from `src/tracker/client.py` (including `search_issues`) goes to the tracker API gateway base URL
- [ ] The `Authorization` header is built from the service-account token. The personal token is no longer read or sent.
- [ ] When the service-account token is missing or empty, the client raises a configuration/auth error before any HTTP request is made. It does not send an unauthenticated request.

## Test Requirements
- [ ] Test in `tests/tracker/test_client.py`: with the service-account token configured, `search_issues` sends a request to the gateway URL whose `Authorization` header carries the service-account token
- [ ] Test: the personal token setting is ignored, even when it is set
- [ ] Test: with the service-account token unset or empty, calling `search_issues` raises before any HTTP call. Assert that the mocked transport was not called.

## Documentation Updates
- `README.md` (if it documents tracker configuration) — replace the personal-token setup with the service-account token and gateway URL configuration

## Dependencies
- None
