# TC-8001 — Release Orchestration, Dedup, and Remediation (Steps 7, 7.5, 8)

> Proposed only. No Jira search, issue creation, link, label, transition, or comment has
> been performed. Every mutation below waits for explicit engineer confirmation.

## Step 7: Concurrent triage detection

**Skipped.** The Upstream Affected Component custom field is not configured in Security
Configuration. That is a prerequisite, so this step is skipped, consistent with Step 4.3.

## Step 7.5: Release Jira orchestration (before any remediation is proposed)

Scope: release Jira covers **non-preemptive** remediation only. In this triage, that
means the **2.2.x** family, which is TC-8001's own stream. The 2.1.x tasks below are
preemptive (Case A), so they are **not** linked to a release Task.

### 7.5.1: Release Epic for 2.2.x (individual confirmation required)

Search to run (not run):
```
jira.search_jql("project = TC AND issuetype = Epic AND summary ~ 'RHTPA 2.2' AND summary ~ 'Release Tasks' ORDER BY created DESC", fields: ["summary","status"], maxResults: 5)
```
- **If an Epic exists** (e.g. "RHTPA 2.2.x Release Tasks"), reuse it and take its version.
- **If none exists**, the latest released version in the 2.2.x matrix is **2.2.4**, so the
  default is the next patch bump, **2.2.5**. Confirmation prompt to show:
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
  Because the matrix is 129 days stale, the engineer should check whether a release
  after 2.2.4 has already shipped before accepting 2.2.5. The version decision has
  high stakes.
  On Accept, create an Epic (`summary: "RHTPA 2.2.5 Release Tasks"`, labels
  `["ai-generated-jira"]`), then post a description digest comment.

### 7.5.2: Release Task (individual confirmation required)

Search to run: `project = TC AND issuetype = Task AND parent = <release-epic-key> AND summary ~ 'RHTPA 2.2.5 CVE triage'`.
If no Task exists, prompt:
```
No release Task found under <release-epic-key>.
Proposed: Create "RHTPA 2.2.5 CVE triage" as child of <release-epic-key>
Proceed? (Yes / No)
```
On Yes, create the Task (labels `["ai-generated-jira"]`, `parent: <release-epic-key>`),
post a digest comment, and store `<release-task-key>` for linking in Step 8. Approving
the Epic does **not** approve the Task. Each one needs its own confirmation.

If the engineer skips either one, Step 8 still creates the 2.2.x tasks without release links.

### 7.5.3: Cross-CVE dedup decision

**Dedup check skipped. No dedup applied.** This check requires the Upstream Affected
Component custom field, which is **not configured**. The protocol says: "If not
configured, skip dedup and proceed to Step 8." The library-summary fallback is meant for
an originating CVE that lacks the Depend link or field value. It does not replace the
missing prerequisite, so it is not used.

Result: no stream is marked as dedup'd. No existing remediation Task is reused, no
Depend link to a covering task is made, and no CVE label is added to an existing task.
Step 8 proceeds with normal task creation for 2.2.x.

## Step 8: Remediation decision

- Supported versions affected: **yes** (2.2.0–2.2.2 in scope; 2.1.0–2.1.1 cross-stream).
- Issue is scoped (`[rhtpa-2.2]`) and another stream (2.1.x) is affected, so the outcome
  is **Case A** (cross-stream comment plus preemptive tasks for 2.1.x if it has no CVE
  Jira of its own) **plus Case B** (standard tasks for 2.2.x).
- Ecosystem: Cargo (source dependency), so **2 tasks per stream**.
  - 2.2.x: fix already on `release/0.4.z`, so **dependency bump + downstream propagation**.
  - 2.1.x: no fix on `release/0.3.z`, so **upstream backport + downstream propagation** (preemptive).
- Not Case C. VEX is not applicable.

> **Engineer attention (2.2.x):** the latest 2.2.x release (2.2.4, backend `v0.4.12`)
> already ships quinn-proto 0.11.14, and so does 2.2.3. The 2.2.x tasks are therefore
> mostly verification work. They confirm `release/0.4.z` HEAD stays at 0.11.14 or higher
> and that the next 2.2.x build keeps pinning a backend tag at or after `v0.4.11`. The
> engineer may decide that customers on 2.2.0–2.2.2 are remediated by upgrading to
> 2.2.3 or later. The skill's template still requires both tasks, so they are proposed below.

Lifecycle (Step 5) and siblings (Step 4) were not checked in this eval. If a
`[rhtpa-2.1]` CVE Jira exists, **do not** create T3/T4. Link it as Related instead, and
2.1.x will be triaged through that issue.

Coordination Guidance is omitted from every task because the Source Repositories table
has no Deployment Context column.

---

### T1 (2.2.x, standard): Dependency bump

- **Summary:** `Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`
- **Links:** TC-8001 → T1 (Depend); T1 → T2 (Blocks); T1 → `<release-task-key>` (Blocks)

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream —
a package manager update is sufficient. quinn-proto before 0.11.14 panics when a
remote peer sends a QUIC frame that opens an excessive number of streams (DoS, CVSS 7.5).

Affected versions: RHTPA 2.2.0 (quinn-proto 0.11.9), RHTPA 2.2.1 (0.11.12),
RHTPA 2.2.2 (retag of 2.2.1). RHTPA 2.2.3 and 2.2.4 already ship 0.11.14.
Source commit(s): v0.4.5, v0.4.8 (backend tags from security-matrix.md)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: to be confirmed (direct vs transitive not determinable from
  triage evidence; inspect Cargo.toml / `cargo tree -i quinn-proto`)
- Tags v0.4.11 and v0.4.12 on this branch already ship quinn-proto 0.11.14; first verify
  release/0.4.z HEAD still resolves quinn-proto >= 0.11.14.
- **Remediation action**: if HEAD is below 0.11.14, run `cargo update -p quinn-proto`
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14` (or bump the direct dependency that
  pulls it in, if transitive)
- Verify Cargo.lock reflects >= 0.11.14 after the update
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

### T2 (2.2.x, standard): Downstream propagation (blocked by T1)

- **Summary:** `Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`
- **Links:** TC-8001 → T2 (Depend); T1 → T2 (Blocks); T2 → `<release-task-key>` (Blocks)

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <T1-key>.

The dependency bump (<T1-key>) ensures quinn-proto 0.11.14 on release/0.4.z.
Once that is confirmed/merged, ensure the source pinning in this Konflux release repo
references a backend tag that ships the fix so the next build ships it.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: to be confirmed — carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
  (must be v0.4.11 or later; latest released pin v0.4.12 already ships 0.11.14)
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

- Depends on: <T1-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### T3 (2.1.x, preemptive): Upstream backport

Create only if no `[rhtpa-2.1]` CVE-2026-31812 Jira exists.

- **Summary:** `Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- **Links:** TC-8001 → T3 (**Related**, not Depend); T3 → T4 (Blocks). No release-Task link (preemptive).

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

Remediate CVE-2026-31812: quinn-proto panic on excessive QUIC stream counts (DoS).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (quinn-proto 0.11.9), RHTPA 2.1.1 (quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12 (backend tags from security-matrix.md)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: to be confirmed (direct vs transitive not determinable from
  triage evidence; inspect Cargo.toml / `cargo tree -i quinn-proto`)
- If the vulnerable dependency is dev-only or build-only, the remediation priority is
  Normal regardless of CVE severity. Add `dev-dependency` label to the task.

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto
- Bump it to a version whose transitive closure includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes

**Fallback: pin the transitive dependency directly**
- Cargo: `cargo add quinn-proto@0.11.14`
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

### T4 (2.1.x, preemptive): Downstream propagation (blocked by T3)

- **Summary:** `Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- **Links:** TC-8001 → T4 (Related); T3 → T4 (Blocks)

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
CVE-2026-31812 fix from <T3-key>.

The upstream backport (<T3-key>) bumps quinn-proto to 0.11.14 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: to be confirmed — carried forward from upstream task
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

- Depends on: <T3-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

## Proposed execution order (after confirmation)

1. Release Epic, then release Task for 2.2.x (Step 7.5, each confirmed individually, each with a digest comment).
2. Create T1, post its digest comment, then create T2 and post its digest comment. Each
   digest comes before any link or other comment on that task.
3. Links: TC-8001 → T1, TC-8001 → T2 (Depend); T1 → T2 (Blocks); T1 and T2 →
   release Task (Blocks); release Task → TC-8001 (Related).
4. Case A cross-stream comment on TC-8001:
   ```
   Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x
   (RHTPA 2.1.0, 2.1.1 ship quinn-proto 0.11.9) based on lock file analysis.
   These streams are tracked by companion issues (see Related links)
   or may require separate PSIRT triage.
   ---
   This comment was AI-generated by sdlc-workflow/triage-security v0.13.10.
   ```
5. If no 2.1.x CVE Jira exists: create T3 and T4 (each followed by its digest), add
   Related links from TC-8001, add T3 → T4 (Blocks), then post the preemptive task-list
   comment (with footnote).
6. Transition TC-8001 to In Progress: **skip**. It will already be `ASSIGNED` from Step 0.8,
   an indeterminate-category status in the Bugzilla-style workflow. It is already assigned
   to the current user.
7. Remediation task-list comment, then add label `ai-cve-triaged`, then the post-triage
   summary comment. The summary includes the impact table, the Affects Versions
   correction, the outcome, task keys, release Epic/Task keys, dedup result (skipped,
   field not configured), an ADF @mention of the TC-8001 reporter, and the Comment Footnote.

## Pre-creation checklist

- [x] Task count per stream: Cargo gives 2 for 2.2.x and 2 for 2.1.x.
- [x] Cross-stream coverage: 2.1.x gets preemptive T3/T4, or uses an existing sibling CVE Jira if one exists.
- [x] Link types: Depend (T1/T2 ↔ TC-8001), Related (T3/T4 ↔ TC-8001), Blocks (T1→T2, T3→T4, T1/T2→release Task).
- [x] Preemptive labels: `security-preemptive` on T3/T4 only.
- [x] Coordination guidance: omitted because there is no Deployment Context column.
- [x] Release Jira linking: only non-preemptive tasks (T1/T2) block the release Task, and the CVE is Related to it.
- [x] Dedup consistency: dedup was skipped (prerequisite field missing), so no stream is marked dedup'd and none needs reuse-only handling.
