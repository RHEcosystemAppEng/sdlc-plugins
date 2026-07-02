# Step 8 -- Remediation: CVE-2026-31812

## Triage Outcome

**Case A (Affected)** applies for the issue-scoped stream (2.2.x): versions 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto < 0.11.14 and are affected.

**Case B (Cross-stream impact)** also applies: the 2.1.x stream (versions 2.1.0, 2.1.1) is also affected but is outside this issue's scope.

## Case A: Remediation Tasks for Stream 2.2.x

Since quinn-proto is a **Cargo** (source dependency) ecosystem, two tasks are created:

### Task 1: Upstream Backport Task

**PROPOSAL -- Jira Issue Creation (requires engineer confirmation)**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task Description:**

```markdown
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8, v0.4.9

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)
- Note: versions 2.2.3+ (tags v0.4.11+) already ship quinn-proto 0.11.14,
  so the fix is available on the release/0.4.z branch at later commits.
  The upstream backport may already be merged -- verify before creating a PR.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

**Post-creation actions:**
1. Post description digest comment on the upstream task
2. Link upstream task to TC-8001 with link type "Depend"

---

### Task 2: Downstream Propagation Subtask

**PROPOSAL -- Jira Issue Creation (requires engineer confirmation)**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task Description:**

```markdown
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Post-creation actions:**
1. Post description digest comment on the downstream task
2. Link downstream task to TC-8001 with link type "Depend"
3. Link downstream task as blocked by the upstream task with link type "Blocks"

---

## Case B: Cross-Stream Impact -- Stream 2.1.x

The version impact analysis shows that the **2.1.x** stream is also affected:

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.1.0 | 0.11.9 | YES |
| 2.1.1 | 0.11.9 | YES |

### Cross-Stream Impact Comment

**PROPOSAL -- Jira Comment on TC-8001 (requires engineer confirmation)**

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. Versions 2.1.0 and 2.1.1 both ship
quinn-proto 0.11.9 which is within the affected range.

This stream is tracked by a companion CVE Jira issue (if one exists)
or may require separate PSIRT triage.
```

### Preemptive Remediation Tasks for 2.1.x

If no companion CVE Jira exists for stream 2.1.x with the CVE-2026-31812 label (verified via JQL search in Step 4), create preemptive remediation tasks:

#### Preemptive Task 1: Upstream Backport (2.1.x)

**PROPOSAL -- Jira Issue Creation (requires engineer confirmation)**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task Description:**

```markdown
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (originating tracking issue -- Related link)
```

**Post-creation actions:**
1. Post description digest comment
2. Link to TC-8001 with link type "Related" (not "Depend" -- preemptive task for a different stream)

#### Preemptive Task 2: Downstream Propagation (2.1.x)

**PROPOSAL -- Jira Issue Creation (requires engineer confirmation)**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task Description:**

```markdown
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-preemptive-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (originating tracking issue -- Related link)
```

**Post-creation actions:**
1. Post description digest comment
2. Link to TC-8001 with link type "Related" (preemptive)
3. Link as blocked by the upstream preemptive task with link type "Blocks"

### Preemptive Tasks Comment on TC-8001

**PROPOSAL -- Jira Comment on TC-8001 (requires engineer confirmation)**

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <upstream-preemptive-task-key> (security-preemptive, upstream backport)
- 2.1.x: <downstream-preemptive-task-key> (security-preemptive, downstream propagation)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

---

## Post-Triage Summary

**PROPOSAL -- Jira Actions on TC-8001 (requires engineer confirmation)**

1. **Add label**: `ai-cve-triaged` to TC-8001
2. **Post summary comment** on TC-8001:

```
CVE-2026-31812 triage complete for TC-8001.

Version impact (quinn-proto < 0.11.14):

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | (cross-stream) |
| 2.1.1 | 0.11.9 | YES | (cross-stream) |
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 0.11.14 | NO | ships fixed version |

Affects Versions corrected: RHTPA 2.0.0 -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

Remediation tasks created (stream 2.2.x):
- <upstream-task-key> (upstream backport: bump quinn-proto to 0.11.14 on release/0.4.z)
- <downstream-task-key> (downstream propagation: update backend ref in rhtpa-release.0.4.z, blocked by <upstream-task-key>)

Preemptive remediation tasks created (stream 2.1.x -- no CVE Jira exists):
- <upstream-preemptive-task-key> (security-preemptive, upstream backport on release/0.3.z)
- <downstream-preemptive-task-key> (security-preemptive, downstream propagation in rhtpa-release.0.3.z)

@<reporter-name> (reporter mention via ADF mention node)

---
[sdlc-workflow:triage-security]
```
