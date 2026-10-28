# Step 8 -- Remediation

## Triage Decision

**Case B: Affected -- create remediation tasks** for the scoped stream (2.2.x).

**Case A: Cross-stream impact** -- stream 2.1.x is also affected and is outside this issue's scope. Preemptive remediation tasks are created for 2.1.x (if no sibling CVE Jira exists).

## Remediation Tasks for Stream 2.2.x (Scoped)

Since Step 2.5 confirms the upstream branch `release/0.4.z` already ships quinn-proto 0.11.14, the **dependency bump variant** is used (not the upstream backport variant).

### Task 1: Dependency Bump Task (2.2.x)

**Summary**: Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`
**Link**: Depend (TC-8001 inward, this task outward)

#### Description

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto versions before 0.11.14) is already fixed
upstream -- a package manager update is sufficient.

Affected versions: 2.2.0 (v0.4.5), 2.2.1 (v0.4.8), 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (quinn-proto is a direct Cargo dependency)
- **Remediation action**: run `cargo update -p quinn-proto` to pull in the latest
  compatible version (>= 0.11.14)
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
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
```

### Task 2: Downstream Propagation Task (2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`
**Links**:
- Depend (TC-8001 inward, this task outward)
- Blocks (Task 1 inward, this task outward) -- blocked by the dependency bump task

#### Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-31812 fix
from the dependency bump task.

The dependency bump task bumps quinn-proto to 0.11.14 on release/0.4.z. Once that
PR merges, update the source pinning in this Konflux release repo so the next build
ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: dependency bump task (upstream fix must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

## Preemptive Remediation Tasks for Stream 2.1.x (Case A -- Cross-Stream)

Stream 2.1.x is affected (2.1.0 and 2.1.1 both ship quinn-proto 0.11.9) but is outside this issue's scope. If no sibling CVE Jira exists for stream 2.1.x, preemptive remediation tasks are created.

The upstream branch `release/0.3.z` does NOT yet ship the fix (quinn-proto 0.11.9 at HEAD), so the **upstream backport variant** is used for 2.1.x.

### Preemptive Task 1: Upstream Backport Task (2.1.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
**Link**: Related (TC-8001 inward, this task outward) -- Related, not Depend, because this is preemptive

#### Description

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for this stream. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto vulnerability (panic on large stream counts).
The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8), 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (quinn-proto is a direct Cargo dependency)
- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- The upstream branch release/0.3.z currently ships quinn-proto 0.11.9 --
  a direct dependency bump is required

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

### Preemptive Task 2: Downstream Propagation Task (2.1.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
**Links**:
- Related (TC-8001 inward, this task outward) -- preemptive
- Blocks (Preemptive Task 1 inward, this task outward) -- blocked by the upstream backport

#### Description

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for this stream. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-31812 fix
from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14 on release/0.3.z. Once
that PR merges, update the source pinning in this Konflux release repo so the next
build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream fix must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

## Link Topology Summary

### Standard remediation (2.2.x -- scoped)

| Link Type | Inward Issue | Outward Issue | Purpose |
|-----------|-------------|---------------|---------|
| Depend | TC-8001 (CVE) | Dependency Bump Task | CVE tracks remediation |
| Depend | TC-8001 (CVE) | Downstream Propagation Task | CVE tracks remediation |
| Blocks | Dependency Bump Task | Downstream Propagation Task | Downstream blocked by upstream |

### Preemptive remediation (2.1.x -- cross-stream)

| Link Type | Inward Issue | Outward Issue | Purpose |
|-----------|-------------|---------------|---------|
| Related | TC-8001 (CVE) | Upstream Backport Task | Cross-stream preemptive |
| Related | TC-8001 (CVE) | Downstream Propagation Task | Cross-stream preemptive |
| Blocks | Upstream Backport Task | Downstream Propagation Task | Downstream blocked by upstream |

## Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8001
2. Post summary comment to TC-8001 documenting:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2)
   - Remediation tasks created for stream 2.2.x (dependency bump + downstream propagation)
   - Preemptive tasks created for stream 2.1.x (upstream backport + downstream propagation)
   - Cross-stream impact notice
