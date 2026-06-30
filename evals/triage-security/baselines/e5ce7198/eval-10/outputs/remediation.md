# Step 7 -- Remediation: TC-8020

## Triage Outcome

- **Case A** (current stream 2.2.x): Affected -- create remediation tasks
- **Case B** (cross-stream 2.1.x): Also affected, no CVE Jira exists -- create preemptive remediation tasks

## Case A -- Remediation Tasks for Stream 2.2.x (Issue Scope)

The issue stream (rhtpa-2.2) has affected versions RHTPA 2.2.0, 2.2.1, and 2.2.2.
Ecosystem is Cargo (source dependency) so two tasks are needed: upstream backport + downstream propagation.

### Task 1: Upstream Backport (rhtpa-2.2)

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

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: tokio use-after-free in task abort.
The vulnerable dependency (tokio < 1.42.0) must be updated
to the fixed version (1.42.0+).

Affected versions: RHTPA 2.2.0 (v0.4.5), RHTPA 2.2.1 (v0.4.8), RHTPA 2.2.2 (retag of 2.2.1)
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

---

**Post-creation actions (proposed):**
- Post description digest comment on the upstream task
- Link upstream task to TC-8020 with type "Depend"

### Task 2: Downstream Propagation (rhtpa-2.2)

**Proposed Jira issue creation:**

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

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-55123 fix from the upstream backport task.

The upstream backport bumps tokio to 1.42.0
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

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8020 (parent tracking issue)

---

**Post-creation actions (proposed):**
- Post description digest comment on the downstream task
- Link downstream task to TC-8020 with type "Depend"
- Link downstream task as blocked by upstream task with type "Blocks"

## Case B -- Preemptive Remediation Tasks for Stream 2.1.x

Stream 2.1.x is affected (tokio 1.40.0 < 1.42.0) but has **no CVE Jira**.
JQL search for sibling CVE Jiras with label CVE-2026-55123 in stream rhtpa-2.1 returned no results.
Preemptive remediation tasks are created per Step 7 Case B and the Preemptive Task Variant
in remediation-templates.md.

### Preemptive Task 1: Upstream Backport (rhtpa-2.1)

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

## Repository

rhtpa-backend

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

- Depends on: TC-8020 (parent tracking issue -- originating CVE, different stream)

---

**Post-creation actions (proposed):**
- Post description digest comment on the preemptive upstream task
- Link to TC-8020 with type **"Related"** (not "Depend" -- preemptive cross-stream linkage)

### Preemptive Task 2: Downstream Propagation (rhtpa-2.1)

**Proposed Jira issue creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Task description:**

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
CVE-2026-55123 fix from the preemptive upstream backport task.

The upstream backport bumps tokio to 1.42.0
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

- Depends on: preemptive upstream backport task (upstream backport must merge first)
- Depends on: TC-8020 (parent tracking issue -- originating CVE, different stream)

---

**Post-creation actions (proposed):**
- Post description digest comment on the preemptive downstream task
- Link to TC-8020 with type **"Related"** (not "Depend" -- preemptive cross-stream linkage)
- Link downstream as blocked by preemptive upstream task with type "Blocks"
- Add `security-preemptive` label

## Post-Triage Summary

### Proposed actions:

1. **Add label** `ai-cve-triaged` to TC-8020
2. **Post summary comment** to TC-8020 documenting:
   - Version impact table (all streams)
   - Affects Versions correction (if needed -- current values RHTPA 2.2.0, RHTPA 2.2.1 match the 2.2.x stream scope)
   - Remediation tasks created (Case A for 2.2.x, Case B preemptive for 2.1.x)
   - @mention of the issue reporter (account ID from Jira issue data)
3. **Transition** TC-8020 to In Progress
4. **Assign** TC-8020 to the current user

All actions are proposed and require engineer confirmation before execution.
