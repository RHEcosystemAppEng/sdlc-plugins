# Step 7 -- Remediation: CVE-2026-31812

## Triage Outcome

**Case A + Case B**: The issue's scoped stream (2.2.x) has affected versions requiring remediation, and cross-stream impact affects the 2.1.x stream as well.

### Affected versions within issue scope (2.2.x stream)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | -- (retag of 2.2.1) | YES |
| 2.2.3 | 0.11.14 | NO (fixed) |
| 2.2.4 | 0.11.14 | NO (fixed) |

### Cross-stream impact (2.1.x stream -- outside issue scope)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.1.0 | 0.11.9 | YES |
| 2.1.1 | 0.11.9 | YES |

---

## Case A: Remediation Tasks for 2.2.x Stream (Issue Scope)

Since quinn-proto is a **Cargo** (source dependency) ecosystem, two tasks are created: an upstream backport task and a downstream propagation subtask.

### Task 1: Upstream Backport Task

**Proposed Jira Issue:**

- **Type**: Task
- **Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`
- **Link**: Depend (inward: TC-8001, outward: this task)

**Task Description:**

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (v0.4.5), RHTPA 2.2.1 (v0.4.8), RHTPA 2.2.2 (v0.4.9, retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

Note: The upstream fix is already present on release/0.4.z as of v0.4.11
(quinn-proto 0.11.14). Remediation requires backporting the dependency
bump to a point that covers versions 2.2.0 and 2.2.1, or confirming that
future releases from v0.4.11+ already carry the fix.

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z
- quinn-proto is a transitive dependency via: reqwest [http3] -> h3 -> quinn -> quinn-proto
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

### Task 2: Downstream Propagation Subtask

**Proposed Jira Issue:**

- **Type**: Task
- **Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`
- **Link**: Depend (inward: TC-8001, outward: this task)
- **Blocked by**: Task 1 (upstream backport)

**Task Description:**

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

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

## Case B: Cross-Stream Impact Notice and Preemptive Tasks for 2.1.x Stream

### Cross-stream impact comment (proposed for TC-8001)

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. Versions 2.1.0 and 2.1.1 both ship
quinn-proto 0.11.9. This stream is tracked by companion issues
(see Related links) or may require separate PSIRT triage.
```

### Preemptive Remediation Tasks for 2.1.x Stream

Since no companion CVE Jira exists for the 2.1.x stream (not detected in this eval), preemptive remediation tasks are proposed.

#### Preemptive Task 1: Upstream Backport for 2.1.x

**Proposed Jira Issue:**

- **Type**: Task
- **Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- **Link**: Related (inward: TC-8001, outward: this task) -- not "Depend" because the originating CVE belongs to a different stream

**Task Description:**

```
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
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (v0.3.8), RHTPA 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.3.z
- quinn-proto is a transitive dependency via: reqwest [http3] -> h3 -> quinn -> quinn-proto
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

- Depends on: TC-8001 (parent tracking issue, cross-stream)
```

#### Preemptive Task 2: Downstream Propagation for 2.1.x

**Proposed Jira Issue:**

- **Type**: Task
- **Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- **Link**: Related (inward: TC-8001, outward: this task)
- **Blocked by**: Preemptive Task 1 (upstream backport for 2.1.x)

**Task Description:**

```
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

- Depends on: upstream backport task for 2.1.x (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue, cross-stream)
```

### Preemptive tasks comment (proposed for TC-8001)

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: [upstream-task-key] (security-preemptive, upstream backport)
- 2.1.x: [downstream-task-key] (security-preemptive, downstream propagation)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

---

## Post-Triage Summary (Proposed)

### Proposed Jira mutations (all require engineer confirmation)

1. **Add label** `ai-cve-triaged` to TC-8001
2. **Correct Affects Versions**: `RHTPA 2.0.0` -> `RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2` (scoped to 2.2.x stream)
3. **Create upstream backport task** for 2.2.x stream (Depend link to TC-8001)
4. **Create downstream propagation task** for 2.2.x stream (Depend link to TC-8001, Blocked by upstream task)
5. **Create preemptive upstream backport task** for 2.1.x stream (Related link to TC-8001, security-preemptive label)
6. **Create preemptive downstream propagation task** for 2.1.x stream (Related link to TC-8001, security-preemptive label, Blocked by preemptive upstream task)
7. **Post cross-stream impact comment** on TC-8001
8. **Post preemptive tasks comment** on TC-8001
9. **Post summary comment** on TC-8001 (with version impact table, Affects Versions correction, triage outcome, task links, reporter @mention, and Comment Footnote)
10. **Transition** TC-8001 to In Progress
11. **Assign** TC-8001 to current user

All actions are proposed -- none will be executed without explicit engineer confirmation.
