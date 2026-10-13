# Step 8 -- Remediation: TC-8060

## Triage Decision

- **Case**: Case B -- Affected versions exist in the 2.2.x stream
- **Affected versions**: 2.2.0, 2.2.1, 2.2.2 (h2 0.4.4 < fixed version 0.4.5)
- **Not affected**: 2.2.3, 2.2.4 (h2 0.4.5 >= fixed version)
- **Ecosystem**: Cargo (source dependency)
- **Upstream fix available**: YES (release/0.4.z already ships h2 0.4.5)
- **Remediation variant**: Dependency bump + downstream propagation (2 tasks)
- **Dependency type**: Transitive (3 levels deep: reqwest -> hyper -> h2)
- **Cross-stream impact**: None (2.1.x is not affected)

## Remediation Task 1: Dependency Bump (upstream)

**Summary**: Remediate CVE-2026-99010: update h2 to 0.4.5 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99010`

### Task Description

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99010: bump h2 to 0.4.5 via dependency update.
The vulnerable dependency (h2 versions before 0.4.5) is already fixed
upstream -- a package manager update is sufficient.

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5 (2.2.0), v0.4.8 (2.2.1), v0.4.8 (2.2.2 retag)

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99010

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend -> reqwest -> hyper -> h2)
- **Remediation action**: this is a transitive dependency -- h2 is NOT a
  direct dependency of the backend workspace. It is pulled in through the
  chain: reqwest -> hyper -> h2 (3 levels deep).

### Remediation approach (transitive dependency)

The vulnerable package h2 is a **transitive** dependency pulled in through
intermediate packages. Use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in h2: **reqwest** (version 0.12)
  - reqwest depends on hyper, which depends on h2
- Bump reqwest to a version whose transitive closure includes h2 >= 0.4.5
- Run `cargo update -p reqwest` to pull in the latest compatible reqwest
  version, which should update hyper and h2 transitively
- After update, verify h2 >= 0.4.5 in Cargo.lock:
  `grep -A2 'name = "h2"' Cargo.lock`
- Verify the bump does not introduce breaking API changes to reqwest

**Fallback: pin the transitive dependency directly**
If bumping reqwest does not result in h2 >= 0.4.5 (e.g., reqwest pins
an older hyper that pins an older h2, or no compatible reqwest version
includes the fix):
- Run `cargo add h2@0.4.5` to add h2 as a direct dependency, overriding
  the transitive resolution
- Document why the reqwest bump was not viable in the PR description
- Note: this creates a direct dependency on h2 that may need to be
  removed once reqwest/hyper publish versions that include h2 >= 0.4.5
  in their own dependency tree

### Full dependency chain

```
backend (workspace)
  -> reqwest 0.12.5 (direct dependency, production)
    -> hyper 1.4.1
      -> h2 0.4.4 (VULNERABLE -- must be >= 0.4.5)
```

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.5
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8060 (parent tracking issue)
```

## Remediation Task 2: Downstream Propagation

**Summary**: Propagate CVE-2026-99010 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99010`

### Task Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99010 fix from the dependency bump task.

The dependency bump task bumps h2 to 0.4.5 (via reqwest/hyper transitive
update) on release/0.4.z. Once that PR merges, update the source pinning
in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: transitive -- carried forward from upstream task
  (chain: backend -> reqwest -> hyper -> h2)
- Update the backend reference to the merged commit or new release tag
- If the upstream fix pinned h2 directly (fallback approach), verify
  the pinning is reflected in the downstream build's lock file after
  the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] h2 >= 0.4.5 confirmed in the rebuilt container image
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: dependency bump task (upstream fix must merge first)
- Depends on: TC-8060 (parent tracking issue)
```

## Jira Linkage Plan

After creating both remediation tasks:

1. **Depend link**: TC-8060 (CVE) -> dependency bump task (upstream)
   - `jira.create_link(inwardIssue: TC-8060, outwardIssue: <bump-task-key>, type: "Depend")`

2. **Depend link**: TC-8060 (CVE) -> downstream propagation task
   - `jira.create_link(inwardIssue: TC-8060, outwardIssue: <downstream-task-key>, type: "Depend")`

3. **Blocks link**: dependency bump task -> downstream propagation task
   - `jira.create_link(inwardIssue: <bump-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")`
   - Downstream propagation is blocked by the upstream dependency bump

## Affects Versions Correction

- **Current (PSIRT-assigned)**: RHTPA 2.2.0
- **Proposed (scoped to 2.2.x stream)**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- PSIRT version is correct but incomplete -- versions 2.2.1 and 2.2.2 must
  be added (both ship h2 0.4.4 which is within the affected range)
- Versions 2.2.3 and 2.2.4 are NOT included (they ship h2 0.4.5, the fixed version)

## Transitive Dependency Context for Remediation

The vulnerable library h2 is a **transitive dependency** at 3 levels of depth:

```
backend (workspace)
  -> reqwest 0.12.5     [direct dependency - production runtime]
    -> hyper 1.4.1      [intermediate - HTTP implementation]
      -> h2 0.4.4       [VULNERABLE - HTTP/2 protocol implementation]
```

This transitive chain determines the remediation approach:

### Two-Tier Remediation Strategy

**Tier 1 (preferred): Bump the direct dependency**
- The direct dependency in the chain is `reqwest` (version 0.12)
- Bump reqwest to a version that transitively pulls in h2 >= 0.4.5
- Command: `cargo update -p reqwest`
- After update, verify: `grep -A2 'name = "h2"' Cargo.lock` shows version >= 0.4.5
- This approach is preferred because it maintains the natural dependency
  graph without introducing artificial direct dependencies

**Tier 2 (fallback): Pin the transitive dependency**
- If reqwest cannot be bumped to a version with h2 >= 0.4.5 (due to breaking
  API changes in reqwest, or hyper pinning an older h2):
- Command: `cargo add h2@0.4.5`
- This overrides the transitive resolution by making h2 a direct dependency
- Document the rationale in the PR description
- Track removal of the direct h2 pin once the intermediate packages
  (hyper, reqwest) publish compatible versions

### Coordination considerations

- The fix (h2 0.4.5) is already available upstream as confirmed by the
  upstream fix PR: https://github.com/hyperium/h2/pull/800
- Versions 2.2.3+ in the 2.2.x stream already ship h2 0.4.5, confirming
  that the upstream branch release/0.4.z has already picked up the fix
- The remediation tasks address the gap in versions 2.2.0-2.2.2 and ensure
  the fix is properly tracked and documented
