# TC-8001 — Remediation (Steps 4–8)

> Everything in this file is a **proposal** waiting for engineer confirmation. No Jira
> search, issue creation, link, label, transition, or comment was performed. Placeholder
> keys (`<upstream-task-2.2>`, `<release-task-2.2>`, ...) stand for the keys Jira would
> return. No real keys are invented.

## Preceding steps (inputs to Step 8)

| Step | Outcome in this eval |
|---|---|
| 4 – Sibling search | Would run `project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8001`. **Not executed.** No sibling data was provided, so no same-stream duplicate (4.1) and no 2.1.x companion (4.2) are known. If a `[rhtpa-2.1]` companion is found, link it with Related and **drop the 2.1.x preemptive tasks below**. |
| 4.3 – Cross-CVE overlap | **Skipped**: Upstream Affected Component, PS Component, and Stream fields are not configured. |
| 4.4 – Preemptive reconciliation | Would run `project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812'`, filtered to `(rhtpa-2.2)`. **Not executed.** No existing preemptive task is known, so 2.2.x task creation is not skipped. |
| 5 – Lifecycle | Product pages (https://access.example.com/product-life-cycle/rhtpa) **not fetched**. All affected versions are treated as supported, pending verification. If 2.1.x turns out to be EOL, drop the 2.1.x preemptive tasks. |
| 6 – Already fixed | Depends on Step 4. No resolved siblings are known, so this check does not close the issue. |
| 7 – Concurrent triage | **Skipped**: Upstream Affected Component field is not configured. |

## Step 7.5 – Release Jira orchestration (confirmations needed before Step 8)

Release Jira is resolved per release family. Only **non-preemptive** remediation tasks
are linked to a release Task.

### 2.2.x family (issue scope, standard remediation)

**7.5.1 – Release Epic.** Search (not executed):
`project = TC AND issuetype = Epic AND summary ~ 'RHTPA 2.2' AND summary ~ 'Release Tasks' ORDER BY created DESC`

- If an Epic exists (for example "RHTPA 2.2.x Release Tasks"), reuse it and take its version.
- If none exists, the default is the next patch after the latest released 2.2.x version in
  the matrix (**2.2.4**), which gives **2.2.5**. **Individual confirmation is required:**

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

  The matrix is 148 days stale, so a 2.2.5 or later may already have shipped. Confirm the
  version (option 2) before accepting.
  On Accept: create Epic "RHTPA 2.2.5 Release Tasks" (labels `ai-generated-jira`), then
  post its description digest comment.

**7.5.2 – Release Task.** Search (not executed):
`project = TC AND issuetype = Task AND parent = <release-epic-2.2> AND summary ~ 'RHTPA 2.2.5 CVE triage'`
If none exists, **individual confirmation is required**:

```
No release Task found under <release-epic-2.2>.

Proposed: Create "RHTPA 2.2.5 CVE triage" as child of <release-epic-2.2>

Proceed? (Yes / No)
```

On Yes: create the Task (labels `ai-generated-jira`, parent `<release-epic-2.2>`), then post
its digest. Store it as `<release-task-2.2>`.

Approving one creation does **not** approve the other. If either is skipped, the
remediation tasks are still created but not linked to a release Task.

### 2.1.x family (outside scope, preemptive only)

The only 2.1.x work is **preemptive** tasks, which are never linked to release Jira. Proposed
default is to **Skip** release Jira for 2.1.x. The engineer can still choose to create
"RHTPA 2.1.2 Release Tasks" / "RHTPA 2.1.2 CVE triage" (next patch after 2.1.1), and each
creation would need its own confirmation.

### 7.5.3 – Cross-CVE dedup decision

**Dedup skipped: no dedup match is possible, so remediation tasks are created as normal.**
The Upstream Affected Component custom field is not configured in Security Configuration,
and 7.5.3 requires it. No existing remediation Task was matched or reused. None of the
dedup actions (Depend link to a covering task, adding the CVE label to it) apply. No stream
is marked as dedup'd.

## Step 8 – Decision

- Supported versions are affected (2.1.0, 2.1.1, 2.2.0–2.2.2), so **not Case C**. No
  Not-a-Bug closure and no VEX value.
- The issue is **scoped** (`[rhtpa-2.2]`) and another stream (2.1.x) is affected, so this is
  **Case A**: post a cross-stream comment, plus preemptive tasks for 2.1.x if it has no
  CVE Jira of its own.
- The in-scope 2.2.x versions are affected, so this is **Case B** for 2.2.x. Cargo is a source
  dependency, so there are **2 tasks**. Step 2.5 shows the fix is on `release/0.4.z`, so the
  pair is a **dependency bump + downstream propagation**.

> **Important caveat for 2.2.x.** RHTPA 2.2.3 (`v0.4.11`) and 2.2.4 (`v0.4.12`) already ship
> quinn-proto 0.11.14. The fix has effectively shipped. The 2.2.x tasks below follow the
> skill's required structure, but their acceptance criteria may already be met. Their real
> value is confirming that `release/0.4.z` HEAD and the next 2.2.x build stay at >= 0.11.14.
> The engineer may decline creating them and instead note in the summary that the fix
> shipped in RHTPA 2.2.3. The skill has no automatic close path for this situation, so
> this is an explicit engineer decision.

Dependency type and profile are **not determined** (see version-impact.md 2.3.5). The
`dev-dependency` label and Normal priority override are **not** applied unless the check
shows quinn-proto is dev/build-only. Coordination Guidance is left out because the Source
Repositories table has no Deployment Context column.

### Case A – Cross-stream impact comment on TC-8001

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s)
2.1.x (RHTPA 2.1.0, RHTPA 2.1.1 — quinn-proto 0.11.9 at v0.3.8 / v0.3.12)
based on lock file analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

---
This comment was AI-generated by sdlc-workflow/triage-security v0.14.0.
```

---

### Task 1 — 2.2.x dependency bump (standard)

- **Summary:** `Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`
- **Links:** Depend (TC-8001 inward → `<bump-task-2.2>` outward). Blocks (`<bump-task-2.2>` → `<downstream-task-2.2>`). Blocks (`<bump-task-2.2>` inward → `<release-task-2.2>` outward), if 7.5 is active.

```
## Repository

backend (rhtpa-backend — https://github.com/rhtpa/rhtpa-backend)

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream —
a package manager update is sufficient. quinn-proto before 0.11.14 panics when a
remote peer sends a STREAMS frame requesting an excessive number of streams (DoS,
CVSS 7.5).

Affected versions: RHTPA 2.2.0 (quinn-proto 0.11.9), RHTPA 2.2.1 (0.11.12),
RHTPA 2.2.2 (retag of 2.2.1). RHTPA 2.2.3 and 2.2.4 already ship 0.11.14.
Source commit(s): v0.4.5, v0.4.8 (backend tags from the supportability matrix)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: not determined during triage — verify with
  `cargo tree -i quinn-proto` (direct vs transitive, e.g. via quinn)
- Released tags v0.4.11 / v0.4.12 on this line already resolve quinn-proto 0.11.14;
  first confirm Cargo.lock at release/0.4.z HEAD. If it is already >= 0.11.14, record
  that in the PR/Jira and no code change is required.
- **Remediation action**: `cargo update -p quinn-proto`
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14` (transitive fallback), or bump the
  direct dependency (e.g. quinn) whose closure includes quinn-proto >= 0.11.14
- Verify the lock file reflects >= 0.11.14 after the update
- If the vulnerable dependency is dev-only or build-only, the remediation priority
  is Normal regardless of CVE severity. Add `dev-dependency` label to the task.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14 on release/0.4.z
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

### Task 2 — 2.2.x downstream propagation (standard, blocked by Task 1)

- **Summary:** `Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`
- **Links:** Depend (TC-8001 → `<downstream-task-2.2>`). Blocked by `<bump-task-2.2>`. Blocks → `<release-task-2.2>`, if active.

```
## Repository

rhtpa-release.0.4.z (git.example.com/rhtpa/rhtpa-release.0.4.z)

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <bump-task-2.2>.

The dependency bump (<bump-task-2.2>) bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g. v0.4.12)
- **Dependency type**: not determined — carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- The current pin (v0.4.12, RHTPA 2.2.4) already ships quinn-proto 0.11.14; if no new
  upstream commit is needed, verify the next build keeps a tag >= v0.4.11
- If the upstream fix pinned a transitive dependency directly (fallback
  approach), verify the pinning is reflected in the downstream build's
  lock file after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <bump-task-2.2> (upstream change must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

### Task 3 — 2.1.x upstream backport (PREEMPTIVE)

Created only if Step 4 finds **no** `[rhtpa-2.1]` CVE Jira for CVE-2026-31812, and Step 5
confirms 2.1.x is supported.

- **Summary:** `Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- **Links:** **Related** (TC-8001 inward → `<upstream-task-2.1>` outward), not Depend. Blocks (`<upstream-task-2.1>` → `<downstream-task-2.1>`). **Not linked to a release Task** (preemptive).

```
## Repository

backend (rhtpa-backend — https://github.com/rhtpa/rhtpa-backend)

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (DoS).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (quinn-proto 0.11.9), RHTPA 2.1.1 (quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12 (backend tags from the supportability matrix)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: not determined during triage — verify with
  `cargo tree -i quinn-proto`
- If the vulnerable dependency is dev-only or build-only, the remediation priority
  is Normal regardless of CVE severity. Add `dev-dependency` label to the task.

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock / Cargo.toml
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (e.g. quinn)
- Bump it to a version whose transitive closure includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes

**Fallback: pin the transitive dependency directly**
- `cargo add quinn-proto@0.11.14` (or `cargo update -p quinn-proto --precise 0.11.14`)
- Document why the direct dep bump was not viable in the PR description

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8001 (originating CVE Jira, stream 2.2.x)
```

### Task 4 — 2.1.x downstream propagation (PREEMPTIVE, blocked by Task 3)

- **Summary:** `Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- **Links:** Related (TC-8001 → `<downstream-task-2.1>`). Blocked by `<upstream-task-2.1>`. No release link.

```
## Repository

rhtpa-release.0.3.z (git.example.com/rhtpa/rhtpa-release.0.3.z)

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from <upstream-task-2.1>.

The upstream backport (<upstream-task-2.1>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g. v0.3.12)
- **Dependency type**: not determined — carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback
  approach), verify the pinning is reflected in the downstream build's
  lock file after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-2.1> (upstream backport must merge first)
- Related to: TC-8001 (originating CVE Jira)
```

---

## Proposed execution order (after confirmation). Nothing has been executed.

For each task: create it, post its description digest
(`[sdlc-workflow] Description digest: <sha256-...>`), and only then create its links.

1. Task 1, then digest, then Depend TC-8001 → Task 1
2. Task 2, then digest, then Depend TC-8001 → Task 2, then Blocks Task 1 → Task 2
3. If release Jira is active for 2.2.x: Blocks Task 1 → `<release-task-2.2>`, Blocks Task 2 → `<release-task-2.2>`, Related `<release-task-2.2>` → TC-8001
4. (Conditional) Task 3, then digest, then Related TC-8001 → Task 3. Task 4, then digest, then Related TC-8001 → Task 4, then Blocks Task 3 → Task 4
5. Case A comment on TC-8001 listing the preemptive tasks (`2.1.x: <upstream-task-2.1>, <downstream-task-2.1> (security-preemptive)`), with footnote
6. Transition to In Progress: skipped, because TC-8001 would already be `ASSIGNED` (indeterminate category) after the early assignment step. The assignment itself was proposed earlier.
7. Remediation-created comment: "Remediation tasks created: `<bump-task-2.2>` (dependency bump), `<downstream-task-2.2>` (downstream propagation, blocked by `<bump-task-2.2>`)", with footnote
8. Post-triage: add the `ai-cve-triaged` label. Post a summary comment with the version impact table, the Affects Versions correction, the outcome, task links, release Epic/Task refs, dedup result ("skipped: Upstream Affected Component field not configured"), and an @mention of the TC-8001 reporter (ADF mention node), with the Comment Footnote (`sdlc-workflow/triage-security v0.14.0`).

## Pre-creation checklist

- [x] Task count per stream: Cargo is a source dependency, so 2 per stream (2.2.x: bump + downstream; 2.1.x: backport + downstream)
- [x] Cross-stream coverage: 2.1.x gets preemptive tasks, or none if a sibling CVE Jira exists
- [x] Link types: Depend for TC-8001 ↔ 2.2.x tasks, Related for preemptive 2.1.x tasks, Blocks from upstream to downstream
- [x] Preemptive labels: on the 2.1.x tasks only
- [x] Coordination guidance: left out (no Deployment Context column, backward-compatibility rule)
- [x] Release Jira linking: only the non-preemptive 2.2.x tasks, plus TC-8001 Related to the release Task
- [x] Dedup consistency: no stream dedup'd (7.5.3 skipped)

## Open items before any Jira write

1. The matrix is 148 days stale. Refresh it, or explicitly confirm proceeding.
2. Development stream not determined (needs Jira unreleased versions).
3. Dependency chain and profile (direct/transitive, prod/dev) not determined.
4. `release/0.4.z` and `release/0.3.z` HEAD lock files not inspected (Step 2.5).
5. Step 4 sibling search, Step 4.4 preemptive search, and Step 5 lifecycle check not executed. Their results can remove Tasks 3–4 or close the issue.
6. Engineer decision on whether the 2.2.x tasks are needed, given the fix already shipped in RHTPA 2.2.3.
