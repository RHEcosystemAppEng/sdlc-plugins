# Step 7 -- Remediation

## Triage Outcome

This issue falls under **Case A** (affected -- create remediation tasks) for the 2.2.x stream, combined with **Case B** (cross-stream impact) for the 2.1.x stream.

- **2.2.x stream** (issue scope): Versions 2.2.0, 2.2.1, 2.2.2 are affected. The upstream fix already exists on `release/0.4.z`. Remediation requires creating tasks.
- **2.1.x stream** (cross-stream): All versions (2.1.0, 2.1.1) are affected. The upstream fix does NOT exist on `release/0.3.z`. Preemptive remediation tasks are needed since this stream has no CVE Jira of its own (assuming no sibling issue found).

Ecosystem: **Cargo** (source dependency) -- requires **two tasks per stream** (upstream backport + downstream propagation).

---

## Case A: 2.2.x Stream Remediation Tasks (Issue Scope)

### Task 1: Upstream Backport Task (2.2.x)

**Summary:** Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description:**

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
> Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
> The vulnerable dependency (quinn-proto < 0.11.14) must be updated
> to the fixed version (0.11.14+).
>
> Affected versions: RHTPA 2.2.0 (quinn-proto 0.11.9), RHTPA 2.2.1 (quinn-proto 0.11.12), RHTPA 2.2.2 (retag of 2.2.1)
> Source commit(s): v0.4.5, v0.4.8
>
> Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
> Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq
>
> ## Implementation Notes
>
> - Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
> - Target branch: release/0.4.z
> - Note: The fix is already present at the HEAD of release/0.4.z (v0.4.11+ ships 0.11.14). Verify whether the branch tip already contains the fix -- if so, this task may only require a downstream propagation to rebuild affected versions.
> - Check for pinned versions or transitive dependency constraints that might prevent the bump
>
> ## Acceptance Criteria
>
> - [ ] quinn-proto dependency is >= 0.11.14
> - [ ] No other dependency conflicts introduced
> - [ ] Existing tests pass
>
> ## Test Requirements
>
> - [ ] Existing test suite passes with the updated dependency
>
> ## Dependencies
>
> - Depends on: TC-8001 (parent tracking issue)

### Task 2: Downstream Propagation Subtask (2.2.x)

**Summary:** Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`

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
> Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
> CVE-2026-31812 fix from the upstream backport task.
>
> The upstream backport bumps quinn-proto to 0.11.14
> on release/0.4.z. Once that PR merges, update the source pinning in this
> Konflux release repo so the next build ships the fix.
>
> ## Implementation Notes
>
> - Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
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
> - Depends on: upstream backport task (upstream backport must merge first)
> - Depends on: TC-8001 (parent tracking issue)

### Jira Linkage (2.2.x)

```
# Link upstream task to CVE
jira.create_link(inwardIssue: "TC-8001", outwardIssue: "<upstream-task-key>", type: "Depend")

# Link downstream subtask as blocked by upstream task
jira.create_link(inwardIssue: "<upstream-task-key>", outwardIssue: "<downstream-task-key>", type: "Blocks")

# Link downstream subtask to CVE
jira.create_link(inwardIssue: "TC-8001", outwardIssue: "<downstream-task-key>", type: "Depend")
```

---

## Case B: 2.1.x Stream Preemptive Remediation Tasks (Cross-Stream Impact)

The 2.1.x stream is also affected (all versions ship quinn-proto 0.11.9) but has no stream-specific CVE Jira. Preemptive remediation tasks are created with the `security-preemptive` label and "Related" link type.

### Task 3: Upstream Backport Task (2.1.x, Preemptive)

**Summary:** Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Description:**

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.
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
> Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
> The vulnerable dependency (quinn-proto < 0.11.14) must be updated
> to the fixed version (0.11.14+).
>
> Affected versions: RHTPA 2.1.0 (quinn-proto 0.11.9), RHTPA 2.1.1 (quinn-proto 0.11.9)
> Source commit(s): v0.3.8, v0.3.12
>
> Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
> Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq
>
> ## Implementation Notes
>
> - Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
> - Target branch: release/0.3.z
> - Note: The upstream fix is NOT yet present on release/0.3.z. A backport of the quinn-proto bump is required on this branch.
> - Check for pinned versions or transitive dependency constraints that might prevent the bump
> - If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)
>
> ## Acceptance Criteria
>
> - [ ] quinn-proto dependency is >= 0.11.14
> - [ ] No other dependency conflicts introduced
> - [ ] Existing tests pass
>
> ## Test Requirements
>
> - [ ] Existing test suite passes with the updated dependency
>
> ## Dependencies
>
> - Depends on: TC-8001 (parent tracking issue)

### Task 4: Downstream Propagation Subtask (2.1.x, Preemptive)

**Summary:** Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Description:**

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.
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
> CVE-2026-31812 fix from the upstream backport task.
>
> The upstream backport bumps quinn-proto to 0.11.14
> on release/0.3.z. Once that PR merges, update the source pinning in this
> Konflux release repo so the next build ships the fix.
>
> ## Implementation Notes
>
> - Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
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
> - Depends on: upstream backport task for 2.1.x (upstream backport must merge first)
> - Depends on: TC-8001 (parent tracking issue)

### Jira Linkage (2.1.x Preemptive)

```
# Link preemptive upstream task to CVE with "Related" (not "Depend")
jira.create_link(inwardIssue: "TC-8001", outwardIssue: "<preemptive-upstream-task-key>", type: "Related")

# Link preemptive downstream subtask as blocked by preemptive upstream task
jira.create_link(inwardIssue: "<preemptive-upstream-task-key>", outwardIssue: "<preemptive-downstream-task-key>", type: "Blocks")

# Link preemptive downstream subtask to CVE with "Related"
jira.create_link(inwardIssue: "TC-8001", outwardIssue: "<preemptive-downstream-task-key>", type: "Related")
```

---

## Cross-Stream Impact Comment

The following comment would be posted to TC-8001:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis.
All versions in the 2.1.x stream (RHTPA 2.1.0, RHTPA 2.1.1) ship quinn-proto 0.11.9.

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <upstream-task-key> (upstream backport, security-preemptive)
- 2.1.x: <downstream-task-key> (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive label.
When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link
them and remove the label.
```

---

## Summary of All Remediation Tasks

| # | Stream | Type | Summary | Labels |
|---|--------|------|---------|--------|
| 1 | 2.2.x | Upstream backport | Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2) | ai-generated-jira, Security, CVE-2026-31812 |
| 2 | 2.2.x | Downstream propagation | Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2) | ai-generated-jira, Security, CVE-2026-31812 |
| 3 | 2.1.x | Upstream backport (preemptive) | Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive |
| 4 | 2.1.x | Downstream propagation (preemptive) | Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive |
