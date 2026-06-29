# Remediation — CVE-2026-55123 (tokio < 1.42.0)

## Case A: Standard Remediation Tasks (stream rhtpa-2.2)

The current issue TC-8020 is scoped to stream rhtpa-2.2. Both RHTPA 2.2.0 and RHTPA 2.2.1 are affected (tokio 1.41.1 < 1.42.0). Standard remediation tasks are created for this stream.

### Task 1: Upstream Backport Task

**Jira Creation:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

**Labels**: `["ai-generated-jira", "Security", "CVE-2026-55123"]`

**Link to TC-8020**: Depend (inward: TC-8020, outward: upstream-task-key)

**Description:**

> ## Repository
>
> backend
>
> ## Target Branch
>
> release/0.4.z
>
> ## Description
>
> Remediate CVE-2026-55123: Use-after-free in task abort in tokio.
> The vulnerable dependency (tokio < 1.42.0) must be updated
> to the fixed version (1.42.0+).
>
> Affected versions: RHTPA 2.2.0, RHTPA 2.2.1
> Source commit(s): v0.4.5 (2.2.0), v0.4.8 (2.2.1)
>
> Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
> Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp
>
> ## Implementation Notes
>
> - Update tokio dependency to >= 1.42.0 in Cargo.lock
> - Target branch: release/0.4.z
> - Check for pinned versions or transitive dependency constraints
>   that might prevent the bump
> - If a direct bump introduces breaking changes, assess whether a
>   code-level workaround is viable (see upstream changelog)
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

### Task 2: Downstream Propagation Subtask

**Jira Creation:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

**Labels**: `["ai-generated-jira", "Security", "CVE-2026-55123"]`

**Link to upstream task**: Blocks (inward: upstream-task-key, outward: downstream-task-key)

**Link to TC-8020**: Depend (inward: TC-8020, outward: downstream-task-key)

**Description:**

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
> Update backend reference in rhtpa-release.0.4.z to pick up the
> CVE-2026-55123 fix from the upstream backport task.
>
> The upstream backport bumps tokio to 1.42.0
> on release/0.4.z. Once that PR merges, update the source pinning in this
> Konflux release repo so the next build ships the fix.
>
> ## Implementation Notes
>
> - Source pinning method: artifacts.lock.yaml (download URL contains tag)
> - Update the backend reference to the merged commit or new release tag
> - Verify the Konflux build pipeline triggers successfully
>
> ## Acceptance Criteria
>
> - [ ] backend reference updated to include the fix
> - [ ] Konflux rebuild triggers new container image
>
> ## Test Requirements
>
> - [ ] Container image builds successfully with the updated reference
>
> ## Dependencies
>
> - Depends on: upstream-task-key (upstream backport must merge first)
> - Depends on: TC-8020 (parent tracking issue)

### Jira Linkage (Case A)

1. Link upstream task to TC-8020 with type "Depend"
2. Link downstream task to TC-8020 with type "Depend"
3. Link downstream task blocked by upstream task with type "Blocks"
4. Transition TC-8020 to In Progress
5. Assign TC-8020 to current user

---

## Case B: Preemptive Remediation Tasks (stream rhtpa-2.1)

Stream rhtpa-2.1 is affected (tokio 1.40.0 < 1.42.0) but has **no CVE Jira** for CVE-2026-55123. Preemptive remediation tasks are created with the `security-preemptive` label.

### Preemptive Task 1: Upstream Backport Task (rhtpa-2.1)

**Jira Creation:**
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

**Link to TC-8020**: Related (not Depend -- because TC-8020 belongs to a different stream)

**Description:**

> ## Repository
>
> backend
>
> ## Target Branch
>
> release/0.3.z
>
> ## Description
>
> > **Preemptive remediation**: This task was created proactively from cross-stream
> > impact analysis of TC-8020 (stream rhtpa-2.2).
> > No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> > this task will be linked and the `security-preemptive` label removed.
>
> Remediate CVE-2026-55123: Use-after-free in task abort in tokio.
> The vulnerable dependency (tokio < 1.42.0) must be updated
> to the fixed version (1.42.0+).
>
> Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
> Source commit(s): v0.3.8 (2.1.0), v0.3.12 (2.1.1)
>
> Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
> Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp
>
> ## Implementation Notes
>
> - Update tokio dependency to >= 1.42.0 in Cargo.lock
> - Target branch: release/0.3.z
> - Check for pinned versions or transitive dependency constraints
>   that might prevent the bump
> - If a direct bump introduces breaking changes, assess whether a
>   code-level workaround is viable (see upstream changelog)
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
> - Related to: TC-8020 (originating CVE Jira, stream rhtpa-2.2)

### Preemptive Task 2: Downstream Propagation Subtask (rhtpa-2.1)

**Jira Creation:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Labels**: `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]`

**Link to TC-8020**: Related (not Depend)

**Link to preemptive upstream task**: Blocks (inward: preemptive-upstream-task-key, outward: preemptive-downstream-task-key)

**Description:**

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
> > **Preemptive remediation**: This task was created proactively from cross-stream
> > impact analysis of TC-8020 (stream rhtpa-2.2).
> > No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> > this task will be linked and the `security-preemptive` label removed.
>
> Update backend reference in rhtpa-release.0.3.z to pick up the
> CVE-2026-55123 fix from the upstream backport task.
>
> The upstream backport bumps tokio to 1.42.0
> on release/0.3.z. Once that PR merges, update the source pinning in this
> Konflux release repo so the next build ships the fix.
>
> ## Implementation Notes
>
> - Source pinning method: artifacts.lock.yaml (download URL contains tag)
> - Update the backend reference to the merged commit or new release tag
> - Verify the Konflux build pipeline triggers successfully
>
> ## Acceptance Criteria
>
> - [ ] backend reference updated to include the fix
> - [ ] Konflux rebuild triggers new container image
>
> ## Test Requirements
>
> - [ ] Container image builds successfully with the updated reference
>
> ## Dependencies
>
> - Depends on: preemptive-upstream-task-key (upstream backport must merge first)
> - Related to: TC-8020 (originating CVE Jira, stream rhtpa-2.2)

### Jira Linkage (Case B -- Preemptive)

1. Link preemptive upstream task to TC-8020 with type **"Related"** (not "Depend")
2. Link preemptive downstream task to TC-8020 with type **"Related"** (not "Depend")
3. Link preemptive downstream task blocked by preemptive upstream task with type "Blocks"
