# Step 8 — Remediation

## Case A: Cross-Stream Impact Detection (Scoped Issue)

The issue TC-8020 is scoped to stream rhtpa-2.2 (suffix `[rhtpa-2.2]`). The version impact analysis reveals that stream **rhtpa-2.1** is also affected (tokio 1.40.0, threshold 1.42.0).

A JQL search for sibling CVE Jiras with label `CVE-2026-55123` returns **no results** for stream rhtpa-2.1. No CVE Jira exists for that stream. This triggers proactive preemptive remediation task creation for stream rhtpa-2.1.

---

## Case B: Standard Remediation Tasks for Current Stream (rhtpa-2.2)

### Affected versions in scope: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

Ecosystem: **Cargo** (source dependency) -- creates **2 tasks** per stream.

### Task 1: Upstream Backport Task (rhtpa-2.2)

**Proposed Jira Issue Creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

**Labels**: `['ai-generated-jira', 'Security', 'CVE-2026-55123']`

**Task Description:**

```markdown
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: tokio use-after-free in task abort.
The vulnerable dependency (tokio < 1.42.0) must be updated
to the fixed version (1.42.0+).

Affected versions: RHTPA 2.2.0 (v0.4.5), RHTPA 2.2.1 (v0.4.8), RHTPA 2.2.2 (v0.4.9, retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

- Update tokio dependency to >= 1.42.0 in Cargo.toml
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

**Post-creation steps:**

1. **Description digest comment** (before links or other comments):
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   # Write description to temp file and compute digest
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

2. **Depend link** to CVE Jira:
   ```
   jira.create_link(
     inwardIssue: "TC-8020",
     outwardIssue: <upstream-task-key>,
     type: "Depend"
   )
   ```

---

### Task 2: Downstream Propagation Subtask (rhtpa-2.2)

**Proposed Jira Issue Creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

**Labels**: `['ai-generated-jira', 'Security', 'CVE-2026-55123']`

**Task Description:**

```markdown
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

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
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

**Post-creation steps:**

1. **Description digest comment** (before links or other comments):
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

2. **Depend link** to CVE Jira:
   ```
   jira.create_link(
     inwardIssue: "TC-8020",
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )
   ```

3. **Blocks link** (downstream blocked by upstream):
   ```
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

---

## Case A (continued): Preemptive Remediation Tasks for Stream rhtpa-2.1

Stream rhtpa-2.1 is affected (tokio 1.40.0 < 1.42.0) but has **no CVE Jira**. Per Case A, proactive preemptive remediation tasks are created.

### Preemptive Task 1: Upstream Backport Task (rhtpa-2.1)

**Proposed Jira Issue Creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Labels**: `['ai-generated-jira', 'Security', 'CVE-2026-55123', 'security-preemptive']`

**Task Description:**

```markdown
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

- Target branch: release/0.3.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

- Update tokio dependency to >= 1.42.0 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8020 (originating CVE Jira, stream rhtpa-2.2 — Related link)
```

**Post-creation steps:**

1. **Description digest comment** (before links or other comments):
   ```
   preemptive_upstream_desc = jira.get_issue(<preemptive-upstream-task-key>, fields=["description"])
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   jira.add_comment(<preemptive-upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

2. **Related link** to originating CVE Jira (NOT Depend, because the originating CVE belongs to a different stream):
   ```
   jira.create_link(
     inwardIssue: "TC-8020",
     outwardIssue: <preemptive-upstream-task-key>,
     type: "Related"
   )
   ```

---

### Preemptive Task 2: Downstream Propagation Subtask (rhtpa-2.1)

**Proposed Jira Issue Creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Labels**: `['ai-generated-jira', 'Security', 'CVE-2026-55123', 'security-preemptive']`

**Task Description:**

```markdown
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

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <preemptive-upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8020 (originating CVE Jira, stream rhtpa-2.2 — Related link)
```

**Post-creation steps:**

1. **Description digest comment** (before links or other comments):
   ```
   preemptive_downstream_desc = jira.get_issue(<preemptive-downstream-task-key>, fields=["description"])
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   jira.add_comment(<preemptive-downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

2. **Related link** to originating CVE Jira (NOT Depend):
   ```
   jira.create_link(
     inwardIssue: "TC-8020",
     outwardIssue: <preemptive-downstream-task-key>,
     type: "Related"
   )
   ```

3. **Blocks link** (downstream blocked by upstream):
   ```
   jira.create_link(
     inwardIssue: <preemptive-upstream-task-key>,
     outwardIssue: <preemptive-downstream-task-key>,
     type: "Blocks"
   )
   ```

---

## Post-Triage Summary

### 1. Add the `ai-cve-triaged` label

Proposed action: Add `ai-cve-triaged` label to TC-8020.

```
jira.edit_issue("TC-8020", fields={
  "labels": ["CVE-2026-55123", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### 2. Transition to In Progress

Proposed action: Transition TC-8020 to In Progress.

### 3. Post summary comment

Proposed action: Post a summary comment to TC-8020 documenting:

```
Triage complete for CVE-2026-55123 (tokio < 1.42.0).

Version impact:

| Version | Stream | tokio | Affected? | Notes |
|---------|--------|-------|-----------|-------|
| 2.1.0 | 2.1.x | 1.40.0 | YES | |
| 2.1.1 | 2.1.x | 1.40.0 | YES | |
| 2.2.0 | 2.2.x | 1.41.1 | YES | |
| 2.2.1 | 2.2.x | 1.41.1 | YES | |
| 2.2.2 | 2.2.x | 1.41.1 | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 1.42.0 | NO | |
| 2.2.4 | 2.2.x | 1.42.0 | NO | |

Affects Versions correction: [RHTPA 2.2.0, RHTPA 2.2.1] (scoped to stream rhtpa-2.2).

Triage outcome: Remediation tasks created.

Standard remediation tasks (rhtpa-2.2):
- <upstream-task-key> (upstream backport: bump tokio to 1.42.0 on release/0.4.z)
- <downstream-task-key> (downstream propagation, blocked by <upstream-task-key>)

Preemptive remediation tasks (rhtpa-2.1, no CVE Jira exists):
- <preemptive-upstream-task-key> (upstream backport: bump tokio to 1.42.0 on release/0.3.z) [security-preemptive]
- <preemptive-downstream-task-key> (downstream propagation, blocked by <preemptive-upstream-task-key>) [security-preemptive]

@<reporter-name> (ADF mention node: { "type": "mention", "attrs": { "id": "<reporter-account-id>", "text": "@<reporter-name>" } })

---
This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.7.
```

## Pre-Creation Checklist

- [x] **Task count per stream**: Cargo (source dependency) produces 2 tasks per stream. rhtpa-2.2: 2 tasks (upstream + downstream). rhtpa-2.1: 2 preemptive tasks (upstream + downstream). Total: 4 tasks.
- [x] **Cross-stream coverage**: rhtpa-2.1 has no CVE Jira -- preemptive tasks created.
- [x] **Link types**: "Depend" for rhtpa-2.2 tasks linked to TC-8020, "Related" for rhtpa-2.1 preemptive tasks linked to TC-8020, "Blocks" for upstream -> downstream within each stream.
- [x] **Preemptive labels**: rhtpa-2.1 tasks carry the `security-preemptive` label.
- [x] **Coordination guidance**: Source Repositories table has no Deployment Context column. All repos default to upstream. Coordination Guidance subsection omitted (backward compatibility).
