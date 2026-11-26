# TC-8001 — Remediation (Steps 7, 7.5, 8)

> **Simulation notice:** Nothing in this file has been executed. No Jira search, issue
> creation, link, label, comment, or transition has been performed. Every item is a
> proposal awaiting explicit engineer confirmation. Task keys are placeholders
> (`<...-key>`), never invented Jira keys.

## Step 7 — Concurrent Triage Detection

**Skipped.** The Upstream Affected Component custom field is not configured in Security
Configuration, so the concurrent-triage JQL cannot be built. The skill proceeds to Step 7.5.

---

## Step 7.5 — Release Jira Orchestration

Release orchestration applies to **non-preemptive** remediation only. Here that means
stream **2.2.x**, which is TC-8001's own scope. Any 2.1.x tasks would be preemptive
(Case A below) and are not linked to release Jira.

### 7.5.1 — Stream-to-version mapping and release Epic (confirmation 1 of 2)

- Stream `2.2.x` (from `[rhtpa-2.2]`) maps to release family **RHTPA 2.2**.
- Proposed search (not executed):
  ```
  jira.search_jql("project = TC AND issuetype = Epic AND summary ~ 'RHTPA 2.2' AND summary ~ 'Release Tasks' ORDER BY created DESC", maxResults: 5)
  ```
- **If an Epic is found** (e.g., `RHTPA 2.2.x Release Tasks`), take its version from the summary and reuse it. No confirmation is needed.
- **If no Epic is found**, the default is the next patch bump after the latest released
  version in the 2.2.x matrix: **2.2.4 → 2.2.5**. This needs **individual engineer
  confirmation**, because the version decision is high-stakes:
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
  On Accept, the proposed call is
  `jira.create_issue(projectKey: "TC", issueTypeName: "Epic", summary: "RHTPA 2.2.5 Release Tasks", labels: ["ai-generated-jira"], security: <TC-8001 security level>)`,
  followed by a description digest comment.

### 7.5.2 — Release Task (confirmation 2 of 2)

- Proposed search (not executed):
  `project = TC AND issuetype = Task AND parent = <release-epic-key> AND summary ~ 'RHTPA 2.2.5 CVE triage'`
- **If none exists**, this needs **separate individual confirmation**. Approving the Epic does not authorize the Task:
  ```
  No release Task found under <release-epic-key>.

  Proposed: Create "RHTPA 2.2.5 CVE triage" as child of <release-epic-key>

  Proceed? (Yes / No)
  ```
  On Yes: `jira.create_issue(issueTypeName: "Task", summary: "RHTPA 2.2.5 CVE triage", parent: <release-epic-key>, labels: ["ai-generated-jira"], security: <TC-8001 security level>)`, then a digest comment.
- If the engineer skips either one, Step 8 still creates the remediation tasks but does not link them to a release Task.

### 7.5.3 — Cross-CVE dedup decision

**Decision: dedup is skipped. No existing coverage is assumed, and new remediation tasks are created.**

The prerequisite is not met: the **Upstream Affected Component custom field is not
configured**. The skill therefore cannot resolve the component on the CVEs linked to
the release Task, so it skips dedup and proceeds to standard Step 8 creation. The
library-summary fallback is only used inside the dedup procedure when the field exists
but a linked CVE lacks it, so it is not used here. No stream is marked as dedup'd.

---

## Step 8 — Decision

| Question | Answer |
|----------|--------|
| Any supported versions affected? | Yes: 2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2 |
| Issue scoped? | Yes, to **2.2.x** |
| Other streams affected? | Yes, **2.1.x**, so **Case A** (cross-stream comment, plus preemptive tasks if 2.1.x has no CVE Jira) |
| In-scope stream affected? | Yes, so **Case B** for 2.2.x |
| Ecosystem | Cargo (source dependency), so **2 tasks per stream** |
| 2.2.x upstream fix | Available on `release/0.4.z` (tags `v0.4.11`/`v0.4.12` ship 0.11.14), so **dependency bump + downstream propagation** |
| 2.1.x upstream fix | Not available (latest `v0.3.12` ships 0.11.9), so **upstream backport + downstream propagation** |
| Dev-only dependency? | No evidence; treated as production. No `dev-dependency` label, priority not overridden |
| Coordination Guidance | **Omitted:** the Source Repositories table has no Deployment Context column (backward-compatibility rule) |
| Security level | Every created task copies TC-8001's security level (`{id, name}` read live). The mock data does not supply it |

> **Engineer attention for 2.2.x:** RHTPA 2.2.3 and 2.2.4 **already ship quinn-proto
> 0.11.14**, and the 2.2.x Konflux repo already pins backend `v0.4.12`. The 2.2.x task
> pair below therefore mainly verifies and records the fix for the 2.2.5 release; little
> or no code change is expected. The engineer may decide at the confirmation gate that
> these tasks are unnecessary and instead record "fixed in RHTPA 2.2.3" in the summary.
> The real code work is in **2.1.x**.

---

## Case A — Cross-stream impact (2.1.x)

### A.1 Cross-stream impact comment on TC-8001 (proposed, not posted)

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x
(RHTPA 2.1.0, RHTPA 2.1.1 — quinn-proto 0.11.9 at backend v0.3.8 / v0.3.12)
based on lock file analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

----
This comment was AI-generated by sdlc-workflow/triage-security v0.14.0.
```

### A.2 Sibling check

Reuse the Step 4 JQL and look for a `CVE-2026-31812` Vulnerability with a `[rhtpa-2.1]` suffix. **Not executed.**
- **If a 2.1.x CVE Jira exists**, skip 2.1.x task creation. That stream is triaged through its own issue.
- **If none exists**, create the two **preemptive** tasks P1 and P2 below.

---

## Case B — Remediation tasks for stream 2.2.x (in scope)

### Task B1 — Dependency bump (2.2.x)

- **Summary:** `Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`
- **Security:** TC-8001's security level

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream —
a package manager update is sufficient.

Affected versions: RHTPA 2.2.0 (quinn-proto 0.11.9), RHTPA 2.2.1 (0.11.12),
RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): backend v0.4.5, v0.4.8 (from supportability matrix)

Note: tags v0.4.11 (RHTPA 2.2.3) and v0.4.12 (RHTPA 2.2.4) already ship
quinn-proto 0.11.14. Verify release/0.4.z HEAD still resolves >= 0.11.14.

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: to be confirmed (direct | transitive — chain not verified
  during triage; see Step 2.3.5)
- **Remediation action**: run the appropriate package manager update command:
  - **Cargo**: `cargo update -p quinn-proto` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- If transitive: prefer bumping the direct dependency (e.g., quinn) whose
  closure includes quinn-proto >= 0.11.14; fall back to pinning quinn-proto
- Verify the lock file (Cargo.lock) reflects >= 0.11.14 after the update
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

### Task B2 — Downstream propagation (2.2.x), blocked by B1

- **Summary:** `Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`
- **Security:** TC-8001's security level

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <B1-key>.

The dependency bump (<B1-key>) bumps quinn-proto to 0.11.14 on release/0.4.z.
Once that PR merges, update the source pinning in this Konflux release repo
so the next build ships the fix.

## Implementation Notes

- Source pinning method: backend — artifacts.lock.yaml (download URL contains
  tag, e.g., v0.4.12)
- **Dependency type**: to be confirmed — carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- The current pin (v0.4.12, RHTPA 2.2.4) already ships quinn-proto 0.11.14;
  confirm the reference for the next release (2.2.5) is >= v0.4.11
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

- Depends on: <B1-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

## Case A preemptive tasks — stream 2.1.x (only if no 2.1.x CVE Jira exists)

### Task P1 — Upstream backport (2.1.x, preemptive)

- **Summary:** `Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- **Security:** TC-8001's security level

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

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (remote DoS
via crafted STREAMS frame).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (quinn-proto 0.11.9), RHTPA 2.1.1 (0.11.9)
Source commit(s): backend v0.3.8, v0.3.12 (from supportability matrix)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: to be confirmed (direct | transitive — chain not verified
  during triage; see Step 2.3.5)
- If the vulnerable dependency is dev-only or build-only (identified
  in Step 2.3.5), the remediation priority is Normal regardless of CVE
  severity. Add `dev-dependency` label to the task.

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (e.g., quinn)
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

- Depends on: TC-8001 (originating CVE, stream 2.2.x — Related link)
```

### Task P2 — Downstream propagation (2.1.x, preemptive), blocked by P1

- **Summary:** `Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- **Security:** TC-8001's security level

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
CVE-2026-31812 fix from <P1-key>.

The upstream backport (<P1-key>) bumps quinn-proto to 0.11.14 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release repo
so the next build ships the fix.

## Implementation Notes

- Source pinning method: backend — artifacts.lock.yaml (download URL contains
  tag, e.g., v0.3.12)
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

- Depends on: <P1-key> (upstream backport must merge first)
- Depends on: TC-8001 (originating CVE, stream 2.2.x — Related link)
```

---

## Proposed creation and linkage order (all pending confirmation)

For each task: create it, post the description digest comment
(`[sdlc-workflow] Description digest: <tagged-digest>`), and only then create links.

| # | Action | Link type / direction |
|---|--------|-----------------------|
| 1 | Create B1, post digest | — |
| 2 | Create B2, post digest | — |
| 3 | TC-8001 → B1 | Depend (TC-8001 inward, B1 outward) |
| 4 | TC-8001 → B2 | Depend |
| 5 | B1 → B2 | Blocks (B1 blocks B2) |
| 6 | B1 → release Task (RHTPA 2.2.5 CVE triage) | Blocks (remediation inward, release Task outward) |
| 7 | B2 → release Task | Blocks |
| 8 | release Task → TC-8001 | Related (release Task inward, CVE outward) |
| 9 | *(if no 2.1.x CVE Jira)* Create P1 and P2, post digests | — |
| 10 | TC-8001 → P1, TC-8001 → P2 | Related (preemptive, not Depend) |
| 11 | P1 → P2 | Blocks |
| 12 | P1/P2 → release Jira | **None.** Preemptive tasks are not linked to release Jira |
| 13 | Transition TC-8001 to In Progress | Skipped: it will already be `ASSIGNED` (indeterminate category) from Step 0.8 |
| 14 | Comment on TC-8001 | "Remediation tasks created: <B1-key> (dependency bump), <B2-key> (downstream propagation, blocked by <B1-key>)" plus the Case A preemptive list (`2.1.x: <P1-key>, <P2-key> (security-preemptive)`) with the reconciliation note, and the Comment Footnote |

## Pre-creation checklist

- [x] Task count per stream: Cargo, so 2 tasks for 2.2.x (B1+B2) and 2 for 2.1.x (P1+P2)
- [x] Cross-stream coverage: 2.1.x is covered by a sibling CVE Jira or by preemptive P1/P2
- [x] Link types: Depend (own CVE), Related (preemptive), Blocks (upstream → downstream, remediation → release Task)
- [x] Preemptive labels: P1/P2 carry `security-preemptive`
- [x] Coordination guidance: intentionally omitted because the Deployment Context column is absent
- [x] Release Jira linking: B1/B2 are linked to the RHTPA 2.2.5 release Task (Blocks), and TC-8001 is linked to it (Related)
- [x] Dedup consistency: no stream dedup'd (7.5.3 skipped)

## Post-Triage Summary (proposed, after confirmation)

1. Add the label `ai-cve-triaged` to TC-8001.
2. Post a summary comment containing the version impact table, the Affects Versions
   correction (RHTPA 2.0.0 → 2.2.0/2.2.1/2.2.2), the outcome (remediation created), task
   keys, release Epic/Task keys, the dedup result ("skipped: Upstream Affected Component
   field not configured"), a note that RHTPA 2.2.3+ already ships the fix, a **mandatory
   ADF @mention of TC-8001's reporter** (account ID from the Step 1 issue data, not
   supplied in the mock), and the Comment Footnote
   (`This comment was AI-generated by sdlc-workflow/triage-security v0.14.0.`).

**Reminder:** none of the operations above were performed. They are proposals for
engineer confirmation.
