# Step 8 – Remediation: TC-8050 (CVE-2026-99001, criterion < 0.5.2) [rhtpa-2.2]

## Decision

- Stream-scoped versions (2.2.0 – 2.2.4) ship criterion 0.5.1 → **affected** → **Case B**:
  create remediation tasks for stream 2.2.x.
- Other stream 2.1.x (2.1.0, 2.1.1) also ships criterion 0.5.1 → **Case A** cross-stream
  impact comment; a preemptive task pair for 2.1.x only if Step 4 finds no 2.1.x CVE Jira.
- Ecosystem: Cargo (source dependency) → **2 tasks** for 2.2.x.
- Upstream fix on `release/0.4.z` not confirmed → upstream backport + downstream propagation.
- **Dependency scope: dev-only** (`[dev-dependencies]` in backend/Cargo.toml, benchmarks
  only, NOT in production builds) → every remediation task gets the **`dev-dependency`
  label** and **priority Normal** (overrides CVE severity; CVE priority not inherited).
- Not Case C: the crate is present in the lock file at affected versions; the dev-only
  scope lowers priority but does not close the issue as Not a Bug.

## Task 1 – Upstream backport (2.2.x)

- **Project**: TC
- **Issue type**: Task
- **Summary**: Remediate CVE-2026-99001: bump criterion to 0.5.2 (2.2.x)
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`
- **Priority**: **Normal** (dev-dependency override — CVE severity not inherited)

```
## Repository

backend (rhtpa-backend)

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99001: criterion path traversal in benchmark output — crafted
benchmark names containing path separators allow writing benchmark output files to
arbitrary paths.
The vulnerable dependency (criterion < 0.5.2) must be updated to the fixed
version (0.5.2+).

> This dependency is dev/build-only and is not shipped in production. Remediation
> priority is Normal (supply chain risk only).

Affected versions: RHTPA 2.2.0, 2.2.1, 2.2.2 (retag of 2.2.1), 2.2.3, 2.2.4
Source commit(s): v0.4.5, v0.4.8, v0.4.11, v0.4.12 (backend tags from security-matrix.md)

Upstream fix: none listed in remote links
Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (chain: backend (workspace) → criterion)
- **Dependency scope**: dev-only — declared in `[dev-dependencies]` in
  backend/Cargo.toml (`criterion = "0.5.1"`); used for benchmarks only and NOT
  present in production builds. Remediation priority is Normal regardless of CVE
  severity; task carries the `dev-dependency` label.

### Remediation approach (direct dependency)

- Update criterion dependency to >= 0.5.2 in backend/Cargo.toml
  `[dev-dependencies]` and Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level
  workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency
- [ ] Benchmarks (`cargo bench --no-run`) still compile with criterion >= 0.5.2

## Dependencies

- Depends on: TC-8050 (parent tracking issue)
```

## Task 2 – Downstream propagation (2.2.x)

- **Project**: TC
- **Issue type**: Task
- **Summary**: Propagate CVE-2026-99001 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`
- **Priority**: **Normal** (dev-dependency override — CVE severity not inherited)

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
release repo so the next build ships the fix.

> This dependency is dev/build-only and is not shipped in production. Remediation
> priority is Normal (supply chain risk only).

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: direct — carried forward from upstream task
- **Dependency scope**: dev-only (criterion in `[dev-dependencies]`, not in the
  production image) — Normal priority, `dev-dependency` label
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

Coordination Guidance subsection omitted: Source Repositories table has no Deployment
Context column (backward compatibility rule).

## Jira operations (proposed — require engineer confirmation; NOT executed)

1. Create Task 1, then post description digest comment (`[sdlc-workflow] Description digest: <tagged-digest>`) before any links.
2. Create Task 2, then post its description digest comment.
3. Links:
   - TC-8050 → Task 1 (`Depend`)
   - TC-8050 → Task 2 (`Depend`)
   - Task 1 → Task 2 (`Blocks` — downstream blocked by upstream)
   - Task 1 and Task 2 → release Task "RHTPA <2.2.x next version> CVE triage" (`Blocks`), if Step 7.5 release Jira is active
   - Release Task → TC-8050 (`Related`)
4. Affects Versions: `[RHTPA 2.2.0]` → `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2, RHTPA 2.2.3, RHTPA 2.2.4]`.
5. Vulnerability already assigned/transitioned at Step 0.8 (New → Assigned); skip In Progress if already Assigned or later.
6. Add `ai-cve-triaged` label to TC-8050.

## Case A – Cross-stream impact comment (proposed)

```
Cross-stream impact: criterion < 0.5.2 also affects stream(s) 2.1.x (RHTPA 2.1.0,
2.1.1 ship criterion 0.5.1) based on lock file analysis. criterion is a dev-only
dependency ([dev-dependencies] in backend/Cargo.toml) and is not shipped in
production. These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

---
<Comment Footnote per shared/comment-footnote.md, skill: triage-security>
```

If Step 4 finds no 2.1.x CVE Jira for CVE-2026-99001, create a preemptive pair for 2.1.x
(upstream backport on `release/0.3.z` + downstream propagation in rhtpa-release.0.3.z)
with labels `ai-generated-jira`, `Security`, `CVE-2026-99001`, `security-preemptive`,
`dev-dependency`, priority **Normal**, "Related" link to TC-8050, and the preemptive
description prefix. These are not part of the 2.2.x issue's own remediation.

## Post-triage summary comment (proposed)

```
Triage summary for CVE-2026-99001 (criterion < 0.5.2) — scoped to 2.2.x

Version impact: RHTPA 2.2.0, 2.2.1, 2.2.2 (retag of 2.2.1), 2.2.3, 2.2.4 ship
criterion 0.5.1 → affected. Dependency chain: backend (workspace) → criterion
(direct dev-dependency, [dev-dependencies], benchmarks only, not in production builds).

Affects Versions: [RHTPA 2.2.0] → [RHTPA 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4]
Outcome: remediation created (dev-dependency, priority Normal — supply chain risk only)
- <upstream-task-key> (upstream backport, release/0.4.z)
- <downstream-task-key> (downstream propagation, blocked by <upstream-task-key>)
Release Jira: <release Epic / release Task keys, if created>
Dedup: none
Cross-stream: 2.1.x also affected (see cross-stream comment)

@<reporter>

---
<Comment Footnote per shared/comment-footnote.md, skill: triage-security>
```

## Pre-creation checklist

- [x] Task count per stream: Cargo (source dependency) → 2 tasks for 2.2.x
- [x] Cross-stream coverage: 2.1.x handled via Case A comment + conditional preemptive tasks
- [x] Link types: Depend (own CVE), Blocks (upstream → downstream; remediation → release Task), Related (preemptive / CVE ↔ release Task)
- [x] Preemptive labels: only on 2.1.x tasks if created
- [x] Coordination guidance: omitted (no Deployment Context column)
- [x] Release Jira linking: planned for non-preemptive tasks
- [x] Dedup consistency: Step 7.5.3 skipped (Upstream Affected Component not configured)
- [x] Dev-dependency handling: `dev-dependency` label + Normal priority on all remediation tasks
