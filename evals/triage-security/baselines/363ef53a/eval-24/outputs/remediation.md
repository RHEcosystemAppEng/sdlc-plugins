# Step 8 -- Remediation: TC-8001 (CVE-2026-31812)

## Triage Outcome

Case B (Affected) for the scoped 2.2.x stream, plus Case A (Cross-stream
impact) for the 2.1.x stream.

Ecosystem: Cargo (source dependency) -- 2 tasks per stream.

- **2.2.x stream** (scoped): upstream fix is already available on release/0.4.z,
  so the dependency bump variant is used (not upstream backport).
- **2.1.x stream** (Case A, preemptive): upstream fix is NOT available on
  release/0.3.z, so the upstream backport variant is used.

---

## 2.2.x Stream -- Remediation Tasks (Scoped)

### Task 1: Dependency Bump (2.2.x)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task description:**

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream --
a package manager update is sufficient.

Affected versions: RHTPA 2.2.0, 2.2.1, 2.2.2
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is retag of v0.4.8)

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

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task description:**

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

- Depends on: dependency bump task (dependency bump must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

### Jira Linkage (2.2.x)

1. Link dependency bump task to TC-8001 (Depend)
2. Link downstream propagation task to TC-8001 (Depend)
3. Link downstream propagation task as blocked by dependency bump task (Blocks)
4. Link both tasks to release Task (Blocks) -- if release Jira is active
5. Link TC-8001 to release Task (Related) -- if release Jira is active

---

## 2.1.x Stream -- Preemptive Remediation Tasks (Case A)

These tasks are created proactively because the 2.1.x stream is also
affected but this CVE issue (TC-8001) is scoped to 2.2.x only. The
upstream fix is NOT available on release/0.3.z, so the upstream backport
variant is used.

### Task 3: Upstream Backport (2.1.x, preemptive)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task description:**

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

Affected versions: RHTPA 2.1.0, 2.1.1
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

### Task 4: Downstream Propagation (2.1.x, preemptive)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task description:**

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

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

### Jira Linkage (2.1.x, preemptive)

1. Link upstream backport task to TC-8001 (Related -- preemptive, not Depend)
2. Link downstream propagation task to TC-8001 (Related -- preemptive)
3. Link downstream propagation task as blocked by upstream backport task (Blocks)
4. Link both tasks to release Task for 2.1.x (Blocks) -- if release Jira is active
5. Link TC-8001 to release Task for 2.1.x (Related) -- if release Jira is active

---

## Summary of All Remediation Tasks

| # | Task Summary | Stream | Type | Labels | Link to TC-8001 |
|---|-------------|--------|------|--------|-----------------|
| 1 | Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2) | 2.2.x | Dependency bump | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 2 | Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2) | 2.2.x | Downstream propagation | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 3 | Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1) | 2.1.x | Upstream backport (preemptive) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |
| 4 | Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1) | 2.1.x | Downstream propagation (preemptive) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |

### Pre-creation checklist

- [x] **Task count per stream**: 2.2.x has 2 tasks (dependency bump + downstream),
  2.1.x has 2 tasks (upstream backport + downstream) -- matches Cargo ecosystem
  classification (source dependency -> 2 tasks per stream)
- [x] **Cross-stream coverage**: 2.1.x stream (outside the issue's 2.2.x scope)
  has preemptive tasks created
- [x] **Link types**: Depend for tasks linked to their own CVE Jira (2.2.x),
  Related for preemptive tasks linked to another stream's CVE Jira (2.1.x)
- [x] **Preemptive labels**: 2.1.x tasks carry the `security-preemptive` label
- [x] **Coordination guidance**: omitted -- Source Repositories table has no
  Deployment Context column (backward compatibility)
- [x] **Blocking chain**: downstream propagation is blocked by its upstream
  task in each stream (Blocks link)
