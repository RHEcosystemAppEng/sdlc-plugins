# Step 8 -- Remediation

## Triage Outcome

- **Issue scope**: 2.2.x stream (from `[rhtpa-2.2]` suffix)
- **Ecosystem**: Cargo (source dependency) -- requires 2 tasks per stream (upstream + downstream)
- **Affected versions in scope (2.2.x)**: 2.2.0, 2.2.1, 2.2.2
- **Fixed versions in scope (2.2.x)**: 2.2.3, 2.2.4
- **Cross-stream impact**: 2.1.x stream also affected (all versions: 2.1.0, 2.1.1)

### Decision

- **Case A** applies: versions in the issue's 2.2.x stream are affected. Create
  remediation tasks for the 2.2.x stream.
- **Case B** applies: the 2.1.x stream (outside this issue's scope) is also affected.
  Post cross-stream impact comment and create preemptive remediation tasks for 2.1.x.

---

## Case A -- Remediation Tasks for 2.2.x Stream

### Task 1: Upstream Backport (2.2.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

#### Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (denial of service).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (quinn-proto 0.11.9), RHTPA 2.2.1 (quinn-proto 0.11.12), RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: to be determined via Cargo.lock dependency chain analysis
- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If quinn-proto is a direct dependency, bump the version in Cargo.toml
- If quinn-proto is a transitive dependency, bump the direct dependency that pulls it in; fall back to pinning quinn-proto directly via `cargo add quinn-proto@0.11.14`

Note: The fix is already present on the release/0.4.z branch as of v0.4.11 (version 2.2.3 ships quinn-proto 0.11.14). Remediation may involve cherry-picking or confirming the fix is on the branch.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

### Task 2: Downstream Propagation (2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

#### Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14 on release/0.4.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
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

---

## Case B -- Cross-Stream Impact and Preemptive Tasks for 2.1.x Stream

### Cross-Stream Impact Comment

The following comment would be posted to TC-8001:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis.
- 2.1.0: quinn-proto 0.11.9 (AFFECTED)
- 2.1.1: quinn-proto 0.11.9 (AFFECTED)

These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

### Preemptive Task 3: Upstream Backport (2.1.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link type**: Related (to TC-8001, because this is a preemptive task for a different stream)

#### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (denial of service).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (quinn-proto 0.11.9), RHTPA 2.1.1 (quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: to be determined via Cargo.lock dependency chain analysis
- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If quinn-proto is a direct dependency, bump the version in Cargo.toml
- If quinn-proto is a transitive dependency, bump the direct dependency that pulls it in; fall back to pinning quinn-proto directly via `cargo add quinn-proto@0.11.14`

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

### Preemptive Task 4: Downstream Propagation (2.1.x)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link type**: Related (to TC-8001, because this is a preemptive task for a different stream)

#### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14 on release/0.3.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task for 2.1.x (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Preemptive Task Comment on TC-8001

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <upstream-task-key> (security-preemptive, upstream backport)
- 2.1.x: <downstream-task-key> (security-preemptive, downstream propagation)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```
