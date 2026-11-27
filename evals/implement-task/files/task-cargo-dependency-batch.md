<!-- SYNTHETIC TEST DATA — fictional Cargo CVE remediation task and workspace state for dependency-update strategy and graph-verification evals. -->

# Mock Jira Task

**Key**: TC-9301
**Summary**: Update quinn-proto to the fixed release in the backend workspace
**Status**: To Do
**Labels**: ai-generated-jira, Security, CVE-2026-31812
**Linked Issues**: depends on CVE issue TC-8001

---

## Repository

trustify-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-31812 in the upstream Rust workspace. The vulnerable
`quinn-proto` releases are `< 0.11.14`; fixed version `0.11.14` is available.
Update the dependency resolution to the fixed version.

## Files to Modify

- `Cargo.lock` — update the workspace dependency resolution

## Files to Create

None.

## Implementation Notes

- Ecosystem: Cargo.
- The workspace root `Cargo.toml` lists `backend` and `client` as members.
- `backend/Cargo.toml` declares `quinn-proto = "0.11"`. This compatible
  requirement already admits fixed version 0.11.14; no manifest change is
  needed for this task state.
- Current `Cargo.lock` resolves `quinn-proto` to 0.11.12.
- The current inverse dependency graph has these workspace paths:
  - `backend -> quinn-proto 0.11.12`
  - `client -> transport-adapter -> quinn-proto 0.11.12`

## Acceptance Criteria

- [ ] `Cargo.lock` resolves `quinn-proto` to version 0.11.14 or later.
- [ ] Existing backend and client tests pass.
- [ ] Keep the task on target branch `release/0.3.z`.

## Test Requirements

- [ ] Run the existing backend and client workspace tests.

## Dependencies

- Depends on: TC-8001
