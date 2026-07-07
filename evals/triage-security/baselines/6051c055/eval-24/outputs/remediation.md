# Step 8 -- Remediation: TC-8001

## Triage Outcome Summary

- **CVE**: CVE-2026-31812
- **Library**: quinn-proto (Cargo ecosystem)
- **Fix threshold**: >= 0.11.14
- **Issue scope**: Stream 2.2.x (from summary suffix `[rhtpa-2.2]`)

### Stream 2.2.x (in-scope) -- Already fixed

The latest released versions in stream 2.2.x (2.2.3 and 2.2.4) already ship quinn-proto 0.11.14, which is at or above the fix threshold. The upstream branch `release/0.4.z` also has the fix at HEAD. No remediation task is needed for this stream -- the fix was picked up organically in the 0.4.11 build.

Affected versions (2.2.0, 2.2.1, 2.2.2) are historical releases that shipped vulnerable quinn-proto versions. The Affects Versions field is corrected to reflect these.

### Stream 2.1.x (cross-stream) -- Case B: Preemptive remediation

All versions in stream 2.1.x (2.1.0, 2.1.1) ship quinn-proto 0.11.9, which is within the affected range. The upstream branch `release/0.3.z` has NOT been fixed (still at 0.11.9). No stream-specific CVE Jira exists for 2.1.x.

Case B applies: create preemptive remediation tasks for stream 2.1.x with `security-preemptive` label and "Related" link type to TC-8001.

---

## Preemptive Upstream Backport Task (Stream 2.1.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

**Link**: Related to TC-8001

### Task Description

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (quinn-proto 0.11.9), 2.1.1 (quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
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

---

## Preemptive Downstream Propagation Subtask (Stream 2.1.x)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

**Link**: Related to TC-8001; Blocked by upstream backport task above

### Task Description

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
