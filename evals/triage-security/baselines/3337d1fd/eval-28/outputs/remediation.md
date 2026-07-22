# Step 8 -- Remediation

## Triage Outcome

**Case A: Affected -- create remediation tasks**

The issue is scoped to the 2.2.x stream. Versions 2.2.0, 2.2.1, and 2.2.2 ship
h2 0.4.4, which is within the affected range (< 0.4.5). Versions 2.2.3 and 2.2.4
already ship h2 0.4.5 (the fixed version).

No cross-stream impact: the 2.1.x stream ships h2 0.4.5 and is not affected.

Ecosystem: Cargo (source dependency) -- **two tasks** are required:
1. Upstream backport task (fix in the source repo)
2. Downstream propagation subtask (update the reference in the Konflux release repo)

The vulnerable dependency (h2) is **transitive** (3 levels deep), so the remediation
tasks include the full dependency chain and the two-tier remediation approach.

---

## Task 1: Upstream Backport Task

**Summary**: Remediate CVE-2026-99010: bump h2 to 0.4.5 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99010`

### Task Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99010: h2 - Memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.5) must be updated to the fixed version (0.4.5+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5 (2.2.0), v0.4.8 (2.2.1, 2.2.2)

Upstream fix: https://github.com/hyperium/h2/pull/800
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99010

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend -> reqwest -> hyper -> h2)

### Remediation approach (transitive dependency)

The vulnerable package h2 is a **transitive** dependency pulled in through
intermediate packages (3 levels deep):

```
backend (workspace) -> reqwest (0.12.5) -> hyper (1.4.1) -> h2 (0.4.4)
```

Use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in h2: `reqwest`
- The chain is: reqwest -> hyper -> h2
- Bump reqwest to a version whose transitive closure includes h2 >= 0.4.5
- Check if a newer reqwest release (beyond 0.12.5) depends on a hyper version
  that pulls in h2 >= 0.4.5
- Verify the bump does not introduce breaking API changes to reqwest

**Fallback: pin the transitive dependency directly**
If bumping reqwest is not viable (breaking API changes, no release available
with the fix):
- Run `cargo add h2@0.4.5` to add h2 as a direct dependency, overriding
  the transitive resolution
- Document why the reqwest bump was not viable in the PR description
- Note: this approach may need revisiting when reqwest is eventually bumped,
  as the direct h2 pin may conflict or become redundant

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.5
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8060 (parent tracking issue)

---

## Task 2: Downstream Propagation Subtask

**Summary**: Propagate CVE-2026-99010 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99010`

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-99010
fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.5 on release/0.4.z. Once that PR merges,
update the source pinning in this Konflux release repo so the next build ships
the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: transitive -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- If the upstream fix pinned h2 as a direct dependency (fallback approach),
  verify the pinning is reflected in the downstream build's Cargo.lock after
  the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8060 (parent tracking issue)

---

## Jira Linkage Plan

After creating both tasks:

1. **Link upstream task to TC-8060** (Vulnerability issue):
   ```
   jira.create_link(
     inwardIssue: "TC-8060",
     outwardIssue: <upstream-task-key>,
     type: "Depend"
   )
   ```

2. **Link downstream subtask to TC-8060** (Vulnerability issue):
   ```
   jira.create_link(
     inwardIssue: "TC-8060",
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )
   ```

3. **Link downstream subtask as blocked by upstream task**:
   ```
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

4. **Transition** TC-8060 to In Progress.

5. **Add the `ai-cve-triaged` label** to TC-8060.

6. **Post summary comment** to TC-8060 documenting:
   - Version impact table (3 of 5 versions affected: 2.2.0, 2.2.1, 2.2.2)
   - Affects Versions correction: Current [RHTPA 2.2.0] -> Proposed [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
   - Remediation tasks created (upstream backport + downstream propagation)
   - Dependency chain: backend -> reqwest -> hyper -> h2 (transitive, 3 levels deep)
   - @mention of reporter psirt-analyst (557058:psirt-analyst-mock-id)

## Affects Versions Correction (Step 3)

PSIRT assigned: `RHTPA 2.2.0`
Proposed (scoped to 2.2.x stream): `RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2`

The current Affects Versions is incomplete -- PSIRT only listed RHTPA 2.2.0,
but lock file analysis shows versions 2.2.1 and 2.2.2 also ship the vulnerable
h2 0.4.4. Versions 2.2.3 and 2.2.4 are not affected (ship h2 0.4.5).
