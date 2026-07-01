# Step 8 -- Remediation

## Case A: Current Stream (rhtpa-2.2) -- Standard Remediation Tasks

The issue is scoped to stream rhtpa-2.2. All versions in this stream (RHTPA 2.2.0 through 2.2.4) are affected. Since tokio is a Cargo (source dependency) ecosystem, two tasks are created: an upstream backport task and a downstream propagation subtask.

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

**Task description:**

---

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: use-after-free in task abort in the tokio crate.
The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed version (1.42.0+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2, RHTPA 2.2.3, RHTPA 2.2.4
Source commit(s): v0.4.5, v0.4.8, v0.4.11, v0.4.12

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

**Post-creation steps (proposed):**

1. Re-fetch the task description from Jira after `create_issue` to get the canonical stored form
2. Compute SHA-256 digest using `python3 scripts/sha256-digest.py /tmp/task-desc.md`
3. Post digest comment: `[sdlc-workflow] Description digest: <tagged-digest>`
4. **Then** create issue link: `jira.create_link(inwardIssue: "TC-8020", outwardIssue: <upstream-task-key>, type: "Depend")`

### Task 2: Downstream Propagation Subtask (rhtpa-2.2)

**Proposed Jira creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

**Task description:**

---

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-55123 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps tokio to 1.42.0
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

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8020 (parent tracking issue)

---

**Post-creation steps (proposed):**

1. Re-fetch the task description from Jira after `create_issue` to get the canonical stored form
2. Compute SHA-256 digest using `python3 scripts/sha256-digest.py /tmp/task-desc.md`
3. Post digest comment: `[sdlc-workflow] Description digest: <tagged-digest>`
4. **Then** create issue links:
   - `jira.create_link(inwardIssue: "TC-8020", outwardIssue: <downstream-task-key>, type: "Depend")`
   - `jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")`

---

## Case B: Other Stream (rhtpa-2.1) -- Preemptive Remediation Tasks

Cross-stream version impact analysis reveals that stream **rhtpa-2.1** is also affected (tokio 1.40.0, fix threshold 1.42.0). A JQL search for sibling CVE Jiras with label `CVE-2026-55123` returns **no results** for stream rhtpa-2.1 -- no CVE Jira exists for that stream.

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

**Labels**: `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]`

Note the `security-preemptive` label distinguishing this from standard remediation tasks.

**Task description:**

---

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-55123: use-after-free in task abort in the tokio crate.
The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed version (1.42.0+).

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
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

- Depends on: TC-8020 (originating CVE Jira -- Related link, not Depend)

---

**Post-creation steps (proposed):**

1. Re-fetch the task description from Jira after `create_issue` to get the canonical stored form
2. Compute SHA-256 digest using `python3 scripts/sha256-digest.py /tmp/task-desc.md`
3. Post digest comment: `[sdlc-workflow] Description digest: <tagged-digest>`
4. **Then** create issue link: `jira.create_link(inwardIssue: "TC-8020", outwardIssue: <preemptive-upstream-task-key>, type: "Related")`

**Link type**: `Related` (not `Depend`) because the originating CVE Jira TC-8020 belongs to stream rhtpa-2.2, not rhtpa-2.1.

### Preemptive Task 2: Downstream Propagation Subtask (rhtpa-2.1)

**Proposed Jira creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Labels**: `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]`

**Task description:**

---

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-55123 fix from <preemptive-upstream-task-key>.

The upstream backport (<preemptive-upstream-task-key>) bumps tokio to 1.42.0
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

- Depends on: <preemptive-upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8020 (originating CVE Jira -- Related link, not Depend)

---

**Post-creation steps (proposed):**

1. Re-fetch the task description from Jira after `create_issue` to get the canonical stored form
2. Compute SHA-256 digest using `python3 scripts/sha256-digest.py /tmp/task-desc.md`
3. Post digest comment: `[sdlc-workflow] Description digest: <tagged-digest>`
4. **Then** create issue links:
   - `jira.create_link(inwardIssue: "TC-8020", outwardIssue: <preemptive-downstream-task-key>, type: "Related")`
   - `jira.create_link(inwardIssue: <preemptive-upstream-task-key>, outwardIssue: <preemptive-downstream-task-key>, type: "Blocks")`

---

## Post-Triage Summary

### Proposed label addition

Add `ai-cve-triaged` label to TC-8020.

### Proposed summary comment on TC-8020

**Proposed content:**

> Triage complete for CVE-2026-55123 (tokio < 1.42.0).
>
> **Version impact:**
>
> | Version | Stream | tokio | Affected? |
> |---------|--------|-------|-----------|
> | RHTPA 2.1.0 | 2.1.x | 1.40.0 | YES |
> | RHTPA 2.1.1 | 2.1.x | 1.40.0 | YES |
> | RHTPA 2.2.0 | 2.2.x | 1.41.1 | YES |
> | RHTPA 2.2.1 | 2.2.x | 1.41.1 | YES |
> | RHTPA 2.2.2 | 2.2.x | -- | YES (retag of 2.2.1) |
> | RHTPA 2.2.3 | 2.2.x | 1.41.1 | YES |
> | RHTPA 2.2.4 | 2.2.x | 1.41.1 | YES |
>
> **Remediation tasks (rhtpa-2.2 -- standard):**
> - <upstream-task-key> (upstream backport: bump tokio to 1.42.0 on release/0.4.z)
> - <downstream-task-key> (downstream propagation, blocked by <upstream-task-key>)
>
> **Preemptive remediation tasks (rhtpa-2.1 -- no CVE Jira exists):**
> - <preemptive-upstream-task-key> (upstream backport: bump tokio to 1.42.0 on release/0.3.z, security-preemptive)
> - <preemptive-downstream-task-key> (downstream propagation, blocked by <preemptive-upstream-task-key>, security-preemptive)
>
> These preemptive tasks use the "Related" link type and carry the security-preemptive label. When PSIRT creates stream-specific CVE Jiras for rhtpa-2.1, Step 4.4 reconciliation will link them and remove the label.
>
> @reporter (ADF mention node: { "type": "mention", "attrs": { "id": "<reporter-account-id>", "text": "@<reporter-name>" } })
>
> ---
> _Comment generated by sdlc-workflow/triage-security._
