# Step 8 -- Remediation

## Case A: Cross-Stream Impact -- Proactive Remediation

The issue is scoped to stream rhtpa-2.2, but the version impact analysis reveals that stream rhtpa-2.1 is also affected. A JQL search for sibling CVE Jiras with label CVE-2026-55123 returns no results for stream rhtpa-2.1 -- no CVE Jira exists for that stream.

Per Step 8 Case A:
- **Stream rhtpa-2.2** (current scope): create standard remediation tasks (Case B).
- **Stream rhtpa-2.1** (no CVE Jira): create proactive preemptive remediation tasks.

---

## Standard Remediation Tasks for Stream rhtpa-2.2 (Case A -> Case B)

Ecosystem: Cargo (source dependency) -- 2 tasks per stream.

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

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: use-after-free in tokio task abort.
The vulnerable dependency (tokio < 1.42.0) must be updated
to the fixed version (1.42.0+).

Affected versions: RHTPA 2.2.0 (v0.4.5), RHTPA 2.2.1 (v0.4.8), RHTPA 2.2.2 (v0.4.9, retag)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
- Update tokio dependency to >= 1.42.0 in Cargo.toml
- Run `cargo update -p tokio` to update the lock file
- Upstream fix is already available on release/0.4.z at HEAD (tokio 1.42.0)

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

1. Post description digest comment (before links):
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

2. Create Depend link:
   ```
   jira.create_link(
     inwardIssue: "TC-8020",
     outwardIssue: <upstream-task-key>,
     type: "Depend"
   )
   ```

---

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

1. Post description digest comment (before links):
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

2. Create Depend link to CVE:
   ```
   jira.create_link(
     inwardIssue: "TC-8020",
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )
   ```

3. Create Blocks link (upstream blocks downstream):
   ```
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

---

## Preemptive Remediation Tasks for Stream rhtpa-2.1 (Case B -- No CVE Jira)

Stream rhtpa-2.1 is affected but has no CVE Jira. Per Step 8 Case A, proactive preemptive remediation tasks are created with the `security-preemptive` label and linked to the originating CVE Jira TC-8020 with a "Related" link (not "Depend", because TC-8020 belongs to a different stream).

Ecosystem: Cargo (source dependency) -- 2 tasks per stream.

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

Affected versions: RHTPA 2.1.0 (v0.3.8), RHTPA 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- Update tokio dependency to >= 1.42.0 in Cargo.toml
- Upstream fix is NOT yet available on release/0.3.z (HEAD has tokio 1.40.0)
  -- this requires an upstream PR to bump tokio on the release/0.3.z branch

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

- Related to: TC-8020 (originating CVE from stream rhtpa-2.2)
```

**Post-creation steps:**

1. Post description digest comment (before links):
   ```
   preemptive_upstream_desc = jira.get_issue(<preemptive-upstream-task-key>, fields=["description"])
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   jira.add_comment(<preemptive-upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

2. Create Related link to originating CVE (not Depend -- different stream):
   ```
   jira.create_link(
     inwardIssue: "TC-8020",
     outwardIssue: <preemptive-upstream-task-key>,
     type: "Related"
   )
   ```

---

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
- Related to: TC-8020 (originating CVE from stream rhtpa-2.2)
```

**Post-creation steps:**

1. Post description digest comment (before links):
   ```
   preemptive_downstream_desc = jira.get_issue(<preemptive-downstream-task-key>, fields=["description"])
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   jira.add_comment(<preemptive-downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

2. Create Related link to originating CVE (not Depend -- different stream):
   ```
   jira.create_link(
     inwardIssue: "TC-8020",
     outwardIssue: <preemptive-downstream-task-key>,
     type: "Related"
   )
   ```

3. Create Blocks link (preemptive upstream blocks preemptive downstream):
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

```
jira.edit_issue("TC-8020", fields={
  "labels": ["CVE-2026-55123", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### 2. Post summary comment on TC-8020

The summary comment documents:
1. The version impact table (all streams)
2. The Affects Versions correction (if any)
3. The triage outcome (remediation created for rhtpa-2.2 + preemptive tasks for rhtpa-2.1)
4. Links to all remediation tasks created
5. @mention of the vulnerability issue's reporter using an ADF mention node

The comment MUST include the Comment Footnote:

```
---
This comment was AI-generated by sdlc-workflow/triage-security v0.13.7.
```
