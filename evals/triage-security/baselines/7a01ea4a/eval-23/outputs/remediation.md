# Step 8 -- Remediation: TC-8001 (CVE-2026-31812)

## Triage Outcome

**Case A + Case B**: The issue is scoped to stream 2.2.x. Versions 2.2.0, 2.2.1, and 2.2.2
are affected within that stream. Additionally, the 2.1.x stream is affected (cross-stream
impact -- Case B).

Ecosystem: **Cargo** (source dependency) -- requires **two tasks** per affected stream:
an upstream backport task and a downstream propagation subtask.

---

## Remediation Task 1: Upstream Backport (2.2.x stream)

**Summary:** Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`

### Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (denial of service).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (v0.4.5, quinn-proto 0.11.9), RHTPA 2.2.1 (v0.4.8, quinn-proto 0.11.12), RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct or transitive (verify via `Cargo.lock` inspection at the pinned commit)

### Remediation approach (direct dependency)

When quinn-proto is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

When quinn-proto is a **transitive** dependency (pulled in through intermediate packages such as quinn or quinn-udp), use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (e.g., quinn)
- Bump the direct dependency to a version whose transitive closure includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes to the direct dependency

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable (breaking API changes, no release available with the fix):
- Cargo: `cargo add quinn-proto@0.11.14` to override the transitive resolution
- Document why the direct dep bump was not viable in the PR description

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

## Remediation Task 2: Downstream Propagation (2.2.x stream)

**Summary:** Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`

### Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14 on release/0.4.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback approach), verify the pinning is reflected in the downstream build's lock file after the source reference update
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Cross-Stream Impact (Case B): 2.1.x Stream

The version impact analysis reveals that the **2.1.x stream** is also affected by CVE-2026-31812:

| Version | Stream | quinn-proto | Affected? |
|---------|--------|-------------|-----------|
| 2.1.0 | 2.1.x | 0.11.9 | YES |
| 2.1.1 | 2.1.x | 0.11.9 | YES |

This issue (TC-8001) is scoped to 2.2.x per its summary suffix `[rhtpa-2.2]`. The 2.1.x stream
impact is outside this issue's scope.

### Cross-stream impact comment (to post on TC-8001)

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file
> analysis. Stream 2.1.x versions (2.1.0, 2.1.1) ship quinn-proto 0.11.9.
> These streams are tracked by companion issues (see Related links) or may require
> separate PSIRT triage.

### Preemptive Remediation Tasks for 2.1.x

If no companion CVE Jira exists for CVE-2026-31812 in the 2.1.x stream, create preemptive
remediation tasks:

#### Preemptive Task 3: Upstream Backport (2.1.x stream)

**Summary:** Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link type:** Related (to TC-8001, not Depend)

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (denial of service).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (v0.3.8, quinn-proto 0.11.9), RHTPA 2.1.1 (v0.3.12, quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct or transitive (verify via `Cargo.lock` inspection at the pinned commit)

### Remediation approach (direct dependency)

When quinn-proto is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

When quinn-proto is a **transitive** dependency (pulled in through intermediate packages), use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto
- Bump the direct dependency to a version whose transitive closure includes quinn-proto >= 0.11.14

**Fallback: pin the transitive dependency directly**
- Cargo: `cargo add quinn-proto@0.11.14` to override the transitive resolution

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8001 (originating CVE from stream 2.2.x)

---

#### Preemptive Task 4: Downstream Propagation (2.1.x stream)

**Summary:** Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link type:** Related (to TC-8001, not Depend)

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14 on release/0.3.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: preemptive upstream backport task (upstream backport must merge first)
- Related to: TC-8001 (originating CVE from stream 2.2.x)

---

## Jira Linkage Summary

### Standard remediation tasks (2.2.x -- in scope):
- Upstream backport task --> TC-8001 (link type: Depend)
- Downstream propagation subtask --> upstream backport task (link type: Blocks)
- Downstream propagation subtask --> TC-8001 (link type: Depend)

### Preemptive remediation tasks (2.1.x -- cross-stream):
- Upstream backport task (2.1.x) --> TC-8001 (link type: Related)
- Downstream propagation subtask (2.1.x) --> upstream backport task (2.1.x) (link type: Blocks)
- Downstream propagation subtask (2.1.x) --> TC-8001 (link type: Related)

## Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8001
2. Post summary comment to TC-8001 documenting:
   - Version impact table
   - Affects Versions correction: `[RHTPA 2.0.0]` --> `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
   - Remediation tasks created (upstream + downstream for 2.2.x)
   - Preemptive tasks created for 2.1.x (with `security-preemptive` label)
   - Cross-stream impact notice for 2.1.x
   - @mention of TC-8001 reporter
