# Step 8 — Remediation: TC-8001 (CVE-2026-31812)

## Triage Outcome

- **Case A**: Cross-stream impact detected — 2.1.x is also affected but has no CVE Jira
- **Case B**: Create remediation tasks for 2.2.x (scoped stream) and preemptive tasks for 2.1.x
- Ecosystem: Cargo (source dependency) — **2 tasks per stream** (upstream backport + downstream propagation)
- Total tasks: **4** (2 for 2.2.x standard, 2 for 2.1.x preemptive)

---

## Stream 2.2.x — Standard Remediation Tasks

### Task 1: Upstream Backport (2.2.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Link**: Depend → TC-8001

#### Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0 (v0.4.5, quinn-proto 0.11.9), 2.2.1 (v0.4.8, quinn-proto 0.11.12), 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (quinn-proto is a direct Cargo dependency)

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- Run `cargo update -p quinn-proto` to update Cargo.lock
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

### Task 2: Downstream Propagation (2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Link**: Depend → TC-8001; Blocked by upstream task (Task 1)

#### Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: direct — carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (Task 1 — upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Stream 2.1.x — Preemptive Remediation Tasks

These tasks are created proactively from cross-stream impact analysis of TC-8001 (stream 2.2.x).
No stream-specific CVE Jira exists for 2.1.x. When PSIRT creates one, Step 4.4 reconciliation
will link it and remove the `security-preemptive` label.

### Task 3: Upstream Backport (2.1.x, preemptive)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link**: Related → TC-8001 (originating CVE Jira, different stream)

#### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

rhtpa-backend

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
- **Dependency type**: direct (quinn-proto is a direct Cargo dependency)

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- Run `cargo update -p quinn-proto` to update Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (originating CVE tracking issue — cross-stream)

---

### Task 4: Downstream Propagation (2.1.x, preemptive)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link**: Related → TC-8001 (originating CVE Jira, different stream); Blocked by upstream task (Task 3)

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

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: direct — carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (Task 3 — upstream backport must merge first)
- Depends on: TC-8001 (originating CVE tracking issue — cross-stream)

---

## Post-Triage Summary

### Actions taken:
1. **Data extraction**: Parsed CVE-2026-31812 metadata from TC-8001
2. **Version impact analysis**: Determined quinn-proto versions at each pinned commit across both streams
3. **Affects Versions correction**: RHTPA 2.0.0 (incorrect) → RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 (scoped to 2.2.x)
4. **Cross-stream impact (Case A)**: Stream 2.1.x also affected (2.1.0, 2.1.1) — preemptive tasks created
5. **Remediation tasks (Case B)**:
   - 2.2.x standard: 2 tasks (upstream backport + downstream propagation)
   - 2.1.x preemptive: 2 tasks (upstream backport + downstream propagation, with `security-preemptive` label)
6. **Label**: `ai-cve-triaged` added to TC-8001

### Version Impact Summary

| Stream | Version | quinn-proto | Affected? | Notes |
|--------|---------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | 0.11.9 | YES | preemptive task created |
| 2.1.x | 2.1.1 | 0.11.9 | YES | preemptive task created |
| 2.2.x | 2.2.0 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | — | YES | retag of 2.2.1 |
| 2.2.x | 2.2.3 | 0.11.14 | NO | fixed |
| 2.2.x | 2.2.4 | 0.11.14 | NO | fixed |
