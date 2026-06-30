# Step 7 -- Remediation: TC-8001 (CVE-2026-31812)

## Triage Outcome

**Case A + Case B**: The issue's stream-scoped versions (2.2.x) include affected versions, AND other streams (2.1.x) are also affected.

- **Case A** (stream 2.2.x -- in scope): Create standard remediation tasks for the affected 2.2.x versions.
- **Case B** (stream 2.1.x -- out of scope): Post cross-stream impact comment and create preemptive remediation tasks (if no sibling CVE Jira exists for stream 2.1.x).

## Ecosystem

**Cargo** (source dependency) -- requires **two tasks per stream**: an upstream backport task and a downstream propagation subtask.

---

## Case A: Remediation Tasks for Stream 2.2.x

### Task 1: Upstream Backport (source repo fix)

**Proposed Jira Issue:**

- **Type**: Task
- **Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)
- **Labels**: ai-generated-jira, Security, CVE-2026-31812

**Description:**

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (v0.4.5, quinn-proto 0.11.9),
RHTPA 2.2.1 (v0.4.8, quinn-proto 0.11.12),
RHTPA 2.2.2 (v0.4.9, retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)
- Note: versions 2.2.3+ already ship 0.11.14 on this branch,
  confirming the fix is compatible

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

**Linkage:**
- Link to TC-8001 with type "Depend"

---

### Task 2: Downstream Propagation (Konflux release repo update)

**Proposed Jira Issue:**

- **Type**: Task
- **Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)
- **Labels**: ai-generated-jira, Security, CVE-2026-31812

**Description:**

```
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

- Depends on: [upstream-backport-task-key] (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Linkage:**
- Link to TC-8001 with type "Depend"
- Link to upstream backport task with type "Blocks" (upstream blocks downstream)

---

## Case B: Cross-Stream Impact -- Stream 2.1.x

### Cross-Stream Impact Comment (proposed for TC-8001)

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
(versions 2.1.0, 2.1.1 both ship quinn-proto 0.11.9) based on lock file analysis.
This stream is tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

### Preemptive Remediation Tasks for Stream 2.1.x

If no sibling CVE Jira exists for stream 2.1.x (i.e., no issue with label CVE-2026-31812 and suffix `[rhtpa-2.1]`), create preemptive tasks:

#### Preemptive Task 1: Upstream Backport for 2.1.x

**Proposed Jira Issue:**

- **Type**: Task
- **Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)
- **Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

**Description:**

```
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (v0.3.8, quinn-proto 0.11.9),
RHTPA 2.1.1 (v0.3.12, quinn-proto 0.11.9)
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

- Depends on: TC-8001 (parent tracking issue)
```

**Linkage:**
- Link to TC-8001 with type "Related" (not "Depend" -- preemptive cross-stream)

---

#### Preemptive Task 2: Downstream Propagation for 2.1.x

**Proposed Jira Issue:**

- **Type**: Task
- **Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)
- **Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

**Description:**

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
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

- Depends on: [preemptive-upstream-task-key] (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Linkage:**
- Link to TC-8001 with type "Related" (not "Depend" -- preemptive cross-stream)
- Link to preemptive upstream backport task with type "Blocks"

---

## Post-Triage Summary (proposed comment for TC-8001)

After all tasks are created, the following summary comment would be posted to TC-8001:

```
## CVE-2026-31812 Triage Summary

### Version Impact Table

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

[RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

### Triage Outcome

**Affected** -- remediation tasks created.

### Remediation Tasks (stream 2.2.x -- standard)

- [upstream-task-key]: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x) (upstream backport)
- [downstream-task-key]: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x) (downstream propagation, blocked by upstream task)

### Preemptive Remediation Tasks (stream 2.1.x -- cross-stream)

- [preemptive-upstream-key]: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x) (security-preemptive)
- [preemptive-downstream-key]: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x) (security-preemptive, blocked by preemptive upstream task)

### Additional Actions

- Add label `ai-cve-triaged` to TC-8001
- Transition TC-8001 to In Progress
- Assign TC-8001 to current user
```

## Proposed Label Addition

Add `ai-cve-triaged` label to TC-8001 to mark the issue as triaged.
