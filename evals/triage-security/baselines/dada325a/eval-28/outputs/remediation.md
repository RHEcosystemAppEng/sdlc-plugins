# Step 8 – Remediation: TC-8060 (CVE-2026-99010, h2 < 0.4.5, stream 2.2.x)

## Decision

- Supported versions affected in scope: **YES** (2.2.0, 2.2.1, 2.2.2)
- Issue scoped: YES (2.2.x). Other streams affected: NO (2.1.x ships h2 0.4.5), so **Case A does not apply**.
- **Case B: create remediation tasks for 2.2.x.**
- Ecosystem: Cargo, a source dependency, so **2 tasks**: upstream (rhtpa-backend `release/0.4.z`) plus downstream propagation (rhtpa-release.0.4.z), where downstream is blocked by upstream.
- Dependency type: **transitive** (`backend → reqwest → hyper → h2`, 3 levels deep, production). Both tasks document the full chain and the **two-tier approach**:
  1. Preferred: bump the direct dependency reqwest (and hyper).
  2. Fallback: pin h2 directly.
- No `dev-dependency` label and no priority override, because h2 is a runtime dependency.
- Coordination Guidance is omitted because the Source Repositories table has no Deployment Context column.
- Step 7.5 release Jira: the release Epic "RHTPA 2.2.5 Release Tasks" and Task "RHTPA 2.2.5 CVE triage" would be found or created with individual confirmation. The next 2.2.x version (2.2.5 assumed) must be confirmed by the engineer. Cross-CVE dedup is skipped because the Upstream Affected Component field is not configured.
- Caveat from Step 2.5: 2.2.3 and later already ship h2 0.4.5, so the fix is likely already on `release/0.4.z`. If so, Task 1 becomes a verification task (dependency-bump variant). The two-tier approach below still applies if HEAD turns out to resolve h2 < 0.4.5.

---

## Task 1 – Upstream remediation (rhtpa-backend)

**Summary:** Remediate CVE-2026-99010: bump h2 to 0.4.5 (2.2.x)
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-99010`
**Link:** TC-8060 → this task (Depend). This task Blocks Task 2 and Blocks the release Task.

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99010: h2 memory exhaustion via CONTINUATION frames (DoS, CVSS 7.5).
h2 does not limit the number of CONTINUATION frames received for a single HEADERS
frame, allowing a remote attacker to exhaust server memory.
The vulnerable dependency (h2 < 0.4.5) must be updated to the fixed version (0.4.5+).

Affected versions: RHTPA 2.2.0 (h2 0.4.4), RHTPA 2.2.1 (h2 0.4.4), RHTPA 2.2.2 (retag of 2.2.1)
Not affected: RHTPA 2.2.3, 2.2.4 (h2 0.4.5)
Source commit(s): backend v0.4.5 (2.2.0), v0.4.8 (2.2.1 / 2.2.2)

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99010

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend (workspace) → reqwest → hyper → h2)
  - 3 levels deep; production profile (reqwest is a runtime [dependencies] entry)
  - Vulnerable resolution (Cargo.lock at v0.4.5 / v0.4.8): reqwest 0.12.5 → hyper 1.4.1 → h2 0.4.4
  - h2 is NOT declared in backend/Cargo.toml; it is pulled in only through reqwest → hyper
  - Present since 2.1.0 (initial project setup)
- First check current state: `git show release/0.4.z:Cargo.lock | grep -A2 'name = "h2"'`.
  Tags v0.4.11 / v0.4.12 already resolve h2 0.4.5, so HEAD may already be fixed; if so,
  confirm the version, add regression protection (see fallback tier for an explicit floor
  if desired), and record the fixing commit for the downstream task.

### Remediation approach (transitive dependency)

h2 is a **transitive** dependency, so use a two-tier approach:

**Preferred: bump the direct dependency (reqwest)**
- The direct dependency that pulls in h2 is `reqwest` (via `hyper`).
- Bump reqwest (and its hyper dependency) to versions whose transitive closure resolves
  h2 >= 0.4.5, e.g. `cargo update -p reqwest` then `cargo update -p hyper`, and verify
  `cargo tree -i h2` shows only h2 >= 0.4.5.
- Since hyper declares a semver-compatible h2 0.4 range, a lock refresh
  (`cargo update -p h2`) within the existing reqwest 0.12 / hyper 1.x line should
  resolve h2 0.4.5 without a manifest change.
- Verify the bump does not introduce breaking API changes in reqwest/hyper.

**Fallback: pin the transitive dependency directly**
If bumping reqwest/hyper is not viable (breaking API changes, no compatible release
with the fix, or an intermediate crate pins h2 < 0.4.5):
- Cargo: `cargo add h2@0.4.5` to add h2 as a direct dependency of backend, overriding
  the transitive resolution (or `cargo update -p h2 --precise 0.4.5` if only the lock
  file needs to move).
- If hyper or reqwest pins h2 to a version range excluding 0.4.5, coordinate with the
  hyper/reqwest maintainers (or use a `[patch.crates-io]` override as a last resort).
- Document why the direct dependency bump was not viable in the PR description.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.5 in Cargo.lock on release/0.4.z
- [ ] `cargo tree -i h2` shows no h2 < 0.4.5 anywhere in the dependency graph
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8060 (parent tracking issue)
```

---

## Task 2 – Downstream propagation (rhtpa-release.0.4.z)

**Summary:** Propagate CVE-2026-99010 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-99010`
**Links:** TC-8060 → this task (Depend). Task 1 Blocks this task. This task Blocks the release Task.

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99010 fix from <Task 1 key>.

The upstream remediation (<Task 1 key>) ensures h2 >= 0.4.5 on release/0.4.z
(transitive chain: backend → reqwest → hyper → h2). Once that PR merges (or is
confirmed already present), update the source pinning in this Konflux release
repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: transitive (chain: backend (workspace) → reqwest → hyper → h2) — carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
  (must be at or after a tag whose Cargo.lock resolves h2 >= 0.4.5; v0.4.11 and
  v0.4.12 already do per lock-file evidence)
- If the upstream fix pinned h2 directly (fallback tier), verify the pin is
  reflected in the downstream build's Cargo.lock after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix (h2 >= 0.4.5)
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <Task 1 key> (upstream remediation must merge first)
- Depends on: TC-8060 (parent tracking issue)
```

---

## Proposed Jira operations (interactive mode, all require confirmation, none executed)

1. Assign TC-8060 to the current user and transition New → Assigned (Step 0.8).
2. Affects Versions: add RHTPA 2.2.1 and RHTPA 2.2.2, keep RHTPA 2.2.0. Post a correction comment with the footnote.
3. Find or create the release Epic and release Task for the next 2.2.x release (Step 7.5).
4. Create Task 1 and post its description digest comment, then create Task 2 and post its description digest comment. Digests are posted before any links.
5. Create these links:
   - TC-8060 → Task 1 (Depend)
   - TC-8060 → Task 2 (Depend)
   - Task 1 → Task 2 (Blocks)
   - Task 1 and Task 2 → release Task (Blocks)
   - release Task → TC-8060 (Related)
6. TC-8060 is already in Assigned, which is in the indeterminate category, so skip the In Progress transition. Post a comment: "Remediation tasks created: <T1> (upstream remediation), <T2> (downstream propagation, blocked by <T1>)" plus the footnote.
7. Add the label `ai-cve-triaged`. Post the summary comment, which contains:
   - the impact table
   - the Affects Versions correction
   - the tasks
   - the release Jira
   - an ADF @mention of reporter psirt-analyst (`557058:psirt-analyst-mock-id`)
   - the Comment Footnote

## Pre-creation checklist

- [x] Task count per stream: 2 (Cargo, a source dependency)
- [x] Cross-stream coverage: 2.1.x is not affected, so no preemptive tasks
- [x] Link types: Depend (own CVE) and Blocks (upstream → downstream, and remediation → release Task)
- [x] Preemptive labels: not applicable
- [x] Coordination guidance: omitted (no Deployment Context column)
- [x] Release Jira linking: planned
- [x] Dedup consistency: not applicable (Upstream Affected Component field not configured)
