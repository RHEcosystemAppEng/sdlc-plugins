# Step 8 -- Remediation: TC-8001

## Triage Decision

The issue TC-8001 is scoped to stream **2.2.x**. The version impact analysis shows:

- **2.2.x stream (scoped):** versions 2.2.0, 2.2.1, 2.2.2 are AFFECTED; versions 2.2.3, 2.2.4 are NOT affected (ship quinn-proto 0.11.14, the fixed version).
- **2.1.x stream (out of scope):** versions 2.1.0, 2.1.1 are AFFECTED.

**Outcome:** Case A (cross-stream impact) + Case B (remediation task creation).

- Upstream fix is already available on the 2.2.x branch (`release/0.4.z` ships quinn-proto 0.11.14 at v0.4.11+).
- Upstream fix is NOT available on the 2.1.x branch (`release/0.3.z` still ships quinn-proto 0.11.9).

Since the Deployment Context column is absent from the Source Repositories table, coordination guidance is omitted from all task descriptions.

---

## Remediation Tasks for Stream 2.2.x (Scoped -- Case B)

Because Step 2.5 confirms the upstream branch `release/0.4.z` already ships the fixed version (0.11.14), the **dependency bump** variant is used (not upstream backport).

### Task 1: Dependency Bump (2.2.x)

**Proposed Jira action:** Create Task

- **Summary:** Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)
- **Issue Type:** Task
- **Labels:** ai-generated-jira, Security, CVE-2026-31812
- **Link:** Depend -- TC-8001 (inward) to this task (outward)

**Description:**

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream --
a package manager update is sufficient.

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (quinn-proto is a direct Cargo dependency)
- **Remediation action**: run `cargo update -p quinn-proto` to pull in the
  latest compatible version (>= 0.11.14)
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

---

### Task 2: Downstream Propagation (2.2.x)

**Proposed Jira action:** Create Task

- **Summary:** Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
- **Issue Type:** Task
- **Labels:** ai-generated-jira, Security, CVE-2026-31812
- **Link:** Depend -- TC-8001 (inward) to this task (outward)
- **Link:** Blocks -- Task 1 (inward) to this task (outward) (blocked by upstream dependency bump)

**Description:**

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the dependency bump task.

The dependency bump task bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
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

- Depends on: dependency bump task (upstream fix must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

## Cross-Stream Impact: Preemptive Tasks for Stream 2.1.x (Case A)

The 2.1.x stream is also affected (versions 2.1.0 and 2.1.1 ship quinn-proto 0.11.9). No sibling CVE Jira exists for stream 2.1.x. Preemptive remediation tasks are created with the `security-preemptive` label and linked to TC-8001 with "Related" (not "Depend").

The upstream branch `release/0.3.z` does NOT ship the fix (quinn-proto is 0.11.9 at v0.3.12), so the **upstream backport** variant is used.

### Task 3: Upstream Backport -- Preemptive (2.1.x)

**Proposed Jira action:** Create Task

- **Summary:** Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)
- **Issue Type:** Task
- **Labels:** ai-generated-jira, Security, CVE-2026-31812, security-preemptive
- **Link:** Related -- TC-8001 (inward) to this task (outward) (preemptive link type)

**Description:**

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

Remediate CVE-2026-31812: quinn-proto allows a remote attacker to cause a panic
via excessive stream counts in QUIC transport frames (DoS).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (quinn-proto is a direct Cargo dependency)
- The upstream branch release/0.3.z does NOT yet ship the fix
  (quinn-proto 0.11.9 at latest tag v0.3.12)
- A backport or dependency bump on release/0.3.z is required to update
  quinn-proto to >= 0.11.14
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue -- cross-stream)
```

---

### Task 4: Downstream Propagation -- Preemptive (2.1.x)

**Proposed Jira action:** Create Task

- **Summary:** Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)
- **Issue Type:** Task
- **Labels:** ai-generated-jira, Security, CVE-2026-31812, security-preemptive
- **Link:** Related -- TC-8001 (inward) to this task (outward) (preemptive link type)
- **Link:** Blocks -- Task 3 (inward) to this task (outward) (blocked by upstream backport)

**Description:**

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

The upstream backport task bumps quinn-proto to 0.11.14
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

- Depends on: upstream backport task (upstream fix must merge first)
- Depends on: TC-8001 (parent tracking issue -- cross-stream)
```

---

## Proposed Jira Mutations Summary

All actions below are **proposed** -- none have been executed.

### Field Edits

1. **Affects Versions correction on TC-8001:**
   - Current: [RHTPA 2.0.0]
   - Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
   - Rationale: PSIRT-assigned "RHTPA 2.0.0" does not match any configured version stream. Lock file analysis shows 2.2.0, 2.2.1, and 2.2.2 ship vulnerable quinn-proto (< 0.11.14) within the 2.2.x scoped stream.

2. **Add label `ai-cve-triaged` to TC-8001** after triage completes.

### Status Transitions

1. **TC-8001:** New -> Assigned (assign to current user and transition)
2. **TC-8001:** Assigned -> In Progress (after remediation tasks are created)

### Task Creation (4 tasks total)

| # | Type | Stream | Summary | Labels | Variant |
|---|------|--------|---------|--------|---------|
| 1 | Dependency bump | 2.2.x | Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2) | ai-generated-jira, Security, CVE-2026-31812 | Standard |
| 2 | Downstream propagation | 2.2.x | Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2) | ai-generated-jira, Security, CVE-2026-31812 | Standard |
| 3 | Upstream backport | 2.1.x | Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Preemptive |
| 4 | Downstream propagation | 2.1.x | Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Preemptive |

### Issue Links

| From (inward) | To (outward) | Link Type | Rationale |
|---------------|-------------|-----------|-----------|
| TC-8001 | Task 1 (dep bump 2.2.x) | Depend | Standard remediation linkage |
| TC-8001 | Task 2 (downstream 2.2.x) | Depend | Standard remediation linkage |
| Task 1 (dep bump) | Task 2 (downstream 2.2.x) | Blocks | Downstream blocked by upstream fix |
| TC-8001 | Task 3 (backport 2.1.x) | Related | Preemptive -- different stream |
| TC-8001 | Task 4 (downstream 2.1.x) | Related | Preemptive -- different stream |
| Task 3 (backport) | Task 4 (downstream 2.1.x) | Blocks | Downstream blocked by upstream fix |

### Comments

1. **Affects Versions correction comment on TC-8001:**
   "Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]. Based on lock file analysis at pinned commits from security-matrix.md. Scoped to stream 2.2.x per issue suffix."

2. **Cross-stream impact comment on TC-8001:**
   "Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x (versions 2.1.0, 2.1.1) based on lock file analysis. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage."

3. **Preemptive task comment on TC-8001:**
   "Preemptive remediation tasks created for streams without CVE Jiras:
   - 2.1.x: Task 3 / Task 4 (security-preemptive)
   These tasks use the Related link type and carry the security-preemptive label. When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link them and remove the label."

4. **Post-triage summary comment on TC-8001** documenting the version impact table, Affects Versions correction, triage outcome, and links to all remediation tasks.

### Description Digest Comments

A description digest comment is posted on each created task (Tasks 1-4) before any links or other comments are created, per the description-digest-protocol.
