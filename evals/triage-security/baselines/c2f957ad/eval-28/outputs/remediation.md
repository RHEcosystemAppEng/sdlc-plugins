# TC-8060 — Step 8: Remediation

## Decision

| Check | Result |
|-------|--------|
| Any supported versions affected? | YES: RHTPA 2.2.0, 2.2.1, 2.2.2 (h2 0.4.4 < 0.4.5) |
| Issue scoped? | YES: `[rhtpa-2.2]` maps to stream 2.2.x |
| Other streams affected? | NO: 2.1.x ships h2 0.4.5. **Case A does not apply** (no cross-stream comment, no preemptive tasks). |
| Dedup (7.5.3) | Not applicable. The Upstream Affected Component field is not configured, so no existing task is assumed. |
| Outcome | **Case B: create remediation tasks for stream 2.2.x** |
| Ecosystem | Cargo, a source dependency: **2 tasks** (upstream backport + downstream propagation) |
| Dependency type | **Transitive**, 3 levels: `backend (workspace) → reqwest → hyper → h2` |
| Dependency scope | Production runtime: no `dev-dependency` label and no priority override |
| Variant | Upstream backport. `release/0.4.z` HEAD has not been confirmed fixed (Step 2.5 UNCONFIRMED). If HEAD is confirmed at h2 >= 0.4.5, switch Task 1 to the dependency-bump template. Task 2 stays the same. |
| Coordination Guidance | Omitted. The Source Repositories table has no Deployment Context column. |

---

## Task 1 — Upstream backport (rhtpa-backend, release/0.4.z)

**Summary:** Remediate CVE-2026-99010: bump h2 to 0.4.5 (2.2.x)
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-99010`
**Security level:** copied from TC-8060 (omitted only if the parent has none)
**Issue type:** Task, project TC

```
## Repository

backend (rhtpa-backend — https://github.com/rhtpa/rhtpa-backend)

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99010: h2 memory exhaustion via CONTINUATION frames
(denial of service; CVSS 7.5 High). h2 does not limit the number of
CONTINUATION frames received for a single HEADERS frame, allowing an
attacker to exhaust server memory.
The vulnerable dependency (h2 < 0.4.5) must be updated to the fixed
version (0.4.5+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 (2.2.2 is a retag of 2.2.1)
Source commit(s): v0.4.5 (2.2.0), v0.4.8 (2.2.1 / 2.2.2)
Not affected: RHTPA 2.2.3 (v0.4.11), RHTPA 2.2.4 (v0.4.12) — already resolve h2 0.4.5

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99010 (CVE record; no GHSA link on the issue)

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend (workspace) → reqwest → hyper → h2)
  - Resolved in affected lock files: reqwest 0.12.5 → hyper 1.4.1 → h2 0.4.4
  - backend/Cargo.toml declares only `reqwest = { version = "0.12", features = ["json"] }`;
    h2 is NOT a direct dependency
  - Profile: production (reqwest is a runtime dependency) — normal CVE priority applies
- Note: tags v0.4.11 / v0.4.12 on this branch already resolve h2 0.4.5. First
  verify `release/0.4.z` HEAD `Cargo.lock`; if h2 >= 0.4.5 is already present,
  this task reduces to confirming the fix and handing off to the downstream task.

### Remediation approach (transitive dependency)

h2 is pulled in through intermediate packages (reqwest → hyper → h2), so use a
two-tier approach:

**Preferred: bump the direct dependency**
- The direct dependency that pulls in h2 is **reqwest** (via hyper).
- Bump reqwest (currently 0.12.5), and hyper with it (currently 1.4.1), to versions
  whose transitive closure resolves h2 >= 0.4.5, e.g. `cargo update -p reqwest`
  and `cargo update -p hyper`. Stay within reqwest 0.12.x / hyper 1.x to avoid API breaks.
- Confirm in Cargo.lock that the resolved h2 is >= 0.4.5.
- Verify the bump does not introduce breaking API changes to reqwest usage in backend.

**Fallback: pin the transitive dependency directly**
If bumping reqwest/hyper is not viable (breaking API changes, no compatible
release with the fix):
- Cargo: `cargo add h2@0.4.5` to add h2 as a direct dependency, overriding the
  transitive resolution (alternatively `cargo update -p h2 --precise 0.4.5`,
  since 0.4.5 is semver-compatible with hyper's `h2 = "0.4"` requirement)
- Document in the PR description why the direct dependency bump was not viable.
- If reqwest or hyper pins h2 to an exact vulnerable version, coordinate with
  those intermediate crate maintainers (hyperium/hyper, seanmonstar/reqwest)
  for a release that permits h2 >= 0.4.5.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.5 in Cargo.lock on release/0.4.z
- [ ] Dependency chain backend → reqwest → hyper → h2 resolves to the fixed h2
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8060 (parent tracking issue)
```

---

## Task 2 — Downstream propagation (rhtpa-release.0.4.z, main)

**Summary:** Propagate CVE-2026-99010 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-99010`
**Security level:** copied from TC-8060
**Issue type:** Task, project TC

```
## Repository

rhtpa-release.0.4.z (git.example.com/rhtpa/rhtpa-release.0.4.z)

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99010 fix from <TASK-1-KEY>.

The upstream backport (<TASK-1-KEY>) bumps h2 to 0.4.5 on release/0.4.z
(via the reqwest → hyper → h2 chain, or by pinning h2 directly). Once that PR
merges, update the source pinning in this Konflux release repo so the next
build ships the fix.

## Implementation Notes

- Source pinning method: backend is pinned via `artifacts.lock.yaml` (download URL
  contains the tag, e.g. `v0.4.12`)
- **Dependency type**: transitive (chain: backend (workspace) → reqwest → hyper → h2)
  — carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned h2 directly (fallback approach), verify the pin is
  reflected in the downstream build's Cargo.lock (h2 >= 0.4.5) after the source
  reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <TASK-1-KEY> (upstream backport must merge first)
- Depends on: TC-8060 (parent tracking issue)
```

---

## Proposed Jira Operations (not executed; each needs engineer confirmation)

1. Create Task 1, then post its description digest comment (`[sdlc-workflow] Description digest: sha256-...`) before any links or other comments.
2. Create Task 2, then post its description digest comment.
3. Links:
   - TC-8060 → Task 1: **Depend** (inward TC-8060, outward Task 1)
   - TC-8060 → Task 2: **Depend**
   - Task 1 → Task 2: **Blocks** (Task 2 is blocked by Task 1)
   - Task 1 and Task 2 → release Task "RHTPA 2.2.<next> CVE triage" (from Step 7.5): **Blocks**
   - Release Task → TC-8060: **Related**
4. Affects Versions: [RHTPA 2.2.0] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2], with a correction comment and footnote.
5. TC-8060 is already moved to Assigned and assigned in Step 0.8. Transition to In Progress if the workflow has it; skip if the issue is already in an indeterminate-category status.
6. Comment on TC-8060: "Remediation tasks created: <TASK-1-KEY> (upstream backport), <TASK-2-KEY> (downstream propagation, blocked by <TASK-1-KEY>)", with the footnote.
7. Add label `ai-cve-triaged` to TC-8060.
8. Post-triage summary comment on TC-8060 containing the version impact table, the Affects Versions correction, outcome (Case B, remediation created), task links, release Epic/Task references, dedup results (none), an @mention of reporter `557058:psirt-analyst-mock-id`, and the Comment Footnote (`triage-security`).

## Pre-creation Checklist

- [x] Task count per stream: 2 for Cargo (source dependency)
- [x] Cross-stream coverage: 2.1.x is not affected, so no preemptive tasks are needed
- [x] Link types: Depend (own CVE), Blocks (upstream → downstream and → release Task), Related (release Task ↔ CVE)
- [x] Preemptive labels: N/A
- [x] Coordination guidance: omitted (no Deployment Context column)
- [x] Release Jira linking: planned for both tasks
- [x] Dedup consistency: no dedup'd streams
- [x] Transitive dependency: full chain and two-tier approach documented in both tasks
