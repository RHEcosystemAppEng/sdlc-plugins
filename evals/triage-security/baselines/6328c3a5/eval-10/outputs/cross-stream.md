# Cross-Stream Impact Analysis: TC-8020

## Case A: Cross-Stream Impact Detected

The issue TC-8020 is scoped to stream **rhtpa-2.2**. Version impact analysis reveals
that stream **rhtpa-2.1** is also affected (tokio 1.40.0, threshold 1.42.0).

## Step 4 -- Sibling CVE Jira Search

JQL search for sibling Vulnerability issues with label CVE-2026-55123:

```
project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020
```

**Result**: No sibling Vulnerability issues found for CVE-2026-55123 in stream rhtpa-2.1.

## Cross-Stream Impact Comment

The following comment would be posted to TC-8020:

---

Cross-stream impact: tokio < 1.42.0 also affects stream rhtpa-2.1 based on lock file analysis.

| Version | Stream | tokio version | Affected? |
|---------|--------|---------------|-----------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES |

No sibling CVE Jira exists for stream rhtpa-2.1. Preemptive remediation tasks have been
created (see below). When PSIRT creates a stream-specific CVE Jira for rhtpa-2.1, Step 4.4
reconciliation will link it and remove the `security-preemptive` label.

---

## Preemptive Remediation Tasks for rhtpa-2.1 (Case A)

Since no CVE Jira exists for stream rhtpa-2.1, preemptive remediation tasks are created
using the same templates as Case B but with the preemptive variant.

### Preemptive Task 1: Upstream Backport / Dependency Bump (rhtpa-2.1)

```
Summary: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)
Issue Type: Task
Labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
Link Type: Related (to TC-8020, not Depend -- because the originating CVE belongs to a different stream)
```

#### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-55123: use-after-free in tokio task abort.
The vulnerable dependency (tokio < 1.42.0) must be updated
to the fixed version (1.42.0+).

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- **Remediation action**: run `cargo update -p tokio` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range, pin explicitly: `cargo add tokio@1.42.0`
- Verify the lock file reflects >= 1.42.0 after the update

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8020 (originating CVE -- Related link, different stream)

#### Jira Linkage

- Link to TC-8020 with type "Related" (not "Depend" -- preemptive task for a different stream)

---

### Preemptive Task 2: Downstream Propagation (rhtpa-2.1)

```
Summary: Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)
Issue Type: Task
Labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
Link Type: Related (to TC-8020 -- preemptive task for a different stream)
```

#### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-55123 fix from the upstream preemptive task.

The upstream task bumps tokio to 1.42.0
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

- Depends on: preemptive upstream task (upstream task must merge first)
- Related to: TC-8020 (originating CVE from different stream)

#### Jira Linkage

- Link to TC-8020 with type "Related" (preemptive -- originating CVE belongs to rhtpa-2.2)
- Link to preemptive upstream task with type "Blocks" (inward: upstream task, outward: this task)

---

## Preemptive Task Comment for TC-8020

The following comment would be posted to TC-8020 documenting the preemptive tasks:

---

Preemptive remediation tasks created for streams without CVE Jiras:
- rhtpa-2.1: {{preemptive-upstream-task.key}} (upstream bump, security-preemptive), {{preemptive-downstream-task.key}} (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.

---

## Reconciliation (Step 4.4)

When PSIRT subsequently creates a CVE Jira for stream rhtpa-2.1 (e.g., TC-XXXX with summary
"CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.1]"), the following reconciliation
will occur during that issue's triage:

1. Step 4.4 searches for preemptive tasks matching CVE-2026-55123 with label `security-preemptive`
2. Finds the preemptive upstream and downstream tasks created above
3. Links the new CVE Jira (TC-XXXX) to the preemptive tasks with "Depend" (standard remediation linkage)
4. Removes the `security-preemptive` label from both tasks
5. Skips new remediation task creation for rhtpa-2.1 (tasks already exist)

## Summary

| Stream | CVE Jira Exists? | Remediation Type | Task Count | Link Type to CVE |
|--------|-----------------|------------------|------------|-----------------|
| rhtpa-2.2 | Yes (TC-8020) | Standard (Case B) | 2 (upstream + downstream) | Depend |
| rhtpa-2.1 | No | Preemptive (Case A) | 2 (upstream + downstream) | Related (to TC-8020) |
