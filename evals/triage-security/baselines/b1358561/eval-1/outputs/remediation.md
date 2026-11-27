# TC-8001 — Pre-remediation checks, Release Orchestration, and Remediation (Steps 4–8)

> **No Jira operation was performed.** Every search, creation, link, transition, label, and
> comment below is a **proposal** that would need explicit engineer confirmation in a live
> interactive run. Task keys are placeholders such as `<2.1-upstream-task>`.

## Steps 4–7 summary (inputs to the remediation decision)

| Step | Result | Basis |
|---|---|---|
| 4 Sibling search (`labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8001`) | Not executed. No sibling data supplied, so I treated it as **no known siblings** (no 2.1.x companion CVE Jira known). | No Jira call |
| 4.1 Same-stream duplicate | None known. No duplicate closure. | — |
| 4.2 Cross-stream coordination | No known companion to link. In a live run, a 2.1.x sibling found here would get a Related link (idempotent check first), and the 2.1.x preemptive tasks below would be **dropped**. | — |
| 4.3 Cross-CVE overlap | **Skipped.** Upstream Affected Component, PS Component, and Stream fields are not configured. | Config |
| 4.4 Preemptive reconciliation (`labels = 'security-preemptive' AND labels = 'CVE-2026-31812'`) | Not executed. None known, so standard task creation goes ahead for 2.2.x. | No Jira call |
| 5 Lifecycle check | Product pages URL not fetched. I **assumed 2.1.x and 2.2.x are supported**, pending a live check. If 2.1.x turns out to be EOL, drop the 2.1.x preemptive tasks. | No WebFetch |
| 6 Already-fixed (resolved siblings) | No resolved siblings known, so no Step 6 closure. Separately, the version impact table shows the fix **already shipped in RHTPA 2.2.3/2.2.4** (see the 2.2.x note below). | Lock data |
| 7 Concurrent triage detection | **Skipped.** Upstream Affected Component field is not configured. | Config |

## Step 7.5 — Release Jira orchestration (confirmations)

Each stream's sub-step 7.5.1 would search:

```
project = TC AND issuetype = Epic AND summary ~ 'RHTPA <major>.<minor>' AND summary ~ 'Release Tasks' ORDER BY created DESC
```

These searches were not executed. The prompts below show what the engineer would be asked if
**no existing Epic/Task were found**. If one exists, it is reused and needs no creation prompt.

### 2.2.x (in-scope, non-preemptive remediation)

**7.5.1 — Release Epic (individual confirmation required; the version decision is high-stakes):**

```
No release Epic found for stream 2.2.x.

Proposed version: RHTPA 2.2.5 Release Tasks
(based on latest released version 2.2.4 in supportability matrix)

Options:
1. Accept — create Epic with version 2.2.5
2. Specify different version
3. Skip — do not create release Jira for this stream

Choose (1/2/3):
```

The matrix is 152 days stale, so a release after 2.2.4 may already exist. The engineer should
check the default version 2.2.5 against the real release history before accepting.

If accepted, the proposed creation (NOT performed) is:
`create_issue(project TC, type Epic, summary "RHTPA 2.2.5 Release Tasks", labels ["ai-generated-jira"], security <TC-8001 security level>)`
followed by a description digest comment.

**7.5.2 — Release Task (separate individual confirmation):**

```
No release Task found under <release-epic-2.2>.

Proposed: Create "RHTPA 2.2.5 CVE triage" as child of <release-epic-2.2>

Proceed? (Yes / No)
```

If confirmed, the proposed creation (NOT performed) is:
`create_issue(project TC, type Task, summary "RHTPA 2.2.5 CVE triage", parent <release-epic-2.2>, labels ["ai-generated-jira"], security <TC-8001 security level>)`
followed by a description digest comment.

### 2.1.x (cross-stream, preemptive-only remediation)

Step 7.5 would present the same Epic prompt with default **RHTPA 2.1.2 Release Tasks** (latest
released 2.1.1). Release Jira linkage only applies to **non-preemptive** remediation, and every
2.1.x task here is preemptive (no 2.1.x CVE Jira exists). **Recommendation: choose "3. Skip" for
2.1.x.** The preemptive tasks are still created, but they are not linked to a release Task. When
PSIRT files a 2.1.x CVE Jira, its own triage will do the 2.1.x release orchestration and Step 4.4
reconciliation.

### 7.5.3 — Cross-CVE dedup decision

- **Decision: dedup SKIPPED. Proceed to standard Step 8 task creation.**
- Reason: 7.5.3 requires the **Upstream Affected Component custom field**, and the Security
  Configuration does not set it. Per the prerequisite, no configured field means skipping dedup.
  The library-summary fallback is also unavailable, because it only applies once the field is
  configured and the originating CVE lacks a Depend link or field value.
- Result: no stream is marked dedup'd. No existing remediation Task is relabeled or linked in
  place of creating new tasks.

## Step 8 — Remediation decision

Decision tree:
1. Supported versions affected? **Yes** (2.2.0, 2.2.1, 2.2.2 in scope; 2.1.0, 2.1.1 cross-stream).
2. Issue scoped? **Yes** (2.2.x).
3. Other streams affected? **Yes** (2.1.x). That triggers **Case A** (cross-stream comment plus
   preemptive tasks for 2.1.x) **and Case B** (remediation for 2.2.x).
4. Ecosystem is Cargo (source dependency), so each stream gets **2 tasks**.
   - 2.2.x: **dependency bump + downstream propagation**. Step 2.5 evidence suggests the upstream
     branch `release/0.4.z` already ships 0.11.14.
   - 2.1.x: **upstream backport + downstream propagation**. The fix is not confirmed on
     `release/0.3.z`. The latest release tag `v0.3.12` ships 0.11.9.

> **Important 2.2.x note for the engineer:** the fixed quinn-proto 0.11.14 already ships in
> released RHTPA **2.2.3** (`v0.4.11`) and **2.2.4** (`v0.4.12`). The two 2.2.x tasks below
> are therefore expected to be mostly verification. The bump task confirms `release/0.4.z`
> HEAD is still at 0.11.14 or later. The propagation task confirms the next 2.2.x build keeps
> it. The engineer may decline these two tasks at the confirmation gate and instead document
> "fixed in RHTPA 2.2.3" on TC-8001. The 2.1.x tasks are needed either way, because no 2.1.x
> release contains the fix.

Dependency type: **not determined** (the manifest and dependency graph were not inspected).
Both direct and transitive approaches are included, as the template provides. No `dev-dependency`
label, since there is no evidence of dev-only scope. No Coordination Guidance subsection, since
the Source Repositories table has no Deployment Context column.

---

### Case B, Task 1 (2.2.x): dependency bump

- **Summary:** `Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`
- **Security:** copied from TC-8001's security level
- **Links (proposed):** Depend (TC-8001 inward, this task outward). Blocks (this task, then
  `<2.2-downstream-task>`). Blocks (this task inward, `<release-task-2.2>` outward), if the
  release Task exists.

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream —
a package manager update is sufficient.

Affected versions: RHTPA 2.2.0 (quinn-proto 0.11.9), RHTPA 2.2.1 (0.11.12), RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8
Note: RHTPA 2.2.3 (v0.4.11) and 2.2.4 (v0.4.12) already ship quinn-proto 0.11.14.

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: not determined during triage (direct or transitive) — verify via `cargo tree -i quinn-proto`
- **Remediation action**: run the appropriate package manager update command:
  - **Cargo**: `cargo update -p quinn-proto` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update (released tags v0.4.11/v0.4.12
  already do; if branch HEAD already satisfies this, record that and close as no change needed)
- If the vulnerable dependency is dev-only or build-only, the remediation priority is
  Normal regardless of CVE severity. Add `dev-dependency` label to the task.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

### Case B, Task 2 (2.2.x): downstream propagation

- **Summary:** `Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`
- **Security:** copied from TC-8001
- **Links (proposed):** Depend (TC-8001, then this task). Blocked by `<2.2-bump-task>`. Blocks
  (this task inward, `<release-task-2.2>` outward).

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <2.2-bump-task>.

The dependency bump (<2.2-bump-task>) bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: not determined — carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
  (current latest pinned tag v0.4.12 already ships quinn-proto 0.11.14; ensure the
  next release does not regress below it)
- If the upstream fix pinned a transitive dependency directly (fallback
  approach), verify the pinning is reflected in the downstream build's
  lock file after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <2.2-bump-task> (upstream dependency bump must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

### Case A: cross-stream impact comment (proposed; NOT posted)

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s)
2.1.x (RHTPA 2.1.0, 2.1.1 — quinn-proto 0.11.9 at v0.3.8 / v0.3.12) based on lock file analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

---
<Comment Footnote per shared/comment-footnote.md, skill name: triage-security>
```

### Case A, Preemptive Task 1 (2.1.x): upstream backport

- **Summary:** `Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- **Security:** copied from TC-8001
- **Links (proposed):** **Related** (TC-8001 inward, this task outward), not Depend. Blocks (this
  task, then `<2.1-downstream-task>`). No release Task link, because preemptive tasks are not
  linked to release Jira.

```
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (remote DoS via a
crafted QUIC STREAMS frame). The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (quinn-proto 0.11.9), RHTPA 2.1.1 (quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: not determined during triage — verify via `cargo tree -i quinn-proto`
- If the vulnerable dependency is dev-only or build-only, the remediation priority is
  Normal regardless of CVE severity. Add `dev-dependency` label to the task.
- Upstream fix status on release/0.3.z HEAD was not verified; if HEAD already ships
  >= 0.11.14, this reduces to a dependency bump (`cargo update -p quinn-proto`).

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

When the vulnerable package is a **transitive** dependency (pulled in
through intermediate packages), use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (e.g., via `cargo tree -i quinn-proto`)
- Bump the direct dependency to a version whose transitive closure
  includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes to the
  direct dependency

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable (breaking API changes,
no release available with the fix):
- Cargo: `cargo add quinn-proto@0.11.14` to add as a direct
  dependency, overriding the transitive resolution
- Document why the direct dep bump was not viable in the PR description

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

### Case A, Preemptive Task 2 (2.1.x): downstream propagation

- **Summary:** `Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- **Security:** copied from TC-8001
- **Links (proposed):** **Related** (TC-8001, then this task). Blocked by `<2.1-upstream-task>`.

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from <2.1-upstream-task>.

The upstream backport (<2.1-upstream-task>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: not determined — carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback
  approach), verify the pinning is reflected in the downstream build's
  lock file after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <2.1-upstream-task> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

## Proposed execution order (after confirmation; NOT performed)

For each task: create it with the parent's security level, then post a description digest
comment (`shared/description-digest-protocol.md`) **before** any link or other comment, then add
its links.

1. Create `<2.2-bump-task>`, post its digest, link Depend TC-8001 → it.
2. Create `<2.2-downstream-task>`, post its digest, link Depend TC-8001 → it, link Blocks
   `<2.2-bump-task>` → `<2.2-downstream-task>`.
3. If the release Task exists: link Blocks for both 2.2.x tasks → `<release-task-2.2>`, and
   Related `<release-task-2.2>` → TC-8001.
4. Post the Case A cross-stream comment on TC-8001.
5. Create `<2.1-upstream-task>` and `<2.1-downstream-task>` (preemptive), post each digest,
   link Related TC-8001 → each, link Blocks upstream → downstream.
6. Comment on TC-8001 listing the preemptive tasks (`2.1.x: <2.1-upstream-task>,
   <2.1-downstream-task> (security-preemptive)`), with footnote.
7. Comment listing the 2.2.x remediation tasks, with footnote.
8. The In Progress transition is skipped, because Step 0.8 would already have moved TC-8001 to
   `ASSIGNED` (an indeterminate-category status). Assignment was already handled in Step 0.8.
9. Post-triage: add the `ai-cve-triaged` label, then post a summary comment. It covers the
   version impact table, the Affects Versions correction, the outcome, the task links, release
   Jira refs, and "dedup skipped (field not configured)". It @mentions the reporter (account ID
   from the live issue read) and includes the Comment Footnote.

## Pre-creation checklist

- [x] Task count per stream: Cargo is a source dependency, so 2 tasks each for 2.2.x and 2.1.x.
- [x] Cross-stream coverage: 2.1.x is covered by preemptive tasks (no known sibling CVE Jira).
- [x] Link types: Depend for 2.2.x tasks with TC-8001; Related for 2.1.x preemptive tasks;
  Blocks from upstream/bump to downstream.
- [x] Preemptive labels: 2.1.x tasks carry `security-preemptive`.
- [x] Coordination guidance: omitted, because the Deployment Context column is absent
  (backward compatibility rule).
- [x] Release Jira linking: 2.2.x non-preemptive tasks link to `<release-task-2.2>` if it is
  created or reused. 2.1.x preemptive tasks are not linked.
- [x] Dedup consistency: dedup skipped (field not configured), so no stream is marked dedup'd.

## Open items requiring live verification

- Matrix staleness (152 days): refresh, or confirm there are no releases after 2.2.4 or 2.1.1.
- MITRE/OSV cross-validation of the 0.11.14 threshold.
- Sibling CVE Jiras for 2.1.x. If one exists, drop the preemptive tasks and Related-link it.
- Product lifecycle status for 2.1.x and 2.2.x.
- `release/0.3.z` and `release/0.4.z` HEAD quinn-proto versions (Step 2.5).
- Direct vs transitive classification of quinn-proto.
- Real Jira version IDs for the RHTPA 2.2.0/2.2.1/2.2.2 correction.
