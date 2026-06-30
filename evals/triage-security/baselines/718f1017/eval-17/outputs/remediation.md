# Step 7 -- Remediation for CVE-2026-31812

## Triage Outcome

**Case A: Affected -- create remediation tasks** for stream 2.2.x (in scope).

The version impact analysis shows that within the issue's scoped stream (2.2.x), versions 2.2.0, 2.2.1, and 2.2.2 are affected by CVE-2026-31812 (quinn-proto < 0.11.14). Versions 2.2.3 and 2.2.4 already ship the fixed version (0.11.14) and are NOT affected.

**Case B: Cross-stream impact** -- stream 2.1.x is also affected (versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). If no companion CVE Jira exists for stream 2.1.x, proactive remediation tasks should be created with the `security-preemptive` label.

## Ecosystem

**Cargo** (source dependency) -- requires **two tasks**:
1. Upstream backport task (fix in the source repo)
2. Downstream propagation subtask (update the reference in the Konflux release repo)

---

## Task 1: Upstream Backport Task (Stream 2.2.x)

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0, 2.2.1, 2.2.2
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is a retag of v0.4.8)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z
- quinn-proto is a transitive dependency via quinn crate; the direct dependency to bump may be quinn itself
- Check for pinned versions or transitive dependency constraints that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

## Task 2: Downstream Propagation Subtask (Stream 2.2.x)

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Jira Linkage

After creating the remediation tasks:

1. **Link upstream task to Vulnerability**: `Depend` link from TC-8001 to upstream task
2. **Link downstream subtask to Vulnerability**: `Depend` link from TC-8001 to downstream task
3. **Link downstream as blocked by upstream**: `Blocks` link from upstream task to downstream task
4. **Transition** TC-8001 to In Progress
5. **Assign** TC-8001 to current user
6. **Add label** `ai-cve-triaged` to TC-8001

## Post-Triage Summary Comment

Add a summary comment to TC-8001 documenting:

1. Version impact table (from Step 2)
2. Affects Versions correction: `RHTPA 2.0.0` (wrong) corrected to `RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2` (scoped to stream 2.2.x)
3. Triage outcome: Remediation tasks created
4. Links to upstream and downstream tasks
5. @mention of reporter (PSIRT analyst)

---

## Cross-Stream Remediation (Case B -- Stream 2.1.x)

Stream 2.1.x is also affected (versions 2.1.0 and 2.1.1 ship quinn-proto 0.11.9).

### Cross-stream impact comment on TC-8001:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. Version 2.1.0 ships quinn-proto 0.11.9
and version 2.1.1 ships quinn-proto 0.11.9.
This stream is tracked by a companion issue (see Related links)
or may require separate PSIRT triage.
```

### If no companion CVE Jira exists for stream 2.1.x:

Create proactive remediation tasks with `security-preemptive` label:

**Preemptive Upstream Task (Stream 2.1.x)**:

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)",
  description: <upstream template with preemptive prefix>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

Description prefix:
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for this stream. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

- Target branch: release/0.3.z
- Link type: "Related" (not "Depend") to TC-8001

**Preemptive Downstream Task (Stream 2.1.x)**:

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <downstream template with preemptive prefix>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

- Link type: "Related" (not "Depend") to TC-8001
- Blocked by the preemptive upstream task

### Comment on TC-8001 for preemptive tasks:

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <upstream-task-key> (security-preemptive), <downstream-task-key> (security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```
