# Remediation — TC-8004

## Triage Outcome

**Case B: Affected** — the 2.1.x stream ships vulnerable versions of h2. Remediation tasks are needed for the 2.1.x stream only.

The 2.2.x stream is **not affected** (all versions ship h2 >= 0.4.8) and requires no remediation.

## Duplicate / Sibling / Overlap Check (Step 4)

- **Sibling issues**: None found (JQL returned empty).
- **Cross-CVE overlap**: Not applicable (Upstream Affected Component custom field not configured).
- **Preemptive task reconciliation**: No preemptive tasks found.

## Version Lifecycle Check (Step 5)

Lifecycle status not checked in this eval (no external tool calls). Assuming all versions are within support lifecycle. Proceed with remediation.

## Already Fixed Check (Step 6)

No resolved sibling issues exist. No already-fixed scenario detected.

## Concurrent Triage Detection (Step 7)

Upstream Affected Component custom field is not configured. Step 7 skipped.

## Release Jira Orchestration (Step 7.5)

Not performed in this eval (no external tool calls). Remediation tasks would be created without release Jira linkage, or release Jira would be resolved at execution time.

## Remediation Tasks — 2.1.x Stream Only

Since h2 is a Cargo (source dependency) ecosystem package, **two tasks** are required per the ecosystem classification table:

### Task 1: Upstream Dependency Bump — h2 on release/0.3.z

**Summary**: `Remediate CVE-2026-33501: bump h2 to 0.4.8 (rhtpa-2.1)`

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-33501`

**Description**:

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: bump h2 to 0.4.8 via dependency update.
The vulnerable dependency (h2 versions before 0.4.8) must be updated
to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (build v0.3.8), RHTPA 2.1.1 (build v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Target branch: release/0.3.z
- Dependency type: direct
- Remediation action: run `cargo update -p h2` to pull in the latest
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

### Task 2: Downstream Propagation — Update backend ref in rhtpa-release.0.3.z

**Summary**: `Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)`

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-33501`

**Description**:

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from the upstream dependency bump task.

The upstream task bumps h2 to 0.4.8 on release/0.3.z. Once that
PR merges, update the source pinning in this Konflux release repo
so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Dependency type: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream dependency bump task (upstream bump must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

## Jira Linkage Plan

After task creation, the following links would be established:

1. **Depend**: TC-8004 (CVE) -> Task 1 (upstream bump)
2. **Depend**: TC-8004 (CVE) -> Task 2 (downstream propagation)
3. **Blocks**: Task 1 (upstream bump) -> Task 2 (downstream propagation)

## Post-Triage Actions

1. **Add label** `ai-cve-triaged` to TC-8004
2. **Transition** TC-8004 to In Progress
3. **Post summary comment** to TC-8004 documenting:
   - Version impact table (2.1.x affected, 2.2.x not affected)
   - Affects Versions correction: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]
   - Remediation tasks created for 2.1.x stream (2 tasks: upstream bump + downstream propagation)
   - No remediation needed for 2.2.x stream (ships h2 >= 0.4.8)

## No Remediation for 2.2.x Stream

The 2.2.x stream requires **no remediation tasks**. All versions in this stream (2.2.0 through 2.2.4) ship h2 >= 0.4.8, which is at or above the fix threshold. The fix was already present when the 2.2.x stream's first version (2.2.0, build v0.4.5) was released.
