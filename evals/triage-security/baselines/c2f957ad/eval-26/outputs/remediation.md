# TC-8050 — Step 8 Remediation

## Decision

- 2.2.x versions are affected and the issue is scoped to 2.2.x, so this is **Case B**: create remediation tasks for 2.2.x.
- 2.1.x is also affected and no 2.1.x CVE Jira was found, so **Case A** also applies: post a cross-stream comment and create **preemptive** tasks for 2.1.x.
- Ecosystem is Cargo (source dependency), so each stream gets **2 tasks**: an upstream backport and a downstream propagation. The upstream fix is not confirmed, so the backport variant is used.
- Dependency scope is **dev-only** (`[dev-dependencies]`). Every task gets the label **`dev-dependency`** and priority **Normal**, which overrides the CVE severity.
- Security level: copied from the parent TC-8050 security level, if it has one. The fixture shows none.

All tasks and links below are proposals. Each one needs engineer confirmation before any Jira mutation.

---

## Task 1 — Upstream backport (2.2.x) [standard]

- **Summary:** Remediate CVE-2026-99001: bump criterion to 0.5.2 (2.2.x)
- **Issue type:** Task
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`
- **Priority:** Normal (dev-only override; the CVE priority is not inherited)
- **Links:** TC-8050 → this task (Depend); this task → Task 2 (Blocks); this task → 2.2.x release Task (Blocks), if Step 7.5 resolves one

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99001: criterion path traversal in benchmark output
(crafted benchmark names containing path separators can write output files to
arbitrary paths). The vulnerable dependency (criterion < 0.5.2) must be updated
to the fixed version (0.5.2+).

This dependency is dev/build-only and is not shipped in production. Remediation
priority is Normal (supply chain risk only).

Affected versions: 2.2.0, 2.2.1, 2.2.2 (retag of 2.2.1), 2.2.3, 2.2.4
Source commit(s): v0.4.5, v0.4.8, v0.4.11, v0.4.12

Upstream fix: none referenced in remote links
Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (chain: backend (workspace) → criterion, declared in
  [dev-dependencies] of backend/Cargo.toml)
- **Dependency scope**: dev-only (benchmarks). Not present in production builds.
  Remediation priority is Normal regardless of CVE severity; `dev-dependency`
  label applied.

### Remediation approach (direct dependency)

- Update criterion dev-dependency to >= 0.5.2 in backend/Cargo.toml
  ([dev-dependencies]) and regenerate Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency
- [ ] Benchmarks (`cargo bench`) compile with the updated criterion

## Dependencies

- Depends on: TC-8050 (parent tracking issue)
```

## Task 2 — Downstream propagation (2.2.x) [standard]

- **Summary:** Propagate CVE-2026-99001 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`
- **Priority:** Normal (dev-only override)
- **Links:** TC-8050 → this task (Depend); blocked by Task 1 (Blocks); this task → 2.2.x release Task (Blocks), if Step 7.5 resolves one

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

This dependency is dev/build-only and is not shipped in production. Remediation
priority is Normal (supply chain risk only).

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: direct — carried forward from upstream task
- **Dependency scope**: dev-only; `dev-dependency` label, Normal priority
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

---

## Case A — Cross-stream impact comment (on TC-8050)

```
Cross-stream impact: criterion < 0.5.2 also affects stream(s) 2.1.x
(2.1.0, 2.1.1 — criterion 0.5.1) based on lock file analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

Note: criterion is a dev-only dependency ([dev-dependencies]) and is not
shipped in production builds.

---
_This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/mrizzi/sdlc-plugins)._
```

## Task 3 — Upstream backport (2.1.x) [preemptive]

- **Summary:** Remediate CVE-2026-99001: bump criterion to 0.5.2 (2.1.x)
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-99001`, `security-preemptive`, `dev-dependency`
- **Priority:** Normal (dev-only override)
- **Links:** TC-8050 → this task (**Related**, preemptive); this task → Task 4 (Blocks). Preemptive tasks are not linked to the release Task.

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8050 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-99001: criterion path traversal in benchmark output.
The vulnerable dependency (criterion < 0.5.2) must be updated to the fixed
version (0.5.2+).

This dependency is dev/build-only and is not shipped in production. Remediation
priority is Normal (supply chain risk only).

Affected versions: 2.1.0, 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: none referenced in remote links
Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (chain: backend (workspace) → criterion, declared in
  [dev-dependencies] of backend/Cargo.toml)
- **Dependency scope**: dev-only; Normal priority; `dev-dependency` label applied.

### Remediation approach (direct dependency)

- Update criterion dev-dependency to >= 0.5.2 in backend/Cargo.toml and regenerate Cargo.lock

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8050 (originating tracking issue, stream 2.2.x)
```

## Task 4 — Downstream propagation (2.1.x) [preemptive]

- **Summary:** Propagate CVE-2026-99001 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-99001`, `security-preemptive`, `dev-dependency`
- **Priority:** Normal (dev-only override)
- **Links:** TC-8050 → this task (Related); blocked by Task 3 (Blocks)

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8050 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-99001 fix from <Task 3 key> (criterion 0.5.2 on release/0.3.z).

This dependency is dev/build-only and is not shipped in production. Remediation
priority is Normal (supply chain risk only).

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: direct — carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <Task 3 key> (upstream backport must merge first)
- Depends on: TC-8050 (originating tracking issue)
```

---

## Ordering per task (digest before links)

For each task: create the task, post the description digest comment (`[sdlc-workflow] Description digest: sha256-...`), then create its links. All task-list, cross-stream, and summary comments come after that.

## Pre-creation checklist

- [x] Task count per stream: 2 per stream (Cargo is a source dependency)
- [x] Cross-stream coverage: 2.1.x gets preemptive tasks (no sibling CVE Jira found)
- [x] Link types: Depend for 2.2.x tasks, Related for 2.1.x preemptive tasks, Blocks from upstream to downstream
- [x] Preemptive labels on the 2.1.x tasks
- [x] Coordination guidance: left out, because Source Repositories has no Deployment Context column
- [x] Release Jira linking: 2.2.x non-preemptive tasks get a Blocks link to the release Task if Step 7.5 resolves one; TC-8050 gets a Related link to it
- [x] Dedup: not applicable (Upstream Affected Component field not configured)
- [x] dev-dependency label + Normal priority on all 4 tasks

## Post-triage actions (proposed)

1. Correct Affects Versions to RHTPA 2.2.0–2.2.4 (Step 3).
2. Add the label `ai-cve-triaged` to TC-8050.
3. Post a summary comment on TC-8050 with: the version impact table, the Affects Versions correction, the outcome (4 remediation tasks: 2 standard, 2 preemptive, all `dev-dependency`/Normal), task links, release Jira references, an @mention of the issue reporter, and the Comment Footnote.
