# Task 2 — Make tracker search fail closed when authentication cannot be proven

**Summary:** TC-9008: Fail closed in search_issues when the gateway request cannot be proven authenticated
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9008)
**Fix Versions:** (omitted — Feature has none)
**Epic:** TC-9008: Tracker gateway authentication

## Repository
release-verifier

## Target Branch
main

## Description
TC-9008 "Known Risks" states that the tracker gateway returns a **successful, empty** search response to an unauthenticated or under-privileged request. Today `search_issues(jql)` exits non-zero only on HTTP 401/403, so in that case it exits 0 with `[]`, which downstream code cannot distinguish from a genuine "no matching issue" result. This lets a verifier run finish green without verifying the pull request.

This task makes `search_issues` fail closed: an empty result is only returned when the client has positively proven that the request was made with an authenticated, sufficiently privileged identity. Otherwise the client raises a distinct auth-unproven error and the CLI entry point exits non-zero. A post-merge live run may supplement this but is not the coverage for this risk.

## Files to Modify
- `src/tracker/client.py` — add an authentication proof for gateway requests and make `search_issues` raise / exit non-zero when the proof fails, instead of returning `[]`
- `src/tracker/auth.py` — expose the expected service-account identity used for the proof (if needed by the client)
- `tests/tracker/test_client.py` — add degraded/empty-path tests

## Implementation Notes
- **Gate site:** `src/tracker/client.py::search_issues`. This is where the `[]` is currently returned with exit 0 for unauthenticated/under-privileged requests; the guard belongs here, before the result is returned to callers.
- Proof of authentication (pick the mechanism the gateway supports; verify at implementation time):
  1. Preferred: an authenticated identity probe (e.g., the tracker's "current user"/"myself" endpoint through the gateway) that must return the configured service-account identity before/with the search; cache it per process run.
  2. Alternatively: a gateway response header/field that identifies the authenticated principal; absence or mismatch = unproven.
  An empty search result is returned to the caller **only** if the proof succeeded for that run.
- Introduce a dedicated exception (e.g., `TrackerAuthUnprovenError`) distinct from "empty result", and a distinct non-zero exit code in the client CLI path (e.g., exit 3) so `scripts/pre-verify.sh` and `src/gate/resolve_issue.py` (Task 3) can fail closed on it. Keep the existing non-zero behavior for HTTP 401/403 and map it to the same auth-failure category.
- Under-privileged identity (probe succeeds but identity lacks browse/search permission, if detectable) must also be treated as unproven, not as empty.
- Do not retry silently into success; do not downgrade to a warning.
- Constraints (docs/constraints.md): §2.1–2.3 commit rules; §3.1–3.3 PR rules; §5.1–5.4 code change rules; §5.8 sibling parity — keep error handling consistent with the existing 401/403 path in `client.py`; §1.4–1.5 implement-task scope rules.

## Reuse Candidates
- `src/tracker/client.py::search_issues` — existing 401/403 non-zero exit handling; extend this path to cover the unproven-auth case rather than adding a separate wrapper
- `src/tracker/auth.py` — single source of the configured service-account token/identity (from Task 1)

## Acceptance Criteria
- [ ] **Fail closed:** when the gateway returns a successful (2xx) empty search response but the request cannot be proven authenticated as the configured service account, `search_issues` raises `TrackerAuthUnprovenError` (or equivalent) and the client CLI exits non-zero — it MUST NOT return `[]` / exit 0.
- [ ] **Fail closed:** when the authenticated identity is under-privileged (proof indicates wrong identity or missing permission), `search_issues` raises the auth-unproven error and exits non-zero instead of returning `[]`.
- [ ] When authentication is proven and the search genuinely matches nothing, `search_issues` returns `[]` and exits 0 (legitimate empty result preserved).
- [ ] HTTP 401/403 responses still cause a non-zero exit, reported in the same auth-failure category.
- [ ] The auth-unproven exit code / exception is distinct from other errors so callers can detect it.

## Test Requirements
- [ ] Test (degraded path): mock the gateway to return 200 with an empty issue list while the identity probe fails/returns no principal; assert `search_issues` raises the auth-unproven error and the CLI exit code is non-zero (not 0, not `[]`).
- [ ] Test (under-privileged path): mock the identity probe to return a different/unprivileged principal with a 200 empty search; assert fail-closed (raise + non-zero exit).
- [ ] Test (legitimate empty): mock a successful identity probe for the service account and a 200 empty search; assert `[]` and exit 0.
- [ ] Test: existing 401/403 behavior still exits non-zero.

## Verification Commands
- `pytest tests/tracker/test_client.py` — all tests pass, including the degraded/empty-path tests

## Dependencies
- Depends on: Task 1 — Authenticate tracker calls with the service-account token via the gateway
