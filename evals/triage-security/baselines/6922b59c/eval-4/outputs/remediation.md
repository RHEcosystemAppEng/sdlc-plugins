# Remediation -- TC-8004

## Triage Outcome

**Case B: Affected -- create remediation tasks** for the 2.1.x stream only.

The 2.2.x stream is **not affected** (all versions ship h2 >= 0.4.8). No remediation is needed for the 2.2.x stream.

Since this is a **Cargo** (source dependency) ecosystem, two tasks are required for the affected 2.1.x stream:
1. Upstream dependency bump task (fix in the source repo)
2. Downstream propagation task (update the reference in the Konflux release repo)

### Sibling/Duplicate Check (Step 4)

No sibling issues exist (JQL returns empty). No duplicates, no cross-stream companions found.

### Cross-CVE Overlap Check (Step 4.3)

Skipped -- Upstream Affected Component custom field is not configured in the mock project configuration.

### Version Lifecycle Check (Step 5)

Assumed all versions are within support lifecycle (no external lifecycle page consulted per eval constraints).

### Already Fixed Check (Step 6)

No resolved sibling issues exist. Proceeding to remediation.

### Concurrent Triage Detection (Step 7)

Skipped -- Upstream Affected Component custom field is not configured.

### Release Jira Orchestration (Step 7.5)

Not executed in this eval. In a live triage, this step would find or create a release Epic and Task for the 2.1.x stream's next patch release.

---

## Remediation Tasks for Stream 2.1.x

### Task 1: Upstream Dependency Bump

**Summary**: Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

**Description**:

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: bump h2 to 0.4.8 via dependency update.
The vulnerable dependency (h2 versions before 0.4.8) is already fixed upstream --
a package manager update is sufficient.

Affected versions: RHTPA 2.1.0 (v0.3.8), RHTPA 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: source dependency (Cargo crate)
- **Remediation action**: run `cargo update -p h2` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add h2@0.4.8`
- Verify the lock file reflects h2 >= 0.4.8 after the update

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

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

**Jira linkage (not executed)**:
```
jira.create_link(
  inwardIssue: "TC-8004",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)
```

---

### Task 2: Downstream Propagation

**Summary**: Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

**Description**:

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from <upstream-task-key>.

The upstream dependency bump (<upstream-task-key>) bumps h2 to >= 0.4.8
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: source dependency -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

**Jira linkage (not executed)**:
```
# Link downstream task to CVE
jira.create_link(
  inwardIssue: "TC-8004",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)

# Link downstream blocked by upstream
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)
```

---

## Post-Triage Summary

### Actions to perform (not executed)

1. **Add label**: `ai-cve-triaged` to TC-8004
2. **Post summary comment** to TC-8004 documenting:
   - Version impact table (2.1.x affected, 2.2.x not affected)
   - Affects Versions correction: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]
   - Triage outcome: Case B -- remediation tasks created for 2.1.x only
   - Remediation tasks: upstream dependency bump + downstream propagation for 2.1.x
   - 2.2.x stream requires no action (ships h2 >= 0.4.8 in all versions)

### Pre-creation checklist

- [x] **Task count per stream**: 2 tasks for 2.1.x (source dependency ecosystem: upstream bump + downstream propagation). 0 tasks for 2.2.x (not affected).
- [x] **Cross-stream coverage**: N/A -- issue is unscoped, Case A does not apply.
- [x] **Link types**: "Depend" for tasks linked to TC-8004, "Blocks" for upstream -> downstream within 2.1.x stream.
- [x] **Preemptive labels**: N/A -- no preemptive tasks needed (issue is unscoped).
- [x] **Coordination guidance**: upstream deployment context guidance included in both task descriptions.
- [x] **Dedup consistency**: No dedup detected.
