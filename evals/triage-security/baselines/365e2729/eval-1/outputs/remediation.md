# TC-8001 — Remediation (Steps 4–8)

> **Eval simulation.** No Jira operation of any kind was performed: no search, create,
> link, edit, transition, or comment. Every item below is a **proposal** that would go to
> the engineer for explicit confirmation before execution. Issue keys for new
> issues are shown as placeholders (`<...-key>`) because no issues exist.

## Prerequisite steps (summary)

| Step | Outcome in this simulation |
|---|---|
| 4 / 4.1 / 4.2 — Sibling search | Would run `project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8001`. **Not executed**, so no sibling data exists. A same-stream (`[rhtpa-2.2]`) open sibling would mean closing TC-8001 as Duplicate. A `[rhtpa-2.1]` sibling would be a companion tracker: create a Related link (idempotent) and do not create preemptive 2.1.x tasks. The proposals below assume **no siblings were found**. |
| 4.3 — Cross-CVE overlap | **Skipped.** The Upstream Affected Component, PS Component, and Stream custom fields are not configured. |
| 4.4 — Preemptive reconciliation | Would search `labels = 'security-preemptive' AND labels = 'CVE-2026-31812'` filtered to `rhtpa-2.2`. Not executed. The proposals assume no match. |
| 5 — Lifecycle | Would fetch `https://access.example.com/product-life-cycle/rhtpa`. Not executed. The proposals assume 2.1.x and 2.2.x are supported, pending that check. |
| 6 — Already fixed | No resolved siblings are known, so the step proceeds. Note that the stream's own later releases (2.2.3 and 2.2.4) already ship 0.11.14. See the decision point under Case B. |
| 7 — Concurrent triage | **Skipped.** The Upstream Affected Component field is not configured. |

---

## Step 7.5 — Release Jira Orchestration (explained before remediation)

Release Jira is scoped per release family. Only **non-preemptive** remediation tasks are linked to it. TC-8001 produces non-preemptive tasks only for the **2.2.x** family, because it is scoped to `[rhtpa-2.2]`. The 2.1.x tasks are preemptive (Case A) and are **not** linked to release Jira, so no 2.1.x release Epic or Task is needed for this triage.

### 7.5.1 — Stream to version mapping and release Epic (2.2.x)

1. Search that would run (not executed):
   `project = TC AND issuetype = Epic AND summary ~ 'RHTPA 2.2' AND summary ~ 'Release Tasks' ORDER BY created DESC`
2. **If an Epic exists** (for example "RHTPA 2.2.x Release Tasks"), reuse it and take the version from its summary.
3. **If no Epic exists**, propose a default version equal to the next patch after the latest released 2.2.x version in the supportability matrix. The latest is **2.2.4**, so the proposal is **2.2.5**. **Individual confirmation is required** because the version decision is high-stakes:

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

   The matrix is 151 days stale. The engineer should check that 2.2.4 really is the latest release before accepting 2.2.5.
4. On acceptance, the step would create Epic `RHTPA 2.2.5 Release Tasks` with labels `ai-generated-jira` and TC-8001's security level, then post a description digest comment. **Not performed.**

### 7.5.2 — Release Task (2.2.x)

1. Search (not executed): `project = TC AND issuetype = Task AND parent = <release-epic-key> AND summary ~ 'RHTPA 2.2.5 CVE triage'`
2. If no Task exists, ask for a **separate individual confirmation**:
   ```
   No release Task found under <release-epic-key>.
   Proposed: Create "RHTPA 2.2.5 CVE triage" as child of <release-epic-key>
   Proceed? (Yes / No)
   ```
3. On "Yes", the step would create Task `RHTPA 2.2.5 CVE triage` (parent `<release-epic-key>`, labels `ai-generated-jira`, TC-8001's security level), then post a digest comment. **Not performed.**
4. If the engineer **skips**, the 2.2.x remediation tasks are still created, just without release links.

### 7.5.3 — Cross-CVE dedup decision

**Decision: dedup is skipped, and new remediation tasks will be proposed.**

Dedup works by matching the **Upstream Affected Component** custom field on CVEs Depend-linked to remediation tasks that Block the release Task. That field is **not configured** in Security Configuration. The prerequisite therefore fails, and the protocol says: "If not configured, skip dedup and proceed to Step 8." The library-summary fallback is used only when the field is configured but missing on a particular CVE. It is not a substitute for an unconfigured field, so it does not apply here. No stream is marked as dedup'd. Step 8 Case B creates tasks for 2.2.x.

---

## Step 8 — Remediation decision

- Supported versions are affected, so this is not Case C.
- The issue is **scoped** to 2.2.x, and **2.1.x is also affected**, so **Case A** (cross-stream comment plus preemptive tasks for 2.1.x) applies, followed by **Case B** for 2.2.x.
- The ecosystem is Cargo, a source dependency, so each stream gets **2 tasks**.
  - 2.2.x: the fix is available on `release/0.4.z`, so use the **dependency bump** task plus downstream propagation.
  - 2.1.x: no known fix on `release/0.3.z`, so use the **upstream backport** task plus downstream propagation.
- Coordination Guidance subsection: **omitted** because the Source Repositories table has no Deployment Context column.
- Dependency type: **not determined** from the available evidence. Both the direct and transitive approaches are included, as the template requires.
- Security level: each creation copies TC-8001's `security` level `{id, name}`, read live from the issue. It is omitted only if TC-8001 has none.

> **Engineer decision point (2.2.x):** releases 2.2.3 (`v0.4.11`) and 2.2.4 (`v0.4.12`)
> already ship quinn-proto 0.11.14. The affected 2.2.0–2.2.2 releases are superseded.
> Tasks 1–2 are therefore expected to amount to *verification* that `release/0.4.z`
> HEAD and the next 2.2.x Konflux pin stay ≥ 0.11.14 / ≥ `v0.4.11`. They remain
> proposed per the Case B rule so that the fix is traceable on the release Task. The
> engineer may decline them and record that 2.2.3+ already contain the fix.

---

### Case A — Cross-stream impact comment on TC-8001 (proposed, NOT posted)

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x
(RHTPA 2.1.0, 2.1.1 ship quinn-proto 0.11.9) based on lock file analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

<Comment Footnote — triage-security>
```

---

### Task 1 — 2.2.x dependency bump (standard, Case B)

- **Summary:** `Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`
- **Security:** TC-8001's level

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream —
a package manager update is sufficient. quinn-proto before 0.11.14 panics when a
remote peer sends a QUIC frame creating an excessive number of streams (DoS, CVSS 7.5).

Affected versions: RHTPA 2.2.0 (quinn-proto 0.11.9), RHTPA 2.2.1 (0.11.12),
RHTPA 2.2.2 (retag of 2.2.1). RHTPA 2.2.3 and 2.2.4 already ship 0.11.14.
Source commit(s): backend v0.4.5, v0.4.8 (from supportability matrix)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: not determined during triage — confirm with `cargo tree -i quinn-proto`
  (direct dependency vs transitive, e.g. via quinn)
- **Remediation action**: run `cargo update -p quinn-proto` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update. Tags v0.4.11/v0.4.12 on this
  branch already resolve 0.11.14, so this may be a verification-only change.
- If the vulnerable dependency is dev-only or build-only, the remediation priority is Normal
  regardless of CVE severity. Add `dev-dependency` label to the task.

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

### Task 2 — 2.2.x downstream propagation (standard, Case B)

- **Summary:** `Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`
- **Security:** TC-8001's level

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <task-1-key>.

The dependency bump (<task-1-key>) bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: not determined — carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
  (must be v0.4.11 or later; 2.2.4 currently pins v0.4.12, which ships 0.11.14)
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

- Depends on: <task-1-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Task 3 — 2.1.x upstream backport (PREEMPTIVE, Case A)

Created only if Step 4 finds no `[rhtpa-2.1]` CVE Jira for CVE-2026-31812.

- **Summary:** `Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- **Security:** TC-8001's level

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

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (DoS, CVSS 7.5).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (quinn-proto 0.11.9), RHTPA 2.1.1 (quinn-proto 0.11.9)
Source commit(s): backend v0.3.8, v0.3.12 (from supportability matrix)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: not determined during triage — confirm with `cargo tree -i quinn-proto`
- If the vulnerable dependency is dev-only or build-only, the remediation priority is Normal
  regardless of CVE severity. Add `dev-dependency` label to the task.

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto
- Bump the direct dependency to a version whose transitive closure
  includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes to the
  direct dependency

**Fallback: pin the transitive dependency directly**
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

### Task 4 — 2.1.x downstream propagation (PREEMPTIVE, Case A)

- **Summary:** `Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- **Security:** TC-8001's level

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
CVE-2026-31812 fix from <task-3-key>.

The upstream backport (<task-3-key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
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

- Depends on: <task-3-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

## Proposed creation order and linkage (NOT performed)

For each task, the order is: create the task, post the description digest comment (`[sdlc-workflow] Description digest: <tagged-digest>`, which must come before any link or comment on that task), then create its links.

| # | Link | Type | Direction |
|---|---|---|---|
| 1 | TC-8001 → Task 1 | Depend | inward TC-8001, outward Task 1 |
| 2 | TC-8001 → Task 2 | Depend | inward TC-8001, outward Task 2 |
| 3 | Task 1 → Task 2 | Blocks | upstream blocks downstream |
| 4 | Task 1 → release Task | Blocks | remediation inward, release Task outward (only if 7.5 is active) |
| 5 | Task 2 → release Task | Blocks | remediation inward, release Task outward (only if 7.5 is active) |
| 6 | release Task → TC-8001 | Related | release Task inward, CVE outward (only if 7.5 is active) |
| 7 | TC-8001 → Task 3 | Related | preemptive, originating CVE inward |
| 8 | TC-8001 → Task 4 | Related | preemptive, originating CVE inward |
| 9 | Task 3 → Task 4 | Blocks | upstream blocks downstream |

Preemptive Tasks 3 and 4 are **not** linked to any release Task.

Other proposed follow-ups (all NOT performed):
- **Transition TC-8001 to In Progress:** skipped. After Step 0.8 the issue would be `ASSIGNED`, which is an indeterminate-category status in the Bugzilla-style workflow.
- **Comment on TC-8001 listing tasks:** "Remediation tasks created: <task-1-key> (dependency bump), <task-2-key> (downstream propagation, blocked by <task-1-key>)", plus the preemptive list: "Preemptive remediation tasks created for streams without CVE Jiras: 2.1.x: <task-3-key>, <task-4-key> (security-preemptive) … Step 4.4 reconciliation will link them and remove the label." Each comment ends with the Comment Footnote.
- **Post-triage:** add the `ai-cve-triaged` label to TC-8001. Post a summary comment covering the impact table, the Affects Versions correction (RHTPA 2.0.0 → 2.2.0/2.2.1/2.2.2), the outcome, task links, release Epic and Task references, and the dedup result (skipped because the field is not configured). Include an ADF @mention of the TC-8001 reporter (account ID taken from the issue; not present in the mock) and the Comment Footnote.

## Pre-creation checklist

- [x] Task count per stream: 2 per stream (Cargo is a source dependency)
- [x] Cross-stream coverage: 2.1.x is covered by preemptive Tasks 3 and 4 (conditional on no sibling)
- [x] Link types: Depend for own CVE, Related for preemptive, Blocks for upstream → downstream
- [x] Preemptive labels: Tasks 3 and 4 carry `security-preemptive`
- [x] Coordination guidance: omitted because there is no Deployment Context column
- [x] Release Jira linking: non-preemptive Tasks 1 and 2 Block the release Task; TC-8001 is Related to it
- [x] Dedup consistency: no stream marked as dedup'd (dedup skipped)
