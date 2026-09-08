# Step 8 -- Remediation

## Triage Decision

- **Case B: Affected -- create remediation tasks**
- Affected versions in the 2.2.x stream: 2.2.0, 2.2.1, 2.2.2
- Not affected: 2.2.3, 2.2.4 (already ship h2 0.4.5)
- Cross-stream impact: None (2.1.x stream ships h2 0.4.5 in all versions)
- Ecosystem: Cargo (source dependency) -- requires 2 tasks per stream

## Remediation Tasks for Stream 2.2.x

Since h2 is a **transitive dependency** (backend -> reqwest -> hyper -> h2, 3 levels deep), the remediation tasks document the full dependency chain and specify the two-tier remediation approach.

---

### Task 1: Upstream Backport Task

**Summary**: Remediate CVE-2026-99010: bump h2 to 0.4.5 via reqwest dependency update (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99010`

#### Repository

rhtpa-backend

#### Target Branch

release/0.4.z

#### Description

Remediate CVE-2026-99010: h2 memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.5) must be updated to the fixed version (0.4.5+).

h2 is a **transitive dependency** pulled in through the following chain:

```
backend (workspace) -> reqwest -> hyper -> h2
Type: transitive (3 levels deep)
Profile: production (reqwest is a runtime dependency)
```

Affected versions: 2.2.0 (backend v0.4.5), 2.2.1 (backend v0.4.8), 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/hyperium/h2/pull/800
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99010

Note: versions 2.2.3+ (backend v0.4.11+) already ship h2 0.4.5 and are not affected.

#### Implementation Notes

- Target branch: `release/0.4.z`
- **Dependency type**: transitive (chain: backend -> reqwest -> hyper -> h2)

##### Remediation approach (transitive dependency -- two-tier)

h2 is a transitive dependency pulled in through reqwest -> hyper -> h2. Use a two-tier approach:

**Preferred: bump the direct dependency (reqwest)**
- Identify a version of reqwest whose transitive closure includes h2 >= 0.4.5
- Check reqwest releases after 0.12.5 for updated hyper/h2 dependencies
- Bump reqwest in `backend/Cargo.toml` to a version that pulls in h2 >= 0.4.5
- Run `cargo update -p reqwest` and verify h2 version in Cargo.lock is >= 0.4.5
- Verify the bump does not introduce breaking API changes to reqwest

**Fallback: pin h2 directly**
If bumping reqwest is not viable (breaking API changes, no reqwest release available with h2 >= 0.4.5):
- Run `cargo add h2@0.4.5` in the backend workspace to add h2 as a direct dependency, overriding the transitive resolution
- Document why the reqwest bump was not viable in the PR description
- This is a temporary workaround; the direct pin should be removed once a compatible reqwest version is available

##### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

#### Acceptance Criteria

- [ ] h2 dependency is >= 0.4.5 (verified in Cargo.lock)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

#### Test Requirements

- [ ] Existing test suite passes with the updated dependency

#### Dependencies

- Depends on: TC-8060 (parent tracking issue)

---

### Task 2: Downstream Propagation Subtask

**Summary**: Propagate CVE-2026-99010 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99010`

**Blocked by**: Task 1 (upstream backport must merge first)

#### Repository

rhtpa-release.0.4.z

#### Target Branch

main

#### Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-99010 fix from the upstream backport task.

The upstream backport task bumps h2 to 0.4.5 (via reqwest dependency update) on `release/0.4.z`. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

h2 is a transitive dependency (backend -> reqwest -> hyper -> h2). The upstream fix either bumps reqwest to pull in h2 >= 0.4.5, or pins h2 directly as a fallback.

#### Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: transitive -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag from the upstream backport
- If the upstream fix pinned h2 directly (fallback approach), verify the pinning is reflected in the downstream build's Cargo.lock after the source reference update
- Verify the Konflux build pipeline triggers successfully

##### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

#### Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the CVE-2026-99010 fix
- [ ] Konflux rebuild triggers new container image
- [ ] h2 version in the rebuilt container is >= 0.4.5

#### Test Requirements

- [ ] Container image builds successfully with the updated reference

#### Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8060 (parent tracking issue)

---

## Jira Linkage Plan

1. Link upstream backport task to TC-8060 with type "Depend"
2. Link downstream propagation task to TC-8060 with type "Depend"
3. Link downstream propagation task as blocked by upstream backport task with type "Blocks"
4. Transition TC-8060 to In Progress
5. Add `ai-cve-triaged` label to TC-8060

## Post-Triage Summary (to be posted as comment on TC-8060)

Version impact analysis for CVE-2026-99010 (h2 < 0.4.5):

| Version | h2 version | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.2.0 | 0.4.4 | YES | |
| 2.2.1 | 0.4.4 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.4.5 | NO | at fix threshold |
| 2.2.4 | 0.4.5 | NO | at fix threshold |

Dependency chain: backend -> reqwest -> hyper -> h2 (transitive, 3 levels deep, production profile)

Affects Versions correction: RHTPA 2.2.0 is correct (PSIRT-assigned). Additionally affected: RHTPA 2.2.1, RHTPA 2.2.2.

Triage outcome: Remediation required. Two tasks created for the 2.2.x stream:
- Upstream backport task: bump h2 to >= 0.4.5 via reqwest update on release/0.4.z
- Downstream propagation task: update rhtpa-backend ref in rhtpa-release.0.4.z (blocked by upstream task)

Cross-stream impact: None -- 2.1.x stream ships h2 0.4.5 in all versions.

@psirt-analyst (557058:psirt-analyst-mock-id) -- triage complete.

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks for 2.2.x stream (Cargo = source dependency ecosystem)
- [x] **Cross-stream coverage**: 2.1.x stream is not affected (h2 already at 0.4.5); no preemptive tasks needed
- [x] **Link types**: "Depend" for both tasks linked to TC-8060; "Blocks" for upstream -> downstream within the stream
- [x] **Preemptive labels**: Not applicable (no cross-stream impact requiring preemptive tasks)
- [x] **Coordination guidance**: Included in both tasks (deployment context: upstream)
- [x] **Dependency chain**: Full transitive chain (reqwest -> hyper -> h2) documented in upstream task
- [x] **Two-tier remediation**: Preferred (bump reqwest) and fallback (pin h2 directly) approaches specified
