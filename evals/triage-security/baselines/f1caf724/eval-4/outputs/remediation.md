# Remediation -- TC-8004 (CVE-2026-33501)

## Triage Outcome

**Case B: Affected -- create remediation tasks** for the 2.1.x stream only.

The 2.2.x stream is NOT affected (all versions ship h2 >= 0.4.8). No remediation tasks are created for the 2.2.x stream.

## Ecosystem Classification

- **Ecosystem**: Cargo (source dependency)
- **Tasks per affected stream**: 2 (upstream backport + downstream propagation)
- **Total tasks**: 2 (one stream affected)

## Task 1: Upstream Backport (2.1.x stream)

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

### Task Description

```
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed
version (0.4.8+).

Affected versions: RHTPA 2.1.0 (v0.3.8), RHTPA 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (or verify via Cargo.lock dependency chain)
- Update h2 dependency to >= 0.4.8 in Cargo.toml / Cargo.lock
- The fix adds a configurable maximum header list size defaulting to 16 KiB

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

### Linkage

```
jira.create_link(
  inwardIssue: "TC-8004",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)
```

---

## Task 2: Downstream Propagation (2.1.x stream)

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <see description below>,
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

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that PR
merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

### Linkage

```
# Link downstream task to CVE issue
jira.create_link(
  inwardIssue: "TC-8004",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)

# Link downstream task as blocked by upstream task
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)
```

---

## Streams Without Remediation

| Stream | Reason | Action |
|--------|--------|--------|
| 2.2.x | All versions ship h2 >= 0.4.8 (the fixed version) | No remediation tasks created |

The 2.2.x stream ships the patched version starting from its earliest release (2.2.0 ships h2 0.4.8). No remediation is needed.

## Case A: Cross-Stream Impact

Case A (cross-stream impact comment) is **not applicable** for this issue. The issue is unscoped (no stream suffix), so it covers all streams by definition. There are no "other streams outside this issue's scope."

## Post-Triage Summary

After all triage actions are complete:

1. **Add label**: `ai-cve-triaged` to TC-8004
2. **Post summary comment** to TC-8004:

```
Triage complete for CVE-2026-33501 (h2 memory exhaustion via CONTINUATION frames).

Version Impact:
| Version | h2 | Affected? | Notes |
|---------|-----|-----------|-------|
| 2.1.0 | 0.4.5 | YES | |
| 2.1.1 | 0.4.5 | YES | |
| 2.2.0 | 0.4.8 | NO | ships fixed version |
| 2.2.1 | 0.4.8 | NO | |
| 2.2.2 | -- | NO | retag of 2.2.1 |
| 2.2.3 | 0.4.9 | NO | |
| 2.2.4 | 0.4.9 | NO | |

Affects Versions corrected: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]

Outcome: Remediation tasks created for 2.1.x stream only.
2.2.x stream is not affected (all versions ship h2 >= 0.4.8).

Remediation tasks:
- <upstream-task-key> (upstream backport: bump h2 to >= 0.4.8 on release/0.3.z)
- <downstream-task-key> (downstream propagation: update rhtpa-backend ref in rhtpa-release.0.3.z, blocked by <upstream-task-key>)
```

3. **Transition** TC-8004 to In Progress
