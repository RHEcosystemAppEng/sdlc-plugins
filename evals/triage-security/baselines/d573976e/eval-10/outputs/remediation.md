# Step 8 -- Remediation

## Triage Decision

The version impact analysis shows:

- **Stream 2.2.x** (this issue's scope): Versions 2.2.0, 2.2.1, 2.2.2 ship tokio < 1.42.0. Affected.
- **Stream 2.1.x** (out of scope): Versions 2.1.0, 2.1.1 ship tokio 1.40.0 < 1.42.0. Also affected.

This triggers **Case A** (create standard remediation tasks for the current stream 2.2.x) and **Case B** (create proactive preemptive remediation tasks for stream 2.1.x, which has no CVE Jira).

---

## Case A: Standard Remediation Tasks for Stream rhtpa-2.2

Since tokio is a Cargo (source dependency) ecosystem, two tasks are created: an upstream backport task and a downstream propagation subtask.

### Task 1: Upstream Backport Task (rhtpa-2.2)

**Proposed Jira issue creation:**

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

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: use-after-free in tokio task abort.
The vulnerable dependency (tokio < 1.42.0) must be updated
to the fixed version (1.42.0+).

Affected versions: RHTPA 2.2.0 (v0.4.5, tokio 1.41.1), RHTPA 2.2.1 (v0.4.8, tokio 1.41.1), RHTPA 2.2.2 (retag of 2.2.1)
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
```

**Post-creation steps (proposed):**

1. Re-fetch the task description from Jira after `create_issue`
2. Write the re-fetched description to a temp file
3. Compute digest: `python3 scripts/sha256-digest.py /tmp/task-desc.md` (outputs `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`)
4. Post digest comment: `jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`
5. Only then proceed to create issue links and other comments

### Task 2: Downstream Propagation Subtask (rhtpa-2.2)

**Proposed Jira issue creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

**Task description:**

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-55123 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps tokio to 1.42.0
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8020 (parent tracking issue)
```

**Post-creation steps (proposed):**

1. Re-fetch the task description from Jira after `create_issue`
2. Write the re-fetched description to a temp file
3. Compute digest: `python3 scripts/sha256-digest.py /tmp/task-desc.md` (outputs `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`)
4. Post digest comment: `jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`
5. Only then proceed to create issue links and other comments

### Linkage for Case A tasks (proposed):

```
# Link upstream task to Vulnerability issue
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)

# Link downstream subtask as blocked by upstream task
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)

# Link downstream subtask to Vulnerability issue
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)
```

---

## Case B: Preemptive Remediation Tasks for Stream rhtpa-2.1

Cross-stream version impact analysis reveals that stream **rhtpa-2.1** is also affected (tokio 1.40.0 < 1.42.0 in versions 2.1.0 and 2.1.1). A JQL search for sibling CVE Jiras with label CVE-2026-55123 in stream rhtpa-2.1 returns no results -- no CVE Jira exists for that stream.

Per Step 8 Case B, proactive preemptive remediation tasks are created for stream rhtpa-2.1 using the same templates as Case A but with the preemptive variant.

### Preemptive Task 1: Upstream Backport Task (rhtpa-2.1)

**Proposed Jira issue creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Task description:**

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-55123: use-after-free in tokio task abort.
The vulnerable dependency (tokio < 1.42.0) must be updated
to the fixed version (1.42.0+).

Affected versions: RHTPA 2.1.0 (v0.3.8, tokio 1.40.0), RHTPA 2.1.1 (v0.3.12, tokio 1.40.0)
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

- Depends on: TC-8020 (originating tracking issue, different stream)
```

**Post-creation steps (proposed):**

1. Re-fetch the task description from Jira after `create_issue`
2. Write the re-fetched description to a temp file
3. Compute digest: `python3 scripts/sha256-digest.py /tmp/task-desc.md`
4. Post digest comment: `jira.add_comment(<preemptive-upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`
5. Only then proceed to create issue links

### Preemptive Task 2: Downstream Propagation Subtask (rhtpa-2.1)

**Proposed Jira issue creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Task description:**

```
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
CVE-2026-55123 fix from <preemptive-upstream-task-key>.

The upstream backport (<preemptive-upstream-task-key>) bumps tokio to 1.42.0
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

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

- Depends on: <preemptive-upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8020 (originating tracking issue, different stream)
```

**Post-creation steps (proposed):**

1. Re-fetch the task description from Jira after `create_issue`
2. Write the re-fetched description to a temp file
3. Compute digest: `python3 scripts/sha256-digest.py /tmp/task-desc.md`
4. Post digest comment: `jira.add_comment(<preemptive-downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`
5. Only then proceed to create issue links

### Linkage for Case B preemptive tasks (proposed):

Preemptive tasks use **"Related"** link type (not "Depend") to the originating CVE Jira, because the originating CVE belongs to a different stream (rhtpa-2.2):

```
# Link preemptive upstream task to originating CVE Jira with "Related"
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <preemptive-upstream-task-key>,
  type: "Related"
)

# Link preemptive downstream subtask as blocked by preemptive upstream task
jira.create_link(
  inwardIssue: <preemptive-upstream-task-key>,
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Blocks"
)

# Link preemptive downstream subtask to originating CVE Jira with "Related"
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Related"
)
```

---

## Post-Triage Summary

### 1. Add `ai-cve-triaged` label

**Proposed action:** Add label `ai-cve-triaged` to TC-8020.

### 2. Post summary comment

**Proposed comment on TC-8020:**

```
Triage summary for CVE-2026-55123 (tokio < 1.42.0):

Version impact:

| Version | Stream | tokio | Affected? | Notes |
|---------|--------|-------|-----------|-------|
| 2.1.0 | 2.1.x | 1.40.0 | YES | |
| 2.1.1 | 2.1.x | 1.40.0 | YES | |
| 2.2.0 | 2.2.x | 1.41.1 | YES | |
| 2.2.1 | 2.2.x | 1.41.1 | YES | |
| 2.2.2 | 2.2.x | 1.41.1 | YES | retag of 2.2.1 |

Affects Versions correction: Current [RHTPA 2.2.0, RHTPA 2.2.1] -> Proposed [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2] (adding 2.2.2 which is a retag of 2.2.1, also affected).

Triage outcome: Remediation required.

Standard remediation tasks created (stream rhtpa-2.2):
- <upstream-task-key> (upstream backport: bump tokio to 1.42.0 on release/0.4.z)
- <downstream-task-key> (downstream propagation: update backend ref in rhtpa-release.0.4.z, blocked by <upstream-task-key>)

Preemptive remediation tasks created for streams without CVE Jiras:
- rhtpa-2.1: <preemptive-upstream-task-key> (security-preemptive, upstream backport on release/0.3.z)
- rhtpa-2.1: <preemptive-downstream-task-key> (security-preemptive, downstream propagation in rhtpa-release.0.3.z)

These preemptive tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.

@<reporter-name> (ADF mention node: {"type": "mention", "attrs": {"id": "<reporter-account-id>", "text": "@<reporter-name>"}})

---
This comment was AI-generated by sdlc-workflow/triage-security v0.11.1.
```

All proposed actions above require engineer confirmation before execution. No Jira mutations have been performed.
