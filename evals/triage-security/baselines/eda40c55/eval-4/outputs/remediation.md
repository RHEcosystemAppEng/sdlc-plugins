# Step 8 -- Remediation

## Triage Decision

**Case A: Affected -- create remediation tasks** for stream 2.1.x only.

Stream 2.2.x is NOT affected (all versions ship h2 >= 0.4.8), so no remediation
tasks are created for that stream. This is not a Case B (cross-stream impact)
scenario because the unaffected stream already ships the fix -- there is no
cross-stream impact to report.

Ecosystem: **Cargo** (source dependency) -- create **two** tasks for the affected
stream:
1. Upstream backport task (fix in the source repo)
2. Downstream propagation subtask (update the reference in the Konflux release repo)

## Task 1: Upstream Backport Task (2.1.x)

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

### Task Description

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: memory exhaustion via CONTINUATION frames in h2.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version
(0.4.8+).

Affected versions: RHTPA 2.1.0 (v0.3.8), RHTPA 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)
- The fix adds a configurable maximum header list size that defaults to 16 KiB

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)
```

### Post-Creation Actions

1. Post description digest comment on the upstream task
2. Link to TC-8004 with "Depend" link type:
   ```
   jira.create_link(
     inwardIssue: "TC-8004",
     outwardIssue: "<upstream-task-key>",
     type: "Depend"
   )
   ```

## Task 2: Downstream Propagation Subtask (2.1.x)

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

### Task Description

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps h2 to 0.4.8
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

### Post-Creation Actions

1. Post description digest comment on the downstream task
2. Link to TC-8004 with "Depend" link type:
   ```
   jira.create_link(
     inwardIssue: "TC-8004",
     outwardIssue: "<downstream-task-key>",
     type: "Depend"
   )
   ```
3. Link downstream as blocked by upstream task:
   ```
   jira.create_link(
     inwardIssue: "<upstream-task-key>",
     outwardIssue: "<downstream-task-key>",
     type: "Blocks"
   )
   ```

## Post-Triage Summary

### 1. Add `ai-cve-triaged` label to TC-8004

### 2. Summary comment on TC-8004

```
Triage summary for CVE-2026-33501 (h2 < 0.4.8):

Version Impact:

| Version | Stream | h2 version | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.4.5 | YES | pinned at v0.3.8 |
| 2.1.1 | 2.1.x | 0.4.5 | YES | pinned at v0.3.12 |
| 2.2.0 | 2.2.x | 0.4.8 | NO | ships fixed version |
| 2.2.1 | 2.2.x | 0.4.8 | NO | ships fixed version |
| 2.2.2 | 2.2.x | -- | NO | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.4.9 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.4.9 | NO | ships fixed version |

Affects Versions corrected: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].
RHTPA 2.2.0 removed (ships h2 0.4.8, not affected). RHTPA 2.1.1 added (ships h2 0.4.5, affected).

Triage outcome: Remediation tasks created for stream 2.1.x.
Stream 2.2.x is not affected (ships h2 >= 0.4.8).

Remediation tasks:
- <upstream-task-key> (upstream backport: bump h2 to >= 0.4.8 on release/0.3.z)
- <downstream-task-key> (downstream propagation: update backend ref in rhtpa-release.0.3.z, blocked by <upstream-task-key>)

@<reporter-name> (PSIRT reporter)

---
This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/mrizzi/sdlc-plugins) v0.12.2.
```

## Tasks NOT Created

No remediation tasks are created for stream 2.2.x because all versions in that
stream ship h2 >= 0.4.8 (the fixed version). The version impact analysis confirms
that 2.2.x was never vulnerable to CVE-2026-33501.
