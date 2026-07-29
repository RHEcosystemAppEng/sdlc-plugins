# Step 8 -- Remediation: TC-8001 (CVE-2026-31812)

## Triage Summary

- **CVE**: CVE-2026-31812
- **Library**: quinn-proto (Cargo / source dependency ecosystem)
- **Affected range**: versions before 0.11.14
- **Fixed version**: 0.11.14
- **Issue scope**: 2.2.x stream (per summary suffix `[rhtpa-2.2]`)
- **Deployment context**: customer-shipped

## Stream-by-Stream Assessment

### Stream 2.2.x (issue scope)

**Affected versions**: RHTPA 2.2.0, 2.2.1, 2.2.2
**Not affected**: RHTPA 2.2.3 (quinn-proto 0.11.14), RHTPA 2.2.4 (quinn-proto 0.11.14)

The fix was organically picked up in version 2.2.3 (build 0.4.11, released 2026-03-23). The upstream branch `release/0.4.z` already ships quinn-proto 0.11.14 at HEAD. No new remediation tasks are required for the 2.2.x stream -- the vulnerability is already resolved in the latest releases.

**Action**: Correct Affects Versions from `[RHTPA 2.0.0]` to `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`. No remediation tasks needed.

### Stream 2.1.x (cross-stream impact -- Case A)

**Affected versions**: RHTPA 2.1.0 (quinn-proto 0.11.9), RHTPA 2.1.1 (quinn-proto 0.11.9)
**Upstream branch status**: `release/0.3.z` -- NOT fixed (latest tag v0.3.12 has quinn-proto 0.11.9)

The 2.1.x stream is affected and has no fix upstream. Since no stream-specific CVE Jira exists for 2.1.x, preemptive remediation tasks are created per Case A (cross-stream impact).

---

## Cross-Stream Impact Comment (Case A)

The following comment would be posted to TC-8001:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. Both versions in the 2.1.x stream (2.1.0 and 2.1.1) ship quinn-proto 0.11.9. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.

---

## Preemptive Remediation Tasks for Stream 2.1.x

Since the issue TC-8001 is scoped to 2.2.x and no stream-specific CVE Jira exists for 2.1.x, the following preemptive remediation tasks are created with the `security-preemptive` label and "Related" link type to TC-8001.

### Task 1: Upstream Backport (2.1.x -- preemptive)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
**Link**: Related to TC-8001

#### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for this stream. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (denial of service).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (v0.3.8), RHTPA 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048)
Advisory: [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq)

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct or transitive (verify by inspecting Cargo.toml at v0.3.12)
- The upstream fix PR (quinn-rs/quinn#2048) has merged. The fix is available in quinn-proto 0.11.14.
- The 2.2.x stream already picked up the fix organically in build 0.4.11 (version 2.2.3). The same dependency bump is needed on the 2.1.x upstream branch.

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

When the vulnerable package is a **transitive** dependency (pulled in through intermediate packages), use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (see dependency chain)
- Bump the direct dependency to a version whose transitive closure includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes to the direct dependency

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable (breaking API changes, no release available with the fix):
- Cargo: `cargo add quinn-proto@0.11.14` to add as a direct dependency, overriding the transitive resolution
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

- Related to: TC-8001 (originating CVE Jira, stream 2.2.x)

---

### Task 2: Downstream Propagation (2.1.x -- preemptive)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
**Link**: Related to TC-8001; Blocked by upstream backport task (Task 1)

#### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for this stream. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-31812 fix from the upstream backport task (Task 1).

The upstream backport bumps quinn-proto to 0.11.14 on release/0.3.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
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

- Blocked by: upstream backport task (Task 1 -- must merge first)
- Related to: TC-8001 (originating CVE Jira, stream 2.2.x)

---

## Preemptive Task Summary Comment

The following comment would be posted to TC-8001:

> Preemptive remediation tasks created for streams without CVE Jiras:
> - 2.1.x: [upstream-task-key] (upstream backport, security-preemptive), [downstream-task-key] (downstream propagation, security-preemptive)
>
> These tasks use the "Related" link type and carry the security-preemptive label.
> When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link them and remove the label.

---

## Pre-Creation Checklist

- [x] **Task count per stream**: 2.1.x stream gets 2 tasks (upstream backport + downstream propagation) -- matches Cargo (source dependency) ecosystem classification.
- [x] **Cross-stream coverage**: 2.1.x stream (outside the issue's 2.2.x scope) has preemptive tasks created. 2.2.x stream already has the fix in 2.2.3+.
- [x] **Link types**: "Related" for preemptive tasks linked to TC-8001 (different stream's CVE Jira). "Blocks" for upstream-to-downstream within the 2.1.x stream.
- [x] **Preemptive labels**: Both tasks for 2.1.x carry the `security-preemptive` label (no stream-specific CVE Jira exists for 2.1.x).
- [x] **Coordination guidance**: Each task's Implementation Notes includes customer-shipped coordination guidance (coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure).

## Post-Triage Actions

1. **Add label**: `ai-cve-triaged` to TC-8001
2. **Correct Affects Versions**: `[RHTPA 2.0.0]` -> `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
3. **Post summary comment** to TC-8001 documenting: version impact table, Affects Versions correction, cross-stream impact, preemptive tasks created for 2.1.x, and @mention of the reporter
