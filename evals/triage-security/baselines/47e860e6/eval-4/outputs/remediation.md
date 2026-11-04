# TC-8004 — Steps 7, 7.5, 8: Remediation

## Decision

- Affected supported versions: **RHTPA 2.1.0 and 2.1.1 (stream 2.1.x)**.
- Unaffected: the whole 2.2.x stream (2.2.0 through 2.2.4 ship h2 >= 0.4.8).
- The issue is unscoped, so **Case A (cross-stream comment / preemptive tasks) is skipped**. Case B applies to the affected streams only.
- **Case B: create remediation tasks for stream 2.1.x only.** No tasks are created for 2.2.x.
- Ecosystem Cargo is a source dependency, so **2 tasks** are created. Step 2.5 could not confirm a fix on `release/0.3.z`, so the pair is upstream backport + downstream propagation.
- Case C (close as Not a Bug) does not apply because 2.1.x is affected.

## Step 7 — Concurrent triage detection

Skipped. The Upstream Affected Component custom field is not configured.

## Step 7.5 — Release Jira orchestration (stream 2.1.x only)

- 7.5.1: Find or create release Epic `RHTPA <next 2.1.x version> Release Tasks`. The latest released 2.1.x version is 2.1.1, so the likely candidate is **RHTPA 2.1.2**. Confirm this with the engineer; the version decision needs individual confirmation and is not assumed.
- 7.5.2: Find or create child Task `RHTPA <version> CVE triage` (individual confirmation).
- 7.5.3: Cross-CVE dedup is skipped (component field not configured). No dedup, so tasks are created.
- No release Jira is created for 2.2.x, since that stream is unaffected.

---

## Task 1 — Upstream backport (2.1.x)

**Summary:** Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)
**Project:** TC | **Type:** Task | **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-33501`

```
## Repository

backend (rhtpa-backend)

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 memory exhaustion via excessive CONTINUATION frames
(unbounded header-block accumulation).
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
Source commit(s): backend v0.3.8 (2.1.0), backend v0.3.12 (2.1.1)

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: to be confirmed. The dependency chain was not available during
  triage; h2 is typically transitive via hyper (e.g. backend -> reqwest/axum -> hyper -> h2).
  Confirm with `cargo tree -i h2` on release/0.3.z.
- Currently resolved: h2 0.4.5 in Cargo.lock.
- If the vulnerable dependency is dev-only or build-only, the remediation priority is
  Normal regardless of CVE severity. Add the `dev-dependency` label to the task.

### Remediation approach (direct dependency)

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level
  workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in h2 (see dependency chain above)
- Bump it to a version whose transitive closure includes h2 >= 0.4.8
  (within the 0.4.x semver range, `cargo update -p h2` may be sufficient)
- Verify the bump does not introduce breaking API changes

**Fallback: pin the transitive dependency directly**
- Cargo: `cargo add h2@0.4.8` to override the transitive resolution
- Document why the direct dep bump was not viable in the PR description

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)
```

(No Coordination Guidance subsection: the Source Repositories table has no Deployment Context column.)

---

## Task 2 — Downstream propagation (2.1.x)

**Summary:** Propagate CVE-2026-33501 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)
**Project:** TC | **Type:** Task | **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-33501`

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from <Task 1 key>.

The upstream backport (<Task 1 key>) bumps h2 to 0.4.8 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release repo so
the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains the backend
  tag, currently `v0.3.12`)
- **Dependency type**: carried forward from the upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned h2 directly (fallback approach), verify the pinning is
  reflected in the downstream build's lock file after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <Task 1 key> (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

---

## Creation sequence (all require confirmation; not executed in the eval)

1. Create Task 1, then post its description digest comment (`[sdlc-workflow] Description digest: sha256-...`).
2. Create Task 2, then post its description digest comment.
3. Links:
   - TC-8004 -> Task 1 (`Depend`)
   - TC-8004 -> Task 2 (`Depend`)
   - Task 1 -> Task 2 (`Blocks`: downstream blocked by upstream)
   - Task 1 -> release Task (`Blocks`), Task 2 -> release Task (`Blocks`), if Step 7.5 is active
   - release Task -> TC-8004 (`Related`)
4. TC-8004 is already ASSIGNED from Step 0.8, so the In Progress transition is skipped. Confirm the assignment.
5. Comment on TC-8004: "Remediation tasks created: <Task 1> (upstream backport), <Task 2> (downstream propagation, blocked by <Task 1>)" plus the Comment Footnote.

**No tasks for 2.2.x.** That stream already ships h2 0.4.8/0.4.9.

## Pre-creation checklist

- [x] Task count per stream: 2.1.x has 2 (Cargo, a source dependency). 2.2.x has 0 (not affected).
- [x] Cross-stream coverage: N/A (unscoped issue, Case A skipped).
- [x] Link types: Depend (tasks to own CVE), Blocks (upstream to downstream, and remediation to release Task).
- [x] Preemptive labels: none (the stream is tracked by this issue itself).
- [x] Coordination guidance: omitted (no Deployment Context column).
- [x] Release Jira linking: planned for the 2.1.x release Task, if confirmed.
- [x] Dedup consistency: no dedup (Step 7.5.3 skipped).

## Post-triage summary (proposed)

- Add label `ai-cve-triaged` to TC-8004.
- Summary comment containing: the version impact table (2.1.x affected, 2.2.x not affected), the Affects Versions correction [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1], the outcome (remediation created for 2.1.x only), links to both tasks, release Epic/Task keys, no dedup, an ADF @mention of the issue reporter, and the Comment Footnote.

## Open items for the engineer

1. The matrix is stale (last updated 2026-06-28). Refresh it before applying.
2. Confirm the h2 dependency chain (direct vs transitive) and the `release/0.3.z` HEAD h2 version. If HEAD is already >= 0.4.8, switch to the dependency-bump variant.
3. Confirm 2.1.x lifecycle status (Step 5) and the release version for 2.1.x (likely 2.1.2).
4. The due date 2026-08-01 has already passed.
