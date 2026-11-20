# TC-8060 — Step 8 Remediation

## Decision

- Supported versions affected in scope (2.2.x): **2.2.0, 2.2.1, 2.2.2** (h2 0.4.4)
- Issue scoped: yes, `[rhtpa-2.2]`. Other streams affected: no (2.1.x ships h2 0.4.5), so **Case A does not apply**.
- **Outcome: Case B. Create remediation tasks for stream 2.2.x.**
- Ecosystem: Cargo, a source dependency, so **2 tasks**: upstream backport and downstream propagation (blocked).
- Dependency type: **transitive**. Chain is `backend (workspace) → reqwest → hyper → h2` (3 levels deep), production profile.
- The approach is **two-tier**: bump the direct dependency (reqwest) first, and fall back to pinning h2 directly.
- Coordination guidance is left out because the Source Repositories table has no Deployment Context column.
- Labels: `ai-generated-jira`, `Security`, `CVE-2026-99010`. Not preemptive, and no `dev-dependency` label (production dep).
- Caveat: this outcome depends on the TC-8060 Cargo.lock evidence. The matrix-mock h2 table conflicts with it (see version-impact.md). It also assumes `release/0.4.z` HEAD is unverified. Released 2.2.3 and 2.2.4 already ship h2 0.4.5.

---

## Task 1 — Upstream backport

**Summary:** Remediate CVE-2026-99010: bump h2 to 0.4.5 (2.2.x)
**Labels:** ai-generated-jira, Security, CVE-2026-99010
**Issue type:** Task (project TC)

```
## Repository

backend (rhtpa-backend — https://github.com/rhtpa/rhtpa-backend)

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99010: h2 memory exhaustion via CONTINUATION frames (DoS,
CVSS 7.5). The h2 crate does not limit the number of CONTINUATION frames per
HEADERS frame, so a remote attacker can exhaust server memory.
The vulnerable dependency (h2 < 0.4.5) must be updated to the fixed version
(0.4.5+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5 (2.2.0), v0.4.8 (2.2.1, 2.2.2)

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99010 (no GHSA advisory linked)

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend (workspace) → reqwest → hyper → h2)
  - 3 levels deep; production profile (reqwest is a runtime `[dependencies]` entry)
  - backend/Cargo.toml declares only `reqwest = { version = "0.12", features = ["json"] }`;
    h2 is NOT a direct dependency
  - Affected Cargo.lock resolution: reqwest 0.12.5 → hyper 1.4.1 → h2 0.4.4
  - Present since 2.1.0 (initial project setup)
- First verify release/0.4.z HEAD: tags v0.4.11 / v0.4.12 (RHTPA 2.2.3 / 2.2.4) already
  resolve h2 0.4.5. If HEAD already has h2 >= 0.4.5, record that and close this task as
  already satisfied — no PR needed.

### Remediation approach (transitive dependency)

h2 is a **transitive** dependency (pulled in through reqwest → hyper), so use a
two-tier approach:

**Preferred: bump the direct dependency**
- The direct dependency that pulls in h2 is **reqwest** (via hyper; see chain above)
- Bump reqwest (and with it hyper) to a version whose transitive closure
  includes h2 >= 0.4.5 — e.g. `cargo update -p reqwest` (and `cargo update -p hyper`
  / `cargo update -p h2` within existing semver constraints: reqwest 0.12 → hyper 1.x →
  h2 0.4.x permits 0.4.5)
- Verify the bump does not introduce breaking API changes to reqwest
- Confirm in Cargo.lock that `name = "h2"` resolves to version >= 0.4.5

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable (breaking API changes, or
reqwest/hyper constrain h2 below 0.4.5 with no release available with the fix):
- Cargo: `cargo add h2@0.4.5` to add h2 as a direct dependency of backend,
  overriding the transitive resolution
- Coordinate with the hyper/reqwest maintainers if an intermediate crate pins
  a vulnerable h2 version
- Document why the direct dep bump was not viable in the PR description

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.5 in Cargo.lock on release/0.4.z
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8060 (parent tracking issue)
```

---

## Task 2 — Downstream propagation (blocked by Task 1)

**Summary:** Propagate CVE-2026-99010 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)
**Labels:** ai-generated-jira, Security, CVE-2026-99010
**Issue type:** Task (project TC)

```
## Repository

rhtpa-release.0.4.z (git.example.com/rhtpa/rhtpa-release.0.4.z)

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99010 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps h2 to 0.4.5 on
release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains the backend tag,
  e.g., `v0.4.12`)
- **Dependency type**: transitive (chain: backend (workspace) → reqwest → hyper → h2) —
  carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Note: the current latest pin (v0.4.12, RHTPA 2.2.4) already resolves h2 0.4.5; confirm
  the next 2.2.z build references a tag at or after the fix
- If the upstream fix pinned h2 directly (fallback approach), verify the pinning is
  reflected in the downstream build's Cargo.lock after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8060 (parent tracking issue)
```

---

## Proposed Jira operations (simulated, each needs engineer confirmation)

1. Create Task 1. Post the description digest comment (`[sdlc-workflow] Description digest: sha256-md:<hex>`) before any links.
2. Create Task 2. Post its description digest comment.
3. Link TC-8060 to Task 1 as **Depend**, and TC-8060 to Task 2 as **Depend**.
4. Link Task 1 to Task 2 as **Blocks** (upstream blocks downstream).
5. If Step 7.5 finds or creates a release Task (`RHTPA <next 2.2.z> CVE triage`): link Task 1 and Task 2 to it as **Blocks**, and link the release Task to TC-8060 as **Related**.
6. Correct Affects Versions on TC-8060 from RHTPA 2.2.0 to RHTPA 2.2.0, 2.2.1, 2.2.2.
7. Assign TC-8060 to the triager. It is already in Assigned after Step 0.8, so the In Progress transition is skipped.
8. Comment on TC-8060: "Remediation tasks created: <upstream-task-key> (upstream backport), <downstream-task-key> (downstream propagation, blocked by <upstream-task-key>)", with the Comment Footnote.
9. Add the `ai-cve-triaged` label. Post the summary comment with the impact table, the AV correction, the outcome, the task links, the release Jira references, an @mention of the reporter psirt-analyst (`557058:psirt-analyst-mock-id`), and the Comment Footnote.

## Pre-creation checklist

- [x] Task count per stream: 2 (Cargo is a source dependency)
- [x] Cross-stream coverage: no other stream affected
- [x] Link types: Depend (to own CVE), Blocks (upstream → downstream)
- [x] Preemptive labels: not applicable
- [x] Coordination guidance: left out (no Deployment Context column)
- [ ] Release Jira linking: pending Step 7.5 (not executed)
- [x] Dedup consistency: no dedup (Step 7.5.3 not run; Upstream Affected Component field not configured)
