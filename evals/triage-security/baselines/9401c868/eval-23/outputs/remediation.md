# Step 8 -- Remediation: TC-8001

## Triage Outcome

CVE-2026-31812 affects quinn-proto versions before 0.11.14. Based on the version impact analysis:

- **Stream 2.2.x (in scope)**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3+ ship the fixed version. The upstream fix IS available on release/0.4.z.
- **Stream 2.1.x (cross-stream)**: Versions 2.1.0 and 2.1.1 are affected. The upstream fix is NOT available on release/0.3.z.

This triggers **Case A** (cross-stream impact) followed by **Case B** (create remediation tasks).

Since the ecosystem is Cargo (source dependency) and the upstream fix is available for 2.2.x (Step 2.5 confirmed v0.4.11 ships quinn-proto 0.11.14), the 2.2.x remediation uses the **dependency bump** variant: 2 tasks (dependency bump + downstream propagation).

For the 2.1.x cross-stream preemptive tasks, the upstream fix is NOT available on release/0.3.z, so the standard upstream backport variant applies: 2 tasks (upstream backport + downstream propagation).

---

## Case A: Cross-Stream Impact Comment

Post to TC-8001:

> Cross-stream impact: quinn-proto (versions before 0.11.14) also affects stream 2.1.x
> based on lock file analysis. Versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9.
> These streams are tracked by companion issues (see Related links) or may require
> separate PSIRT triage.

---

## Case B: Remediation Tasks -- Stream 2.2.x (In Scope)

### Task 1: Dependency Bump (upstream fix available)

**Summary**: Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description**:

> ## Repository
>
> rhtpa-backend
>
> ## Target Branch
>
> release/0.4.z
>
> ## Description
>
> Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
> The vulnerable dependency (quinn-proto versions before 0.11.14) is already fixed upstream --
> a package manager update is sufficient.
>
> Affected versions: 2.2.0 (v0.4.5), 2.2.1 (v0.4.8), 2.2.2 (v0.4.9, retag of 2.2.1)
> Source commit(s): v0.4.5, v0.4.8
>
> Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
> Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq
>
> ## Implementation Notes
>
> - Target branch: release/0.4.z
> - **Dependency type**: direct (or transitive -- to be confirmed via Cargo.lock inspection)
> - **Remediation action**: run `cargo update -p quinn-proto` to pull in the latest compatible version
> - If the update pulls a version that still falls within the affected range,
>   pin explicitly: `cargo add quinn-proto@0.11.14`
> - Verify the lock file reflects >= 0.11.14 after the update
>
> ### Coordination Guidance
>
> This component is shipped to customers. Coordinate with Product Security for CVE assignment,
> advisory preparation, and formal disclosure. Fix must be released via a security advisory
> with explicit CVE-to-component mapping.
>
> ## Acceptance Criteria
>
> - [ ] quinn-proto dependency is >= 0.11.14
> - [ ] Lock file updated via package manager (not manual edit)
> - [ ] No other dependency conflicts introduced
> - [ ] Existing tests pass
>
> ## Test Requirements
>
> - [ ] Existing test suite passes with the updated dependency
>
> ## Dependencies
>
> - Depends on: TC-8001 (parent tracking issue)

**Jira linkage**: Link to TC-8001 with type "Depend"

---

### Task 2: Downstream Propagation (2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description**:

> ## Repository
>
> rhtpa-release.0.4.z
>
> ## Target Branch
>
> main
>
> ## Description
>
> Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
> CVE-2026-31812 fix from the dependency bump task.
>
> The dependency bump task bumps quinn-proto to 0.11.14 on release/0.4.z.
> Once that PR merges, update the source pinning in this Konflux release repo
> so the next build ships the fix.
>
> ## Implementation Notes
>
> - Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
> - **Dependency type**: carried forward from upstream task
> - Update the rhtpa-backend reference to the merged commit or new release tag
> - Verify the Konflux build pipeline triggers successfully
>
> ### Coordination Guidance
>
> This component is shipped to customers. Coordinate with Product Security for CVE assignment,
> advisory preparation, and formal disclosure. Fix must be released via a security advisory
> with explicit CVE-to-component mapping.
>
> ## Acceptance Criteria
>
> - [ ] rhtpa-backend reference updated to include the fix
> - [ ] Konflux rebuild triggers new container image
>
> ## Test Requirements
>
> - [ ] Container image builds successfully with the updated reference
>
> ## Dependencies
>
> - Depends on: [dependency-bump-task-key] (dependency bump must merge first)
> - Depends on: TC-8001 (parent tracking issue)

**Jira linkage**:
- Link to TC-8001 with type "Depend"
- Link to Task 1 (dependency bump) with type "Blocks" (Task 1 blocks Task 2)

---

## Case A: Preemptive Remediation Tasks -- Stream 2.1.x (Cross-Stream)

These tasks are created proactively because the version impact analysis shows 2.1.x is affected
but the issue TC-8001 is scoped to 2.2.x only. No sibling CVE Jira exists for 2.1.x.

For 2.1.x, the upstream fix is NOT available on release/0.3.z (latest tag v0.3.12 ships
quinn-proto 0.11.9), so the standard upstream backport variant is used.

### Task 3: Upstream Backport (preemptive, 2.1.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Description**:

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists yet
> for this stream. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.
>
> ## Repository
>
> rhtpa-backend
>
> ## Target Branch
>
> release/0.3.z
>
> ## Description
>
> Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
> The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
> to the fixed version (0.11.14+).
>
> Affected versions: 2.1.0 (v0.3.8), 2.1.1 (v0.3.12)
> Source commit(s): v0.3.8, v0.3.12
>
> Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
> Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq
>
> ## Implementation Notes
>
> - Target branch: release/0.3.z
> - **Dependency type**: direct (or transitive -- to be confirmed via Cargo.lock inspection)
> - Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
> - If a direct bump introduces breaking changes, assess whether a
>   code-level workaround is viable (see upstream changelog)
>
> ### Coordination Guidance
>
> This component is shipped to customers. Coordinate with Product Security for CVE assignment,
> advisory preparation, and formal disclosure. Fix must be released via a security advisory
> with explicit CVE-to-component mapping.
>
> ## Acceptance Criteria
>
> - [ ] quinn-proto dependency is >= 0.11.14
> - [ ] No other dependency conflicts introduced
> - [ ] Existing tests pass
>
> ## Test Requirements
>
> - [ ] Existing test suite passes with the updated dependency
>
> ## Dependencies
>
> - Depends on: TC-8001 (parent tracking issue)

**Jira linkage**: Link to TC-8001 with type "Related" (preemptive -- different stream)

---

### Task 4: Downstream Propagation (preemptive, 2.1.x)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Description**:

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists yet
> for this stream. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.
>
> ## Repository
>
> rhtpa-release.0.3.z
>
> ## Target Branch
>
> main
>
> ## Description
>
> Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
> CVE-2026-31812 fix from the upstream backport task.
>
> The upstream backport task bumps quinn-proto to 0.11.14 on release/0.3.z.
> Once that PR merges, update the source pinning in this Konflux release repo
> so the next build ships the fix.
>
> ## Implementation Notes
>
> - Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
> - **Dependency type**: carried forward from upstream task
> - Update the rhtpa-backend reference to the merged commit or new release tag
> - Verify the Konflux build pipeline triggers successfully
>
> ### Coordination Guidance
>
> This component is shipped to customers. Coordinate with Product Security for CVE assignment,
> advisory preparation, and formal disclosure. Fix must be released via a security advisory
> with explicit CVE-to-component mapping.
>
> ## Acceptance Criteria
>
> - [ ] rhtpa-backend reference updated to include the fix
> - [ ] Konflux rebuild triggers new container image
>
> ## Test Requirements
>
> - [ ] Container image builds successfully with the updated reference
>
> ## Dependencies
>
> - Depends on: [upstream-backport-task-key] (upstream backport must merge first)
> - Depends on: TC-8001 (parent tracking issue)

**Jira linkage**:
- Link to TC-8001 with type "Related" (preemptive -- different stream)
- Link to Task 3 (upstream backport) with type "Blocks" (Task 3 blocks Task 4)

---

## Pre-Creation Checklist

- [x] **Task count per stream**: 2.2.x has 2 tasks (dependency bump + downstream propagation) -- matches Cargo/source dependency classification. 2.1.x has 2 preemptive tasks (upstream backport + downstream propagation) -- matches source dependency with fix not available upstream.
- [x] **Cross-stream coverage**: 2.1.x (outside issue scope) has preemptive tasks created (Tasks 3 and 4).
- [x] **Link types**: "Depend" for tasks linked to their own CVE Jira (Tasks 1, 2 to TC-8001). "Related" for preemptive tasks linked to another stream's CVE Jira (Tasks 3, 4 to TC-8001). "Blocks" for upstream to downstream within a stream (Task 1 blocks Task 2; Task 3 blocks Task 4).
- [x] **Preemptive labels**: Tasks 3 and 4 (2.1.x stream) carry the `security-preemptive` label.
- [x] **Coordination guidance**: Each task's Implementation Notes includes the `customer-shipped` guidance: "This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping."
- [x] **Release Jira linking**: Would be performed after Step 7.5 produces release Tasks (not executed in this eval).
- [x] **Dedup consistency**: No dedup detected -- all tasks are new.

## Preemptive Tasks Comment (to post on TC-8001)

> Preemptive remediation tasks created for streams without CVE Jiras:
> - 2.1.x: [task-3-key] (upstream backport, security-preemptive), [task-4-key] (downstream propagation, security-preemptive)
>
> These tasks use the "Related" link type and carry the security-preemptive label.
> When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link
> them and remove the label.

## Post-Triage Summary

Triage of TC-8001 (CVE-2026-31812, quinn-proto panic on large stream counts):

1. **Version impact**: quinn-proto versions before 0.11.14 affect 2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2. Versions 2.2.3+ ship the fixed version (0.11.14).
2. **Affects Versions correction**: RHTPA 2.0.0 (incorrect) corrected to RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 (scoped to 2.2.x stream per issue suffix).
3. **Triage outcome**: Remediation tasks created (Case B) with cross-stream preemptive tasks (Case A for 2.1.x).
4. **Remediation tasks**:
   - 2.2.x: Dependency bump task + downstream propagation task (fix available upstream)
   - 2.1.x: Upstream backport task + downstream propagation task (preemptive, fix not yet on release/0.3.z)
5. **Coordination**: All tasks include customer-shipped coordination guidance (coordinate with Product Security for advisory preparation and formal disclosure).
