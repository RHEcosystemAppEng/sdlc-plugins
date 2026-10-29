# Step 8 -- Remediation: TC-8001 (CVE-2026-31812)

## Triage Outcome

- **Case B** applies for the scoped 2.2.x stream: versions 2.2.0, 2.2.1, and 2.2.2 are affected.
- **Case A** applies for cross-stream impact: the 2.1.x stream is also affected but has no stream-specific CVE Jira. Preemptive remediation tasks will be created for 2.1.x.

## Remediation Task Topology

Since quinn-proto is a **Cargo** (source dependency) ecosystem, each affected stream requires **2 tasks**: an upstream fix task + a downstream propagation task.

- **2.2.x stream** (scoped -- standard remediation): upstream fix is available (Step 2.5 confirms release/0.4.z ships quinn-proto 0.11.14), so the upstream task is a **dependency bump** variant.
- **2.1.x stream** (cross-stream -- preemptive remediation): upstream fix is NOT available on release/0.3.z, so the upstream task is a standard **upstream backport**.

---

## Stream 2.2.x -- Standard Remediation Tasks

### Task 1: Dependency Bump (2.2.x)

**PROPOSAL** -- Create Jira Task:

```
Summary: Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x)
Labels: ai-generated-jira, Security, CVE-2026-31812
Link: Depend -> TC-8001
```

#### Task Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream --
a package manager update is sufficient.

Affected versions: 2.2.0 (v0.4.5), 2.2.1 (v0.4.8), 2.2.2 (v0.4.9, retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (or transitive -- to be confirmed via Cargo.toml inspection)
- **Remediation action**: run the appropriate package manager update command:
  - **Cargo**: `cargo update -p quinn-proto` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

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

**PROPOSAL** -- Create Jira Task:

```
Summary: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)
Labels: ai-generated-jira, Security, CVE-2026-31812
Link: Depend -> TC-8001
Link: Blocks (blocked by Task 1 above)
```

#### Task Description

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

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag)
- **Dependency type**: carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: dependency bump task (upstream fix must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Stream 2.1.x -- Preemptive Remediation Tasks

These tasks are created proactively from cross-stream impact analysis. No stream-specific CVE Jira exists for 2.1.x yet for CVE-2026-31812. The upstream fix is NOT available on release/0.3.z, so an upstream backport is required.

### Task 3: Upstream Backport (2.1.x, preemptive)

**PROPOSAL** -- Create Jira Task:

```
Summary: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)
Labels: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
Link: Related -> TC-8001 (not Depend, because this is preemptive for a different stream)
```

#### Task Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for the 2.1.x stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-31812: quinn-proto allows a remote attacker to cause a panic
by sending a QUIC transport frame that creates an excessive number of streams (DoS).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8), 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (or transitive -- to be confirmed via Cargo.toml inspection)
- The upstream fix (quinn-proto 0.11.14) is NOT yet available on release/0.3.z (latest tag v0.3.12 ships quinn-proto 0.11.9)
- A backport or dependency bump is required on the release/0.3.z branch
- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue -- cross-stream)

---

### Task 4: Downstream Propagation (2.1.x, preemptive)

**PROPOSAL** -- Create Jira Task:

```
Summary: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)
Labels: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
Link: Related -> TC-8001 (preemptive)
Link: Blocks (blocked by Task 3 above)
```

#### Task Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for the 2.1.x stream. When PSIRT creates one,
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

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag)
- **Dependency type**: carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream fix must merge first)
- Depends on: TC-8001 (parent tracking issue -- cross-stream)

---

## Jira Linkage Summary (PROPOSALS)

All of the following are proposed mutations, not executed actions:

### Standard remediation (2.2.x stream)

1. **Task 1** (dependency bump) -> TC-8001: link type **Depend**
2. **Task 2** (downstream propagation) -> TC-8001: link type **Depend**
3. **Task 1** -> **Task 2**: link type **Blocks** (downstream blocked by upstream)

### Preemptive remediation (2.1.x stream)

4. **Task 3** (upstream backport) -> TC-8001: link type **Related** (preemptive, cross-stream)
5. **Task 4** (downstream propagation) -> TC-8001: link type **Related** (preemptive, cross-stream)
6. **Task 3** -> **Task 4**: link type **Blocks** (downstream blocked by upstream)

### Post-creation actions (PROPOSALS)

- Add label `ai-cve-triaged` to TC-8001
- Post cross-stream impact comment to TC-8001 noting 2.1.x is also affected
- Post preemptive task list comment to TC-8001 listing Task 3 and Task 4
- Post post-triage summary comment to TC-8001 documenting the full triage outcome

## Pre-Creation Checklist

- [x] **Task count per stream**: 2.2.x has 2 tasks (dependency bump + downstream propagation); 2.1.x has 2 tasks (upstream backport + downstream propagation) -- matches Cargo ecosystem classification
- [x] **Cross-stream coverage**: 2.1.x stream (outside the scoped 2.2.x) has preemptive tasks created (no existing sibling CVE Jira found for 2.1.x)
- [x] **Link types**: "Depend" for tasks linked to their own CVE Jira (2.2.x standard); "Related" for preemptive tasks linked to another stream's CVE Jira (2.1.x preemptive); "Blocks" from upstream to downstream within each stream
- [x] **Preemptive labels**: Tasks for 2.1.x (no own CVE Jira) carry the `security-preemptive` label
- [x] **Coordination guidance**: Each task's Implementation Notes includes the `customer-shipped` coordination guidance: "Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping."
- [x] **Release Jira linking**: Not evaluated (Step 7.5 would require Jira interaction to discover/create release Epics and Tasks)
- [x] **Dedup consistency**: No prior dedup detected (no existing remediation tasks found)
