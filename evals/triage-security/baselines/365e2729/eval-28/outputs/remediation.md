# TC-8060 — Step 8: Remediation

## Decision

- Issue scoped to 2.2.x; affected 2.2.x versions: 2.2.0, 2.2.1, 2.2.2 -> **Case B** (create remediation tasks).
- Other streams affected? 2.1.x not affected -> **Case A not triggered** (no cross-stream comment, no preemptive tasks).
- Ecosystem Cargo = source dependency -> **2 tasks** for 2.2.x.
- Step 2.5: fix already on `release/0.4.z` (shipped in 2.2.3/2.2.4) -> **dependency bump variant** + downstream propagation.
- Dependency type: **transitive** (backend → reqwest → hyper → h2) -> **two-tier remediation** (bump direct dep first, pin transitive dep as fallback).
- Production dependency -> no `dev-dependency` label, no priority override.
- Deployment Context column absent -> Coordination Guidance subsection omitted (backward-compat rule).

**Triage note for engineer:** the newest 2.2.x releases (2.2.3, 2.2.4) already ship h2 0.4.5. If
no further 2.2.0–2.2.2 respins are planned, the engineer may decide that the remediation is "upgrade
to 2.2.3+" and that Task 1 reduces to verifying `release/0.4.z` HEAD, rather than new code change.
The tasks below are the skill's standard output and are presented for confirmation only (no Jira
writes performed).

---

## Task 1 — Dependency bump (upstream source repo)

**Summary:** Remediate CVE-2026-99010: update h2 to 0.4.5 (2.2.x)
**Labels:** ai-generated-jira, Security, CVE-2026-99010
**Security level:** copied from TC-8060 (`security` field; omit only if null)
**Priority / fixVersion:** prompted at creation (Jira Field Defaults: prompt for both)

```
## Repository

rhtpa-backend (backend)

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99010: bump h2 to 0.4.5 via dependency update.
h2 before 0.4.5 does not limit CONTINUATION frames for a single HEADERS frame, allowing
a remote attacker to cause memory exhaustion (DoS, CVSS 7.5 High).
The vulnerable dependency (h2 < 0.4.5) is already fixed upstream — a package manager
update is sufficient.

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): backend v0.4.5 (2.2.0), v0.4.8 (2.2.1 / 2.2.2)
Not affected: RHTPA 2.2.3 (v0.4.11), RHTPA 2.2.4 (v0.4.12) — ship h2 0.4.5

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99010

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend (workspace) → reqwest → hyper → h2, 3 levels deep)
  - backend/Cargo.toml declares only `reqwest = { version = "0.12", features = ["json"] }`;
    h2 is NOT a direct dependency.
  - Affected Cargo.lock: reqwest 0.12.5 -> hyper 1.4.1 -> h2 0.4.4
  - Profile: production (reqwest is a runtime dependency) — not dev/build-only
- First appeared: 2.1.0 (reqwest has always depended on hyper/h2)

### Remediation approach (transitive dependency)

h2 is pulled in through intermediate packages, so use a two-tier approach:

**Preferred: bump the direct dependency**
- The direct dependency that pulls in h2 is `reqwest` (via `hyper`).
- Bump reqwest (and hyper) to versions whose transitive closure includes h2 >= 0.4.5:
  `cargo update -p reqwest` / `cargo update -p hyper`, then `cargo update -p h2`
  (h2 0.4.5 is semver-compatible with hyper 1.4.x's h2 0.4 requirement).
- Verify the bump does not introduce breaking API changes in reqwest/hyper.
- If the update still resolves h2 within the affected range, continue to the fallback.

**Fallback: pin the transitive dependency directly**
If bumping reqwest/hyper is not viable (breaking API changes, no release available with the fix,
or an intermediate crate pins h2 < 0.4.5):
- `cargo add h2@0.4.5` in backend to add h2 as a direct dependency, overriding the transitive resolution
- Document in the PR why the direct dependency bump was not viable
- If reqwest or hyper pins the vulnerable h2 version, coordinate with those crates' maintainers

- Verify Cargo.lock reflects h2 >= 0.4.5 after the update (note: release/0.4.z appears to already
  ship 0.4.5 per tags v0.4.11/v0.4.12 — confirm at HEAD; if so, record the fixing commit and skip the code change)

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.5 in Cargo.lock
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8060 (parent tracking issue)
```

---

## Task 2 — Downstream propagation (Konflux release repo)

**Summary:** Propagate CVE-2026-99010 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)
**Labels:** ai-generated-jira, Security, CVE-2026-99010
**Security level:** copied from TC-8060

```
## Repository

rhtpa-release.0.4.z (git.example.com/rhtpa/rhtpa-release.0.4.z)

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-99010 fix
from <Task 1 key>.

The dependency bump (<Task 1 key>) brings h2 to 0.4.5 on release/0.4.z (transitively via
reqwest → hyper → h2). Once that PR merges, update the source pinning in this Konflux release
repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: transitive (backend → reqwest → hyper → h2) — carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
  (tags v0.4.11+ already ship h2 0.4.5; any build pinned at or after that tag is fixed)
- If the upstream fix pinned h2 directly (fallback approach), verify the pin is reflected in the
  downstream build's Cargo.lock after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <Task 1 key> (dependency bump must merge first)
- Depends on: TC-8060 (parent tracking issue)
```

---

## Proposed Jira operations (not executed — eval)

1. Create Task 1; post description digest comment (`[sdlc-workflow] Description digest: sha256-...`) before any link.
2. Create Task 2; post description digest comment.
3. Links: TC-8060 -> Task 1 (Depend); TC-8060 -> Task 2 (Depend); Task 1 -> Task 2 (Blocks).
4. If Step 7.5 release Jira exists (RHTPA 2.2.x release Task): Task 1/Task 2 Blocks release Task; release Task Related TC-8060.
5. Update Affects Versions: RHTPA 2.2.0 -> RHTPA 2.2.0, 2.2.1, 2.2.2.
6. Transition TC-8060 to In Progress (skip if already Assigned/indeterminate or later).
7. Add `ai-cve-triaged` label.
8. Post summary comment: version impact table, Affects Versions correction, outcome (Case B), task links,
   release Jira refs, dependency chain, @mention of reporter psirt-analyst (557058:psirt-analyst-mock-id),
   and the Comment Footnote.

### Pre-creation checklist

- [x] Task count per stream: 2 (Cargo = source dependency)
- [x] Cross-stream coverage: 2.1.x not affected — no preemptive tasks needed
- [x] Link types: Depend (own CVE), Blocks (bump -> downstream)
- [x] Preemptive labels: N/A
- [x] Coordination guidance: omitted (no Deployment Context column)
- [ ] Release Jira linking: pending Step 7.5 lookup
- [x] Dedup consistency: Step 7.5.3 not applicable (Upstream Affected Component field not configured)
