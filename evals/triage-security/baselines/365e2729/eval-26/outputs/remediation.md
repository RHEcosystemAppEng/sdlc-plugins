# TC-8050 — Step 8: Remediation

## Decision

- Supported 2.2.x versions affected: **YES**. 2.2.0 through 2.2.4 ship criterion 0.5.1, below 0.5.2, as a **dev-only dependency**.
- Issue scope: 2.2.x (scoped). 2.1.x is also affected, so **Case A** (cross-stream comment and possible preemptive tasks) applies, followed by **Case B** for 2.2.x.
- Ecosystem: Cargo (source dependency), so **2 tasks per stream**: upstream backport and downstream propagation. The upstream fix on `release/0.4.z` is not confirmed.
- **Dependency scope override (Step 2.3.5):** criterion is declared in `[dev-dependencies]` in backend/Cargo.toml and is not present in production builds. As a result:
  - Every remediation task gets the **`dev-dependency`** label.
  - Every remediation task has priority **Normal**. The CVE's severity (CVSS 5.3 Medium) and priority are not inherited.
  - Every task description includes the dev-only note.
- This is not Case C. The tasks are still needed because a vulnerable dev dependency is a supply chain risk.
- Release Jira (Step 7.5): find or create "RHTPA <next 2.2.x version> Release Tasks" and "RHTPA <version> CVE triage". That requires Jira lookups and individual confirmation, so it was not executed in the eval. The links are shown as placeholders.

---

## Task 1 — Upstream backport (2.2.x)

**Summary:** Remediate CVE-2026-99001: bump criterion to 0.5.2 (2.2.x)
**Issue type:** Task
**Project:** TC
**Priority:** Normal (overridden; dev-only dependency)
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`
**Security level:** copied from TC-8050 (if set)

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99001: criterion path traversal in benchmark output
(crafted benchmark names containing path separators allow writing benchmark
output files to arbitrary paths). The vulnerable dependency (criterion < 0.5.2)
must be updated to the fixed version (0.5.2+).

This dependency is dev/build-only and is not shipped in production. Remediation
priority is Normal (supply chain risk only).

Affected versions: RHTPA 2.2.0, 2.2.1, 2.2.2 (retag of 2.2.1), 2.2.3, 2.2.4
(all ship criterion 0.5.1 as a dev-dependency)
Source commit(s): v0.4.5, v0.4.8, v0.4.11, v0.4.12

Upstream fix: none provided in remote links
Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (chain: backend (workspace) → criterion)
- **Dependency scope**: dev-only — declared in `[dev-dependencies]` of
  backend/Cargo.toml; used for benchmarks only; NOT present in production builds.
  Remediation priority is Normal regardless of CVE severity; task carries the
  `dev-dependency` label.
- Update criterion to >= 0.5.2 in backend/Cargo.toml `[dev-dependencies]`
  (currently `criterion = "0.5.1"`) and refresh Cargo.lock
  (`cargo update -p criterion`)
- If a direct bump introduces breaking changes in benchmark code, assess whether
  a code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency
- [ ] Benchmarks (`cargo bench --no-run`) still compile

## Dependencies

- Depends on: TC-8050 (parent tracking issue)
```

---

## Task 2 — Downstream propagation (2.2.x)

**Summary:** Propagate CVE-2026-99001 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)
**Issue type:** Task
**Project:** TC
**Priority:** Normal (overridden; dev-only dependency)
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`
**Security level:** copied from TC-8050 (if set)

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99001 fix from {{upstream-task-key}}.

The upstream backport ({{upstream-task-key}}) bumps criterion to 0.5.2 on
release/0.4.z. Once that PR merges, update the source pinning in this Konflux
release repo so the next build carries the fix.

This dependency is dev/build-only and is not shipped in production. Remediation
priority is Normal (supply chain risk only).

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag,
  e.g., v0.4.12)
- **Dependency type**: direct — carried forward from upstream task
- **Dependency scope**: dev-only (`[dev-dependencies]`); the shipped container
  image does not contain criterion — this propagation keeps the source
  reference aligned for supply chain hygiene
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: {{upstream-task-key}} (upstream backport must merge first)
- Depends on: TC-8050 (parent tracking issue)
```

---

## Proposed linkage (requires confirmation)

1. Post a description digest comment on each task right after creating it, before any links.
2. TC-8050 → Task 1 (Depend). TC-8050 → Task 2 (Depend).
3. Task 1 → Task 2 (Blocks).
4. Task 1 and Task 2 → RHTPA 2.2.x release Task (Blocks). TC-8050 ↔ release Task (Related), if Step 7.5 is active.
5. Transition TC-8050 to In Progress if it is not already there, and assign it to the current user.
6. Post this comment on TC-8050: "Remediation tasks created: {{upstream-task-key}} (upstream backport), {{downstream-task-key}} (downstream propagation, blocked by {{upstream-task-key}}). Both carry the `dev-dependency` label with Normal priority: criterion is a dev-only dependency and is not shipped in production." Include the Comment Footnote.

## Case A — Cross-stream (2.1.x)

Proposed comment on TC-8050, with Comment Footnote:

> Cross-stream impact: criterion < 0.5.2 also affects stream(s) 2.1.x based on lock file analysis (2.1.0 and 2.1.1 ship criterion 0.5.1 as a dev-dependency only, not shipped in production). These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.

If Step 4 finds no 2.1.x CVE Jira for CVE-2026-99001, create the preemptive pair below. Each task is linked to TC-8050 with **Related**, not Depend.

- **Remediate CVE-2026-99001: bump criterion to 0.5.2 (2.1.x)**
  - Repository: backend. Target branch: `release/0.3.z`.
  - Labels: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `security-preemptive`, `dev-dependency`. Priority: **Normal**.
  - Description starts with this note: "> **Preemptive remediation**: This task was created proactively from cross-stream impact analysis of TC-8050 (stream 2.2.x). No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one, this task will be linked and the `security-preemptive` label removed."
  - It also contains the dev-only note.
  - Affected versions: 2.1.0 and 2.1.1, source commits v0.3.8 and v0.3.12.
- **Propagate CVE-2026-99001 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)**
  - Same labels and Normal priority.
  - Blocked by the 2.1.x upstream task.

## Post-triage

- Add the `ai-cve-triaged` label to TC-8050.
- Post a summary comment covering:
  - the version impact table
  - the Affects Versions correction (add RHTPA 2.2.1 through 2.2.4)
  - the outcome: remediation created, dev-dependency, Normal priority
  - task links and release Jira refs
  - an @mention of the reporter
  - the Comment Footnote
