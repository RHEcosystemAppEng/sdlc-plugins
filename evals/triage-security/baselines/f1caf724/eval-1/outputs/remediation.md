# Step 8 -- Remediation

## Triage Outcome

TC-8001 is a **scoped** issue for stream **2.2.x**. The version impact analysis shows:

- **Stream 2.2.x** (in scope): versions 2.2.0, 2.2.1, 2.2.2 are affected -- **Case B applies**
- **Stream 2.1.x** (out of scope): versions 2.1.0, 2.1.1 are also affected -- **Case A applies** (cross-stream impact)

Ecosystem: **Cargo** (source dependency) -- 2 tasks per affected stream (upstream backport + downstream propagation).

---

## Case A: Cross-Stream Impact (2.1.x)

The 2.1.x stream is affected but outside this issue's scope. Post a cross-stream impact comment on TC-8001, and create preemptive remediation tasks for 2.1.x (assuming no sibling CVE Jira exists for 2.1.x).

### Cross-stream impact comment (on TC-8001)

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. Versions 2.1.0 and 2.1.1 both ship
quinn-proto 0.11.9.

Stream 2.1.x is tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

### Preemptive Task 1: Upstream Backport (2.1.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)

**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

**Link**: Related to TC-8001

**Description**:

```
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for stream 2.1.x. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

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
- **Dependency type**: direct or transitive (to be confirmed via Cargo.lock inspection)
- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8001 (originating CVE Jira, stream 2.2.x)
```

### Preemptive Task 2: Downstream Propagation (2.1.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

**Link**: Related to TC-8001; Blocked by upstream backport task (2.1.x)

**Description**:

```
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for stream 2.1.x. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release
repo so the next build ships the fix.

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

- Blocked by: upstream backport task (rhtpa-2.1) -- upstream backport must merge first
- Related to: TC-8001 (originating CVE Jira, stream 2.2.x)
```

---

## Case B: Remediation Tasks (2.2.x -- in scope)

Create standard remediation tasks for the 2.2.x stream. These are linked to TC-8001 with "Depend".

### Task 1: Upstream Backport (2.2.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)

**Labels**: ai-generated-jira, Security, CVE-2026-31812

**Link**: Depend on TC-8001

**Description**:

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0 (v0.4.5, quinn-proto 0.11.9), 2.2.1 (v0.4.8, quinn-proto 0.11.12), 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Note: Versions 2.2.3 (v0.4.11) and 2.2.4 (v0.4.12) already ship quinn-proto
0.11.14 and are not affected. The fix was introduced at build 0.4.11.
The upstream branch release/0.4.z already contains the fix at its latest tag.

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct or transitive (to be confirmed via Cargo.lock inspection)
- The fix is already present at v0.4.11+ on this branch. Verify that the
  backport covers the maintenance window for versions 2.2.0 and 2.2.1.
  If a point release rebuild is needed for 2.2.0/2.2.1, ensure the quinn-proto
  bump is cherry-picked to the appropriate commit range.
- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

### Task 2: Downstream Propagation (2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: ai-generated-jira, Security, CVE-2026-31812

**Link**: Depend on TC-8001; Blocked by upstream backport task (2.2.x)

**Description**:

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14 on release/0.4.z.
Once that PR merges, update the source pinning in this Konflux release
repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Blocked by: upstream backport task (rhtpa-2.2) -- upstream backport must merge first
- Depends on: TC-8001 (parent tracking issue)
```

---

## Task Summary

| # | Task | Stream | Type | Labels | Link to TC-8001 |
|---|------|--------|------|--------|-----------------|
| 1 | Upstream backport: bump quinn-proto to 0.11.14 (rhtpa-2.1) | 2.1.x | Preemptive upstream | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |
| 2 | Downstream propagation: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1) | 2.1.x | Preemptive downstream | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |
| 3 | Upstream backport: bump quinn-proto to 0.11.14 (rhtpa-2.2) | 2.2.x | Standard upstream | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 4 | Downstream propagation: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2) | 2.2.x | Standard downstream | ai-generated-jira, Security, CVE-2026-31812 | Depend |

### Pre-creation checklist

- [x] **Task count per stream**: 2 tasks per stream (Cargo = source dependency ecosystem)
- [x] **Cross-stream coverage**: 2.1.x (out of scope) covered by preemptive tasks (no sibling CVE Jira exists)
- [x] **Link types**: "Depend" for 2.2.x tasks linked to TC-8001; "Related" for 2.1.x preemptive tasks linked to TC-8001; "Blocks" for upstream -> downstream within each stream
- [x] **Preemptive labels**: 2.1.x tasks carry `security-preemptive` label
