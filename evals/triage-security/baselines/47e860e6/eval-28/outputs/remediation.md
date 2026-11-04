# Step 8 – Remediation: TC-8060 (CVE-2026-99010, h2 < 0.4.5)

## Decision

- Supported versions affected in scope (2.2.x): **2.2.0, 2.2.1, 2.2.2**, so this is **Case B** (create remediation tasks).
- The issue is scoped to 2.2.x. The other stream, 2.1.x, ships h2 0.4.5 and is not affected, so **Case A does not apply**.
- Ecosystem: Cargo is a source dependency, so there are **2 tasks** for stream 2.2.x: an upstream task and a downstream propagation task.
- Dependency type: **transitive**. The full chain is `backend (workspace) → reqwest → hyper → h2`, 3 levels deep, production profile.
- Step 7.5.3 dedup: not run in eval (no Upstream Affected Component field), so tasks are created.
- Caveats for the engineer at the confirmation gate:
  1. The fixture contains two conflicting h2 data sets. See `version-impact.md`.
  2. 2.2.3+ already ships h2 0.4.5. If Step 2.5 confirms `release/0.4.z` HEAD resolves h2 >= 0.4.5, Task 1 reduces to verifying and documenting the fix. Task 2 is only needed if a respin of a 2.2.0–2.2.2 based build is required.

Nothing below was executed. All of it is a proposal that needs engineer confirmation.

---

## Task 1 – Upstream remediation (rhtpa-backend, release/0.4.z)

**Summary:** Remediate CVE-2026-99010: bump h2 to 0.4.5 (2.2.x)
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-99010`
**Priority:** inherit from CVE (High, CVSS 7.5). Production dependency, so no override.

```
## Repository

backend (rhtpa-backend)

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99010: h2 memory exhaustion via unbounded CONTINUATION frames (DoS).
The vulnerable dependency (h2 < 0.4.5) must be updated to the fixed version (0.4.5+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 (2.2.2 is a backend retag of 2.2.1)
Not affected: RHTPA 2.2.3, RHTPA 2.2.4 (ship h2 0.4.5)
Source commit(s): v0.4.5 (2.2.0), v0.4.8 (2.2.1 / 2.2.2)

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99010

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend (workspace) → reqwest → hyper → h2)
  - h2 is NOT declared in backend/Cargo.toml. It is resolved through
    reqwest 0.12.5 → hyper 1.4.1 → h2 0.4.4 in the affected Cargo.lock.
  - Direct dependency to bump: `reqwest` (declared as
    `reqwest = { version = "0.12", features = ["json"] }`)
  - Intermediate package: `hyper` (1.4.1 in affected builds)
- Profile: production (reqwest is a runtime dependency). Not dev/build-only,
  so normal CVE priority applies.

### Remediation approach (transitive dependency)

h2 is a transitive dependency, so use a two-tier approach:

**Preferred: bump the direct dependency**
- Bump reqwest (and with it hyper) to a version whose transitive closure
  resolves h2 >= 0.4.5, e.g. `cargo update -p reqwest -p hyper -p h2`.
  The reqwest 0.12 and hyper 1.x semver ranges should allow h2 0.4.5 without
  a manifest change.
- Verify that Cargo.lock now shows `name = "h2"` / `version = "0.4.5"` (or later)
- Verify the bump does not introduce breaking API changes in reqwest/hyper

**Fallback: pin the transitive dependency directly**
If bumping reqwest/hyper is not viable (breaking API changes, or no release
with a compatible h2 range):
- `cargo update -p h2 --precise 0.4.5`, or `cargo add h2@0.4.5` to add h2 as
  a direct dependency and override the transitive resolution
- If hyper (or reqwest) pins an h2 version below 0.4.5, coordinate with the
  intermediate package maintainers (hyperium/hyper, seanmonstar/reqwest) for
  a release that allows h2 >= 0.4.5
- Document in the PR description why the direct dependency bump was not viable

Note: release tags v0.4.11 and v0.4.12 on this branch already ship h2 0.4.5.
First check `git show release/0.4.z:Cargo.lock | grep -A2 'name = "h2"'`. If HEAD
is already >= 0.4.5, record the fixing commit or tag and close this task as
already remediated upstream.

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

## Task 2 – Downstream propagation (rhtpa-release.0.4.z)

**Summary:** Propagate CVE-2026-99010 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-99010`

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99010 fix from <Task 1 key>.

The upstream task (<Task 1 key>) bumps h2 to 0.4.5 on release/0.4.z, either
through reqwest → hyper or by pinning h2 directly. Once that PR merges, update
the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (the download URL contains the
  backend tag, e.g. v0.4.12)
- **Dependency type**: transitive (backend → reqwest → hyper → h2), carried
  forward from the upstream task
- Update the backend reference to the merged commit or new release tag.
  Tags v0.4.11 and later already contain h2 0.4.5.
- If the upstream fix pinned h2 directly (fallback approach), verify the
  pin is reflected in the downstream build's Cargo.lock after the source
  reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix (h2 >= 0.4.5)
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <Task 1 key> (upstream fix must merge first)
- Depends on: TC-8060 (parent tracking issue)
```

---

## Jira operations (proposed order, interactive mode, not executed)

1. Create Task 1, then post its description digest comment (`[sdlc-workflow] Description digest: sha256-...`).
2. Create Task 2, then post its description digest comment.
3. Links:
   - TC-8060 → Task 1 (Depend)
   - TC-8060 → Task 2 (Depend)
   - Task 1 → Task 2 (Blocks)
   - If Step 7.5 finds or creates a release Task, for example "RHTPA 2.2.x CVE triage":
     - Task 1 → release Task (Blocks)
     - Task 2 → release Task (Blocks)
     - release Task → TC-8060 (Related)
4. Update Affects Versions on TC-8060 to RHTPA 2.2.0, 2.2.1, 2.2.2 (from Step 3).
5. Transition TC-8060 to In Progress (or equivalent), using the target taken from live transitions.
6. Comment on TC-8060: "Remediation tasks created: <Task 1> (upstream remediation), <Task 2> (downstream propagation, blocked by <Task 1>)". Include the comment footnote.
7. Add the `ai-cve-triaged` label to TC-8060.
8. Post the summary comment. It contains:
   - the version impact table
   - the dependency chain
   - the Affects Versions correction
   - the outcome (Case B, 2 tasks)
   - the task links
   - release Jira references
   - the data-discrepancy note
   - an ADF @mention of the reporter: `{ "type": "mention", "attrs": { "id": "557058:psirt-analyst-mock-id", "text": "@psirt-analyst" } }`
   - the triage-security comment footnote

## Pre-creation checklist

- [x] Task count per stream: 2 (Cargo is a source dependency)
- [x] Cross-stream coverage: 2.1.x is not affected, so no preemptive tasks are needed
- [x] Link types: Depend (CVE→tasks), Blocks (upstream→downstream, tasks→release Task), Related (release Task→CVE)
- [x] Preemptive labels: N/A
- [x] Coordination guidance: omitted. The Source Repositories table has no Deployment Context column, and remediation-templates.md says to leave the subsection out in that case.
- [ ] Release Jira linking: pending Step 7.5 (not executable in eval)
- [x] Dedup consistency: no dedup marking (Step 7.5.3 could not run)
