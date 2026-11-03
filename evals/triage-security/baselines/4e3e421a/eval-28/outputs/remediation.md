# TC-8060 — Step 8 Remediation

CVE-2026-99010: h2 < 0.4.5 (fixed 0.4.5). Scope: 2.2.x. Ecosystem: Cargo (source dependency). Dependency: **transitive**.

## Pre-remediation steps (Steps 3–7.5) — summary

| Step | Result |
|------|--------|
| 3 Affects Versions | Proposed change from `RHTPA 2.2.0` to `RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2` (needs confirmation) |
| 4 Duplicates/siblings | JQL `project = TC AND issuetype = 10024 AND labels = CVE-2026-99010` not run (no Jira). No sibling data in the fixtures, so no known duplicates. 4.3 overlap skipped (Upstream Affected Component field not configured) |
| 5 Lifecycle | Product pages not queried. 2.2.x is the latest configured stream, so it is assumed supported. Verify in a live run |
| 6 Already fixed | No resolved siblings known. Note: released 2.2.3/2.2.4 already ship h2 0.4.5 (see Outcome note below) |
| 7 Concurrent triage | Skipped (Upstream Affected Component field not configured) |
| 7.5 Release Jira | Find or create Epic "RHTPA <next-2.2.z> Release Tasks" and Task "RHTPA <next-2.2.z> CVE triage". The next version (probably 2.2.5) must come from the Jira unreleased-versions lookup and needs individual confirmation. 7.5.3 dedup skipped (no Upstream Affected Component field) |

## Decision

- Supported versions affected in scope: **yes** (2.2.0, 2.2.1, 2.2.2), so this is **Case B**.
- Other streams affected: **no** (2.1.x ships h2 0.4.5), so Case A does not apply and no preemptive tasks are needed.
- Ecosystem: Cargo, a source dependency, so **2 tasks** for stream 2.2.x.
- Step 2.5 suggests the fix is already on `release/0.4.z` (inferred from tags `v0.4.11`/`v0.4.12`), so the **dependency bump** variant plus downstream propagation is used.
- Dependency is transitive (`backend → reqwest → hyper → h2`), so each task documents the full chain and the **two-tier approach**: bump the direct dependency first, and fall back to pinning h2 directly.
- Production runtime dependency: no `dev-dependency` label and no priority override.
- No Deployment Context column in Source Repositories, so the Coordination Guidance subsection is left out.

**Outcome note for the engineer:** the latest 2.2.x release (2.2.4, `v0.4.12`) already ships h2 0.4.5. The two tasks below make sure the next 2.2.z build is confirmed fixed and keep the stream from regressing. If the engineer decides the 2.2.3/2.2.4 releases already close the gap, the downstream task reduces to verification. Also, the fixtures disagree on h2 versions per tag (see version-impact.md). Settle this against the real `Cargo.lock` before creating anything.

---

## Task 1 — Dependency bump (upstream source repo)

**Summary:** Remediate CVE-2026-99010: update h2 to 0.4.5 (2.2.x)
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-99010`
**Link:** TC-8060 → Task 1 (`Depend`); Task 1 → release Task (`Blocks`)

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99010: bump h2 to 0.4.5 via dependency update.
The vulnerable dependency (h2 < 0.4.5) allows a remote attacker to cause
memory exhaustion by sending an unbounded sequence of HTTP/2 CONTINUATION
frames (DoS, CVSS 7.5). It is already fixed upstream. A package manager update
of the direct dependency chain is sufficient.

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 (2.2.2 is a retag of 2.2.1)
Source commit(s): v0.4.5 (2.2.0), v0.4.8 (2.2.1 / 2.2.2)
Not affected: 2.2.3 (v0.4.11) and 2.2.4 (v0.4.12) already resolve h2 0.4.5

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99010

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend (workspace) → reqwest → hyper → h2)
  - 3 levels deep. h2 is NOT declared in backend/Cargo.toml
  - Manifest: `reqwest = { version = "0.12", features = ["json"] }`
  - Affected lock resolution: reqwest 0.12.5 → hyper 1.4.1 → h2 0.4.4
  - Profile: production (reqwest is a runtime `[dependencies]` entry)
  - Present since 2.1.0 (reqwest has always depended on hyper/h2)
- First confirm the current state: `git show release/0.4.z:Cargo.lock | grep -A2 'name = "h2"'`.
  Tags v0.4.11/v0.4.12 already resolve h2 0.4.5. If HEAD is >= 0.4.5, record
  that and close this task as already satisfied.

### Remediation approach (transitive dependency)

h2 is a transitive dependency, so use a two-tier approach:

**Preferred: bump the direct dependency**
- The direct dependency that pulls in h2 is `reqwest` (through `hyper`)
- Run `cargo update -p reqwest -p hyper -p h2` (or `cargo update -p h2`, which
  works because h2 0.4.5 is semver-compatible with hyper 1.x's `h2 = "0.4"`
  requirement) so the lock file resolves h2 >= 0.4.5
- If the current reqwest 0.12.x / hyper 1.x line cannot resolve h2 >= 0.4.5,
  bump reqwest to a release whose dependency tree includes h2 >= 0.4.5
- Verify the bump does not introduce breaking API changes to reqwest/hyper

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable (breaking API changes, no
reqwest/hyper release available with the fix, or an intermediate crate pins
h2 < 0.4.5):
- Cargo: `cargo add h2@0.4.5` in the backend workspace to add h2 as a direct
  dependency, which overrides the transitive resolution
- If an intermediate package (reqwest or hyper) pins a vulnerable h2,
  coordinate with that package's maintainers and track the upstream bump
- Document in the PR description why the direct dependency bump was not viable

- Verify the lock file shows h2 >= 0.4.5 after the update (`cargo tree -i h2`)
- This is a production dependency, so it keeps normal CVE priority (no `dev-dependency` label)

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.5 in Cargo.lock on release/0.4.z
- [ ] Lock file updated via package manager (not manual edit)
- [ ] `cargo tree -i h2` shows the chain backend → reqwest → hyper → h2 resolving to >= 0.4.5 (or h2 pinned directly if the fallback was used)
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
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-99010`
**Links:** TC-8060 → Task 2 (`Depend`); Task 1 → Task 2 (`Blocks`); Task 2 → release Task (`Blocks`)

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99010 fix from <Task 1 key>.

The dependency bump (<Task 1 key>) makes sure h2 >= 0.4.5 on release/0.4.z
(transitive chain backend → reqwest → hyper → h2). Once that is merged or
confirmed, update the source pinning in this Konflux release repo so the
next 2.2.z build ships the fix.

## Implementation Notes

- Source pinning method: backend via `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: transitive (chain: backend (workspace) → reqwest → hyper → h2) — carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
  (must be >= v0.4.11, the first tag known to resolve h2 0.4.5)
- If the upstream fix pinned h2 directly (fallback approach), verify the pin
  shows up in the downstream build's Cargo.lock after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix (h2 >= 0.4.5)
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <Task 1 key> (upstream dependency bump must merge first)
- Depends on: TC-8060 (parent tracking issue)
```

---

## Jira operations that would follow (each needs confirmation; none executed)

1. Create Task 1, then post the description digest comment (`[sdlc-workflow] Description digest: sha256-md:<hex>`) before any links.
2. Create Task 2, then post its description digest comment.
3. Links: TC-8060 → Task 1 (Depend), TC-8060 → Task 2 (Depend), Task 1 → Task 2 (Blocks), Task 1 → release Task (Blocks), Task 2 → release Task (Blocks), release Task → TC-8060 (Related).
4. Transition TC-8060 to In Progress. It should already be assigned to the triager from Step 0.8.
5. Comment on TC-8060: "Remediation tasks created: <Task 1 key> (dependency bump), <Task 2 key> (downstream propagation, blocked by <Task 1 key>)", with the comment footnote.
6. Add label `ai-cve-triaged` to TC-8060.
7. Post the post-triage summary comment: version impact table, Affects Versions correction (2.2.0 to 2.2.0/2.2.1/2.2.2), outcome (Case B, remediation created), task links, release Epic/Task keys, no dedup, the ADF @mention of reporter `557058:psirt-analyst-mock-id`, and the triage-security comment footnote.

## Pre-creation checklist

- [x] Task count per stream: 2 (Cargo is a source dependency)
- [x] Cross-stream coverage: no other stream affected (2.1.x h2 0.4.5)
- [x] Link types: Depend (own CVE), Blocks (upstream to downstream, and to the release Task), Related (CVE to the release Task)
- [x] Preemptive labels: not applicable
- [x] Coordination guidance: left out (no Deployment Context column)
- [x] Release Jira linking: planned, pending 7.5 version confirmation
- [x] Dedup consistency: no dedup (7.5.3 skipped)
