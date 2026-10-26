# Remediation Tasks for TC-8001 (CVE-2026-31812)

## Summary

| Stream | Type | Task Count | Remediation Variant | Labels |
|--------|------|------------|---------------------|--------|
| 2.2.x | Standard | 2 | Dependency bump + downstream propagation | ai-generated-jira, Security, CVE-2026-31812 |
| 2.1.x | Preemptive | 2 | Upstream backport + downstream propagation | ai-generated-jira, Security, CVE-2026-31812, security-preemptive |

---

## Stream 2.2.x -- Standard Remediation (Case B)

The upstream branch `release/0.4.z` already ships quinn-proto 0.11.14 (confirmed at tag v0.4.11+). Remediation uses the dependency bump variant.

### Task 1: Dependency Bump (2.2.x)

**Summary**: Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x)
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`
**Link**: Depend -- TC-8001 (parent Vulnerability issue)

#### Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream --
a package manager update is sufficient.

Affected versions: 2.2.0 (v0.4.5, quinn-proto 0.11.9), 2.2.1 (v0.4.8, quinn-proto 0.11.12), 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (quinn-proto is a Cargo dependency)
- **Remediation action**: run `cargo update -p quinn-proto` to pull in the latest compatible version (>= 0.11.14)
- If the update pulls a version that still falls within the affected range, pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

### Task 2: Downstream Propagation (2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`
**Link**: Depend -- TC-8001 (parent Vulnerability issue)
**Link**: Blocks -- blocked by Task 1 (dependency bump must merge first)

#### Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the dependency bump task.

The dependency bump task updates quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: Task 1 (dependency bump must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Stream 2.1.x -- Preemptive Remediation (Case A)

No sibling CVE Jira exists for stream 2.1.x. The upstream branch `release/0.3.z` does NOT ship the fix (v0.3.12 has quinn-proto 0.11.9). Remediation uses the upstream backport variant. Tasks carry the `security-preemptive` label and are linked with "Related" (not "Depend") to TC-8001.

### Task 3: Upstream Backport (2.1.x, preemptive)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
**Link**: Related -- TC-8001 (originating CVE from 2.2.x stream)

#### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8, quinn-proto 0.11.9), 2.1.1 (v0.3.12, quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (quinn-proto is a Cargo dependency)
- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

### Task 4: Downstream Propagation (2.1.x, preemptive)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
**Link**: Related -- TC-8001 (originating CVE from 2.2.x stream)
**Link**: Blocks -- blocked by Task 3 (upstream backport must merge first)

#### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: Task 3 (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Post-Triage Actions

### Affects Versions Correction
- **Current**: `[RHTPA 2.0.0]`
- **Corrected**: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
- Rationale: RHTPA 2.0.0 does not exist in any configured stream. Lock file analysis at pinned commits confirms versions 2.2.0-2.2.2 ship vulnerable quinn-proto (< 0.11.14). Versions 2.2.3+ ship fixed version 0.11.14. Scoped to 2.2.x stream per issue suffix.

### Labels
- Add `ai-cve-triaged` to TC-8001

### Cross-Stream Impact Comment
Post to TC-8001:
> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis.
> This stream is not tracked by a companion issue and may require separate PSIRT triage.
>
> Preemptive remediation tasks created for stream 2.1.x:
> - Task 3 (upstream backport, security-preemptive)
> - Task 4 (downstream propagation, security-preemptive)
>
> These tasks use the "Related" link type and carry the security-preemptive label.
> When PSIRT creates a stream-specific CVE Jira for 2.1.x, Step 4.4 reconciliation
> will link them and remove the label.

### Post-Triage Summary Comment
Post to TC-8001:
> **Triage Summary for CVE-2026-31812 (quinn-proto)**
>
> **Version Impact:**
>
> | Version | quinn-proto | Affected? | Notes |
> |---------|-------------|-----------|-------|
> | 2.1.0 | 0.11.9 | YES | |
> | 2.1.1 | 0.11.9 | YES | |
> | 2.2.0 | 0.11.9 | YES | |
> | 2.2.1 | 0.11.12 | YES | |
> | 2.2.2 | -- | YES | retag of 2.2.1 |
> | 2.2.3 | 0.11.14 | NO | ships fixed version |
> | 2.2.4 | 0.11.14 | NO | ships fixed version |
>
> **Affects Versions Correction**: `[RHTPA 2.0.0]` --> `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
>
> **Triage Outcome**: Remediation tasks created.
>
> **Standard remediation (2.2.x)**:
> - Task 1: Dependency bump -- update quinn-proto to 0.11.14 on release/0.4.z
> - Task 2: Downstream propagation -- update backend ref in rhtpa-release.0.4.z (blocked by Task 1)
>
> **Preemptive remediation (2.1.x)**:
> - Task 3: Upstream backport -- bump quinn-proto to 0.11.14 on release/0.3.z (security-preemptive)
> - Task 4: Downstream propagation -- update backend ref in rhtpa-release.0.3.z (blocked by Task 3, security-preemptive)
