# Step 8 -- Remediation

## Triage Outcome: Case A + Case B

TC-8001 is scoped to stream **2.2.x**. The version impact analysis shows:

- **2.2.x stream** (in scope): versions 2.2.0, 2.2.1, 2.2.2 are affected -> **Case A** (create remediation tasks)
- **2.1.x stream** (out of scope): versions 2.1.0, 2.1.1 are also affected -> **Case B** (cross-stream impact)

The ecosystem is **Cargo** (source dependency), so each affected stream requires
**two tasks**: an upstream backport task and a downstream propagation subtask.

---

## Case A -- Remediation Tasks for Stream 2.2.x (In-Scope)

### Task 1: Upstream Backport Task (2.2.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

#### Description

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (v0.4.5, quinn-proto 0.11.9),
RHTPA 2.2.1 (v0.4.8, quinn-proto 0.11.12),
RHTPA 2.2.2 (retag of v0.4.8, quinn-proto 0.11.12)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: to be confirmed via Cargo.lock inspection
- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Note: version 2.2.3 (build 0.4.11) already ships quinn-proto 0.11.14,
  confirming the fix is available on this branch

### Remediation approach (direct dependency)

When the vulnerable package is a direct dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml/Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

When the vulnerable package is a transitive dependency (pulled in
through intermediate packages), use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (see
  dependency chain above)
- Bump the direct dependency to a version whose transitive closure
  includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable:
- Cargo: `cargo add quinn-proto@0.11.14` to add as a direct
  dependency, overriding the transitive resolution
- Document why the direct dep bump was not viable in the PR description

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

### Task 2: Downstream Propagation Subtask (2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

#### Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14 on release/0.4.z.
Once that PR merges, update the source pinning in this Konflux release
repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Jira Linkage (2.2.x tasks)

```
# Link upstream task to CVE issue
jira.create_link(inwardIssue: "TC-8001", outwardIssue: <upstream-task-key>, type: "Depend")

# Link downstream subtask as blocked by upstream task
jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
```

---

## Case B -- Cross-Stream Impact (2.1.x)

The version impact analysis reveals that stream **2.1.x** (outside this issue's
scope) is also affected:

- RHTPA 2.1.0: quinn-proto 0.11.9 (affected)
- RHTPA 2.1.1: quinn-proto 0.11.9 (affected)

### Cross-Stream Impact Comment

Post to TC-8001:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on
lock file analysis. These streams are tracked by companion issues (see Related
links) or may require separate PSIRT triage.
```

### Preemptive Remediation Tasks for Stream 2.1.x

If no sibling CVE Jira exists for CVE-2026-31812 scoped to 2.1.x, create
preemptive remediation tasks:

#### Preemptive Task 1: Upstream Backport (2.1.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link type**: Related (to TC-8001, not Depend)

##### Description

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

Affected versions: RHTPA 2.1.0 (v0.3.8, quinn-proto 0.11.9),
RHTPA 2.1.1 (v0.3.12, quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: to be confirmed via Cargo.lock inspection
- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml/Cargo.lock

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto
- Bump to a version whose transitive closure includes quinn-proto >= 0.11.14

**Fallback: pin the transitive dependency directly**
- Cargo: `cargo add quinn-proto@0.11.14`

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

#### Preemptive Task 2: Downstream Propagation (2.1.x)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link type**: Related (to TC-8001, not Depend)

##### Description

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

The upstream backport bumps quinn-proto to 0.11.14 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release
repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <preemptive-upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Preemptive Task Linkage

```
# Link preemptive upstream task to originating CVE with Related (not Depend)
jira.create_link(inwardIssue: "TC-8001", outwardIssue: <preemptive-upstream-task-key>, type: "Related")

# Link preemptive downstream subtask as blocked by preemptive upstream task
jira.create_link(inwardIssue: <preemptive-upstream-task-key>, outwardIssue: <preemptive-downstream-task-key>, type: "Blocks")

# Link preemptive downstream task to originating CVE with Related
jira.create_link(inwardIssue: "TC-8001", outwardIssue: <preemptive-downstream-task-key>, type: "Related")
```

### Preemptive Task Comment on TC-8001

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <preemptive-upstream-task-key> (upstream backport, security-preemptive)
- 2.1.x: <preemptive-downstream-task-key> (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```
