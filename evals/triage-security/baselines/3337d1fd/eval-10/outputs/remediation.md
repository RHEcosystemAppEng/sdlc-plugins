# Remediation — CVE-2026-55123 (tokio)

## Triage Outcome

- **Case A**: Affected — create remediation tasks for the in-scope stream (rhtpa-2.2)
- **Case B**: Cross-stream impact — create preemptive remediation tasks for stream rhtpa-2.1 (no CVE Jira exists for that stream)

Ecosystem: **Cargo** (source dependency) — requires 2 tasks per stream: upstream backport + downstream propagation.

---

## Case A: Remediation Tasks for Stream rhtpa-2.2 (In-Scope)

### Task 1: Upstream Backport (rhtpa-2.2)

**Summary**: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`

**Description**:

> ## Repository
>
> rhtpa-backend
>
> ## Target Branch
>
> release/0.4.z
>
> ## Description
>
> Remediate CVE-2026-55123: use-after-free in task abort in the tokio crate.
> The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed version (1.42.0+).
>
> Affected versions: RHTPA 2.2.0 (tokio 1.41.1), RHTPA 2.2.1 (tokio 1.41.1)
> Source commit(s): v0.4.5, v0.4.8
>
> Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
> Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp
>
> ## Implementation Notes
>
> - Target branch: release/0.4.z
> - **Dependency type**: direct
>
> ### Remediation approach (direct dependency)
>
> When the vulnerable package is a **direct** dependency of a workspace member:
>
> - Update tokio dependency to >= 1.42.0 in Cargo.toml
> - If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)
>
> ## Acceptance Criteria
>
> - [ ] tokio dependency is >= 1.42.0
> - [ ] No other dependency conflicts introduced
> - [ ] Existing tests pass
>
> ## Test Requirements
>
> - [ ] Existing test suite passes with the updated dependency
>
> ## Dependencies
>
> - Depends on: TC-8020 (parent tracking issue)

**Jira operations**:
```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)",
  description: <upstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)

# Post description digest comment
jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: sha256-md:<hex>")

# Link to vulnerability issue
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)
```

### Task 2: Downstream Propagation (rhtpa-2.2)

**Summary**: Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`

**Description**:

> ## Repository
>
> rhtpa-release.0.4.z
>
> ## Target Branch
>
> main
>
> ## Description
>
> Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
> CVE-2026-55123 fix from the upstream backport task.
>
> The upstream backport bumps tokio to 1.42.0 on release/0.4.z. Once that PR
> merges, update the source pinning in this Konflux release repo so the next
> build ships the fix.
>
> ## Implementation Notes
>
> - Source pinning method: artifacts.lock.yaml (download URL contains tag)
> - **Dependency type**: direct — carried forward from upstream task
> - Update the rhtpa-backend reference to the merged commit or new release tag
> - Verify the Konflux build pipeline triggers successfully
>
> ## Acceptance Criteria
>
> - [ ] rhtpa-backend reference updated to include the fix
> - [ ] Konflux rebuild triggers new container image
>
> ## Test Requirements
>
> - [ ] Container image builds successfully with the updated reference
>
> ## Dependencies
>
> - Depends on: <upstream-task-key> (upstream backport must merge first)
> - Depends on: TC-8020 (parent tracking issue)

**Jira operations**:
```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <downstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)

# Post description digest comment
jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: sha256-md:<hex>")

# Link downstream blocked by upstream
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)

# Link to vulnerability issue
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)
```

---

## Case B: Preemptive Remediation Tasks for Stream rhtpa-2.1 (Cross-Stream)

Stream rhtpa-2.1 is affected (tokio 1.40.0 < 1.42.0) but has no CVE Jira.
Preemptive remediation tasks are created with the `security-preemptive` label and
linked to the originating CVE TC-8020 with "Related" (not "Depend").

### Task 3: Upstream Backport — Preemptive (rhtpa-2.1)

**Summary**: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`

**Description**:

> > **Preemptive remediation**: This task was created proactively from cross-stream
> > impact analysis of TC-8020 (stream rhtpa-2.2).
> > No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> > this task will be linked and the `security-preemptive` label removed.
>
> ## Repository
>
> rhtpa-backend
>
> ## Target Branch
>
> release/0.3.z
>
> ## Description
>
> Remediate CVE-2026-55123: use-after-free in task abort in the tokio crate.
> The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed version (1.42.0+).
>
> Affected versions: RHTPA 2.1.0 (tokio 1.40.0), RHTPA 2.1.1 (tokio 1.40.0)
> Source commit(s): v0.3.8, v0.3.12
>
> Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
> Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp
>
> ## Implementation Notes
>
> - Target branch: release/0.3.z
> - **Dependency type**: direct
>
> ### Remediation approach (direct dependency)
>
> When the vulnerable package is a **direct** dependency of a workspace member:
>
> - Update tokio dependency to >= 1.42.0 in Cargo.toml
> - If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)
>
> ## Acceptance Criteria
>
> - [ ] tokio dependency is >= 1.42.0
> - [ ] No other dependency conflicts introduced
> - [ ] Existing tests pass
>
> ## Test Requirements
>
> - [ ] Existing test suite passes with the updated dependency
>
> ## Dependencies
>
> - Depends on: TC-8020 (originating CVE — Related link, cross-stream)

**Jira operations**:
```
preemptive_upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)",
  description: <preemptive-upstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)

# Post description digest comment
jira.add_comment(<preemptive-upstream-task-key>, "[sdlc-workflow] Description digest: sha256-md:<hex>")

# Link to originating CVE with "Related" (not "Depend")
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <preemptive-upstream-task-key>,
  type: "Related"
)
```

### Task 4: Downstream Propagation — Preemptive (rhtpa-2.1)

**Summary**: Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`

**Description**:

> > **Preemptive remediation**: This task was created proactively from cross-stream
> > impact analysis of TC-8020 (stream rhtpa-2.2).
> > No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> > this task will be linked and the `security-preemptive` label removed.
>
> ## Repository
>
> rhtpa-release.0.3.z
>
> ## Target Branch
>
> main
>
> ## Description
>
> Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
> CVE-2026-55123 fix from the preemptive upstream backport task.
>
> The upstream backport bumps tokio to 1.42.0 on release/0.3.z. Once that PR
> merges, update the source pinning in this Konflux release repo so the next
> build ships the fix.
>
> ## Implementation Notes
>
> - Source pinning method: artifacts.lock.yaml (download URL contains tag)
> - **Dependency type**: direct — carried forward from upstream task
> - Update the rhtpa-backend reference to the merged commit or new release tag
> - Verify the Konflux build pipeline triggers successfully
>
> ## Acceptance Criteria
>
> - [ ] rhtpa-backend reference updated to include the fix
> - [ ] Konflux rebuild triggers new container image
>
> ## Test Requirements
>
> - [ ] Container image builds successfully with the updated reference
>
> ## Dependencies
>
> - Depends on: <preemptive-upstream-task-key> (upstream backport must merge first)
> - Depends on: TC-8020 (originating CVE — Related link, cross-stream)

**Jira operations**:
```
preemptive_downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <preemptive-downstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)

# Post description digest comment
jira.add_comment(<preemptive-downstream-task-key>, "[sdlc-workflow] Description digest: sha256-md:<hex>")

# Link downstream blocked by upstream
jira.create_link(
  inwardIssue: <preemptive-upstream-task-key>,
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Blocks"
)

# Link to originating CVE with "Related" (not "Depend")
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Related"
)
```
