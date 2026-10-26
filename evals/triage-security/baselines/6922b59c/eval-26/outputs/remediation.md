# Step 8 — Remediation: TC-8050

## Triage Outcome

**Case B: Affected -- create remediation tasks**

All supported versions in the 2.2.x stream ship criterion 0.5.1, which is within the affected range (< 0.5.2). The upstream branch (`release/0.4.z`) does not yet ship the fix. Remediation requires two tasks: an upstream dependency bump and a downstream propagation task.

Since criterion is a **dev-only dependency** (declared in `[dev-dependencies]`, not shipped in production), both tasks carry the `dev-dependency` label and **Normal** priority override per the dependency scope decision tree.

---

## Task 1: Upstream Dependency Bump (2.2.x stream)

**Summary**: Remediate CVE-2026-99001: bump criterion to 0.5.2 (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority**: Normal

### Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99001: bump criterion to 0.5.2 via dependency update.
The vulnerable dependency (criterion < 0.5.2) allows path traversal in benchmark output files.

This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only).

Affected versions: 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4
Source commit(s): v0.4.5, v0.4.8, v0.4.11, v0.4.12

CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct dev-dependency
- **Dependency scope**: dev-only ([dev-dependencies] in backend/Cargo.toml) -- NOT shipped in production builds, used for benchmarks only
- **Remediation action**: run `cargo update -p criterion` to pull in criterion >= 0.5.2. If the update does not pull a version >= 0.5.2, pin explicitly: `cargo add criterion@0.5.2 --dev`
- Verify the lock file reflects criterion >= 0.5.2 after the update

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8050 (parent tracking issue)

---

## Task 2: Downstream Propagation (2.2.x stream)

**Summary**: Propagate CVE-2026-99001 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority**: Normal

### Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-99001 fix from the upstream dependency bump task.

The upstream dependency bump task bumps criterion to 0.5.2 on release/0.4.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only).

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct dev-dependency -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream dependency bump task (upstream bump must merge first)
- Depends on: TC-8050 (parent tracking issue)

---

## Jira Linkage Plan

1. **Depend**: TC-8050 (CVE) -> upstream dependency bump task
2. **Depend**: TC-8050 (CVE) -> downstream propagation task
3. **Blocks**: upstream dependency bump task -> downstream propagation task

## Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8050
2. Post summary comment to TC-8050 documenting:
   - Version impact table (all 2.2.x versions affected)
   - Dependency chain context (dev-only, not shipped in production)
   - dev-dependency label and Normal priority override rationale
   - Links to both remediation tasks created
