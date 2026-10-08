# Step 8 -- Remediation: TC-8004

## Triage Outcome: Case B (Affected -- create remediation tasks)

Only the **2.1.x stream** is affected. The 2.2.x stream ships h2 >= 0.4.8 (the fixed version) and requires no remediation.

Since the issue is **unscoped**, Case A (cross-stream impact) is skipped entirely -- unscoped issues cover all streams by definition, so there are no "other streams outside this issue's scope."

## Remediation Tasks (2.1.x stream only)

Ecosystem: **Cargo** (source dependency, fix available upstream)
Tasks per stream: **2** (dependency bump + downstream propagation)

### Task 1: Dependency Bump (upstream)

**Summary**: Remediate CVE-2026-33501: update h2 to 0.4.8 (2.1.x)
**Labels**: ai-generated-jira, Security, CVE-2026-33501

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: bump h2 to 0.4.8 via dependency update.
The vulnerable dependency (h2 < 0.4.8) is already fixed upstream --
a package manager update is sufficient.

Affected versions: RHTPA 2.1.0 (v0.3.8), RHTPA 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct or transitive (verify via Cargo.lock inspection)
- **Remediation action**: run `cargo update -p h2` to pull in the latest
  compatible version (>= 0.4.8)
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add h2@0.4.8`
- Verify the lock file reflects >= 0.4.8 after the update

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)
```

### Task 2: Downstream Propagation (2.1.x)

**Summary**: Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)
**Labels**: ai-generated-jira, Security, CVE-2026-33501

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from the upstream dependency bump task.

The upstream dependency bump task bumps h2 to 0.4.8 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release
repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream dependency bump task (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

## Jira Linkage Plan

1. **Depend**: TC-8004 (CVE) -> Task 1 (dependency bump)
2. **Depend**: TC-8004 (CVE) -> Task 2 (downstream propagation)
3. **Blocks**: Task 1 (dependency bump) -> Task 2 (downstream propagation)
   _(downstream is blocked by upstream -- cannot propagate until the fix lands)_

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks for 2.1.x (Cargo source dependency with fix available) -- matches ecosystem classification table
- [x] **Cross-stream coverage**: N/A -- issue is unscoped, Case A skipped. 2.2.x is not affected, so no remediation needed there
- [x] **Link types**: "Depend" for tasks linked to CVE TC-8004; "Blocks" for upstream -> downstream within 2.1.x stream
- [x] **Preemptive labels**: N/A -- no preemptive tasks needed (2.2.x is not affected)
- [x] **Coordination guidance**: included (deployment context: upstream)
- [x] **Dedup consistency**: no sibling issues exist (JQL returns empty), no dedup needed

## No Remediation for 2.2.x Stream

The 2.2.x stream requires no remediation. All versions in this stream ship h2 >= 0.4.8:

| Version | h2 version | Status |
|---------|------------|--------|
| 2.2.0 | 0.4.8 | Fixed (exact fix version) |
| 2.2.1 | 0.4.8 | Fixed |
| 2.2.2 | (retag of 2.2.1) | Fixed |
| 2.2.3 | 0.4.9 | Fixed (above fix threshold) |
| 2.2.4 | 0.4.9 | Fixed (above fix threshold) |
