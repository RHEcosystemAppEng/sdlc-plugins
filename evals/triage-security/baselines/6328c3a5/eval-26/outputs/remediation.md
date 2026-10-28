# Step 8 -- Remediation

## Triage Outcome

**Case B: Affected -- create remediation tasks** for the 2.2.x stream.

All 2.2.x versions ship criterion 0.5.1 (affected range: < 0.5.2). Since criterion is a Cargo source dependency, two tasks are created: upstream backport + downstream propagation.

**Dev-dependency handling**: criterion is a dev-only dependency (`[dev-dependencies]`). Per the dependency scope decision tree, both tasks receive the `dev-dependency` label and priority is overridden to **Normal** regardless of CVE severity (CVSS 5.3 Medium).

## Cross-stream Impact (Case A)

The 2.1.x stream is also affected (criterion 0.5.1 in tags v0.3.8 and v0.3.12), but this issue is scoped to 2.2.x via the `[rhtpa-2.2]` suffix. A cross-stream impact comment would be posted to TC-8050:

> Cross-stream impact: criterion < 0.5.2 also affects stream 2.1.x based on lock file analysis. This stream is tracked by a companion issue (see Related links) or may require separate PSIRT triage.

---

## Remediation Task 1: Upstream Backport (2.2.x)

**Summary**: Remediate CVE-2026-99001: bump criterion to 0.5.2 (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority**: Normal

### Task Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99001: path traversal in benchmark output in criterion.
The vulnerable dependency (criterion < 0.5.2) must be updated to the fixed version (0.5.2+).

This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only).

Affected versions: 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4
Source commit(s): v0.4.5, v0.4.8, v0.4.11, v0.4.12

CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct dev-dependency (chain: backend -> criterion)
- **Dependency scope**: dev-only (`[dev-dependencies]` in backend/Cargo.toml) -- NOT shipped in production, used for benchmarks only
- Remediation priority is Normal regardless of CVE severity. `dev-dependency` label applied.

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update criterion dependency to >= 0.5.2 in backend/Cargo.toml `[dev-dependencies]`
- Run `cargo update -p criterion` to update Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8050 (parent tracking issue)

---

## Remediation Task 2: Downstream Propagation (2.2.x)

**Summary**: Propagate CVE-2026-99001 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority**: Normal

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-99001 fix from the upstream backport task.

The upstream backport bumps criterion to 0.5.2 on release/0.4.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only).

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct dev-dependency -- carried forward from upstream task
- **Dependency scope**: dev-only -- NOT shipped in production
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8050 (parent tracking issue)

---

## Jira Linkage Plan

1. **Depend**: TC-8050 (CVE) -> upstream backport task
2. **Depend**: TC-8050 (CVE) -> downstream propagation task
3. **Blocks**: upstream backport task -> downstream propagation task
4. Release Jira linking (if Step 7.5 produced a release Task): remediation tasks -> release Task (Blocks), TC-8050 -> release Task (Related)

## Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8050
2. Post summary comment to TC-8050 documenting:
   - Version impact table (all 2.2.x versions affected)
   - Dependency chain: dev-only direct dependency, NOT shipped in production
   - Remediation tasks created with `dev-dependency` label and Normal priority
   - Cross-stream impact on 2.1.x noted
