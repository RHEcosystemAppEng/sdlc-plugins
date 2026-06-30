# Step 7 — Remediation for TC-8001 (CVE-2026-31812)

## Triage Outcome

**Case A + Case B**: The 2.2.x stream (this issue's scope) has affected versions
(2.2.0, 2.2.1, 2.2.2), so remediation tasks are created (Case A). Additionally,
the 2.1.x stream is also affected but is outside this issue's scope, triggering
cross-stream impact handling (Case B).

Ecosystem: Cargo (source dependency) -> **two tasks** per stream:
1. Upstream backport task (fix in rhtpa-backend source repo)
2. Downstream propagation subtask (update reference in Konflux release repo)

---

## Case A: Remediation Tasks for Stream 2.2.x (Issue Scope)

### Task 1: Upstream Backport Task

**Jira Creation:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task Description:**

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is a retag of v0.4.8)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)
- quinn-proto is a transitive dependency via quinn; bumping quinn
  or its version constraint may be required

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

**Post-creation:** Post description digest comment per `shared/description-digest-protocol.md`:
```
[sdlc-workflow] Description digest: sha256-md:<computed-64-char-hex-digest>
```

### Task 2: Downstream Propagation Subtask

**Jira Creation:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task Description:**

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

- Depends on: <upstream-backport-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Post-creation:** Post description digest comment per `shared/description-digest-protocol.md`:
```
[sdlc-workflow] Description digest: sha256-md:<computed-64-char-hex-digest>
```

### Jira Linkage for 2.2.x Tasks

```
# Link upstream task to vulnerability
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)

# Link downstream task to vulnerability
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)

# Link downstream task as blocked by upstream task
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)

# Transition vulnerability to In Progress
jira.transition_issue("TC-8001", status="In Progress")

# Assign vulnerability to current user
jira.edit_issue("TC-8001", fields={"assignee": {"accountId": "<current-user>"}})
```

---

## Case B: Cross-Stream Impact — Stream 2.1.x

### Cross-Stream Impact Comment on TC-8001

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
(versions 2.1.0, 2.1.1) based on lock file analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

### Sibling Check for 2.1.x Stream

Search for existing CVE Jira for the 2.1.x stream:
```
jira.search_jql(
  "project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8001"
)
```

If no sibling CVE Jira exists for stream 2.1.x, create **preemptive remediation tasks**.

### Preemptive Task 1: Upstream Backport (2.1.x stream)

**Jira Creation:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task Description:**

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
- quinn-proto is a transitive dependency via quinn; bumping quinn
  or its version constraint may be required

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue — cross-stream, linked via Related)
```

**Post-creation:** Post description digest comment per `shared/description-digest-protocol.md`:
```
[sdlc-workflow] Description digest: sha256-md:<computed-64-char-hex-digest>
```

### Preemptive Task 2: Downstream Propagation (2.1.x stream)

**Jira Creation:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task Description:**

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

- Depends on: <upstream-preemptive-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue — cross-stream, linked via Related)
```

**Post-creation:** Post description digest comment per `shared/description-digest-protocol.md`:
```
[sdlc-workflow] Description digest: sha256-md:<computed-64-char-hex-digest>
```

### Preemptive Task Linkage for 2.1.x

Preemptive tasks use "Related" link type (not "Depend") because the originating CVE (TC-8001) belongs to a different stream:

```
# Link preemptive upstream task to originating CVE via Related
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <preemptive-upstream-task-key>,
  type: "Related"
)

# Link preemptive downstream task to originating CVE via Related
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Related"
)

# Link downstream subtask as blocked by upstream task
jira.create_link(
  inwardIssue: <preemptive-upstream-task-key>,
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Blocks"
)
```

### Preemptive Task Comment on TC-8001

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <preemptive-upstream-task-key> (security-preemptive, upstream backport)
- 2.1.x: <preemptive-downstream-task-key> (security-preemptive, downstream propagation)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

---

## Post-Triage Summary

### 1. Add `ai-cve-triaged` label to TC-8001

```
jira.edit_issue("TC-8001", fields={
  "labels": ["CVE-2026-31812", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### 2. Post summary comment on TC-8001

```
Triage complete for CVE-2026-31812 (quinn-proto < 0.11.14).

Version Impact:

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | — | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | ships fixed version |

Affects Versions corrected: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
(RHTPA 2.0.0 does not match any configured stream; corrected to actual affected 2.2.x versions)

Remediation tasks created (2.2.x stream — this issue's scope):
- <upstream-task-key> (upstream backport: bump quinn-proto to 0.11.14 on release/0.4.z)
- <downstream-task-key> (downstream propagation: update rhtpa-backend ref in rhtpa-release.0.4.z, blocked by <upstream-task-key>)

Cross-stream impact: 2.1.x stream also affected (versions 2.1.0, 2.1.1).
Preemptive remediation tasks created:
- <preemptive-upstream-task-key> (security-preemptive, upstream backport for 2.1.x)
- <preemptive-downstream-task-key> (security-preemptive, downstream propagation for 2.1.x)

@<reporter-name> (reporter)

---
This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/mrizzi/sdlc-plugins) v0.11.0.
```

The @mention of the reporter uses an ADF mention node with the reporter's account ID from the Jira issue data:
```json
{ "type": "mention", "attrs": { "id": "<reporter-account-id>", "text": "@<reporter-name>" } }
```

### Comment Footnote

Every Jira comment posted during this triage includes the Comment Footnote:
```
---
This comment was AI-generated by sdlc-workflow/triage-security v0.11.0.
```

Rendered as ADF with a horizontal rule node followed by a paragraph containing a hyperlink to `https://github.com/mrizzi/sdlc-plugins`.
