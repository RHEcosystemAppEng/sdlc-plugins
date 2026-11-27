# TC-8060 — Step 8: Remediation

**Decision: Case B.** The issue is scoped to 2.2.x, and 2.2.0, 2.2.1 and 2.2.2 are affected. The cross-stream check found 2.1.x not affected, so Case A does not apply and no preemptive tasks are needed.

- Ecosystem: Cargo, a source dependency, so **2 tasks** for stream 2.2.x: an upstream remediation task plus a downstream propagation task that it blocks.
- Dependency type: **transitive**. The chain is `backend (workspace) → reqwest → hyper → h2`, 3 levels deep, production profile.
- Remediation approach: **two-tier**. First bump the direct dependency (reqwest, and hyper through it) so h2 resolves to 0.4.5 or later. If that is not viable, pin h2 directly.
- Template: Upstream backport, with the transitive two-tier section. Step 2.5 evidence (h2 0.4.5 at `v0.4.11` and `v0.4.12`) suggests `release/0.4.z` already ships the fix. Branch HEAD was not inspected, though. If the engineer confirms HEAD is at 0.4.5 or later, switch task 1 to the **dependency bump** variant (same labels, links and downstream task). Engineer note: the latest 2.2.x releases (2.2.3 and 2.2.4) already ship h2 0.4.5. Confirm that a new remediation build is still wanted, as opposed to recording "fixed in 2.2.3" for the affected 2.2.0 to 2.2.2.
- Coordination Guidance: left out, because the Source Repositories table has no Deployment Context column.
- Labels: `ai-generated-jira`, `Security`, `CVE-2026-99010`. There is no `dev-dependency` label (production dependency) and no `security-preemptive` label (own CVE Jira).
- Security level: copy the security level of parent TC-8060 into both tasks. It was not readable in this eval; omit it only if the parent has none.
- Priority and fixVersion: prompt the engineer, since no default is configured.

---

## Task 1: Upstream remediation (rhtpa-backend, release/0.4.z)

**Summary:** Remediate CVE-2026-99010: bump h2 to 0.4.5 (2.2.x)
**Project:** TC | **Issue type:** Task
**Labels:** ai-generated-jira, Security, CVE-2026-99010
**Security:** `<TC-8060 security level>`

```
## Repository

rhtpa-backend (backend)

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99010: h2 memory exhaustion via CONTINUATION frames (DoS,
CVSS 7.5 High). h2 before 0.4.5 does not limit the number of CONTINUATION
frames received for a single HEADERS frame, so a remote attacker can exhaust
server memory. The vulnerable dependency (h2 < 0.4.5) must be updated
to the fixed version (0.4.5+).

h2 is NOT a direct dependency of backend. It is pulled in transitively:

  backend (workspace) → reqwest → hyper → h2
  Type: transitive (3 levels deep)
  Profile: production (reqwest is a runtime dependency)

Resolved versions in the affected Cargo.lock: reqwest 0.12.5 → hyper 1.4.1 →
h2 0.4.4.

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 (retag of 2.2.1)
Not affected: RHTPA 2.2.3, RHTPA 2.2.4 (ship h2 0.4.5)
Source commit(s): backend v0.4.5 (2.2.0), v0.4.8 (2.2.1 / 2.2.2)

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99010

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend (workspace) → reqwest → hyper → h2)
- Direct dependency to bump first: reqwest (backend/Cargo.toml:
  `reqwest = { version = "0.12", features = ["json"] }`). The intermediate crate is hyper (1.4.1).
- The dependency is in production [dependencies], not dev-only or build-only, so
  no `dev-dependency` label and no priority override.
- Lock-file evidence shows release/0.4.z already resolves h2 0.4.5 as of
  v0.4.11 (2.2.3). Before changing anything, check the branch HEAD with
  `git show release/0.4.z:Cargo.lock | grep -A2 'name = "h2"'`. If it already
  shows >= 0.4.5, no source change is needed: record the fixing commit or tag for
  the downstream task.

### Remediation approach (transitive dependency)

h2 is a **transitive** dependency, so use a two-tier approach:

**Preferred: bump the direct dependency**
- The direct dependency that pulls in h2 is reqwest (reqwest → hyper → h2).
- Bump reqwest (and hyper through it) to versions whose transitive closure
  resolves h2 >= 0.4.5. Within the existing semver ranges (reqwest 0.12,
  hyper 1.x, h2 0.4) this is usually `cargo update -p reqwest -p hyper -p h2`.
- Verify the bump does not introduce breaking API changes to reqwest or hyper.

**Fallback: pin the transitive dependency directly**
If bumping reqwest/hyper is not viable (breaking API changes, no release
with the fix, or an intermediate crate pins h2 < 0.4.5):
- Cargo: `cargo add h2@0.4.5` to add h2 as a direct dependency, overriding the
  transitive resolution. Alternatively, `cargo update -p h2 --precise 0.4.5` if
  the semver ranges allow it.
- If hyper (or another intermediate crate) pins h2 < 0.4.5, coordinate with
  the intermediate crate's maintainers. A `[patch.crates-io]` override is a
  temporary measure until they release.
- Document why the direct-dependency bump was not viable in the PR description.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.5 in Cargo.lock
- [ ] Dependency chain backend → reqwest → hyper → h2 resolves h2 >= 0.4.5 (or h2 is pinned directly with a documented reason)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8060 (parent tracking issue)
```

---

## Task 2: Downstream propagation (rhtpa-release.0.4.z, main)

**Summary:** Propagate CVE-2026-99010 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)
**Project:** TC | **Issue type:** Task
**Labels:** ai-generated-jira, Security, CVE-2026-99010
**Security:** `<TC-8060 security level>`

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99010 fix from {{upstream-task-key}}.

The upstream task ({{upstream-task-key}}) bumps h2 to 0.4.5 on release/0.4.z,
either through reqwest → hyper or by pinning h2 directly. Once that PR merges
(or once the existing fixing tag is confirmed), update the source pinning in
this Konflux release repo so the next build ships the fix.

Dependency chain: backend (workspace) → reqwest → hyper → h2 (transitive, 3 levels)

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (the download URL contains the backend tag, e.g. v0.4.12)
- **Dependency type**: transitive (backend → reqwest → hyper → h2), carried forward from the upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag. Tags
  v0.4.11 and later already resolve h2 0.4.5.
- If the upstream fix pinned h2 directly (fallback approach), check that the
  pinning shows up in the downstream build's Cargo.lock (h2 >= 0.4.5) after
  the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix (h2 >= 0.4.5)
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: {{upstream-task-key}} (upstream remediation must merge first)
- Depends on: TC-8060 (parent tracking issue)
```

---

## Proposed Jira operations (not executed, eval mode)

1. Create Task 1, then post a description digest comment (`[sdlc-workflow] Description digest: sha256-md:<hex>`) before any links.
2. Create Task 2, then post its description digest comment.
3. Links:
   - TC-8060 → Task 1 (Depend)
   - TC-8060 → Task 2 (Depend)
   - Task 1 → Task 2 (Blocks: upstream blocks downstream)
   - Task 1 and Task 2 → "RHTPA 2.2.x CVE triage" release Task (Blocks), if Step 7.5 is active
   - Release Task → TC-8060 (Related)
4. Update Affects Versions on TC-8060 to RHTPA 2.2.0, 2.2.1, 2.2.2.
5. Transition TC-8060 to In Progress, skipped if it is already Assigned or in a later indeterminate status. Assign it to the current user.
6. Comment on TC-8060: "Remediation tasks created: {{upstream-task-key}} (upstream backport), {{downstream-task-key}} (downstream propagation, blocked by {{upstream-task-key}})", plus the Comment Footnote.
7. Add the `ai-cve-triaged` label. Post a summary comment with the version impact table, the Affects Versions correction, the outcome (Case B, 2 tasks), task links, release Jira references, the dependency chain, and an @mention of reporter psirt-analyst (`557058:psirt-analyst-mock-id`), plus the Comment Footnote.

### Pre-creation checklist

- [x] Task count per stream: 2 (Cargo is a source dependency)
- [x] Cross-stream coverage: 2.1.x is not affected, so no preemptive tasks are needed
- [x] Link types: Depend (to own CVE), Blocks (upstream to downstream), Related (CVE to release Task)
- [x] Preemptive labels: none needed
- [x] Coordination guidance: left out (no Deployment Context column)
- [ ] Release Jira linking: pending the engineer's choice of 2.2.x release version (Step 7.5)
- [x] Dedup consistency: no dedup (Upstream Affected Component field not configured)

### Open items for the engineer

1. Settle the h2 lock-version discrepancy between the issue fixture and the matrix mock (see `version-impact.md`). If the matrix-mock values are correct, the outcome becomes Case C: close as Not a Bug, VEX "Component not Present".
2. Confirm the h2 version at the `release/0.4.z` HEAD, which decides between the backport and dependency-bump variants.
3. Confirm 2.2.0 through 2.2.2 are still in lifecycle (Step 5), given that 2.2.3 and 2.2.4 already ship the fix.
4. The matrix is 152 days old. Consider refreshing it.
5. The due date (2026-08-15) has passed.
