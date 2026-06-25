# Step 7 -- Remediation

## Triage Outcome

Based on the version impact analysis:

- **Stream 2.2.x (in-scope)**: Version 2.2.0 is affected (h2 0.4.5 < 0.4.8).
  Versions 2.2.1+ are NOT affected. However, since 2.2.0 shipped with the
  vulnerable dependency and the Affects Versions field includes RHTPA 2.2.0,
  remediation applies to this stream.
- **Stream 2.1.x (cross-stream)**: All versions (2.1.0, 2.1.1) are affected
  (h2 0.4.5 < 0.4.8). This stream has no stream-specific CVE Jira.

This is a combination of **Case A** (affected -- create remediation tasks for
the in-scope stream) and **Case B** (cross-stream impact -- create preemptive
remediation tasks for stream 2.1.x).

## Case A: Remediation Tasks for Stream 2.2.x

Since h2 is a Cargo (source dependency) ecosystem, two tasks are created:
an upstream backport task and a downstream propagation subtask.

Note: Upstream branch `release/0.4.z` already has h2 0.4.9 (fixed). The
upstream backport task may already be satisfied; however, the task is created
for tracking and verification.

### Task 1: Upstream Backport Task (2.2.x)

**Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (2.2.x)

**Labels**: ai-generated-jira, Security, CVE-2026-48901

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed
version (0.4.8+).

Affected versions: 2.2.0 (h2 0.4.5)
Source commit(s): v0.4.5

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

Note: Upstream branch release/0.4.z already has h2 0.4.9 at HEAD.
This task may already be satisfied -- verify and close if so.

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Target branch: release/0.4.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8030 (parent tracking issue)
```

### Task 2: Downstream Propagation Subtask (2.2.x)

**Summary**: Propagate CVE-2026-48901 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: ai-generated-jira, Security, CVE-2026-48901

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-48901 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8+ on release/0.4.z. Once that PR
merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

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
- Depends on: TC-8030 (parent tracking issue)
```

### Linkage (2.2.x)

1. Link upstream task to TC-8030 with type "Depend"
2. Link downstream subtask to TC-8030 with type "Depend"
3. Link downstream subtask as blocked by upstream task with type "Blocks"

## Case B: Cross-Stream Preemptive Remediation for Stream 2.1.x

Stream 2.1.x is also affected (all versions ship h2 0.4.5 < 0.4.8) but has
no stream-specific CVE Jira. Creating preemptive remediation tasks.

Note: Upstream branch `release/0.3.z` still has h2 0.4.5 (NOT fixed). The
upstream backport is required before downstream propagation.

### Task 3: Preemptive Upstream Backport Task (2.1.x)

**Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-48901, security-preemptive

```
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for stream 2.1.x. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed
version (0.4.8+).

Affected versions: 2.1.0 (h2 0.4.5), 2.1.1 (h2 0.4.5)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

Note: Upstream branch release/0.3.z has h2 0.4.5 at HEAD -- upstream
backport is needed.

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8030 (parent tracking issue)
```

### Task 4: Preemptive Downstream Propagation Subtask (2.1.x)

**Summary**: Propagate CVE-2026-48901 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-48901, security-preemptive

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for stream 2.1.x. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-48901 fix from the preemptive upstream backport task.

The upstream backport bumps h2 to 0.4.8+ on release/0.3.z. Once that PR
merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

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
- Depends on: TC-8030 (parent tracking issue)
```

### Linkage (2.1.x -- preemptive)

1. Link preemptive upstream task to TC-8030 with type "Related" (not "Depend" -- cross-stream)
2. Link preemptive downstream subtask to TC-8030 with type "Related"
3. Link preemptive downstream subtask as blocked by preemptive upstream task with type "Blocks"

## Post-Creation Actions

1. Post description digest comment on each created task (per description-digest-protocol.md)
2. Add `ai-cve-triaged` label to TC-8030
3. Post summary comment to TC-8030 listing all created tasks
4. Post cross-stream impact comment to TC-8030:

   > Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock
   > file analysis. Preemptive remediation tasks created for stream 2.1.x
   > (security-preemptive). Stream 2.1.x does not have a stream-specific CVE Jira.

5. Transition TC-8030 to In Progress
6. Assign TC-8030 to current user
