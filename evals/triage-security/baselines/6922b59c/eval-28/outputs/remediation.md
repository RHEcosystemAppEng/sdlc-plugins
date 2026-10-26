# Step 8 -- Remediation

## Triage Outcome: Case B -- Affected versions require remediation

Affected versions within the 2.2.x stream: **2.2.0, 2.2.1, 2.2.2**
Not affected: 2.2.3, 2.2.4 (ship h2 0.4.5, at or above fix threshold)
Cross-stream impact: 2.1.x is NOT affected (h2 0.4.5 in all versions)

### Ecosystem classification

| Property | Value |
|----------|-------|
| Ecosystem | Cargo (source dependency) |
| Fix available upstream? | Yes (h2 0.4.5 ships in 2.2.3+) |
| Task variant | Dependency bump + downstream propagation |
| Tasks to create | 2 |

### Dependency chain

```
backend (workspace) -> reqwest (0.12) -> hyper (1.4.1) -> h2 (0.4.4, vulnerable)
```

- h2 is a **transitive dependency** (3 levels deep)
- Profile: **production** (reqwest is a runtime dependency)
- h2 is NOT a direct dependency in `backend/Cargo.toml`

---

## Task 1: Dependency Bump Task

**Summary**: Remediate CVE-2026-99010: update h2 to 0.4.5 (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99010`

### Task Description

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99010: bump h2 to 0.4.5 via dependency update.
The vulnerable dependency (h2 < 0.4.5) is already fixed upstream --
a package manager update is sufficient.

h2 allows a remote attacker to cause memory exhaustion by sending a
large number of CONTINUATION frames (denial of service).

Affected versions: 2.2.0, 2.2.1, 2.2.2
Source commit(s): v0.4.5 (2.2.0), v0.4.8 (2.2.1/2.2.2)

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99010

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend -> reqwest -> hyper -> h2)
- **Remediation action**: use the two-tier approach for transitive dependencies:

### Remediation approach (transitive dependency)

The vulnerable package h2 is a **transitive** dependency, pulled in through
the chain: `backend -> reqwest (0.12) -> hyper (1.4.1) -> h2`.

**Preferred: bump the direct dependency (reqwest)**
- Check if a newer version of reqwest (>= 0.12) includes hyper with
  h2 >= 0.4.5 in its transitive closure
- Run `cargo update -p reqwest` to pull the latest compatible reqwest
  version, which should transitively update hyper and h2
- Verify that h2 >= 0.4.5 appears in the updated Cargo.lock
- Verify the bump does not introduce breaking API changes to reqwest

**Fallback: pin the transitive dependency directly**
If bumping reqwest does not bring in h2 >= 0.4.5 (e.g., hyper pins an
older h2 version):
- Run `cargo add h2@0.4.5` to add h2 as a direct dependency, overriding
  the transitive resolution
- Alternatively, run `cargo update -p h2` to update h2 specifically
  within the existing dependency constraints
- Document why the reqwest bump was not sufficient in the PR description

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.5 in Cargo.lock
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8060 (parent tracking issue)
```

---

## Task 2: Downstream Propagation Task

**Summary**: Propagate CVE-2026-99010 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)

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

The dependency bump task updates h2 to 0.4.5 on release/0.4.z by bumping
the transitive dependency chain (backend -> reqwest -> hyper -> h2). Once
that PR merges, update the source pinning in this Konflux release repo so
the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: transitive -- carried forward from upstream task
- **Dependency chain**: backend -> reqwest -> hyper -> h2
- Update the backend reference to the merged commit or new release tag
  that includes h2 >= 0.4.5
- If the upstream fix pinned h2 directly (fallback approach via
  `cargo add h2@0.4.5`), verify the pinning is reflected in the
  downstream build's Cargo.lock after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the h2 >= 0.4.5 fix
- [ ] Konflux rebuild triggers new container image
- [ ] Built container image no longer ships h2 < 0.4.5

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: Task 1 (dependency bump must merge first)
- Depends on: TC-8060 (parent tracking issue)
```

---

## Jira Linkage Plan

After creating both tasks:

1. **Link Task 1 (dependency bump) to TC-8060** (Vulnerability):
   - Link type: `Depend` (inward: TC-8060, outward: Task 1)

2. **Link Task 2 (downstream propagation) to TC-8060** (Vulnerability):
   - Link type: `Depend` (inward: TC-8060, outward: Task 2)

3. **Link Task 2 as blocked by Task 1** (upstream -> downstream):
   - Link type: `Blocks` (inward: Task 1, outward: Task 2)

4. **Post description digest comments** on both tasks before creating links.

5. **Release Jira linking** (if release Task exists from Step 7.5):
   - Link Task 1 -> release Task (Blocks)
   - Link Task 2 -> release Task (Blocks)
   - Link TC-8060 -> release Task (Related)

## Post-Triage Actions

1. **Add label** `ai-cve-triaged` to TC-8060
2. **Correct Affects Versions** to include RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
3. **Post summary comment** to TC-8060 documenting:
   - Version impact table (3 affected, 2 not affected)
   - Affects Versions correction (added 2.2.1, 2.2.2)
   - Remediation tasks created (dependency bump + downstream propagation)
   - Transitive dependency chain: backend -> reqwest -> hyper -> h2
   - Two-tier remediation approach documented in tasks
   - `@`mention of reporter psirt-analyst (account ID: 557058:psirt-analyst-mock-id)
