# Step 7 -- Remediation: TC-8001 (CVE-2026-31812)

## Triage Outcome

This issue falls under **Case A** (Affected -- create remediation tasks) for the scoped stream 2.2.x, and **Case B** (Cross-stream impact) for the 2.1.x stream.

### Stream 2.2.x (in scope -- Case A)

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Already fixed in: RHTPA 2.2.3, RHTPA 2.2.4 (ship quinn-proto 0.11.14)

Since the fix is already present in the latest released versions (2.2.3+), and the issue is scoped to the 2.2.x stream, the affected versions (2.2.0, 2.2.1, 2.2.2) are older releases within a stream that has already picked up the fix. Remediation tasks are created to formally track the fix.

### Stream 2.1.x (out of scope -- Case B cross-stream impact)

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
The 2.1.x stream is outside this issue's scope but is affected. If no sibling CVE Jira exists for the 2.1.x stream, preemptive remediation tasks should be created.

---

## Remediation Tasks -- Stream 2.2.x (Case A, standard)

Since quinn-proto is a Cargo (source dependency) ecosystem, **two tasks** are created for this stream.

### Task 1: Upstream Backport Task (2.2.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)
**Labels**: ai-generated-jira, Security, CVE-2026-31812

#### Description

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (DoS).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8, v0.4.9

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)
- Note: tags v0.4.11 and v0.4.12 already ship quinn-proto 0.11.14,
  so the fix may already be present on the release/0.4.z branch HEAD

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

### Task 2: Downstream Propagation Subtask (2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
**Labels**: ai-generated-jira, Security, CVE-2026-31812

#### Description

```
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

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: [upstream-task-key] (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Jira Linkage (2.2.x tasks)

1. Link upstream task to TC-8001 with "Depend"
2. Link downstream task to TC-8001 with "Depend"
3. Link downstream task as blocked by upstream task with "Blocks"
4. Transition TC-8001 to In Progress
5. Assign TC-8001 to current user
6. Add ai-cve-triaged label to TC-8001

---

## Remediation Tasks -- Stream 2.1.x (Case B, preemptive)

The 2.1.x stream is affected (all versions ship quinn-proto 0.11.9) but is outside this issue's stream scope. If no sibling CVE Jira exists for stream 2.1.x (verified via JQL search for CVE-2026-31812 with suffix `[rhtpa-2.1]`), preemptive remediation tasks are created.

### Task 3: Upstream Backport Task (2.1.x, preemptive)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)
**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

#### Description

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (DoS).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

### Task 4: Downstream Propagation Subtask (2.1.x, preemptive)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)
**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

#### Description

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: [upstream-task-key-2.1.x] (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Jira Linkage (2.1.x preemptive tasks)

1. Link upstream preemptive task to TC-8001 with "Related" (not "Depend" -- preemptive cross-stream)
2. Link downstream preemptive task to TC-8001 with "Related"
3. Link downstream preemptive task as blocked by upstream preemptive task with "Blocks"

### Cross-stream Impact Comment

The following comment would be posted to TC-8001:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. All 2.1.x versions (2.1.0, 2.1.1) ship
quinn-proto 0.11.9.

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: [upstream-task-key] (security-preemptive), [downstream-task-key] (security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

---

## Post-Triage Summary

After all triage actions are complete:

1. **Add label**: `ai-cve-triaged` to TC-8001
2. **Post summary comment** to TC-8001 documenting:
   - Version impact table (all streams)
   - Affects Versions correction: `[RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
   - Triage outcome: remediation tasks created for 2.2.x (standard) and 2.1.x (preemptive)
   - Links to all remediation tasks created
   - @mention of the reporter (PSIRT analyst)
