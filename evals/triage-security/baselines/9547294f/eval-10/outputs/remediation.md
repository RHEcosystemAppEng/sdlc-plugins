# Step 8 -- Remediation

## Case A: Affected -- Create Remediation Tasks for Current Stream (rhtpa-2.2)

The issue is scoped to stream rhtpa-2.2. Versions RHTPA 2.2.0, 2.2.1, and 2.2.2 are affected (tokio < 1.42.0). Since tokio is a Cargo (source dependency) ecosystem, two tasks are created: an upstream backport task and a downstream propagation subtask.

### Task 1: Upstream Backport Task (rhtpa-2.2)

**Proposed Jira creation:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

**Task Description:**

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: tokio use-after-free in task abort.
The vulnerable dependency (tokio < 1.42.0) must be updated
to the fixed version (1.42.0+).

Affected versions: RHTPA 2.2.0 (v0.4.5), RHTPA 2.2.1 (v0.4.8), RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Update tokio dependency to >= 1.42.0 in Cargo.lock
- Target branch: release/0.4.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8020 (parent tracking issue)

---

**Post-creation digest procedure:**
1. Re-fetch the task description from Jira after create_issue
2. Write the re-fetched description to a temp file
3. Compute SHA-256 digest using `python3 scripts/sha256-digest.py /tmp/task-desc.md`
4. Post digest comment: `[sdlc-workflow] Description digest: <tagged-digest>`
5. Then create issue links (Depend link to TC-8020)

### Task 2: Downstream Propagation Subtask (rhtpa-2.2)

**Proposed Jira creation:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

**Task Description:**

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-55123 fix from the upstream backport task.

The upstream backport task bumps tokio to 1.42.0
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

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8020 (parent tracking issue)

---

**Post-creation digest procedure:**
1. Re-fetch the task description from Jira after create_issue
2. Write the re-fetched description to a temp file
3. Compute SHA-256 digest using `python3 scripts/sha256-digest.py /tmp/task-desc.md`
4. Post digest comment: `[sdlc-workflow] Description digest: <tagged-digest>`
5. Then create issue links (Depend link to TC-8020, Blocks link from upstream task)

### Linkage for Current Stream Tasks (rhtpa-2.2)

After both tasks are created and digest comments posted:

```
# Link upstream task to CVE Jira
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)

# Link downstream task to CVE Jira
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)

# Link downstream as blocked by upstream
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)
```

---

## Case B: Cross-Stream Impact -- Preemptive Remediation Tasks for rhtpa-2.1

The cross-stream version impact analysis reveals that stream rhtpa-2.1 is also affected (tokio 1.40.0, threshold 1.42.0). A JQL search for sibling CVE Jiras with label CVE-2026-55123 returns no results for stream rhtpa-2.1 -- no CVE Jira exists for that stream.

Per Step 8 Case B, proactive preemptive remediation tasks are created for stream rhtpa-2.1.

### Preemptive Task 1: Upstream Backport Task (rhtpa-2.1)

**Proposed Jira creation:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Task Description:**

## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-55123: tokio use-after-free in task abort.
The vulnerable dependency (tokio < 1.42.0) must be updated
to the fixed version (1.42.0+).

Affected versions: RHTPA 2.1.0 (v0.3.8), RHTPA 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Update tokio dependency to >= 1.42.0 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8020 (originating CVE Jira, stream rhtpa-2.2)

---

**Post-creation digest procedure:**
1. Re-fetch the task description from Jira after create_issue
2. Write the re-fetched description to a temp file
3. Compute SHA-256 digest using `python3 scripts/sha256-digest.py /tmp/task-desc.md`
4. Post digest comment: `[sdlc-workflow] Description digest: <tagged-digest>`
5. Then create the Related link to TC-8020

### Preemptive Task 2: Downstream Propagation Subtask (rhtpa-2.1)

**Proposed Jira creation:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Task Description:**

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-55123 fix from the upstream backport task.

The upstream backport task bumps tokio to 1.42.0
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

- Depends on: preemptive upstream backport task (upstream backport must merge first)
- Related to: TC-8020 (originating CVE Jira, stream rhtpa-2.2)

---

**Post-creation digest procedure:**
1. Re-fetch the task description from Jira after create_issue
2. Write the re-fetched description to a temp file
3. Compute SHA-256 digest using `python3 scripts/sha256-digest.py /tmp/task-desc.md`
4. Post digest comment: `[sdlc-workflow] Description digest: <tagged-digest>`
5. Then create the Related link to TC-8020 and Blocks link from upstream preemptive task

### Linkage for Preemptive Tasks (rhtpa-2.1)

Preemptive tasks use "Related" link type (not "Depend") to the originating CVE Jira TC-8020, because the originating CVE belongs to a different stream (rhtpa-2.2):

```
# Link preemptive upstream task to originating CVE with "Related"
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <preemptive-upstream-task-key>,
  type: "Related"
)

# Link preemptive downstream task to originating CVE with "Related"
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Related"
)

# Link preemptive downstream as blocked by preemptive upstream
jira.create_link(
  inwardIssue: <preemptive-upstream-task-key>,
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Blocks"
)
```

### Comment on originating CVE Jira (TC-8020)

After creating the preemptive tasks, a comment is proposed for TC-8020:

```
Preemptive remediation tasks created for streams without CVE Jiras:
- rhtpa-2.1: <preemptive-upstream-task-key> (upstream backport, security-preemptive),
  <preemptive-downstream-task-key> (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.

---
_Generated by sdlc-workflow skill `triage-security`._
```

---

## Post-Triage Summary

### Proposed: Add `ai-cve-triaged` label to TC-8020

### Proposed: Post summary comment to TC-8020

The post-triage summary comment would document:

1. The version impact table (showing both streams affected)
2. Affects Versions correction for stream rhtpa-2.2 (scoped to issue)
3. Triage outcome: remediation tasks created for rhtpa-2.2 (Case A) and preemptive remediation tasks created for rhtpa-2.1 (Case B)
4. Links to all created tasks (upstream + downstream for both streams)

All proposed actions (task creation, link creation, label additions, status transitions) are presented for engineer confirmation before execution. No Jira mutations are executed without explicit approval.

---
_Generated by sdlc-workflow skill `triage-security`._
