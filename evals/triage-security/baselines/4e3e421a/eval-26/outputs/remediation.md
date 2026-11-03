# Step 8 – Remediation: TC-8050 (CVE-2026-99001, criterion, stream 2.2.x)

All Jira mutations below are **proposed only**. In interactive mode each one needs explicit engineer confirmation. This eval executed none of them.

## Steps 3–7.5 recap (context for remediation)

- **Step 3, Affects Versions (scoped to 2.2.x):** change RHTPA 2.2.0 to RHTPA 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4. Post a correction comment with the footnote.
- **Step 4, Duplicates/siblings:** no sibling data in the fixture, so no known 2.2.x duplicate and no known 2.1.x companion CVE Jira. Step 4.3 (cross-CVE overlap) is skipped because the Upstream Affected Component field is not configured.
- **Step 5, Lifecycle:** no lifecycle data in the fixture. The 2.2.x versions are treated as supported.
- **Step 6, Already fixed:** no resolved siblings, so it is not already fixed.
- **Step 7, Concurrent triage:** skipped because the Upstream Affected Component field is not configured.
- **Step 7.5, Release Jira:** no release metadata in the fixture. Proposed: find or create "RHTPA 2.2.5 Release Tasks" (Epic) and "RHTPA 2.2.5 CVE triage" (Task). The version is a placeholder that needs individual engineer confirmation. No cross-CVE dedup was possible because the field is not configured.

## Decision

- Supported 2.2.x versions are affected (criterion 0.5.1 < 0.5.2), so this is **Case B**: create remediation tasks.
- The issue is scoped and 2.1.x is also affected, so **Case A** also applies: post a cross-stream comment and create preemptive tasks for 2.1.x.
- Ecosystem is Cargo (source dependency). The upstream fix is not confirmed, so each stream gets **2 tasks**: upstream backport + downstream propagation.
- **Dependency scope is dev-only** (`[dev-dependencies]`, not in production builds):
  - Every task gets the **`dev-dependency`** label.
  - **Priority is overridden to Normal.** The CVE's own priority (CVSS 5.3 Medium) is not inherited.
  - Every description includes the dev/build-only note.
- Case C (close as Not a Bug) does **not** apply. The skill's decision tree treats dev-only dependencies as supply-chain risk that still needs remediation, not as "not affected".

---

## Task 1 – Upstream backport (2.2.x)

- **Project:** TC
- **Issue type:** Task
- **Summary:** Remediate CVE-2026-99001: bump criterion to 0.5.2 (2.2.x)
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`
- **Priority:** **Normal** (dev-dependency override; CVE severity not inherited)

```
## Repository

backend (rhtpa-backend)

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99001: criterion path traversal in benchmark output. Crafted
benchmark names containing path separators allow benchmark output files to be
written to arbitrary paths. The vulnerable dependency (criterion < 0.5.2) must be
updated to the fixed version (0.5.2+).

This dependency is dev/build-only and is not shipped in production. Remediation
priority is Normal (supply chain risk only).

Affected versions: RHTPA 2.2.0, 2.2.1, 2.2.2 (retag of 2.2.1), 2.2.3, 2.2.4
Source commit(s): v0.4.5, v0.4.8, v0.4.11, v0.4.12

Upstream fix: none listed in remote links
Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (chain: backend (workspace) → criterion)
- **Dependency scope**: dev-only — declared in `[dev-dependencies]` in
  backend/Cargo.toml (`criterion = "0.5.1"`); used for benchmarks only and NOT
  present in production builds
- The vulnerable dependency is dev-only (identified in Step 2.3.5), so the
  remediation priority is Normal regardless of CVE severity. The
  `dev-dependency` label is applied to this task.
- Update criterion to >= 0.5.2 in backend/Cargo.toml `[dev-dependencies]` and
  regenerate Cargo.lock (e.g., `cargo update -p criterion`)
- If the bump introduces breaking changes in benchmark code, assess whether a
  code-level adjustment to the benchmarks is needed (see criterion changelog)

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency
- [ ] Benchmarks compile (`cargo bench --no-run`)

## Dependencies

- Depends on: TC-8050 (parent tracking issue)
```

After creation, post the description digest comment (`[sdlc-workflow] Description digest: <tagged-digest>`) before any links.

---

## Task 2 – Downstream propagation (2.2.x)

- **Project:** TC
- **Issue type:** Task
- **Summary:** Propagate CVE-2026-99001 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`
- **Priority:** **Normal** (dev-dependency override; CVE severity not inherited)

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-99001
fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps criterion to 0.5.2 on
release/0.4.z. Once that PR merges, update the source pinning in this Konflux
release repo so the next build carries the fixed lock file.

This dependency is dev/build-only and is not shipped in production. Remediation
priority is Normal (supply chain risk only).

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: direct — carried forward from upstream task
- **Dependency scope**: dev-only (`[dev-dependencies]`); the production
  container image does not contain criterion, so this propagation only aligns
  the pinned source/lock file with the fix — priority Normal, `dev-dependency`
  label applied
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8050 (parent tracking issue)
```

After creation, post the description digest comment before any links.

---

## Case A – Cross-stream (2.1.x) preemptive tasks

**Cross-stream comment on TC-8050:**

> Cross-stream impact: criterion < 0.5.2 also affects stream(s) 2.1.x (2.1.0, 2.1.1 ship criterion 0.5.1 as a dev-only dependency) based on lock file analysis. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.
>
> _Comment footnote per shared/comment-footnote.md (skill: triage-security)_

No 2.1.x sibling CVE Jira was found in the fixture data. Two preemptive tasks are proposed using the same templates as Tasks 1 and 2, with these differences:

| Task | Summary | Labels | Priority | Link to TC-8050 |
|------|---------|--------|----------|-----------------|
| 3 | Remediate CVE-2026-99001: bump criterion to 0.5.2 (2.1.x). Target `release/0.3.z`; source commits `v0.3.8`, `v0.3.12` | `ai-generated-jira`, `Security`, `CVE-2026-99001`, `security-preemptive`, `dev-dependency` | **Normal** | Related |
| 4 | Propagate CVE-2026-99001 fix: update backend ref in rhtpa-release.0.3.z (2.1.x) | `ai-generated-jira`, `Security`, `CVE-2026-99001`, `security-preemptive`, `dev-dependency` | **Normal** | Related |

Each preemptive description starts with this prefix:

> **Preemptive remediation**: This task was created proactively from cross-stream impact analysis of TC-8050 (stream 2.2.x). No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one, this task will be linked and the `security-preemptive` label removed.

It also includes the same dev-only note: "This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only)."

---

## Jira linkage (proposed)

1. TC-8050 → Task 1: **Depend**
2. TC-8050 → Task 2: **Depend**
3. Task 1 → Task 2: **Blocks** (upstream blocks downstream)
4. TC-8050 → Task 3, Task 4: **Related** (preemptive)
5. Task 3 → Task 4: **Blocks**
6. Task 1 and Task 2 → release Task "RHTPA 2.2.x CVE triage": **Blocks**, if Step 7.5 is active
7. Release Task → TC-8050: **Related**
8. Move TC-8050 to In Progress. Confirm it is assigned to the current triager.
9. Comment on TC-8050: "Remediation tasks created: <Task 1> (upstream backport), <Task 2> (downstream propagation, blocked by <Task 1>)", plus a comment listing the preemptive tasks. Both comments include the footnote.

## Pre-creation checklist

- [x] Task count per stream: Cargo is a source dependency → 2 tasks for 2.2.x (and 2 preemptive for 2.1.x)
- [x] Cross-stream coverage: 2.1.x gets preemptive tasks (no sibling CVE Jira known)
- [x] Link types: Depend (own CVE), Related (preemptive), Blocks (upstream → downstream)
- [x] Preemptive labels on the 2.1.x tasks
- [x] Coordination guidance omitted: the Source Repositories table has no Deployment Context column
- [x] `dev-dependency` label on all tasks; priority overridden to **Normal** on all tasks
- [x] Dedup consistency: no dedup possible (field not configured)

## Post-triage summary (proposed)

- Add the `ai-cve-triaged` label to TC-8050.
- Post a summary comment covering:
  - the version impact table
  - the Affects Versions correction
  - the outcome: remediation tasks created at Normal priority with the dev-dependency label
  - the task links
  - release Jira references
  - "no dedup"
  - an ADF @mention of the issue reporter. The fixture has no reporter account ID; take it from the live issue data.
  - the comment footnote
