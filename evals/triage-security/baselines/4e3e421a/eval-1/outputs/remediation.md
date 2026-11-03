# TC-8001 — Remediation Proposal (Steps 4–8)

> Everything below is a **proposal awaiting engineer confirmation**. No Jira issue,
> link, label, comment, field edit, or transition has been created or performed.
> Jira keys for new issues are shown as placeholders (`<upstream-2.2-key>` etc.)
> because none exist.

## Steps 4–7 inputs to remediation (summary)

| Step | Outcome in this eval |
|------|----------------------|
| 4 – Siblings / duplicates | Needs `search_jql("project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8001")`. No sibling data was supplied, so **no same-stream duplicate is known** and no 2.1.x companion issue is known. This result decides the Case A handling below. |
| 4.3 – Cross-CVE overlap | **Skipped.** The Upstream Affected Component, PS Component, and Stream fields are not configured. |
| 4.4 – Preemptive reconciliation | Needs `search_jql("project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812'")`. No data, so no existing preemptive task for `(rhtpa-2.2)` is known and creation proceeds. |
| 5 – Lifecycle | The Product pages URL was not fetched. 2.2.0–2.2.2 and 2.1.0–2.1.1 are **assumed supported pending verification**. If any are EOL, they are dropped from Affects Versions and from the task scope. |
| 6 – Already fixed | No resolved siblings are known, so remediation proceeds. |
| 7 – Concurrent triage | **Skipped.** The Upstream Affected Component field is not configured. |

## Step 7.5 — Release Jira Orchestration (before remediation)

Scope: release Jira applies to **non-preemptive** remediation only. TC-8001's standard remediation is in the **2.2.x** family, so orchestration runs for that family. Proposed preemptive tasks for 2.1.x are *not* linked to a release Task.

### 7.5.1 – Release Epic (individual confirmation required)

1. Stream `2.2.x` maps to release family **RHTPA 2.2**.
2. Proposed search:
   `project = TC AND issuetype = Epic AND summary ~ 'RHTPA 2.2' AND summary ~ 'Release Tasks' ORDER BY created DESC`
3. **No release evidence is available in this eval**, so I cannot tell whether an Epic exists. A missing result here does **not** prove that no Epic exists.
   - If the search finds an Epic, for example "RHTPA 2.2.x Release Tasks", reuse it and take the version from its summary.
   - If none exists, the default version is the next patch after the latest released 2.2.x version in the matrix (2.2.4), which gives **2.2.5**. Because the matrix is 128 days stale, a newer 2.2.x release may already exist, so the engineer should check the version carefully.
4. Confirmation prompt shown to the engineer, with the exact version needing an explicit decision:
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
5. After acceptance only, run `jira.create_issue(projectKey: "TC", issueTypeName: "Epic", summary: "RHTPA <confirmed-version> Release Tasks", labels: ["ai-generated-jira"])`, then post a description digest comment.

**Status: PENDING.** No Epic has been created or confirmed.

### 7.5.2 – Release Task (separate, individual confirmation)

1. Proposed search:
   `project = TC AND issuetype = Task AND parent = <release-epic-key> AND summary ~ 'RHTPA <version> CVE triage'`
2. If none exists, ask separately. Approving the Epic does not approve the Task:
   ```
   No release Task found under <release-epic-key>.

   Proposed: Create "RHTPA <confirmed-version> CVE triage" as child of <release-epic-key>

   Proceed? (Yes / No)
   ```
3. After "Yes" only, create it with `jira.create_issue(projectKey: "TC", issueTypeName: "Task", summary: "RHTPA <confirmed-version> CVE triage", labels: ["ai-generated-jira"], parent: <release-epic-key>)` and post a digest comment.

**Status: PENDING.** No release Task exists from this run. If the engineer skips either step, Step 8 still creates the remediation tasks, but they are not linked to a release Task.

### 7.5.3 – Cross-CVE dedup decision

**Dedup is SKIPPED.** Its prerequisite, the Upstream Affected Component custom field, is **not configured** in Security Configuration. That means:
- No traversal of the release Task's Blocks links runs, and no originating-CVE component comparison happens.
- The library-summary fallback is **not** used either. That fallback only covers a missing Depend link or missing component value on an originating CVE when the field *is* configured. It does not replace an unconfigured field.

For reference, with the field configured the procedure would: read the release Task's inward Blocks links (the remediation Tasks), follow each Task's Depend links to its originating CVE, and compare that CVE's Upstream Affected Component with TC-8001's. It falls back to matching "quinn-proto" in the Task summary only when the Depend link or component value is missing, never when the component is present but different. On a match it would create no new task and would instead propose: a Depend link (TC-8001 to the covering Task), a Related link (release Task to TC-8001), and adding the `CVE-2026-31812` label to the covering Task while keeping its existing labels.

**Result: no stream is marked dedup'd, so Step 8 creates standard tasks for 2.2.x.**

## Step 8 — Decision

```
Version impact → Step 7 (skipped) → Step 7.5 (release pending, dedup skipped)
  → supported versions affected? YES (2.2.0, 2.2.1, 2.2.2; also 2.1.0, 2.1.1)
  → issue scoped? YES ([rhtpa-2.2] → 2.2.x)
  → other streams affected? YES (2.1.x) → Case A (cross-stream) + Case B (2.2.x)
  → ecosystem Cargo = source dependency → 2 tasks per stream
```

Upstream fix status (Step 2.5) is **unverified**, so the tasks below use the **upstream backport** template. If the engineer confirms that `release/0.4.z` HEAD already ships quinn-proto >= 0.11.14 (likely, since `v0.4.11` and `v0.4.12` ship 0.11.14), task 1 switches to the **dependency bump** variant: summary "Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)", with a `cargo update -p quinn-proto` action. In that case the downstream task only needs to point the release repo at a fixed tag such as `v0.4.11` or later. The task count and the Blocks link stay the same.

Coordination Guidance is omitted because the Source Repositories table has no Deployment Context column. The `dev-dependency` label is not used because there is no evidence of dev-only or build-only scope.

---

### Case B — Task 1 of 2 (2.2.x): Upstream backport

- **Summary:** Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)
- **Issue type:** Task, project TC
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (remote DoS via
an excessive number of streams in a QUIC STREAMS frame).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (quinn-proto 0.11.9), RHTPA 2.2.1 (0.11.12),
RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): backend v0.4.5 (2.2.0), v0.4.8 (2.2.1, 2.2.2)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: to be confirmed. Direct vs transitive could not be
  determined from the available evidence (see Step 2.3.5); verify in Cargo.toml / Cargo.lock.
- If the vulnerable dependency is dev-only or build-only, the remediation
  priority is Normal regardless of CVE severity. Add `dev-dependency` label.
- Note: backend tags v0.4.11 and v0.4.12 already ship quinn-proto 0.11.14. Check
  release/0.4.z HEAD first; if already >= 0.11.14, no code change is needed and
  this task reduces to confirming the fixed commit/tag for downstream propagation.

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (e.g. quinn)
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

### Case B — Task 2 of 2 (2.2.x): Downstream propagation (blocked by Task 1)

- **Summary:** Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
- **Issue type:** Task, project TC
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <upstream-2.2-key>.

The upstream backport (<upstream-2.2-key>) bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: backend via `artifacts.lock.yaml` (download URL contains
  tag, e.g., `v0.4.12`)
- **Dependency type**: carried forward from upstream task (to be confirmed)
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

- Depends on: <upstream-2.2-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Case B — proposed creation and linkage order (2.2.x)

1. Create Task 1, then post its description digest comment (`[sdlc-workflow] Description digest: sha256-md:<hex>`) before any link or other comment.
2. Create Task 2, then post its description digest comment.
3. Link Depend: TC-8001 (inward) to `<upstream-2.2-key>` (outward).
4. Link Depend: TC-8001 to `<downstream-2.2-key>`.
5. Link **Blocks**: `<upstream-2.2-key>` (inward) to `<downstream-2.2-key>` (outward), so the downstream task is blocked by the upstream one.
6. *Only if Step 7.5 produced a confirmed release Task:* link Blocks from `<upstream-2.2-key>` and from `<downstream-2.2-key>` to `<release-task-key>`, and link Related from `<release-task-key>` (inward) to TC-8001 (outward).
7. Transition TC-8001 to In Progress. Discover the transition dynamically. It is still a proposal.
8. Comment on TC-8001, with footnote: "Remediation tasks created: `<upstream-2.2-key>` (upstream backport), `<downstream-2.2-key>` (downstream propagation, blocked by `<upstream-2.2-key>`)".

---

## Case A — Cross-stream impact (2.1.x)

### Proposed cross-stream comment on TC-8001 (with Comment Footnote)

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x
(RHTPA 2.1.0 and 2.1.1 ship quinn-proto 0.11.9 at backend v0.3.8 / v0.3.12)
based on lock file analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

<Comment Footnote, skill name: triage-security>
```

### Preemptive tasks: conditional on the Step 4 sibling search

- **If a 2.1.x sibling CVE Jira for CVE-2026-31812 exists** (for example `[rhtpa-2.1]`), skip task creation. That stream is triaged through its own issue, and Step 4.2 proposes a Related link.
- **If no 2.1.x sibling exists**, propose the two preemptive tasks below. Both carry `security-preemptive`, are linked **Related** (not Depend) to TC-8001, and are not linked to the 2.2 release Task.

#### Preemptive Task 1 (2.1.x): Upstream backport

- **Summary:** Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

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

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (remote DoS).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (quinn-proto 0.11.9), RHTPA 2.1.1 (0.11.9)
Source commit(s): backend v0.3.8 (2.1.0), v0.3.12 (2.1.1)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: to be confirmed (direct vs transitive not determinable from
  available evidence)
- If dev-only or build-only, priority is Normal and the `dev-dependency` label applies.

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess a code-level workaround

### Remediation approach (transitive dependency)

**Preferred:** bump the direct dependency that pulls in quinn-proto to a version
whose closure includes quinn-proto >= 0.11.14.
**Fallback:** `cargo add quinn-proto@0.11.14`; document why in the PR.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (originating tracking issue, linked Related)
```

#### Preemptive Task 2 (2.1.x): Downstream propagation (blocked by Preemptive Task 1)

- **Summary:** Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

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
CVE-2026-31812 fix from <upstream-2.1-key>.

The upstream backport (<upstream-2.1-key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: backend via `artifacts.lock.yaml` (download URL contains
  tag, e.g., `v0.3.12`)
- **Dependency type**: carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the fallback pin was used upstream, verify it is reflected in the downstream lock file
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-2.1-key> (upstream backport must merge first)
- Depends on: TC-8001 (originating tracking issue, linked Related)
```

Proposed preemptive linkage: create each task, then post its digest comment. Then link Related: TC-8001 to `<upstream-2.1-key>`, Related: TC-8001 to `<downstream-2.1-key>`, and Blocks: `<upstream-2.1-key>` to `<downstream-2.1-key>`. Finally, comment on TC-8001 (with footnote) listing the preemptive tasks and explaining that Step 4.4 reconciliation will relink them when PSIRT creates a `[rhtpa-2.1]` CVE Jira.

---

## Pre-creation checklist

- [x] Task count per stream: Cargo is a source dependency, so 2 tasks for 2.2.x and 2 preemptive tasks for 2.1.x.
- [x] Cross-stream coverage: 2.1.x has either preemptive tasks or an existing sibling CVE Jira (decided by the Step 4 search).
- [x] Link types: Depend for TC-8001 and its 2.2.x tasks, Related for TC-8001 and its 2.1.x preemptive tasks, Blocks from upstream to downstream within each stream.
- [x] Preemptive labels: `security-preemptive` on both 2.1.x tasks.
- [x] Coordination guidance: omitted, because there is no Deployment Context column (backward compatibility).
- [ ] Release Jira linking: **pending.** It applies only after the release Epic and Task are confirmed in Step 7.5.
- [x] Dedup consistency: dedup was skipped (field not configured), and no stream is marked dedup'd.

## Post-triage summary (proposed, after all confirmed actions)

- Add the label `ai-cve-triaged` to TC-8001.
- Post a summary comment on TC-8001 containing: the version impact table, the Affects Versions correction (`[RHTPA 2.0.0]` to `[RHTPA 2.2.0, 2.2.1, 2.2.2]`), the outcome (remediation proposed), links to the remediation tasks, release Epic and Task references (or "pending/skipped"), dedup result ("skipped — Upstream Affected Component field not configured"), a mandatory ADF @mention of the issue reporter (account ID taken from the Step 1 `get_issue` response; not present in the mock), and the Comment Footnote.

**Nothing in this document has been executed in Jira. Every item above waits for explicit engineer confirmation.**
