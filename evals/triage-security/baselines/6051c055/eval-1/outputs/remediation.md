# Step 8 -- Remediation

## Triage Outcome

- **Issue:** TC-8001 (scoped to 2.2.x stream)
- **CVE:** CVE-2026-31812
- **Library:** quinn-proto
- **Fix threshold:** >= 0.11.14
- **Ecosystem:** Cargo (source dependency -- two tasks per stream)

### Case A: Affected versions within scope (2.2.x stream)

Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fix. Create remediation tasks for the 2.2.x stream.

### Case B: Cross-stream impact (2.1.x stream)

The version impact analysis reveals that the **2.1.x** stream (outside this issue's scope) is also affected -- all versions (2.1.0, 2.1.1) ship quinn-proto 0.11.9, which is below the fix threshold. Since this is a scoped issue, Case B applies.

Proposed cross-stream impact comment on TC-8001:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. This stream is tracked by companion issues
(see Related links) or may require separate PSIRT triage.
```

Assuming no existing CVE Jira exists for the 2.1.x stream, preemptive remediation tasks would be created for that stream (see below).

---

## Remediation Tasks -- 2.2.x Stream (Case A, standard)

### Task 1: Upstream Backport (2.2.x)

**Summary:** Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description:**

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (v0.4.5), RHTPA 2.2.1 (v0.4.8), RHTPA 2.2.2 (v0.4.9, retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
- The upstream branch (release/0.4.z) already contains the fix at tags
  v0.4.11 and v0.4.12 (quinn-proto 0.11.14). A cherry-pick or merge
  from a later point on the branch may be sufficient.

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

**Jira creation:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <upstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Linkage:**
```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)
```

---

### Task 2: Downstream Propagation (2.2.x)

**Summary:** Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description:**

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: direct -- carried forward from upstream task
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
- Depends on: TC-8001 (parent tracking issue)
```

**Jira creation:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <downstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Linkage:**
```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)

jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)
```

---

## Remediation Tasks -- 2.1.x Stream (Case B, preemptive)

These tasks are created proactively because the 2.1.x stream is also affected but has no stream-specific CVE Jira. They carry the `security-preemptive` label and use "Related" links to the originating CVE (TC-8001).

### Task 3: Upstream Backport -- Preemptive (2.1.x)

**Summary:** Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Description:**

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (v0.3.8), RHTPA 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- The release/0.3.z branch still ships quinn-proto 0.11.9 at the latest
  tag (v0.3.12). An upstream backport is required to bump quinn-proto
  to >= 0.11.14 on this branch.

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (originating CVE tracking issue -- Related link)
```

**Jira creation:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)",
  description: <upstream-preemptive-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Linkage (Related, not Depend -- preemptive):**
```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <preemptive-upstream-task-key>,
  type: "Related"
)
```

---

### Task 4: Downstream Propagation -- Preemptive (2.1.x)

**Summary:** Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Description:**

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from <preemptive-upstream-task-key>.

The upstream backport (<preemptive-upstream-task-key>) bumps quinn-proto
to 0.11.14 on release/0.3.z. Once that PR merges, update the source
pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: direct -- carried forward from upstream task
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

- Depends on: <preemptive-upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (originating CVE tracking issue -- Related link)
```

**Jira creation:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <downstream-preemptive-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Linkage (Related to originating CVE, Blocks from upstream preemptive task):**
```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Related"
)

jira.create_link(
  inwardIssue: <preemptive-upstream-task-key>,
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Blocks"
)
```

---

## Proposed Comment on TC-8001 (Preemptive Tasks)

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <preemptive-upstream-task-key> (upstream backport, security-preemptive),
         <preemptive-downstream-task-key> (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

---

## Task Summary

| # | Task | Stream | Type | Labels | Link to TC-8001 |
|---|------|--------|------|--------|-----------------|
| 1 | Upstream backport: bump quinn-proto to 0.11.14 (rhtpa-2.2) | 2.2.x | Standard | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 2 | Downstream propagation: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2) | 2.2.x | Standard | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 3 | Upstream backport: bump quinn-proto to 0.11.14 (rhtpa-2.1) | 2.1.x | Preemptive | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |
| 4 | Downstream propagation: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1) | 2.1.x | Preemptive | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |

Task 2 is blocked by Task 1. Task 4 is blocked by Task 3.
