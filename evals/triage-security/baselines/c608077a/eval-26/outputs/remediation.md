# TC-8050 — Step 8: Remediation

## Outcome

- **Case B:** the scoped stream 2.2.x is affected (2.2.0–2.2.4 all ship criterion 0.5.1, which is below 0.5.2). Create remediation tasks for 2.2.x.
- **Case A:** stream 2.1.x (2.1.0, 2.1.1) is also affected, outside this issue's scope. Post a cross-stream comment. Create preemptive tasks for 2.1.x only if Step 4 finds no `[rhtpa-2.1]` sibling CVE Jira (JQL was not run in this eval).
- Ecosystem: Cargo, a **source dependency**, so **2 tasks per stream**: upstream backport + downstream propagation. The upstream fix status is unknown, so the backport variant is used.
- **Dev-dependency override (from Step 2.3.5):** criterion is declared only under `[dev-dependencies]` in backend/Cargo.toml and is NOT shipped in production. Every remediation task below therefore:
  - carries the **`dev-dependency`** label
  - has priority **Normal**, overriding the CVE severity (CVSS 5.3 Medium); the CVE priority is not inherited
  - includes the note that this is a dev/build-only, supply-chain-only risk
- No VEX closure applies. The package is present at an affected version, so the issue is not closed as Not a Bug.
- Step 7.5 release Jira: the release Epic "RHTPA <version> Release Tasks" and Task "RHTPA <version> CVE triage" for the next 2.2.x release (likely 2.2.5) must be found or created with individual confirmation. That was not executed here. The links to the release Task are listed below as placeholders.
- Coordination Guidance is omitted because the Source Repositories table has no Deployment Context column.

---

## Task 1 (2.2.x): Upstream backport

- **Project:** TC
- **Issue type:** Task
- **Summary:** Remediate CVE-2026-99001: bump criterion to 0.5.2 (2.2.x)
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`
- **Priority:** **Normal** (dev-dependency override; CVE severity is Medium / CVSS 5.3)

```
## Repository

backend (rhtpa-backend)

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99001: criterion path traversal in benchmark output
(crafted benchmark names containing path separators can write benchmark
output files to arbitrary paths). The vulnerable dependency
(criterion < 0.5.2) must be updated to the fixed version (0.5.2+).

> **Dev-dependency:** This dependency is dev/build-only and is not shipped in
> production. Remediation priority is Normal (supply chain risk only).
> criterion is declared under [dev-dependencies] in backend/Cargo.toml and is
> used for benchmarks only.

Affected versions: RHTPA 2.2.0, 2.2.1, 2.2.2 (retag of 2.2.1), 2.2.3, 2.2.4
Source commit(s): v0.4.5, v0.4.8, v0.4.11, v0.4.12 (backend tags from supportability matrix)

Upstream fix: none linked
Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (chain: backend (workspace) → criterion, [dev-dependencies])
- **Dependency scope**: dev-only. NOT present in production builds. Priority
  is Normal regardless of CVE severity; `dev-dependency` label applied.

### Remediation approach (direct dependency)

- Update criterion to >= 0.5.2 in backend/Cargo.toml `[dev-dependencies]`
  (currently `criterion = "0.5.1"`) and refresh Cargo.lock
  (e.g., `cargo update -p criterion`)
- If a direct bump introduces breaking changes in benchmark code, assess
  whether a code-level workaround is viable (see upstream changelog)

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

## Task 2 (2.2.x): Downstream propagation

- **Project:** TC
- **Issue type:** Task
- **Summary:** Propagate CVE-2026-99001 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`
- **Priority:** **Normal** (dev-dependency override)

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99001 fix from <Task 1 key>.

The upstream backport (<Task 1 key>) bumps criterion to 0.5.2 on
release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build carries the fix.

> **Dev-dependency:** This dependency is dev/build-only and is not shipped in
> production. Remediation priority is Normal (supply chain risk only).
> The shipped container image content is not expected to change for
> criterion; this propagation keeps the pinned source free of the vulnerable
> dev-dependency version.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: direct (dev-only), carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <Task 1 key> (upstream backport must merge first)
- Depends on: TC-8050 (parent tracking issue)
```

### 2.2.x links (proposed)

1. TC-8050 → Task 1: **Depend**
2. TC-8050 → Task 2: **Depend**
3. Task 1 → Task 2: **Blocks** (upstream blocks downstream)
4. Task 1 and Task 2 → RHTPA 2.2.x release Task: **Blocks** (if Step 7.5 is active)
5. Release Task → TC-8050: **Related**

Post a description digest comment (`[sdlc-workflow] Description digest: <tagged-digest>`) on each task immediately after it is created, before any links or other comments.

---

## Case A: Cross-stream impact (2.1.x)

### Cross-stream comment on TC-8050 (proposed)

```
Cross-stream impact: criterion < 0.5.2 also affects stream(s) 2.1.x
(RHTPA 2.1.0, 2.1.1 ship criterion 0.5.1) based on lock file analysis.
criterion is a dev-only dependency ([dev-dependencies] in backend/Cargo.toml)
and is not shipped in production builds.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

---
This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0.
```

### Preemptive tasks for 2.1.x (only if no `[rhtpa-2.1]` sibling CVE Jira exists)

These tasks follow the same templates as Tasks 1 and 2, with these differences:

- **Task 3 summary:** Remediate CVE-2026-99001: bump criterion to 0.5.2 (2.1.x). Repo backend, target branch `release/0.3.z`, affected versions 2.1.0 and 2.1.1, tags v0.3.8 and v0.3.12.
- **Task 4 summary:** Propagate CVE-2026-99001 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-99001`, `security-preemptive`, `dev-dependency`
- **Priority:** **Normal** (dev-dependency override)
- **Description prefix:**
  > **Preemptive remediation**: This task was created proactively from cross-stream impact analysis of TC-8050 (stream 2.2.x). No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one, this task will be linked and the `security-preemptive` label removed.
- **Dev-dependency note:** the same as in Tasks 1 and 2.
- **Links:** TC-8050 → Task 3 and Task 4: **Related** (not Depend). Task 3 → Task 4: **Blocks**. Preemptive tasks are not linked to the release Task.

---

## Pre-creation checklist

- [x] Task count per stream: Cargo is a source dependency, so 2 tasks for 2.2.x (and 2 preemptive for 2.1.x if needed)
- [x] Cross-stream coverage: 2.1.x is covered by preemptive tasks or an existing sibling CVE Jira (pending the Step 4 JQL)
- [x] Link types: Depend for own CVE, Related for preemptive, Blocks for upstream → downstream
- [x] Preemptive labels: `security-preemptive` on the 2.1.x tasks
- [x] Dev-dependency handling: `dev-dependency` label and Normal priority on **all** tasks, with the supply-chain note in each description
- [x] Coordination guidance: omitted (no Deployment Context column)
- [ ] Release Jira linking: pending Step 7.5 confirmation
- [x] Dedup consistency: Step 7.5.3 was not evaluated because the Upstream Affected Component field is not configured

## Post-triage (proposed)

- Add the `ai-cve-triaged` label to TC-8050.
- Correct Affects Versions to RHTPA 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4.
- Transition TC-8050 to In Progress / Assigned.
- Post a summary comment with the version impact table, the Affects Versions correction, the task links, the release Jira references, an @mention of the issue reporter, and the Comment Footnote.

All Jira mutations above need explicit engineer confirmation. None were executed in this eval.
