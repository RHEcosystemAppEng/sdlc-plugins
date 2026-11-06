# TC-8001 — Release Orchestration, Dedup and Remediation (Steps 7.5 and 8)

> **Simulation notice:** No Jira operation was performed. Every search, create, link,
> label, transition and comment below is a **proposal** that waits for explicit engineer
> confirmation. Issue keys that would only exist after creation appear as placeholders
> such as `<TASK-2.1-UPSTREAM>`.

## Inputs carried forward

- **Scope:** TC-8001 is scoped to **2.2.x** (`[rhtpa-2.2]`).
- **Affected in scope:** RHTPA 2.2.0, 2.2.1 and 2.2.2. RHTPA 2.2.3 and 2.2.4 ship
  quinn-proto 0.11.14 and are not affected.
- **Affected outside scope:** RHTPA 2.1.0 and 2.1.1 (quinn-proto 0.11.9).
- **Ecosystem:** Cargo, a source dependency, so 2 tasks per stream.
- **Upstream fix status:**
  - `release/0.4.z`: fixed (0.11.14 shipped in tags `v0.4.11` and `v0.4.12`).
  - `release/0.3.z`: no evidence of a fix.
- **Step 7 (concurrent triage):** skipped because the Upstream Affected Component field
  is not configured. Triage proceeds to Step 7.5.

---

## Step 7.5 — Release Jira orchestration (confirmations)

Release Jira is resolved per **release family**. Only **non-preemptive** remediation
tasks are linked to it.

### Family 2.2.x (the issue's own stream)

**7.5.1 — Find or create the release Epic**

1. Search (not executed):
   ```
   jira.search_jql("project = TC AND issuetype = Epic AND summary ~ 'RHTPA 2.2' AND summary ~ 'Release Tasks' ORDER BY created DESC", fields: ["summary","status"], maxResults: 5)
   ```
2. If an Epic is found (for example "RHTPA 2.2.5 Release Tasks"), reuse it and take
   the version from its summary. No creation is needed.
3. If no Epic is found, the latest released 2.2.x version in the matrix is **2.2.4**,
   so the default is the next patch, **2.2.5**. The engineer must confirm this
   **individually** because the version choice is high-stakes:
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
   - The matrix is 131 days old. A 2.2.5 or later release may already exist, so the
     engineer should check this before accepting the default.
   - On Accept, create the Epic with summary "RHTPA 2.2.5 Release Tasks" and label
     `ai-generated-jira`, then post its description digest comment.

**7.5.2 — Find or create the release Task**

- Search for a Task with `parent = <release-epic-key>` and summary
  `'RHTPA 2.2.5 CVE triage'`.
- If no Task is found, ask for a **separate individual** confirmation:
  ```
  No release Task found under <release-epic-key>.
  Proposed: Create "RHTPA 2.2.5 CVE triage" as child of <release-epic-key>
  Proceed? (Yes / No)
  ```
- On Yes, create the Task with label `ai-generated-jira` and parent
  `<release-epic-key>`, then post its description digest comment.
- Approving the Epic does **not** approve the Task, and the reverse is also true.

**Conditional on the Step 8 decision below:** the 2.2.x release Jira is only needed
if 2.2.x remediation tasks are created (Option 2 below). If the engineer accepts the
recommendation (Option 1, no new 2.2.x tasks), choose **Skip** for 2.2.x. No release
Epic or Task is created, and no release Task is linked.

### Family 2.1.x (outside the issue's scope)

- Every 2.1.x task from this triage would be **preemptive**. These tasks carry the
  `security-preemptive` label, use a Related link, and are never linked to release Jira.
- If a 2.1.x companion CVE Jira exists, this triage creates no 2.1.x tasks at all.
- In both cases this triage does not need 2.1.x release Jira. **Recommendation: Skip
  2.1.x release Jira.** If confirmation were requested anyway, the default would be
  **RHTPA 2.1.2** (the latest 2.1.x release is 2.1.1).
- 2.1.x release Jira is created when PSIRT's 2.1.x CVE Jira is triaged and the
  preemptive tasks are reconciled in Step 4.4.

### 7.5.3 — Cross-CVE dedup decision

- **Decision: dedup SKIPPED, so no stream is marked as dedup'd.**
- Reason: 7.5.3 requires the Upstream Affected Component custom field, and it is not
  configured in Security Configuration.
- The library-summary fallback is not used either. That fallback applies only when the
  field is configured but the Depend link or the field value on the originating CVE is
  missing.
- Result:
  - No existing remediation task is reused.
  - No Depend or Related links to a covering task are proposed.
  - No CVE label is added to an existing task.
  - Step 8 applies the standard task-creation rules to every in-scope stream.
- Note: until that field is configured, separate CVEs against quinn-proto will not be
  deduplicated automatically. Engineers should check the release Task's Blocks links
  by hand.

---

## Step 8 — Remediation decision

Decision path: Step 7 skipped → Step 7.5 dedup skipped → supported versions affected
→ the issue is scoped → another stream (2.1.x) is also affected → **Case A**
(cross-stream) plus **Case B** (in-scope stream).

### Case B — stream 2.2.x (in scope)

The skill's rule is to create remediation tasks when stream-scoped versions are
affected. The lock-file evidence shows that the fix **has already shipped** in the
2.2.x line:

- RHTPA 2.2.3 (backend `v0.4.11`) and 2.2.4 (backend `v0.4.12`) both ship quinn-proto
  0.11.14.
- The Konflux repo `rhtpa-release.0.4.z` already pins `v0.4.12`.

A dependency-bump task on `release/0.4.z` plus a downstream ref update would have
nothing to change. Two options go to the engineer:

- **Option 1 (recommended):** create **no** new 2.2.x remediation tasks.
  - Record in the summary comment that 2.2.0–2.2.2 are affected and the fix is
    available from **RHTPA 2.2.3**. Affected customers should upgrade to 2.2.3 or later.
  - Affects Versions still carries 2.2.0, 2.2.1 and 2.2.2 for VEX and advisory accuracy.
  - Before choosing this option, the engineer must confirm two things this eval could
    not check:
    - the development-stream HEAD ships 0.11.14 or later;
    - `release/0.4.z` HEAD has not regressed.
- **Option 2 (literal Case B):** create the 2.2.x **dependency bump** and **downstream
  propagation** pair (Tasks 3 and 4 below) as verification and tracking tasks. Link
  both to the 2.2.x release Task.

### Case A — stream 2.1.x (outside scope)

1. **Cross-stream impact comment** on TC-8001 (proposed):
   ```
   Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s)
   2.1.x (RHTPA 2.1.0, RHTPA 2.1.1 — quinn-proto 0.11.9) based on lock file analysis.
   These streams are tracked by companion issues (see Related links)
   or may require separate PSIRT triage.

   ---
   <Comment Footnote per shared/comment-footnote.md, skill name: triage-security>
   ```
2. **Check for a 2.1.x sibling CVE Jira.** Reuse the Step 4 JQL and look for the
   suffix `[rhtpa-2.1]`. This search was not executed.
   - If a sibling exists, create **no** 2.1.x tasks. Add a Related link from TC-8001 to
     the sibling, after checking for an existing link first.
   - If no sibling exists, create the two **preemptive** tasks below (Tasks 1 and 2).
3. After the tasks are created, post a task-list comment on TC-8001. The comment comes
   after each task's digest and links.

### Pre-creation checklist

| Check | Result |
|-------|--------|
| Task count per stream | 2.1.x: 2 (Cargo). 2.2.x: 2 under Option 2, 0 under Option 1. |
| Cross-stream coverage | 2.1.x is covered by preemptive tasks or by an existing sibling CVE Jira. |
| Link types | Related: TC-8001 → preemptive tasks. Depend: TC-8001 → its own 2.2.x tasks. Blocks: upstream/bump task → downstream task. |
| Preemptive labels | 2.1.x tasks carry `security-preemptive`. |
| Coordination guidance | Left out. The Source Repositories table has no Deployment Context column. |
| Release Jira linking | Only Option 2 tasks block the 2.2.x release Task. Preemptive tasks are never linked. |
| Dedup consistency | Dedup was skipped, so no stream is dedup'd. |
| Dev-dependency handling | Not applied. There is no evidence of dev/build-only scope. |

---

## Proposed remediation task descriptions

### Task 1 — 2.1.x upstream backport (PREEMPTIVE)

- **Summary:** `Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- **Link:** Related (TC-8001 inward, `<TASK-2.1-UPSTREAM>` outward)

```
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists yet for
> this stream. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panics when a remote peer sends a QUIC frame that
creates an excessive number of streams (denial of service, CVSS 7.5).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (quinn-proto 0.11.9), RHTPA 2.1.1 (quinn-proto 0.11.9)
Source commit(s): backend v0.3.8 (2.1.0), backend v0.3.12 (2.1.1)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: not determined during triage (Cargo.lock graph not inspected).
  Run `cargo tree -i quinn-proto` to see whether it is direct or transitive, and
  record the chain in the PR.
- If the vulnerable dependency is dev-only or build-only, the remediation priority is
  Normal regardless of CVE severity. Add `dev-dependency` label to the task.

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (e.g. quinn or an HTTP/3 client)
- Bump the direct dependency to a version whose transitive closure
  includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes to the
  direct dependency

**Fallback: pin the transitive dependency directly**
- Cargo: `cargo update -p quinn-proto --precise 0.11.14` (0.11.x is semver-compatible),
  or `cargo add quinn-proto@0.11.14` to override the transitive resolution
- Document why the direct dep bump was not viable in the PR description

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14 in Cargo.lock on release/0.3.z
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8001 (originating CVE Jira, stream 2.2.x — preemptive)
```

### Task 2 — 2.1.x downstream propagation (PREEMPTIVE)

- **Summary:** `Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- **Links:**
  - Related (TC-8001 inward, `<TASK-2.1-DOWNSTREAM>` outward)
  - Blocks (`<TASK-2.1-UPSTREAM>` inward, `<TASK-2.1-DOWNSTREAM>` outward)

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists yet for
> this stream. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from <TASK-2.1-UPSTREAM>.

The upstream backport (<TASK-2.1-UPSTREAM>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: backend is pinned in `artifacts.lock.yaml` (download URL
  contains the tag, currently `v0.3.12`)
- **Dependency type**: carried forward from <TASK-2.1-UPSTREAM>
- Update the rhtpa-backend reference to the merged commit or new release tag
  (e.g. a new v0.3.x tag cut from release/0.3.z)
- If the upstream fix pinned a transitive dependency directly (fallback
  approach), verify the pinning is reflected in the downstream build's
  lock file after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix (quinn-proto >= 0.11.14)
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <TASK-2.1-UPSTREAM> (upstream backport must merge first)
- Related to: TC-8001 (originating CVE Jira, stream 2.2.x — preemptive)
```

### Task 3 — 2.2.x dependency bump (only if Option 2 is chosen)

- **Summary:** `Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`
- **Links:**
  - Depend (TC-8001 inward, `<TASK-2.2-BUMP>` outward)
  - Blocks (`<TASK-2.2-BUMP>` inward, `<RELEASE-TASK-2.2.5>` outward)

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream —
a package manager update is sufficient.

Affected versions: RHTPA 2.2.0 (0.11.9), RHTPA 2.2.1 (0.11.12), RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): backend v0.4.5, v0.4.8
Already fixed in: backend v0.4.11 / v0.4.12 (quinn-proto 0.11.14; shipped in RHTPA 2.2.3 / 2.2.4)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: not determined during triage — confirm with `cargo tree -i quinn-proto`
- **Remediation action**: verify release/0.4.z HEAD Cargo.lock has quinn-proto >= 0.11.14
  (expected, since v0.4.11 already does). Only if HEAD regressed, run
  `cargo update -p quinn-proto`; if the result is still < 0.11.14, pin explicitly with
  `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14 on release/0.4.z
- [ ] Lock file updated via package manager (not manual edit), if any change is required
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

### Task 4 — 2.2.x downstream propagation (only if Option 2 is chosen)

- **Summary:** `Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`
- **Links:**
  - Depend (TC-8001 inward, `<TASK-2.2-DOWNSTREAM>` outward)
  - Blocks (`<TASK-2.2-BUMP>` inward, `<TASK-2.2-DOWNSTREAM>` outward)
  - Blocks (`<TASK-2.2-DOWNSTREAM>` inward, `<RELEASE-TASK-2.2.5>` outward)

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <TASK-2.2-BUMP>.

The dependency bump (<TASK-2.2-BUMP>) ensures quinn-proto 0.11.14 on release/0.4.z.
The current pin (v0.4.12, RHTPA 2.2.4) already ships 0.11.14; confirm the next build
keeps a reference at or after v0.4.11.

## Implementation Notes

- Source pinning method: backend is pinned in `artifacts.lock.yaml` (download URL
  contains the tag, currently `v0.4.12`)
- **Dependency type**: carried forward from <TASK-2.2-BUMP>
- Update the rhtpa-backend reference only if <TASK-2.2-BUMP> produced a new commit/tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference includes the fix (quinn-proto >= 0.11.14)
- [ ] Konflux rebuild triggers new container image (if the reference changed)

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <TASK-2.2-BUMP> (dependency bump must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

## Order of operations after confirmation (proposed, not executed)

For each task:

1. `create_issue`.
2. Post the description digest comment (`[sdlc-workflow] Description digest: <tagged-digest>`)
   per `shared/description-digest-protocol.md`, **before** any link or other comment.
3. Create links: Related or Depend to TC-8001, upstream → downstream Blocks, and
   (Option 2 only) remediation → release Task Blocks.
4. Option 2 only: add a Related link with the release Task inward and TC-8001 outward.

Then, on TC-8001:

- No In Progress transition is needed. The `ASSIGNED` status from Step 0.8 is already
  in the indeterminate category.
- Post the task-list comment.
- Add the label `ai-cve-triaged`.
- Post the post-triage summary comment. It contains:
  - the impact table;
  - the Affects Versions correction (2.0.0 → 2.2.0/2.2.1/2.2.2);
  - the outcome: fixed in 2.2.3, plus 2.1.x preemptive tasks;
  - task keys;
  - release Jira references, or "skipped";
  - "dedup skipped — Upstream Affected Component field not configured";
  - a mandatory @mention of the issue reporter;
  - the Comment Footnote.
