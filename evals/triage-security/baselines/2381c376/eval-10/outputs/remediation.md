# Step 8 -- Remediation: TC-8020

## Triage Decision

- Issue scoped to stream: **rhtpa-2.2**
- Affected versions in scope: RHTPA 2.2.0, 2.2.1, 2.2.2 (retag)
- Cross-stream impact: rhtpa-2.1 also affected (no sibling CVE Jira exists)
- Ecosystem: **Cargo** (source dependency) -- 2 tasks per stream
- Outcome: **Case A** (cross-stream impact) + **Case B** (create remediation tasks)

---

## Case B: Standard Remediation Tasks for Current Stream (rhtpa-2.2)

These tasks are linked to TC-8020 with "Depend" link type.

### Task 1: Upstream -- Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)

**Proposed Jira action -- create issue (not executed):**

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
> Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 (retag of 2.2.1)
> Source commit(s): v0.4.5, v0.4.8
>
> Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
> Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp
>
> ## Implementation Notes
>
> - Target branch: release/0.4.z
> - **Dependency type**: to be confirmed via lock file / manifest analysis
> - Run `cargo update -p tokio` to pull in tokio >= 1.42.0
> - If the update pulls a version still within the affected range,
>   pin explicitly: `cargo add tokio@1.42.0`
> - Verify Cargo.lock reflects tokio >= 1.42.0 after the update
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

**Proposed post-creation actions:**
1. Post description digest comment on the new task
2. Link: `jira.create_link(inwardIssue: "TC-8020", outwardIssue: "<upstream-task-key>", type: "Depend")`

### Task 2: Downstream -- Propagate CVE-2026-55123 fix to rhtpa-release.0.4.z (rhtpa-2.2)

**Proposed Jira action -- create issue (not executed):**

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
> CVE-2026-55123 fix from the upstream task.
>
> The upstream task bumps tokio to 1.42.0
> on release/0.4.z. Once that PR merges, update the source pinning in this
> Konflux release repo so the next build ships the fix.
>
> ## Implementation Notes
>
> - Source pinning method: `artifacts.lock.yaml` (download URL contains tag)
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
> - Depends on: upstream task (upstream backport/bump must merge first)
> - Depends on: TC-8020 (parent tracking issue)

**Proposed post-creation actions:**
1. Post description digest comment on the new task
2. Link: `jira.create_link(inwardIssue: "TC-8020", outwardIssue: "<downstream-task-key>", type: "Depend")`
3. Link: `jira.create_link(inwardIssue: "<upstream-task-key>", outwardIssue: "<downstream-task-key>", type: "Blocks")`

---

## Case A: Preemptive Remediation Tasks for Cross-Stream (rhtpa-2.1)

Stream rhtpa-2.1 is affected (tokio 1.40.0 < 1.42.0) but **no sibling CVE Jira exists** for this stream. Preemptive remediation tasks are created with the `security-preemptive` label and linked to the originating CVE TC-8020 with "Related" (not "Depend").

### Preemptive Task 1: Upstream -- Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)

**Proposed Jira action -- create issue (not executed):**

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
> > No stream-specific CVE Jira exists yet for stream rhtpa-2.1. When PSIRT creates one,
> > this task will be linked and the `security-preemptive` label removed.
>
> Remediate CVE-2026-55123: Use-after-free in task abort in tokio.
> The vulnerable dependency (tokio < 1.42.0) must be updated
> to the fixed version (1.42.0+).
>
> Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
> Source commit(s): v0.3.8, v0.3.12
>
> Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
> Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp
>
> ## Implementation Notes
>
> - Target branch: release/0.3.z
> - **Dependency type**: to be confirmed via lock file / manifest analysis
> - Run `cargo update -p tokio` to pull in tokio >= 1.42.0
> - If the update pulls a version still within the affected range,
>   pin explicitly: `cargo add tokio@1.42.0`
> - Verify Cargo.lock reflects tokio >= 1.42.0 after the update
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
> - Related to: TC-8020 (originating CVE from stream rhtpa-2.2)

**Proposed post-creation actions:**
1. Post description digest comment on the new task
2. Link: `jira.create_link(inwardIssue: "TC-8020", outwardIssue: "<preemptive-upstream-task-key>", type: "Related")`

### Preemptive Task 2: Downstream -- Propagate CVE-2026-55123 fix to rhtpa-release.0.3.z (rhtpa-2.1)

**Proposed Jira action -- create issue (not executed):**

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
> > No stream-specific CVE Jira exists yet for stream rhtpa-2.1. When PSIRT creates one,
> > this task will be linked and the `security-preemptive` label removed.
>
> Update backend reference in rhtpa-release.0.3.z to pick up the
> CVE-2026-55123 fix from the preemptive upstream task.
>
> The upstream task bumps tokio to 1.42.0
> on release/0.3.z. Once that PR merges, update the source pinning in this
> Konflux release repo so the next build ships the fix.
>
> ## Implementation Notes
>
> - Source pinning method: `artifacts.lock.yaml` (download URL contains tag)
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
> - Depends on: preemptive upstream task (upstream backport/bump must merge first)
> - Related to: TC-8020 (originating CVE from stream rhtpa-2.2)

**Proposed post-creation actions:**
1. Post description digest comment on the new task
2. Link: `jira.create_link(inwardIssue: "TC-8020", outwardIssue: "<preemptive-downstream-task-key>", type: "Related")`
3. Link: `jira.create_link(inwardIssue: "<preemptive-upstream-task-key>", outwardIssue: "<preemptive-downstream-task-key>", type: "Blocks")`

---

## Post-Triage Summary (Proposed Actions)

### 1. Add `ai-cve-triaged` label to TC-8020

**Proposed action (not executed):**
```
jira.edit_issue("TC-8020", fields={
  "labels": ["CVE-2026-55123", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### 2. Post summary comment on TC-8020

**Proposed action (not executed):**

Post a comment to TC-8020 documenting:
1. Version impact table (all streams)
2. Affects Versions status (no correction needed)
3. Triage outcome: remediation tasks created for rhtpa-2.2, preemptive tasks created for rhtpa-2.1
4. Links to all remediation tasks (4 total: 2 standard for rhtpa-2.2, 2 preemptive for rhtpa-2.1)
5. Cross-stream impact notice for rhtpa-2.1

### Pre-Creation Checklist

- [x] **Task count per stream**: Cargo (source dependency) -- 2 tasks per stream (upstream + downstream). rhtpa-2.2: 2 tasks. rhtpa-2.1: 2 preemptive tasks.
- [x] **Cross-stream coverage**: rhtpa-2.1 (outside issue scope) has no sibling CVE Jira -- preemptive tasks created.
- [x] **Link types**: "Depend" for standard tasks linked to TC-8020, "Related" for preemptive tasks linked to TC-8020, "Blocks" for upstream-to-downstream within each stream.
- [x] **Preemptive labels**: rhtpa-2.1 tasks carry `security-preemptive` label.
- [x] **Coordination guidance**: omitted (no Deployment Context column in Source Repositories table).
