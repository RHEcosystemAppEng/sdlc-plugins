# Step 8 -- Remediation

## Triage Outcome: Case A -- Affected (create remediation tasks)

Affected versions in the 2.2.x stream: 2.2.0, 2.2.1, 2.2.2
Not affected: 2.2.3, 2.2.4 (already ship h2 0.4.5)

Ecosystem: Cargo (source dependency) -- requires **two** tasks:
1. Upstream backport task (fix in rhtpa-backend source repo)
2. Downstream propagation subtask (update reference in rhtpa-release.0.4.z)

---

## Task 1: Upstream Backport Task

**Summary**: Remediate CVE-2026-99010: bump h2 to 0.4.5 (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99010`

### Repository

rhtpa-backend

### Target Branch

release/0.4.z

### Description

Remediate CVE-2026-99010: h2 memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.5) must be updated to the fixed version (0.4.5+).

h2 is a **transitive** dependency pulled in through the chain:
**backend -> reqwest -> hyper -> h2** (3 levels deep)

Affected versions: 2.2.0, 2.2.1, 2.2.2 (all ship h2 0.4.4)
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is a retag of v0.4.8)

Upstream fix: https://github.com/hyperium/h2/pull/800
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99010

### Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend -> reqwest -> hyper -> h2)

#### Remediation approach (transitive dependency)

The vulnerable package h2 is a **transitive** dependency, pulled in through
intermediate packages (reqwest -> hyper -> h2). Use a two-tier approach:

**Preferred: bump the direct dependency (reqwest)**
- Identify a version of reqwest whose transitive closure includes h2 >= 0.4.5
- Bump reqwest in backend/Cargo.toml to that version
- Run `cargo update` to regenerate Cargo.lock and verify h2 resolves to >= 0.4.5
- Verify the bump does not introduce breaking API changes to reqwest

**Fallback: pin the transitive dependency directly**
If bumping reqwest is not viable (breaking API changes, no release available
with the fix):
- `cargo add h2@0.4.5` to add h2 as a direct dependency, overriding the
  transitive resolution
- Document why the reqwest bump was not viable in the PR description

#### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

### Acceptance Criteria

- [ ] h2 dependency is >= 0.4.5 (verified in Cargo.lock)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

### Test Requirements

- [ ] Existing test suite passes with the updated dependency

### Dependencies

- Depends on: TC-8060 (parent tracking issue)

---

## Task 2: Downstream Propagation Subtask

**Summary**: Propagate CVE-2026-99010 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99010`

### Repository

rhtpa-release.0.4.z

### Target Branch

main

### Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99010 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.5 (via reqwest update or direct h2
pinning) on release/0.4.z. Once that PR merges, update the source pinning
in this Konflux release repo so the next build ships the fix.

### Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: transitive -- carried forward from upstream task
- Dependency chain: backend -> reqwest -> hyper -> h2
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned h2 directly (fallback approach with `cargo add h2@0.4.5`),
  verify the pinning is reflected in the downstream build's Cargo.lock after the
  source reference update
- Verify the Konflux build pipeline triggers successfully

### Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image
- [ ] New container image ships h2 >= 0.4.5

### Test Requirements

- [ ] Container image builds successfully with the updated reference

### Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8060 (parent tracking issue)

---

## Jira Linkage Plan

1. Link upstream backport task to TC-8060 with type "Depend"
2. Link downstream propagation subtask to upstream backport task with type "Blocks"
3. Link downstream propagation subtask to TC-8060 with type "Depend"
4. Transition TC-8060 to In Progress
5. Add `ai-cve-triaged` label to TC-8060

## Cross-Stream Impact

No cross-stream impact. The 2.1.x stream is not affected (all versions ship
h2 0.4.5). Case B does not apply -- no preemptive remediation tasks needed.
