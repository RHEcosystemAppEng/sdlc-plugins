# Step 8 -- Remediation

## Triage Outcome

- **Case A**: Stream 2.2.x (scoped stream) is affected -- versions 2.2.0,
  2.2.1, and 2.2.2 ship vulnerable quinn-proto. Create remediation tasks.
- **Case B**: Cross-stream impact -- stream 2.1.x is also affected (versions
  2.1.0 and 2.1.1 ship quinn-proto 0.11.9). Create preemptive remediation
  tasks for stream 2.1.x (no sibling CVE Jira exists for that stream).

Ecosystem: **Cargo** (source dependency) -- two tasks per stream (upstream
backport + downstream propagation).

---

## Case A: Stream 2.2.x Remediation Tasks

### Task 1 -- Upstream Backport (stream 2.2.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

#### Task Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (v0.4.5), RHTPA 2.2.1 (v0.4.8), RHTPA 2.2.2 (v0.4.8 retag)
Source commit(s): `v0.4.5`, `v0.4.8`

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

Note: The upstream fix is already present on release/0.4.z (quinn-proto 0.11.14
at tag v0.4.11). No new code change is needed on this branch -- the fix was
incorporated in build 0.4.11 (released as RHTPA 2.2.3). This task tracks
confirmation that the upstream branch carries the fix.

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)
- Upstream fix already landed at tag v0.4.11 on this branch -- verify
  the fix is present and no regression was introduced

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

### Task 2 -- Downstream Propagation (stream 2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

#### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

Affected product versions requiring rebuild: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., `v0.4.12`)
- Update the backend reference to the merged commit or new release tag
  that includes quinn-proto >= 0.11.14
- Verify the Konflux build pipeline triggers successfully
- The fix is already present at backend tag v0.4.11+; update the reference
  for affected version rebuilds to pick up the patched source

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

### Jira Linkage (stream 2.2.x)

After creating the above tasks:

1. Link upstream task to TC-8001 with type "Depend"
2. Link downstream task to TC-8001 with type "Depend"
3. Link downstream task as blocked by upstream task with type "Blocks"
4. Post description digest comment on each task per description-digest-protocol

---

## Case B: Cross-Stream Impact -- Stream 2.1.x Preemptive Tasks

Cross-stream impact detected: quinn-proto versions before 0.11.14 also affects
stream 2.1.x (versions RHTPA 2.1.0 and 2.1.1 ship quinn-proto 0.11.9).

No sibling CVE Jira exists for stream 2.1.x. Creating preemptive remediation
tasks with `security-preemptive` label and "Related" link type.

### Proposed Cross-Stream Impact Comment on TC-8001

```
Cross-stream impact: quinn-proto versions before 0.11.14 also affects stream
2.1.x based on lock file analysis. Versions RHTPA 2.1.0 and 2.1.1 ship
quinn-proto 0.11.9. This stream does not have its own CVE Jira.

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <upstream-task-key> (security-preemptive, upstream backport)
- 2.1.x: <downstream-task-key> (security-preemptive, downstream propagation)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.

---
This comment was AI-generated by sdlc-workflow/triage-security v0.11.1.
```

### Task 3 -- Upstream Backport (stream 2.1.x, preemptive)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

#### Task Description

## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (v0.3.8), RHTPA 2.1.1 (v0.3.12)
Source commit(s): `v0.3.8`, `v0.3.12`

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

Note: The upstream fix is NOT present on release/0.3.z. Both tags v0.3.8 and
v0.3.12 ship quinn-proto 0.11.9. A backport of the quinn-proto bump is required
on this branch.

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)
- The upstream fix (quinn-rs/quinn#2048) must be picked up by bumping
  the quinn-proto crate version in the lock file

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

### Task 4 -- Downstream Propagation (stream 2.1.x, preemptive)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

#### Task Description

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

Affected product versions requiring rebuild: RHTPA 2.1.0, RHTPA 2.1.1.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., `v0.3.12`)
- Update the backend reference to the merged commit or new release tag
  that includes quinn-proto >= 0.11.14
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task for 2.1.x (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

### Jira Linkage (stream 2.1.x, preemptive)

After creating the above preemptive tasks:

1. Link upstream task to TC-8001 with type "Related" (not "Depend" -- preemptive)
2. Link downstream task to TC-8001 with type "Related" (not "Depend" -- preemptive)
3. Link downstream task as blocked by upstream task with type "Blocks"
4. Post description digest comment on each task per description-digest-protocol
