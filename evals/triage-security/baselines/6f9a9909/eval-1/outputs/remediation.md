# Step 8 -- Remediation

## Triage Outcome

- **Case A applies**: The issue is scoped to stream 2.2.x, but cross-stream analysis
  reveals that stream 2.1.x is also affected. A cross-stream impact comment is posted,
  and preemptive remediation tasks are created for the 2.1.x stream (assuming no
  sibling CVE Jira exists for 2.1.x).
- **Case B applies**: Affected versions exist in the 2.2.x stream (2.2.0, 2.2.1, 2.2.2).
  Remediation tasks are created.
- **Ecosystem**: Cargo (source dependency) -- 2 tasks per stream (upstream backport +
  downstream propagation).

---

## Case A: Cross-Stream Impact Comment

```
Cross-stream impact: quinn-proto (versions before 0.11.14) also affects stream 2.1.x
based on lock file analysis:
  - 2.1.0 (v0.3.8): quinn-proto 0.11.9
  - 2.1.1 (v0.3.12): quinn-proto 0.11.9

These streams are tracked by companion issues (see Related links) or may require
separate PSIRT triage.
```

---

## Case B: Remediation Tasks for Stream 2.2.x

### Task 1: Upstream Backport (2.2.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)

**Labels**: ai-generated-jira, Security, CVE-2026-31812

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

Affected versions: RHTPA 2.2.0 (v0.4.5, quinn-proto 0.11.9),
RHTPA 2.2.1 (v0.4.8, quinn-proto 0.11.12),
RHTPA 2.2.2 (v0.4.9, retag of v0.4.8)

Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: to be determined via dependency chain analysis
- Note: versions 2.2.3+ (v0.4.11+) already ship quinn-proto 0.11.14,
  confirming the fix is available on this branch

### Remediation approach (direct dependency)

When quinn-proto is a direct dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

When quinn-proto is a transitive dependency (pulled in through
intermediate packages), use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto
  (see dependency chain)
- Bump the direct dependency to a version whose transitive closure
  includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable:
- `cargo add quinn-proto@0.11.14` to override the transitive resolution
- Document why the direct dep bump was not viable in the PR description

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

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

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Linkage (2.2.x tasks)

```
# Link upstream task to CVE
jira.create_link(inwardIssue: "TC-8001", outwardIssue: <upstream-task-key>, type: "Depend")

# Link downstream task to CVE
jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-key>, type: "Depend")

# Block downstream on upstream
jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
```

---

## Case A: Preemptive Remediation Tasks for Stream 2.1.x

These tasks are created because stream 2.1.x is affected but has no CVE Jira of its own
(assuming no sibling found in Step 4). They carry the `security-preemptive` label and
use the "Related" link type to the originating CVE TC-8001.

### Task 3: Upstream Backport (2.1.x, preemptive)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)

**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

**Description**:

```
## Repository

backend

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

Affected versions: RHTPA 2.1.0 (v0.3.8, quinn-proto 0.11.9),
RHTPA 2.1.1 (v0.3.12, quinn-proto 0.11.9)

Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: to be determined via dependency chain analysis
- Both 2.1.x versions ship quinn-proto 0.11.9 -- the fix requires
  bumping to 0.11.14 on the release/0.3.z branch

### Remediation approach (direct dependency)

When quinn-proto is a direct dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

When quinn-proto is a transitive dependency (pulled in through
intermediate packages), use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto
- Bump the direct dependency to a version whose transitive closure
  includes quinn-proto >= 0.11.14

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable:
- `cargo add quinn-proto@0.11.14` to override the transitive resolution

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (originating CVE -- Related link)
```

### Task 4: Downstream Propagation (2.1.x, preemptive)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

**Description**:

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

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release
repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-preemptive-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (originating CVE -- Related link)
```

### Linkage (2.1.x preemptive tasks)

```
# Link preemptive upstream task to originating CVE with "Related" (not "Depend")
jira.create_link(inwardIssue: "TC-8001", outwardIssue: <preemptive-upstream-key>, type: "Related")

# Link preemptive downstream task to originating CVE with "Related"
jira.create_link(inwardIssue: "TC-8001", outwardIssue: <preemptive-downstream-key>, type: "Related")

# Block preemptive downstream on preemptive upstream
jira.create_link(inwardIssue: <preemptive-upstream-key>, outwardIssue: <preemptive-downstream-key>, type: "Blocks")
```

### Cross-Stream Preemptive Tasks Comment on TC-8001

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <preemptive-upstream-key> (upstream backport, security-preemptive)
- 2.1.x: <preemptive-downstream-key> (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

---

## Summary of All Remediation Tasks

| # | Stream | Type | Summary | Labels |
|---|--------|------|---------|--------|
| 1 | 2.2.x | Upstream backport | Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2) | ai-generated-jira, Security, CVE-2026-31812 |
| 2 | 2.2.x | Downstream propagation | Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2) | ai-generated-jira, Security, CVE-2026-31812 |
| 3 | 2.1.x | Upstream backport (preemptive) | Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive |
| 4 | 2.1.x | Downstream propagation (preemptive) | Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive |
