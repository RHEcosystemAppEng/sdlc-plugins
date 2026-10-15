# Step 8 -- Remediation: TC-8001 (CVE-2026-31812)

## Triage Outcome

- **Case A** applies: the issue is scoped to stream 2.2.x (`[rhtpa-2.2]`), but stream 2.1.x is also affected. Cross-stream impact comment and preemptive remediation tasks are required for 2.1.x.
- **Case B** applies: affected versions exist within the issue's stream scope (2.2.0, 2.2.1, 2.2.2). Remediation tasks are created for the 2.2.x stream.
- Ecosystem: Cargo (source dependency) -- 2 tasks per stream (dependency bump or upstream backport + downstream propagation).

### Upstream Fix Determination

- **2.2.x stream**: upstream branch `release/0.4.z` already ships quinn-proto 0.11.14 (fixed). Use **dependency bump** variant.
- **2.1.x stream**: upstream branch `release/0.3.z` ships quinn-proto 0.11.9 (not fixed). Use **upstream backport** variant. Tasks are **preemptive** (no 2.1.x CVE Jira exists).

---

## Stream 2.2.x Remediation Tasks (Standard)

### Task 1: Dependency Bump -- bump quinn-proto to 0.11.14 (rhtpa-2.2)

**Proposed Jira Issue:**
- Type: Task
- Summary: `Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)`
- Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`
- Link: Depend -- TC-8001 (parent Vulnerability issue)

**Task Description:**

```
## Repository

rhtpa-backend

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
- **Dependency type**: direct
- **Remediation action**: run the appropriate package manager update command:
  - **Cargo**: `cargo update -p quinn-proto` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for
CVE assignment, advisory preparation, and formal disclosure. Fix must be
released via a security advisory with explicit CVE-to-component mapping.

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

### Task 2: Downstream Propagation -- update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Proposed Jira Issue:**
- Type: Task
- Summary: `Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)`
- Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`
- Link: Depend -- TC-8001 (parent Vulnerability issue)
- Link: Blocks -- blocked by Task 1 (dependency bump must merge first)

**Task Description:**

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the dependency bump task.

The dependency bump task bumps quinn-proto to 0.11.14 on release/0.4.z.
Once that PR merges, update the source pinning in this Konflux release repo
so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for
CVE assignment, advisory preparation, and formal disclosure. Fix must be
released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: dependency bump task (upstream fix must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

## Stream 2.1.x Preemptive Remediation Tasks (Case A -- Cross-Stream Impact)

These tasks are created proactively because stream 2.1.x is also affected but
has no stream-specific CVE Jira. They carry the `security-preemptive` label
and use the "Related" link type to the originating CVE Jira (TC-8001).

### Task 3: Upstream Backport -- bump quinn-proto to 0.11.14 (rhtpa-2.1)

**Proposed Jira Issue:**
- Type: Task
- Summary: `Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)`
- Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- Link: Related -- TC-8001 (originating CVE Jira, different stream)

**Task Description:**

```
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2). No stream-specific CVE Jira
> exists yet for this stream. When PSIRT creates one, this task will be linked
> and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- The upstream fix is NOT yet available on release/0.3.z (current version:
  quinn-proto 0.11.9). An upstream backport is required.

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for
CVE assignment, advisory preparation, and formal disclosure. Fix must be
released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

### Task 4: Downstream Propagation -- update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Proposed Jira Issue:**
- Type: Task
- Summary: `Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)`
- Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- Link: Related -- TC-8001 (originating CVE Jira, different stream)
- Link: Blocks -- blocked by Task 3 (upstream backport must merge first)

**Task Description:**

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2). No stream-specific CVE Jira
> exists yet for this stream. When PSIRT creates one, this task will be linked
> and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release repo
so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for
CVE assignment, advisory preparation, and formal disclosure. Fix must be
released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream fix must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

## Proposed Jira Mutations (Not Executed)

The following Jira operations are proposed but not executed. All require
engineer confirmation before execution.

### Affects Versions Correction (Step 3)

- **Action**: Update TC-8001 Affects Versions
- **Current**: `[RHTPA 2.0.0]`
- **Proposed**: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
- **Rationale**: PSIRT-assigned RHTPA 2.0.0 does not exist in the supportability matrix. Lock file analysis at pinned commits confirms quinn-proto < 0.11.14 in versions 2.2.0, 2.2.1, and 2.2.2. Scoped to 2.2.x stream per issue suffix `[rhtpa-2.2]`.

### Cross-Stream Impact Comment (Case A)

- **Action**: Post comment on TC-8001
- **Content**: Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x (versions 2.1.0, 2.1.1) based on lock file analysis. Preemptive remediation tasks created for 2.1.x (no stream-specific CVE Jira exists).

### Issue Links

| From | To | Link Type | Reason |
|------|----|-----------|--------|
| TC-8001 | Task 1 (dep bump, 2.2.x) | Depend | Standard remediation linkage |
| TC-8001 | Task 2 (downstream, 2.2.x) | Depend | Standard remediation linkage |
| Task 1 | Task 2 | Blocks | Downstream blocked by upstream |
| TC-8001 | Task 3 (backport, 2.1.x) | Related | Preemptive -- different stream |
| TC-8001 | Task 4 (downstream, 2.1.x) | Related | Preemptive -- different stream |
| Task 3 | Task 4 | Blocks | Downstream blocked by upstream |

### Labels

- **Action**: Add `ai-cve-triaged` label to TC-8001

### Post-Triage Summary Comment

- **Action**: Post summary comment on TC-8001 documenting:
  - Version impact table (all streams)
  - Affects Versions correction: `[RHTPA 2.0.0]` -> `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
  - Triage outcome: remediation created
  - Standard remediation tasks for 2.2.x: Task 1 (dependency bump), Task 2 (downstream propagation)
  - Preemptive remediation tasks for 2.1.x: Task 3 (upstream backport), Task 4 (downstream propagation)

---

## Coordination Guidance Reference

The deployment context for repository **rhtpa-backend** is **customer-shipped** (from the Source Repositories table in CLAUDE.md Security Configuration). This deployment context triggers the following coordination guidance in every remediation task's Implementation Notes:

> This component is shipped to customers. Coordinate with Product Security for
> CVE assignment, advisory preparation, and formal disclosure. Fix must be
> released via a security advisory with explicit CVE-to-component mapping.

This guidance is included in all four remediation task descriptions above (Tasks 1-4).
