# Step 8 -- Remediation

## Triage Outcome

TC-8050 is scoped to stream **2.2.x**. Within this stream, all versions (2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4) are affected -- they all ship criterion 0.5.1 which is < 0.5.2. This triggers **Case A** (affected -- create remediation tasks).

Additionally, stream **2.1.x** (versions 2.1.0 and 2.1.1) is also affected but outside this issue's scope, which triggers **Case B** (cross-stream impact -- proactive remediation if no sibling CVE Jira exists for 2.1.x).

**Dev-dependency handling**: criterion is a dev-only dependency (`[dev-dependencies]` in backend/Cargo.toml), NOT shipped in production builds. Per the dependency scope decision tree, remediation tasks receive the `dev-dependency` label and priority is overridden to **Normal** regardless of CVE severity.

Since criterion is a **Cargo** (source dependency) ecosystem, two remediation tasks are created per affected stream: an upstream backport task and a downstream propagation subtask with a Blocks dependency.

---

## Case A: Remediation Tasks for Stream 2.2.x (In-Scope)

### Task 1: Upstream Backport Task (2.2.x)

**PROPOSAL: Create Jira Task**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-99001: bump criterion to 0.5.2 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99001", "dev-dependency"],
  priority: "Normal"
)
```

**Task Description:**

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99001: criterion path traversal in benchmark output.
The vulnerable dependency (criterion < 0.5.2) must be updated
to the fixed version (0.5.2+).

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

Affected versions: RHTPA 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is retag of v0.4.8), v0.4.11, v0.4.12

CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct dev-dependency (criterion declared in [dev-dependencies])
- Update criterion dependency to >= 0.5.2 in backend/Cargo.toml [dev-dependencies]
- Run `cargo update -p criterion` to update Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (direct dependency)

criterion is a direct dev-dependency of the backend workspace member:

- Update criterion dependency to >= 0.5.2 in backend/Cargo.toml
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8050 (parent tracking issue)
```

**PROPOSAL: Post description digest comment**

```
jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: sha256-md:<computed-64-char-hex-digest>")
```

**PROPOSAL: Link to Vulnerability issue**

```
jira.create_link(
  inwardIssue: "TC-8050",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)
```

---

### Task 2: Downstream Propagation Subtask (2.2.x)

**PROPOSAL: Create Jira Task**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-99001 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99001", "dev-dependency"],
  priority: "Normal"
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
CVE-2026-99001 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps criterion to 0.5.2
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: direct dev-dependency -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8050 (parent tracking issue)
```

**PROPOSAL: Post description digest comment**

```
jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: sha256-md:<computed-64-char-hex-digest>")
```

**PROPOSAL: Link to Vulnerability issue**

```
jira.create_link(
  inwardIssue: "TC-8050",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)
```

**PROPOSAL: Link downstream blocked by upstream**

```
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)
```

---

## Case B: Cross-Stream Proactive Remediation for Stream 2.1.x

Stream 2.1.x is also affected (2.1.0 and 2.1.1 both ship criterion 0.5.1) but has no stream suffix match for this issue. Before creating preemptive tasks, the skill would search for existing sibling CVE Jiras for the 2.1.x stream:

```
jira.search_jql(
  "project = TC AND labels = 'CVE-2026-99001' AND issuetype = 10024 AND key != TC-8050"
)
```

If no sibling CVE Jira exists for stream 2.1.x, the following preemptive tasks would be created:

### Task 3: Preemptive Upstream Backport Task (2.1.x)

**PROPOSAL: Create Jira Task**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-99001: bump criterion to 0.5.2 (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99001", "security-preemptive", "dev-dependency"],
  priority: "Normal"
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
> impact analysis of TC-8050 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-99001: criterion path traversal in benchmark output.
The vulnerable dependency (criterion < 0.5.2) must be updated
to the fixed version (0.5.2+).

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

Affected versions: RHTPA 2.1.0, 2.1.1
Source commit(s): v0.3.8, v0.3.12

CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct dev-dependency (criterion declared in [dev-dependencies])
- Update criterion dependency to >= 0.5.2 in backend/Cargo.toml [dev-dependencies]
- Run `cargo update -p criterion` to update Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8050 (parent tracking issue)
```

**PROPOSAL: Post description digest comment**

```
jira.add_comment(<preemptive-upstream-task-key>, "[sdlc-workflow] Description digest: sha256-md:<computed-64-char-hex-digest>")
```

**PROPOSAL: Link to originating CVE Jira (Related, not Depend)**

```
jira.create_link(
  inwardIssue: "TC-8050",
  outwardIssue: <preemptive-upstream-task-key>,
  type: "Related"
)
```

---

### Task 4: Preemptive Downstream Propagation Subtask (2.1.x)

**PROPOSAL: Create Jira Task**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-99001 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99001", "security-preemptive", "dev-dependency"],
  priority: "Normal"
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
> impact analysis of TC-8050 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-99001 fix from <preemptive-upstream-task-key>.

The upstream backport (<preemptive-upstream-task-key>) bumps criterion to 0.5.2
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: direct dev-dependency -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <preemptive-upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8050 (parent tracking issue)
```

**PROPOSAL: Post description digest comment**

```
jira.add_comment(<preemptive-downstream-task-key>, "[sdlc-workflow] Description digest: sha256-md:<computed-64-char-hex-digest>")
```

**PROPOSAL: Link to originating CVE Jira (Related, not Depend)**

```
jira.create_link(
  inwardIssue: "TC-8050",
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Related"
)
```

**PROPOSAL: Link downstream blocked by upstream**

```
jira.create_link(
  inwardIssue: <preemptive-upstream-task-key>,
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Blocks"
)
```

---

## Post-Triage Summary

### PROPOSAL: Add `ai-cve-triaged` label to TC-8050

```
jira.edit_issue("TC-8050", fields={
  "labels": ["CVE-2026-99001", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### PROPOSAL: Post summary comment on TC-8050

```
Triage complete for CVE-2026-99001 (criterion < 0.5.2).

**Dev-dependency note**: criterion is declared in [dev-dependencies] and is NOT
present in production builds (used for benchmarks only). Remediation tasks carry
the `dev-dependency` label and Normal priority (supply chain risk only).

**Version Impact:**

| Version | Stream | criterion | Affected? | Notes |
|---------|--------|-----------|-----------|-------|
| 2.1.0 | 2.1.x | 0.5.1 | YES | dev-dependency |
| 2.1.1 | 2.1.x | 0.5.1 | YES | dev-dependency |
| 2.2.0 | 2.2.x | 0.5.1 | YES | dev-dependency |
| 2.2.1 | 2.2.x | 0.5.1 | YES | dev-dependency |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.5.1 | YES | dev-dependency |
| 2.2.4 | 2.2.x | 0.5.1 | YES | dev-dependency |

**Affects Versions correction:** [RHTPA 2.2.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2, RHTPA 2.2.3, RHTPA 2.2.4]

**Remediation (stream 2.2.x):**
- <upstream-task-key>: Upstream backport -- bump criterion to 0.5.2 on release/0.4.z (dev-dependency, Normal priority)
- <downstream-task-key>: Downstream propagation -- update rhtpa-backend ref in rhtpa-release.0.4.z (dev-dependency, blocked by <upstream-task-key>)

**Preemptive remediation (stream 2.1.x):**
- <preemptive-upstream-task-key>: Upstream backport -- bump criterion to 0.5.2 on release/0.3.z (security-preemptive, dev-dependency, Normal priority)
- <preemptive-downstream-task-key>: Downstream propagation -- update rhtpa-backend ref in rhtpa-release.0.3.z (security-preemptive, dev-dependency, blocked by <preemptive-upstream-task-key>)
```
