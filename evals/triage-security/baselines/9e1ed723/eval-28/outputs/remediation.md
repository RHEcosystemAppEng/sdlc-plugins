# TC-8060 — Step 8: Remediation

## Decision

- Issue scope: 2.2.x (scoped by `[rhtpa-2.2]`).
- Affected in scope: RHTPA 2.2.0, 2.2.1, 2.2.2 (h2 0.4.4 < 0.4.5).
- Other streams affected: none based on available data (2.1.x shows h2 0.4.5), so **Case A is not triggered**.
- Ecosystem: Cargo (source dependency). **Case B: 2 tasks for stream 2.2.x**, an upstream backport (two-tier transitive approach) plus downstream propagation (blocked by the upstream task).
- Dependency type: **transitive**, chain `backend (workspace) → reqwest → hyper → h2` (3 levels deep), production profile.
- Dedup (Step 7.5.3): not applicable (Upstream Affected Component not configured).
- Coordination Guidance: left out. The Source Repositories table has no Deployment Context column, so `remediation-templates.md` says to omit this subsection.
- Labels: `ai-generated-jira`, `Security`, `CVE-2026-99010` (no `dev-dependency`, because this is a production dependency; no `security-preemptive`, because the task is for the issue's own stream).

All Jira mutations below are **proposed only**. Each would need engineer confirmation and was not executed in this eval.

---

## Task 1 — Upstream backport (2.2.x)

**Summary**: Remediate CVE-2026-99010: bump h2 to 0.4.5 (2.2.x)
**Labels**: ai-generated-jira, Security, CVE-2026-99010
**Issue type**: Task, project TC

```
## Repository

backend (rhtpa-backend)

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99010: h2 memory exhaustion via CONTINUATION frames (DoS,
CVSS 7.5). h2 before 0.4.5 does not limit the number of CONTINUATION frames
received for a single HEADERS frame, so an attacker can exhaust server memory.
The vulnerable dependency (h2 < 0.4.5) must be updated to the fixed version
(0.4.5+).

Affected versions: RHTPA 2.2.0 (h2 0.4.4), RHTPA 2.2.1 (h2 0.4.4),
RHTPA 2.2.2 (same as 2.2.1, backend retag)
Not affected: RHTPA 2.2.3, RHTPA 2.2.4 (h2 0.4.5)
Source commit(s): backend v0.4.5 (2.2.0), backend v0.4.8 (2.2.1 / 2.2.2)

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99010 (no separate GHSA advisory linked)

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend (workspace) → reqwest → hyper → h2)
  - Depth: 3 levels. h2 is NOT declared in backend/Cargo.toml.
  - Direct dependency that pulls it in: `reqwest = { version = "0.12", features = ["json"] }`
  - Affected lock state: reqwest 0.12.5 → hyper 1.4.1 → h2 0.4.4
  - Profile: production (runtime dependency, shipped). Not dev-only, so
    priority follows CVE severity.
- First check the current h2 version on release/0.4.z HEAD
  (`grep -A2 'name = "h2"' Cargo.lock`). Tags v0.4.11/v0.4.12 already ship
  h2 0.4.5. If HEAD is already >= 0.4.5, record that in the task and close it
  as already fixed upstream. Only the downstream propagation task remains.

### Remediation approach (transitive dependency)

h2 is a **transitive** dependency, so use a two-tier approach:

**Preferred: bump the direct dependency**
- The direct dependency that pulls in h2 is `reqwest` (via `hyper`).
- Bump reqwest (and with it hyper) to a version whose transitive closure
  resolves h2 >= 0.4.5, e.g. `cargo update -p reqwest -p hyper -p h2`
  within the existing `reqwest = "0.12"` constraint. hyper 1.x accepts
  h2 0.4.x, so a semver-compatible update should resolve h2 0.4.5.
- Verify the bump does not introduce breaking API changes to reqwest/hyper.
- Check that hyper does not pin h2 to a version range that excludes 0.4.5. If
  it does, a hyper/reqwest release may need coordinating with intermediate
  maintainers.

**Fallback: pin the transitive dependency directly**
If bumping reqwest/hyper is not viable (breaking API changes, or no release
whose closure includes the fix):
- Cargo: `cargo add h2@0.4.5` to add h2 as a direct dependency, overriding
  the transitive resolution (or `cargo update -p h2 --precise 0.4.5`).
- Explain in the PR description why the direct dependency bump was not viable.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.5 in Cargo.lock on release/0.4.z
- [ ] Dependency chain backend → reqwest → hyper → h2 resolves to h2 >= 0.4.5
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8060 (parent tracking issue)
```

---

## Task 2 — Downstream propagation (2.2.x)

**Summary**: Propagate CVE-2026-99010 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)
**Labels**: ai-generated-jira, Security, CVE-2026-99010
**Issue type**: Task, project TC

```
## Repository

rhtpa-release.0.4.z (git.example.com/rhtpa/rhtpa-release.0.4.z)

## Target Branch

main

## Description

Update the backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99010 fix from <Task 1 key>.

The upstream backport (<Task 1 key>) bumps h2 to 0.4.5 on release/0.4.z.
h2 is pulled in transitively (backend → reqwest → hyper → h2). Once that PR
merges, or once it is confirmed the branch already ships h2 0.4.5 (backend
tags v0.4.11 and later do), update the source pinning in this Konflux
release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains the
  backend tag, e.g. v0.4.12)
- **Dependency type**: transitive (chain: backend (workspace) → reqwest → hyper → h2), carried forward from upstream task
- Update the backend reference to the merged commit or new release tag (at
  least a tag whose Cargo.lock has h2 >= 0.4.5)
- If the upstream fix pinned h2 directly (fallback approach), verify the pin
  appears in the downstream build's Cargo.lock after the source reference
  update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix (h2 >= 0.4.5)
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <Task 1 key> (upstream backport must merge first)
- Depends on: TC-8060 (parent tracking issue)
```

---

## Proposed Jira operations (order; none executed)

1. Step 0.8: assign TC-8060 to the current user and transition New → Assigned.
2. Step 3: set Affects Versions on TC-8060 to RHTPA 2.2.0, 2.2.1, 2.2.2, plus a correction comment with the footnote.
3. Step 7.5: find or create release Epic "RHTPA <2.2.z version> Release Tasks" and release Task "RHTPA <2.2.z version> CVE triage" (version chosen by engineer, with individual confirmation for each).
4. Create Task 1, then post the description digest comment (`[sdlc-workflow] Description digest: sha256-...`).
5. Create Task 2, then post its description digest comment.
6. Links:
   - TC-8060 → Task 1 (Depend); TC-8060 → Task 2 (Depend)
   - Task 1 → Task 2 (Blocks)
   - Task 1 → release Task (Blocks); Task 2 → release Task (Blocks)
   - release Task → TC-8060 (Related)
7. Status: TC-8060 is already in Assigned (an indeterminate-category status), so no further transition.
8. Comment on TC-8060: "Remediation tasks created: <Task 1> (upstream backport), <Task 2> (downstream propagation, blocked by <Task 1>)" with footnote.
9. Add label `ai-cve-triaged` to TC-8060.
10. Post the post-triage summary comment: impact table, Affects Versions correction, outcome (Case B), task links, release Jira refs, no dedup, @mention of reporter psirt-analyst (account ID 557058:psirt-analyst-mock-id), and Comment Footnote.

## Caveats for the engineer

- **Fixture conflict**: the security matrix's "h2 versions by tag" table (0.4.8 / 0.4.9 for 2.2.x) contradicts the issue's Cargo.lock evidence (0.4.4 / 0.4.5). This analysis follows the Cargo.lock evidence. If the matrix table is correct, every 2.2.x version is unaffected, and the outcome becomes Case C (close as Not a Bug, VEX customfield_12345 = "Component not Present", or rather "Vulnerable Code not Present" because the fixed version ships). Verify with `git show v0.4.5:Cargo.lock` before confirming.
- The latest 2.2.x releases (2.2.3, 2.2.4) already ship h2 0.4.5. Remediation may only need confirmation that the next build is cut from a fixed tag, plus customer guidance to upgrade to 2.2.3 or later.
- External CVE data (MITRE/OSV) was not consulted, so fix-threshold confidence is reduced.
- The matrices are 148 days stale. Newer 2.2.x releases may exist.
- Due date 2026-08-15 has passed.
