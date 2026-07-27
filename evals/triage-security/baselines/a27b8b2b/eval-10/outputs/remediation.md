# Step 8 -- Remediation

## Triage Outcome

Affected versions exist in the current stream (rhtpa-2.2): RHTPA 2.2.0,
RHTPA 2.2.1, RHTPA 2.2.2. Additionally, cross-stream analysis reveals
that stream rhtpa-2.1 (RHTPA 2.1.0, RHTPA 2.1.1) is also affected and
has no CVE Jira of its own.

**Ecosystem:** Cargo (source dependency) -- 2 tasks per stream (upstream
backport + downstream propagation).

---

## Case A -- Standard Remediation Tasks for Current Stream (rhtpa-2.2)

### Task 1: Upstream Backport (rhtpa-2.2)

**Proposed Jira issue creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

**Labels:** `["ai-generated-jira", "Security", "CVE-2026-55123"]`

**Link to CVE Jira:**
```
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)
```

#### Task Description

```markdown
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: use-after-free in task abort in the tokio crate.
The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed
version (1.42.0+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8, v0.4.9 (retag of v0.4.8)

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

#### Description Digest Protocol (planned)

After creating this task:

1. Re-fetch the task description from Jira:
   ```
   jira.get_issue(<upstream-task-key>, fields=["description"])
   ```
2. Write the description to a temp file and compute digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
3. Post the digest comment BEFORE creating any issue links or other comments:
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

---

### Task 2: Downstream Propagation (rhtpa-2.2)

**Proposed Jira issue creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

**Labels:** `["ai-generated-jira", "Security", "CVE-2026-55123"]`

**Link to CVE Jira:**
```
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)
```

**Blocked by upstream task:**
```
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)
```

#### Task Description

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

#### Description Digest Protocol (planned)

After creating this task:

1. Re-fetch the task description from Jira:
   ```
   jira.get_issue(<downstream-task-key>, fields=["description"])
   ```
2. Write the description to a temp file and compute digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
3. Post the digest comment BEFORE creating issue links or other comments:
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

---

## Case B -- Preemptive Remediation Tasks for Stream rhtpa-2.1

Stream rhtpa-2.1 is affected (tokio 1.40.0, threshold 1.42.0) but has
**no CVE Jira** for this stream. Creating proactive preemptive remediation
tasks per Step 8 Case B.

### Task 3: Preemptive Upstream Backport (rhtpa-2.1)

**Proposed Jira issue creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Labels:** `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]`

**Link to originating CVE Jira (Related, not Depend):**
```
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <preemptive-upstream-task-key>,
  type: "Related"
)
```

The link type is "Related" (not "Depend") because the originating CVE Jira
TC-8020 belongs to a different stream (rhtpa-2.2).

#### Task Description

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

Remediate CVE-2026-55123: use-after-free in task abort in the tokio crate.
The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed
version (1.42.0+).

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
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

- Depends on: TC-8020 (originating CVE Jira, stream rhtpa-2.2 -- Related link)
```

#### Description Digest Protocol (planned)

After creating this task:

1. Re-fetch the task description from Jira:
   ```
   jira.get_issue(<preemptive-upstream-task-key>, fields=["description"])
   ```
2. Write the description to a temp file and compute digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
3. Post the digest comment BEFORE creating issue links or other comments:
   ```
   jira.add_comment(<preemptive-upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

---

### Task 4: Preemptive Downstream Propagation (rhtpa-2.1)

**Proposed Jira issue creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Labels:** `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]`

**Link to originating CVE Jira (Related, not Depend):**
```
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Related"
)
```

**Blocked by preemptive upstream task:**
```
jira.create_link(
  inwardIssue: <preemptive-upstream-task-key>,
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Blocks"
)
```

#### Task Description

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
- Depends on: TC-8020 (originating CVE Jira, stream rhtpa-2.2 -- Related link)
```

#### Description Digest Protocol (planned)

After creating this task:

1. Re-fetch the task description from Jira:
   ```
   jira.get_issue(<preemptive-downstream-task-key>, fields=["description"])
   ```
2. Write the description to a temp file and compute digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
3. Post the digest comment BEFORE creating issue links or other comments:
   ```
   jira.add_comment(<preemptive-downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

---

## Pre-Creation Checklist

- [x] **Task count per stream**: Cargo (source dependency) -- 2 tasks per stream. rhtpa-2.2 gets 2 standard tasks, rhtpa-2.1 gets 2 preemptive tasks.
- [x] **Cross-stream coverage**: rhtpa-2.1 has no sibling CVE Jira, so preemptive tasks are created for that stream.
- [x] **Link types**: "Depend" for standard tasks linked to TC-8020, "Related" for preemptive tasks linked to TC-8020 (different stream), "Blocks" for upstream-to-downstream within each stream.
- [x] **Preemptive labels**: rhtpa-2.1 tasks carry the `security-preemptive` label.
- [x] **Coordination guidance**: omitted -- Source Repositories table has no Deployment Context column (backward compatibility).

## Post-Triage Actions

### 1. Add `ai-cve-triaged` label to TC-8020

```
jira.edit_issue("TC-8020", fields={
  "labels": ["CVE-2026-55123", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### 2. Transition TC-8020 to In Progress

```
jira.get_transitions("TC-8020")
jira.transition_issue("TC-8020", <in-progress-transition-id>)
```

### 3. Post summary comment to TC-8020

A post-triage summary comment would be posted to TC-8020 documenting:
1. The version impact table
2. The Affects Versions correction
3. The triage outcome (remediation tasks created)
4. Links to all remediation tasks (standard + preemptive)
5. An @mention of the vulnerability reporter using an ADF mention node

The comment MUST include the Comment Footnote:

```
---
This comment was AI-generated by sdlc-workflow/triage-security v0.13.6.
```
