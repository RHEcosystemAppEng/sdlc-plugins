# Step 8 -- Remediation: CVE-2026-99010 (h2) -- Stream 2.2.x

## Triage Decision

- **Case B**: Affected versions exist within the scoped stream (2.2.0, 2.2.1, 2.2.2)
- Ecosystem: Cargo (source dependency) -- 2 tasks required per stream
- Versions 2.2.3+ already ship h2 0.4.5 (fixed), confirming the upstream fix is available
- Remediation variant: **dependency bump + downstream propagation** (fix already available upstream)

## Dependency Chain

```
backend (workspace) -> reqwest -> hyper -> h2
Type: transitive (3 levels deep)
Profile: production (reqwest is a runtime dependency)
```

h2 is NOT a direct dependency. The two-tier remediation approach applies:
- **Preferred**: Bump the direct dependency (reqwest) to a version whose transitive closure includes h2 >= 0.4.5
- **Fallback**: Pin h2 directly via `cargo add h2@0.4.5` if bumping reqwest is not viable

---

## Task 1: Dependency Bump (Upstream)

**Summary**: Remediate CVE-2026-99010: update h2 to 0.4.5 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99010`

### Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99010: bump h2 to 0.4.5 via dependency update.
The vulnerable dependency (h2 versions before 0.4.5) is already fixed upstream --
a package manager update is sufficient.

Affected versions: 2.2.0, 2.2.1, 2.2.2
Source commit(s): v0.4.5 (2.2.0), v0.4.8 (2.2.1, 2.2.2)

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99010

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend -> reqwest -> hyper -> h2)
- **Remediation action**: Because h2 is a transitive dependency (3 levels deep), use the two-tier approach:

### Preferred: bump the direct dependency

1. Check if a newer version of reqwest (currently 0.12.5) is available whose transitive closure includes h2 >= 0.4.5
2. If available: `cargo update -p reqwest` or update the version constraint in backend/Cargo.toml
3. Verify that the updated Cargo.lock shows h2 >= 0.4.5
4. Verify the reqwest API changes are backward-compatible with backend usage

### Fallback: pin the transitive dependency directly

If bumping reqwest does not result in h2 >= 0.4.5 (because hyper or reqwest pins an older h2):
1. `cargo add h2@0.4.5` to add h2 as a direct dependency, overriding the transitive resolution
2. Document why the reqwest bump was not viable in the PR description
3. Verify Cargo.lock shows h2 >= 0.4.5 after the override

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.5 (verify in Cargo.lock)
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8060 (parent tracking issue)

---

## Task 2: Downstream Propagation

**Summary**: Propagate CVE-2026-99010 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99010`

### Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99010 fix from the upstream dependency bump task.

The upstream dependency bump task bumps h2 to 0.4.5 (via reqwest/hyper transitive chain)
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: transitive -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- If the upstream fix pinned h2 as a direct transitive override (fallback approach), verify the pinning is reflected in the downstream build's Cargo.lock after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the h2 >= 0.4.5 fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream dependency bump task (upstream bump must merge first)
- Depends on: TC-8060 (parent tracking issue)

---

## Jira Linkage Plan

1. **Depend**: TC-8060 (CVE) -> upstream dependency bump task
2. **Depend**: TC-8060 (CVE) -> downstream propagation task
3. **Blocks**: upstream dependency bump task -> downstream propagation task (downstream blocked by upstream)

## Post-Triage Actions

1. Correct Affects Versions: `[RHTPA 2.2.0]` -> `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
2. Add `ai-cve-triaged` label to TC-8060
3. Post summary comment on TC-8060 with version impact table, remediation task links, and @mention of reporter (psirt-analyst, account ID: 557058:psirt-analyst-mock-id)
4. Transition TC-8060 to In Progress
