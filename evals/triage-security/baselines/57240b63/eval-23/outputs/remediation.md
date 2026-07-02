# Step 8 -- Remediation: TC-8001 (CVE-2026-31812)

## Triage Outcome

- **Issue**: TC-8001
- **CVE**: CVE-2026-31812
- **Library**: quinn-proto (Cargo ecosystem)
- **Fixed version**: 0.11.14
- **Stream scope**: 2.2.x (per issue suffix [rhtpa-2.2])
- **Deployment context**: customer-shipped

### Case A -- Stream 2.2.x (Scoped Stream)

Stream 2.2.x has affected versions (2.2.0, 2.2.1, 2.2.2) but the upstream branch release/0.4.z already has the fix (quinn-proto 0.11.14 at v0.4.11+). Versions 2.2.3 and 2.2.4 already ship the fixed version. The fix has already been propagated to the latest builds.

Since the upstream fix is already present and the latest released versions (2.2.3, 2.2.4) already ship the fixed dependency, the upstream backport task for the 2.2.x stream is not required. The remediation has already been completed in build 0.4.11 (version 2.2.3).

**PROPOSAL**: Correct Affects Versions to RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 and add a triage comment noting that 2.2.3+ already ship the fix. No new remediation tasks are needed for stream 2.2.x.

### Case B -- Stream 2.1.x (Cross-Stream Impact, Preemptive)

Stream 2.1.x is fully affected (all versions ship quinn-proto 0.11.9, which is below the fix threshold of 0.11.14). The upstream branch release/0.3.z has NOT been fixed. No CVE Jira exists for stream 2.1.x.

Preemptive remediation tasks are proposed below. These carry the `security-preemptive` label and use the "Related" link type to TC-8001 (the originating CVE Jira for stream 2.2.x).

---

## Remediation Task Descriptions

### Task 1: Upstream Backport -- bump quinn-proto on release/0.3.z (2.1.x, preemptive)

**PROPOSAL -- Jira Task Creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task Description:**

## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (v0.3.8: quinn-proto 0.11.9), RHTPA 2.1.1 (v0.3.12: quinn-proto 0.11.9)
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

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

### Task 2: Downstream Propagation -- update backend ref in rhtpa-release.0.3.z (2.1.x, preemptive)

**PROPOSAL -- Jira Task Creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task Description:**

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Jira Linkage (PROPOSALS)

### Preemptive Task Linkage (2.1.x)

Both preemptive tasks use **"Related"** link type to TC-8001 (not "Depend"), because TC-8001 belongs to a different stream (2.2.x):

```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <upstream-task-key>,
  type: "Related"
)

jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <downstream-task-key>,
  type: "Related"
)
```

The downstream propagation subtask is blocked by the upstream backport task:

```
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)
```

### Post-Creation Comment on TC-8001 (PROPOSAL)

```
Cross-stream impact: quinn-proto (versions before 0.11.14) also affects stream 2.1.x
based on lock file analysis. Stream 2.1.x is not tracked by a companion CVE Jira.

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <upstream-task-key> (upstream backport, security-preemptive)
- 2.1.x: <downstream-task-key> (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

### ai-cve-triaged Label (PROPOSAL)

Add the `ai-cve-triaged` label to TC-8001 to mark triage as complete.

---

## Post-Triage Summary Comment (PROPOSAL)

```
## CVE-2026-31812 Triage Summary

### Version Impact

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | ships fixed version |

### Affects Versions Correction

Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

Scoped to stream 2.2.x per issue suffix [rhtpa-2.2]. Based on lock file analysis
at pinned commits from security-matrix.md.

### Triage Outcome

**Stream 2.2.x (scoped)**: Fix already shipped in 2.2.3+ (quinn-proto 0.11.14 at
build 0.4.11). No new remediation tasks needed for this stream. Upstream branch
release/0.4.z already contains the fix.

**Stream 2.1.x (cross-stream, preemptive)**: All versions affected. Upstream branch
release/0.3.z does not yet have the fix. Preemptive remediation tasks created:
- <upstream-task-key>: Upstream backport (bump quinn-proto to 0.11.14 on release/0.3.z)
- <downstream-task-key>: Downstream propagation (update backend ref in rhtpa-release.0.3.z)

### Deployment Context

Repository rhtpa-backend has deployment context: **customer-shipped**.
All remediation tasks include coordination guidance for Product Security
advisory preparation and formal disclosure.
```
