# Remediation - TC-8004

## Step 7 - Remediation Decision

### Triage Outcome: Case A - Affected (create remediation tasks)

The version impact analysis shows that the **2.1.x stream** is affected (all versions ship h2 0.4.5, which is vulnerable). The **2.2.x stream** is NOT affected (all versions ship h2 >= 0.4.8).

Since h2 is a **Cargo** (source dependency) ecosystem, two remediation tasks are needed for the affected 2.1.x stream:
1. Upstream backport task (fix in backend source repo)
2. Downstream propagation subtask (update reference in Konflux release repo)

No remediation is needed for the 2.2.x stream -- it already ships the fixed version.

---

## Remediation Task 1: Upstream Backport (2.1.x stream)

**Summary**: Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

### Task Description

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 - Memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (tag v0.3.8, h2 0.4.5), RHTPA 2.1.1 (tag v0.3.12, h2 0.4.5)
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

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)

---

## Remediation Task 2: Downstream Propagation (2.1.x stream)

**Summary**: Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

### Task Description

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-33501 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)

---

## Jira Operations (proposed)

### 1. Create upstream backport task
```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)",
  description: <upstream-task-description above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

### 2. Create downstream propagation subtask
```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <downstream-task-description above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

### 3. Link tasks to vulnerability issue
```
jira.create_link(inwardIssue: "TC-8004", outwardIssue: <upstream-task-key>, type: "Depend")
jira.create_link(inwardIssue: "TC-8004", outwardIssue: <downstream-task-key>, type: "Depend")
```

### 4. Link downstream as blocked by upstream
```
jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
```

### 5. Add ai-cve-triaged label to TC-8004

### 6. Post triage summary comment to TC-8004

## Post-Triage Summary

**Issue**: TC-8004 - CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames

**Version Impact**:
| Version | Stream | h2 version | Affected? |
|---------|--------|------------|-----------|
| 2.1.0 | 2.1.x | 0.4.5 | YES |
| 2.1.1 | 2.1.x | 0.4.5 | YES |
| 2.2.0 | 2.2.x | 0.4.8 | NO |
| 2.2.1 | 2.2.x | 0.4.8 | NO |
| 2.2.2 | 2.2.x | -- | NO (retag of 2.2.1) |
| 2.2.3 | 2.2.x | 0.4.9 | NO |
| 2.2.4 | 2.2.x | 0.4.9 | NO |

**Affects Versions Correction**: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]

**Triage Outcome**: Remediation tasks created for 2.1.x stream only. The 2.2.x stream is not affected -- all versions ship h2 >= 0.4.8. Two tasks created: upstream backport (bump h2 to >= 0.4.8 on release/0.3.z) and downstream propagation (update backend ref in rhtpa-release.0.3.z).

---
_Generated by `/triage-security` skill._
