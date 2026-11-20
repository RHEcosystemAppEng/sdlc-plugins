# TC-8001 — Release Orchestration, Dedup Decision, and Remediation (Steps 7 – 8)

> **Simulation notice:** No Jira operation was performed. Every search, creation, link,
> label, transition, and comment below is a **proposal**. Each one needs explicit engineer
> confirmation before it runs. Jira keys for new issues appear as placeholders
> (`<release-epic-2.2>`, `<task-A>`, ...). No keys were invented.

## Inputs carried forward

- CVE-2026-31812, quinn-proto < 0.11.14, fixed in 0.11.14, Cargo (source dependency).
- Issue scope: **2.2.x**. Affected in scope: RHTPA 2.2.0, 2.2.1, 2.2.2. Not affected: 2.2.3 and 2.2.4 (0.11.14 already shipped).
- Other stream: **2.1.x**. 2.1.0 and 2.1.1 are affected (0.11.9). No fix is evident on `release/0.3.z`.
- Steps 4 to 6: no siblings, overlap, or preemptive tasks are known (searches not run in this eval). The lifecycle is assumed supported (page not fetched). Nothing was already fixed by a sibling.

## Step 7 — Concurrent triage detection

**Skipped.** The Upstream Affected Component custom field is not configured in Security
Configuration. The step's prerequisite is not met, so no JQL runs and there is no concurrent
triage prompt. The `concurrent-triage-overlap` label is not added.

## Step 7.5 — Release Jira orchestration

Scope: release Jira applies **per release family**, and only to **non-preemptive**
remediation. TC-8001 is scoped to 2.2.x, so its Case B tasks are non-preemptive and are
linked to the 2.2.x release Jira. The 2.1.x tasks are preemptive (Case A) and are **not**
linked to release Jira. They are linked to TC-8001 with "Related" only. When PSIRT creates a
2.1.x CVE Jira, its own triage (Step 4.4 reconciliation, then 7.5) handles 2.1.x release
linking.

### 7.5.1 — Release Epic for family 2.2.x (individual confirmation)

1. Search (not executed):
   ```
   project = TC AND issuetype = Epic AND summary ~ 'RHTPA 2.2' AND summary ~ 'Release Tasks' ORDER BY created DESC
   ```
2. **If an Epic exists** (for example "RHTPA 2.2.5 Release Tasks"), reuse it and take the version from its summary. No creation confirmation is needed.
3. **If none exists**, the default is the next patch after the latest released 2.2.x version in the matrix (2.2.4), which is **2.2.5**. Ask the engineer separately for this decision, because the version choice is high-stakes:
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
   Caveat: the matrix is 145 days stale. A 2.2.5 or later may already have shipped. This makes the version confirmation (or a matrix refresh) especially important.
4. On Accept, create the Epic: summary `RHTPA 2.2.5 Release Tasks`, labels `["ai-generated-jira"]`, description "Release tracking Epic for RHTPA 2.2.5. Contains CVE triage and remediation tasks for this release." Then post a description digest comment.

### 7.5.2 — Release Task (separate individual confirmation)

1. Search (not executed): `project = TC AND issuetype = Task AND parent = <release-epic-2.2> AND summary ~ 'RHTPA 2.2.5 CVE triage'`.
2. If none exists, ask:
   ```
   No release Task found under <release-epic-2.2>.

   Proposed: Create "RHTPA 2.2.5 CVE triage" as child of <release-epic-2.2>

   Proceed? (Yes / No)
   ```
   Approving the Epic does **not** approve the Task. Each creation needs its own confirmation.
3. On Yes, create the Task: summary `RHTPA 2.2.5 CVE triage`, parent `<release-epic-2.2>`, labels `["ai-generated-jira"]`. Post a digest comment. Store `<release-task-2.2>` for Step 8 linking.
4. If the engineer skips at either prompt, Step 8 still creates the 2.2.x tasks without release links.

### 7.5.3 — Cross-CVE dedup decision

**Dedup is skipped. No dedup match exists, so new remediation tasks are planned.**

- Prerequisite: the Upstream Affected Component custom field must be configured. It is **not** configured in this project's Security Configuration, so the whole dedup check is skipped. That includes the library-summary fallback, which only applies inside the check when a resolved CVE lacks the Depend link or the field value.
- Result: no stream is marked as dedup'd. Nothing is linked to an existing remediation task, and no CVE label is added to an existing task. Step 8 proceeds with standard task creation.
- Risk note for the engineer: without the field, a quinn-proto remediation task created for another CVE in the same release would not be detected automatically. Glance at `<release-task-2.2>`'s Blocks links for a quinn-proto bump before confirming creation.

## Step 8 — Remediation decision

```
Supported versions affected?  YES
Issue scoped?                 YES (2.2.x)
Other streams affected?       YES (2.1.x)  → Case A (cross-stream) + Case B (in-scope)
Ecosystem                     Cargo → source dependency → 2 tasks per stream
  2.2.x: fix already on release/0.4.z  → dependency bump + downstream propagation
  2.1.x: fix NOT on release/0.3.z      → upstream backport + downstream propagation (preemptive)
```

**Recommendation and caveat for 2.2.x:** lock-file evidence shows the 2.2.x stream
**already ships the fix since RHTPA 2.2.3** (backend `v0.4.11` and `v0.4.12` contain
quinn-proto 0.11.14), and the Konflux repo already pins `v0.4.12`. The Case B tasks below
follow the skill's dependency-bump variant, but in practice they are verification tasks.
At the confirmation gate the engineer should choose one of:
(a) create them so the next 2.2.x release Task tracks the CVE formally, or
(b) decline them and record in the summary comment that 2.2.x was fixed in 2.2.3.
**The 2.1.x preemptive tasks are the substantive remediation.**

### Case A — Cross-stream impact (proposed comment on TC-8001)

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x
(RHTPA 2.1.0, 2.1.1 — quinn-proto 0.11.9 at backend v0.3.8 / v0.3.12)
based on lock file analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

---
This comment was AI-generated by sdlc-workflow/triage-security v0.14.0.
```

Check for a 2.1.x sibling CVE Jira (Step 4 JQL with suffix `[rhtpa-2.1]`):
- **If one exists**, do not create 2.1.x tasks. The sibling's own triage handles them.
- **If none exists** (assumed here, because the search was not run), create preemptive tasks A and B below.

---

### Task A — 2.1.x upstream backport (PREEMPTIVE)

- **Summary:** `Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- **Link:** TC-8001 → Task A, **Related** (not Depend, because TC-8001 belongs to stream 2.2.x)

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

Remediate CVE-2026-31812: quinn-proto panic on excessive stream counts (remote DoS via
crafted QUIC STREAMS frame, CVSS 7.5).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (quinn-proto 0.11.9), RHTPA 2.1.1 (quinn-proto 0.11.9)
Source commit(s): backend v0.3.8 (2.1.0), backend v0.3.12 (2.1.1)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: not determined during triage (Cargo.toml / reverse-dependency data
  unavailable) — likely transitive via `quinn`; confirm with `cargo tree -i quinn-proto`
- If the vulnerable dependency is dev-only or build-only (identified
  in Step 2.3.5), the remediation priority is Normal regardless of CVE
  severity. Add `dev-dependency` label to the task.

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

When the vulnerable package is a **transitive** dependency (pulled in
through intermediate packages), use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (see `cargo tree -i quinn-proto`)
- Bump the direct dependency to a version whose transitive closure
  includes quinn-proto >= 0.11.14 (`cargo update -p quinn-proto` is usually sufficient
  within the 0.11.x semver range)
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

- Depends on: TC-8001 (parent tracking issue — originating CVE, stream 2.2.x; linked via Related)
```

### Task B — 2.1.x downstream propagation (PREEMPTIVE, blocked by Task A)

- **Summary:** `Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- **Links:** TC-8001 → Task B, **Related**. Task A → Task B, **Blocks**.

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
CVE-2026-31812 fix from <task-A>.

The upstream backport (<task-A>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: backend — `artifacts.lock.yaml` (download URL contains tag,
  currently `v0.3.12`)
- **Dependency type**: carried forward from <task-A> (to be confirmed there)
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

- Depends on: <task-A> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue — originating CVE, stream 2.2.x; linked via Related)
```

---

### Task C — 2.2.x dependency bump (Case B, fix already available upstream)

- **Summary:** `Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`
- **Links:** TC-8001 → Task C, **Depend**. Task C → `<release-task-2.2>`, **Blocks** (if Step 7.5 is active).

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream —
a package manager update is sufficient.

Affected versions: RHTPA 2.2.0 (quinn-proto 0.11.9), RHTPA 2.2.1 (quinn-proto 0.11.12),
RHTPA 2.2.2 (retag of 2.2.1). Not affected: RHTPA 2.2.3, 2.2.4 (quinn-proto 0.11.14).
Source commit(s): backend v0.4.5 (2.2.0), backend v0.4.8 (2.2.1, 2.2.2)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- Triage evidence: backend tags v0.4.11 and v0.4.12 already ship quinn-proto 0.11.14, so
  release/0.4.z is expected to be fixed already. Primary action is to confirm HEAD of
  release/0.4.z still resolves quinn-proto >= 0.11.14; only run an update if it regressed.
- **Dependency type**: not determined during triage — likely transitive via `quinn`;
  confirm with `cargo tree -i quinn-proto`
- **Remediation action**: run the appropriate package manager update command:
  - **Cargo**: `cargo update -p quinn-proto` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update
- If the vulnerable dependency is dev-only or build-only (identified
  in Step 2.3.5), the remediation priority is Normal regardless of CVE
  severity. Add `dev-dependency` label to the task.

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

### Task D — 2.2.x downstream propagation (Case B, blocked by Task C)

- **Summary:** `Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`
- **Links:** TC-8001 → Task D, **Depend**. Task C → Task D, **Blocks**. Task D → `<release-task-2.2>`, **Blocks** (if active).

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <task-C>.

The dependency bump (<task-C>) ensures quinn-proto is 0.11.14
on release/0.4.z. Once that is confirmed/merged, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: backend — `artifacts.lock.yaml` (download URL contains tag,
  currently `v0.4.12`)
- Triage evidence: the current pin `v0.4.12` already ships quinn-proto 0.11.14 (fixed since
  RHTPA 2.2.3). If <task-C> required no change, verify the pin is >= v0.4.11 and close
  this task with no code change.
- **Dependency type**: carried forward from <task-C>
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

- Depends on: <task-C> (dependency bump must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

Coordination Guidance is intentionally **omitted** from all four tasks. The Source
Repositories table has no Deployment Context column, and backward compatibility says to omit
the subsection in that case.

## Proposed execution order (after confirmation; nothing executed)

1. (7.5) Find or create `<release-epic-2.2>` (confirmation 1), then find or create `<release-task-2.2>` (confirmation 2). Post a digest comment on each newly created issue.
2. For each task in order A, B, C, D: create the task, then **immediately post its description digest comment** (`[sdlc-workflow] Description digest: <tagged-digest>`) before any link or other comment.
3. Links:
   - A: TC-8001 → A, Related.
   - B: TC-8001 → B, Related. A → B, Blocks.
   - C: TC-8001 → C, Depend. C → `<release-task-2.2>`, Blocks.
   - D: TC-8001 → D, Depend. C → D, Blocks. D → `<release-task-2.2>`, Blocks.
   - Release: `<release-task-2.2>` → TC-8001, Related.
4. Transition TC-8001 to In Progress: **skip**. The TC Vulnerability workflow has no In Progress status, and after Step 0.8 the issue is in `ASSIGNED` (indeterminate category). Assignment is already done in Step 0.8.
5. Comments on TC-8001, each with the Comment Footnote "This comment was AI-generated by sdlc-workflow/triage-security v0.14.0.":
   - Cross-stream impact comment (Case A, above).
   - Preemptive task list: "Preemptive remediation tasks created for streams without CVE Jiras: 2.1.x: <task-A>, <task-B> (security-preemptive) ..."
   - Remediation task list: "Remediation tasks created: <task-C> (dependency bump), <task-D> (downstream propagation, blocked by <task-C>)"
6. Post-triage: add the `ai-cve-triaged` label to TC-8001. Post a summary comment with the version impact table, the Affects Versions correction (RHTPA 2.0.0 → 2.2.0/2.2.1/2.2.2), the outcome, task links, release Epic/Task refs, the dedup result ("skipped: Upstream Affected Component field not configured"), an ADF @mention of the reporter (account ID from the issue's reporter field, not in the fixture), and the footnote.

## Pre-creation checklist

- [x] Task count per stream: Cargo is a source dependency, so 2 tasks per stream (A+B for 2.1.x, C+D for 2.2.x).
- [x] Cross-stream coverage: 2.1.x gets preemptive tasks, conditional on no `[rhtpa-2.1]` sibling CVE Jira existing.
- [x] Link types: Depend for C and D (own CVE). Related for A and B (preemptive). Blocks for A→B and C→D.
- [x] Preemptive labels: A and B carry `security-preemptive`. C and D do not.
- [x] Coordination guidance: omitted, because the Deployment Context column is absent.
- [x] Release Jira linking: C and D link to `<release-task-2.2>` with Blocks. TC-8001 links to it with Related. A and B (preemptive) are not linked.
- [x] Dedup consistency: no stream is dedup'd (7.5.3 skipped), so no conflict.

## Open items needing live verification

- The matrix is 145 days stale. Refresh it before acting, because new 2.1.x or 2.2.x releases may change both the release version (2.2.5) and the impact.
- Sibling search (Step 4), preemptive-task search (4.4), lifecycle page (Step 5), MITRE/OSV cross-check (1.5), development stream (2.2), upstream branch HEADs (2.5), and the dependency chain (2.3.5) were all not executed in this eval.
- The due date (2026-07-15) is already past. Raise this with the engineer.
