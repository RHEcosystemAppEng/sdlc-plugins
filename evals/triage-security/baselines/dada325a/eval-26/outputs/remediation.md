# TC-8050 — Step 8: Remediation

## Decision

- 2.2.x is the in-scope stream, and all of its versions are affected by lock-file evidence (criterion 0.5.1 < 0.5.2). That makes this **Case B**: create remediation tasks.
- 2.1.x is outside the scope and is also affected, which triggers **Case A**: a cross-stream impact comment, plus preemptive tasks if no 2.1.x CVE Jira exists.
- Ecosystem is Cargo (source dependency), so each stream gets **2 tasks**: upstream backport and downstream propagation (blocked).
- Dependency scope is **dev-only** (`[dev-dependencies]`, not shipped). Every remediation task therefore gets:
  - Label **`dev-dependency`**
  - Priority **Normal**, overriding the CVE's priority, which is not inherited (CVSS 5.3 Medium)
  - The note: "This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only)."
- Coordination Guidance is omitted because the Source Repositories table has no Deployment Context column.

All of the following are **proposals awaiting engineer confirmation**. No Jira calls were made.

---

## Task 1 — Upstream backport (2.2.x)

- **Summary**: Remediate CVE-2026-99001: bump criterion to 0.5.2 (2.2.x)
- **Issue type**: Task
- **Project**: TC
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`
- **Priority**: **Normal** (dev-dependency override; the CVE's severity is not inherited)

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99001: path traversal in criterion benchmark output. Crafted
benchmark names containing path separators allow benchmark output files to be
written to arbitrary paths.
The vulnerable dependency (criterion < 0.5.2) must be updated to the fixed
version (0.5.2+).

This dependency is dev/build-only and is not shipped in production. Remediation
priority is Normal (supply chain risk only).

Affected versions: RHTPA 2.2.0, 2.2.1, 2.2.2 (retag of 2.2.1), 2.2.3, 2.2.4
Source commit(s): backend v0.4.5, v0.4.8, v0.4.11, v0.4.12

Upstream fix: none listed in remote links
Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (chain: backend (workspace) → criterion)
- **Dependency scope**: dev-only — declared under `[dev-dependencies]` in
  backend/Cargo.toml (`criterion = "0.5.1"`); used for benchmarks only and NOT
  present in production builds. Remediation priority is Normal regardless of
  CVE severity; task carries the `dev-dependency` label.

### Remediation approach (direct dependency)

- Update criterion dependency to >= 0.5.2 in backend/Cargo.toml
  `[dev-dependencies]` and refresh Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level
  workaround is viable in the benchmark code (see upstream changelog)

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass
- [ ] Benchmarks still compile (`cargo bench --no-run`)

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8050 (parent tracking issue)
```

## Task 2 — Downstream propagation (2.2.x)

- **Summary**: Propagate CVE-2026-99001 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)
- **Issue type**: Task
- **Project**: TC
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`
- **Priority**: **Normal** (dev-dependency override)

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99001 fix from <Task 1 key>.

The upstream backport (<Task 1 key>) bumps criterion to 0.5.2 on release/0.4.z.
Once that PR merges, update the source pinning in this Konflux release repo so
the next build's source tree carries the fix.

This dependency is dev/build-only and is not shipped in production. Remediation
priority is Normal (supply chain risk only).

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag,
  e.g., `v0.4.12`)
- **Dependency type**: direct — carried forward from upstream task
- **Dependency scope**: dev-only (`[dev-dependencies]`); not in the shipped
  container image. Priority Normal; `dev-dependency` label applied.
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <Task 1 key> (upstream backport must merge first)
- Depends on: TC-8050 (parent tracking issue)
```

### Creation and linkage plan (2.2.x)

1. Create Task 1, then post the description digest comment (`[sdlc-workflow] Description digest: sha256-md:<hex>`).
2. Create Task 2, then post its description digest comment.
3. Link TC-8050 → Task 1 (**Depend**). Link TC-8050 → Task 2 (**Depend**).
4. Link Task 1 → Task 2 (**Blocks**, so the downstream task is blocked by the upstream task).
5. If the Step 7.5 release Task is active, link Task 1 and Task 2 → release Task (**Blocks**), and link the release Task ↔ TC-8050 (**Related**).
6. Move TC-8050 to In Progress. Skip this if it is already in Assigned or a later indeterminate status.
7. Comment on TC-8050: "Remediation tasks created: <Task 1 key> (upstream backport), <Task 2 key> (downstream propagation, blocked by <Task 1 key>). Both tasks are labeled `dev-dependency` with Normal priority — criterion is a dev-only dependency not shipped in production." Include the Comment Footnote.

---

## Case A — Cross-stream impact (2.1.x)

Proposed comment on TC-8050 (with Comment Footnote):

```
Cross-stream impact: criterion < 0.5.2 also affects stream(s) 2.1.x
(RHTPA 2.1.0, 2.1.1 — criterion 0.5.1 at backend v0.3.8 / v0.3.12) based on
lock file analysis. Note: criterion is a dev-only dependency ([dev-dependencies])
and is not shipped in production builds. These streams are tracked by companion
issues (see Related links) or may require separate PSIRT triage.
```

Step 4 sibling JQL was not run in the eval, so I could not determine whether a `[rhtpa-2.1]` CVE-2026-99001 Jira exists.
- **If one exists**: do not create tasks for 2.1.x. That stream is triaged through its own issue.
- **If none exists**: create preemptive tasks for 2.1.x using the same two templates as above, with these substitutions:
  - Repository and branch: Task 3 targets `rhtpa-backend` / `release/0.3.z`. Task 4 targets `rhtpa-release.0.3.z` / `main`.
  - Affected versions: RHTPA 2.1.0, 2.1.1. Source commits: v0.3.8, v0.3.12.
  - **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `security-preemptive`, `dev-dependency`
  - **Priority**: **Normal** (dev-dependency override)
  - Description prefix:
    > **Preemptive remediation**: This task was created proactively from cross-stream impact analysis of TC-8050 (stream 2.2.x). No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one, this task will be linked and the `security-preemptive` label removed.
  - The same dev-only note as above.
  - Links: TC-8050 → Task 3 and Task 4 (**Related**, not Depend), and Task 3 → Task 4 (**Blocks**). Preemptive tasks are not linked to the release Task.

## Pre-creation checklist

- [x] Task count per stream: Cargo is a source dependency, so 2 tasks per stream
- [x] Cross-stream coverage: 2.1.x gets either preemptive tasks or its existing sibling CVE Jira (pending Step 4 result)
- [x] Link types: Depend for in-scope tasks, Related for preemptive tasks, Blocks for upstream → downstream
- [x] Preemptive labels: `security-preemptive` on 2.1.x tasks only
- [x] Dev-dependency handling: `dev-dependency` label and Normal priority on **all** tasks
- [x] Coordination guidance: omitted (no Deployment Context column)
- [x] Release Jira linking: in-scope tasks only, if the release Task is active
- [x] Dedup consistency: Step 7.5.3 not applicable (Upstream Affected Component field not configured)

## Post-triage (proposed)

- Add label `ai-cve-triaged` to TC-8050.
- Post a summary comment with these parts:
  - The version impact table and dependency chain (dev-only)
  - The Affects Versions correction (RHTPA 2.2.0 changed to 2.2.0–2.2.4)
  - Outcome: remediation tasks created at Normal priority with the `dev-dependency` label
  - Task keys and release Jira keys
  - An @mention of the TC-8050 reporter
  - The Comment Footnote
