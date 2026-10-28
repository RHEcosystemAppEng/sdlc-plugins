# Step 8 -- Remediation: TC-8001

## Triage Outcome

**Case B (Affected)** for scoped stream 2.2.x, plus **Case A (Cross-stream impact)** for 2.1.x.

Affected versions within scope (2.2.x): 2.2.0, 2.2.1, 2.2.2
Affected versions outside scope (2.1.x): 2.1.0, 2.1.1

Since the upstream fix is already available on the 2.2.x stream (v0.4.11+ ships quinn-proto 0.11.14), the remediation uses the **dependency bump** variant (not upstream backport).

## Remediation Tasks -- Stream 2.2.x (Scoped)

### Task 1: Dependency Bump (Source Repository)

**Summary**: Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description**:

> ## Repository
>
> backend
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
> - **Dependency type**: to be determined via Cargo.lock/Cargo.toml analysis
> - **Remediation action**: run `cargo update -p quinn-proto` to pull in the latest compatible version
> - If the update pulls a version that still falls within the affected range,
>   pin explicitly: `cargo add quinn-proto@0.11.14`
> - Verify the lock file reflects >= 0.11.14 after the update
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

**Link**: Depend (TC-8001 inward, this task outward)

---

### Task 2: Downstream Propagation (Konflux Release Repo)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)

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
> Update backend reference in rhtpa-release.0.4.z to pick up the
> CVE-2026-31812 fix from the dependency bump task.
>
> The dependency bump task bumps quinn-proto to 0.11.14
> on release/0.4.z. Once that PR merges, update the source pinning in this
> Konflux release repo so the next build ships the fix.
>
> ## Implementation Notes
>
> - Source pinning method: `artifacts.lock.yaml` (download URL contains tag)
> - Update the backend reference to the merged commit or new release tag
> - Verify the Konflux build pipeline triggers successfully
>
> ## Acceptance Criteria
>
> - [ ] backend reference updated to include the fix
> - [ ] Konflux rebuild triggers new container image
>
> ## Test Requirements
>
> - [ ] Container image builds successfully with the updated reference
>
> ## Dependencies
>
> - Depends on: dependency bump task (upstream fix must merge first)
> - Depends on: TC-8001 (parent tracking issue)

**Link**: Depend (TC-8001 inward, this task outward)
**Link**: Blocks (dependency bump task inward/blocks this downstream task outward)

---

## Preemptive Remediation Tasks -- Stream 2.1.x (Cross-Stream, Case A)

Since TC-8001 is scoped to 2.2.x but 2.1.x is also affected, preemptive remediation tasks are created for 2.1.x (assuming no sibling CVE Jira exists for 2.1.x).

### Task 3: Preemptive Upstream Backport (Source Repository, 2.1.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Description**:

> > **Preemptive remediation**: This task was created proactively from cross-stream
> > impact analysis of TC-8001 (stream 2.2.x).
> > No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> > this task will be linked and the `security-preemptive` label removed.
>
> ## Repository
>
> backend
>
> ## Target Branch
>
> release/0.3.z
>
> ## Description
>
> Remediate CVE-2026-31812: bump quinn-proto to 0.11.14.
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
> - **Dependency type**: to be determined via Cargo.lock/Cargo.toml analysis
> - The upstream fix may need to be backported to the release/0.3.z branch if
>   quinn-proto 0.11.14 is not yet available on this branch
> - If a direct bump introduces breaking changes, assess whether a
>   code-level workaround is viable (see upstream changelog)
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
> - Depends on: TC-8001 (originating CVE tracking issue)

**Link**: Related (TC-8001 inward, this task outward) -- uses Related, not Depend, because this is a preemptive task for a different stream

---

### Task 4: Preemptive Downstream Propagation (Konflux Release Repo, 2.1.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Description**:

> > **Preemptive remediation**: This task was created proactively from cross-stream
> > impact analysis of TC-8001 (stream 2.2.x).
> > No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> > this task will be linked and the `security-preemptive` label removed.
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
> Update backend reference in rhtpa-release.0.3.z to pick up the
> CVE-2026-31812 fix from the preemptive upstream task.
>
> The upstream task bumps quinn-proto to 0.11.14
> on release/0.3.z. Once that PR merges, update the source pinning in this
> Konflux release repo so the next build ships the fix.
>
> ## Implementation Notes
>
> - Source pinning method: `artifacts.lock.yaml` (download URL contains tag)
> - Update the backend reference to the merged commit or new release tag
> - Verify the Konflux build pipeline triggers successfully
>
> ## Acceptance Criteria
>
> - [ ] backend reference updated to include the fix
> - [ ] Konflux rebuild triggers new container image
>
> ## Test Requirements
>
> - [ ] Container image builds successfully with the updated reference
>
> ## Dependencies
>
> - Depends on: preemptive upstream task (upstream fix must merge first)
> - Depends on: TC-8001 (originating CVE tracking issue)

**Link**: Related (TC-8001 inward, this task outward) -- preemptive, uses Related
**Link**: Blocks (preemptive upstream task inward/blocks this downstream task outward)

---

## Summary of All Remediation Tasks

| # | Stream | Type | Summary | Labels | Link to TC-8001 |
|---|--------|------|---------|--------|-----------------|
| 1 | 2.2.x | Dependency bump | Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x) | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 2 | 2.2.x | Downstream propagation | Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x) | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 3 | 2.1.x | Preemptive upstream | Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |
| 4 | 2.1.x | Preemptive downstream | Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |

## Affects Versions Correction

- **Remove**: RHTPA 2.0.0 (no such version stream exists)
- **Add**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

## Cross-Stream Impact Comment

Post to TC-8001:

> Cross-stream impact: quinn-proto (versions before 0.11.14) also affects stream 2.1.x
> based on lock file analysis. Versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9.
> Preemptive remediation tasks have been created for stream 2.1.x.
> These streams are tracked by preemptive tasks (see Related links)
> or may require separate PSIRT triage.

## Post-Triage Actions

1. Add label `ai-cve-triaged` to TC-8001
2. Post summary comment to TC-8001 documenting:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 removed; RHTPA 2.2.0, 2.2.1, 2.2.2 added)
   - Remediation tasks created (4 total: 2 for 2.2.x, 2 preemptive for 2.1.x)
   - Cross-stream impact notice for 2.1.x
