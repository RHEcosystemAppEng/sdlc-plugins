# TC-8001 Triage — Step 8 Remediation

_Simulated output. No Jira mutations executed; each would require engineer confirmation._

## Decision

- Issue scope: **2.2.x** (summary suffix `[rhtpa-2.2]`).
- Affected in scope: 2.2.0, 2.2.1, 2.2.2 (retag of 2.2.1). 2.2.3 / 2.2.4 ship quinn-proto 0.11.14 (not affected).
- Affected outside scope: 2.1.0, 2.1.1 (quinn-proto 0.11.9).
- Ecosystem: Cargo → source dependency → **2 tasks per stream**.
- Result: **Case B** for 2.2.x (Depend-linked tasks) + **Case A** for 2.1.x (cross-stream
  comment + preemptive tasks, Related-linked, `security-preemptive` label).
- Deployment context: rhtpa-backend defaulted to `upstream` because the Source
  Repositories table has no Deployment Context column. Per backward-compatibility rule,
  **no Coordination Guidance subsection is included** in any task below.

---

## Task 1 — 2.2.x dependency bump (Case B)

**Summary**: Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x)
**Labels**: ai-generated-jira, Security, CVE-2026-31812
**Links**: TC-8001 → Task 1 (Depend); Task 1 → Task 2 (Blocks); Task 1 → release Task (Blocks)

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream —
a package manager update is sufficient.

Affected versions: 2.2.0 (quinn-proto 0.11.9), 2.2.1 (quinn-proto 0.11.12), 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: not determined during triage (manifest not inspected) — verify
  whether quinn-proto is direct or transitive (e.g., via quinn) before bumping
- **Remediation action**: run the appropriate package manager update command:
  - **Cargo**: `cargo update -p quinn-proto` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update
- Released tags v0.4.11 and v0.4.12 already ship quinn-proto 0.11.14; confirm
  release/0.4.z HEAD is at >= 0.11.14 — if so this task may close as already done
- If the vulnerable dependency is dev-only or build-only, the remediation priority is
  Normal regardless of CVE severity. Add `dev-dependency` label to the task.

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

## Task 2 — 2.2.x downstream propagation (Case B)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)
**Labels**: ai-generated-jira, Security, CVE-2026-31812
**Links**: TC-8001 → Task 2 (Depend); blocked by Task 1; Task 2 → release Task (Blocks)

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <Task 1 key>.

The dependency bump (<Task 1 key>) bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback
  approach), verify the pinning is reflected in the downstream build's
  lock file after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <Task 1 key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

## Case A — cross-stream impact comment on TC-8001

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s)
2.1.x based on lock file analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

---
<Comment Footnote per shared/comment-footnote.md, skill: triage-security>
```

## Task 3 — 2.1.x upstream backport (preemptive)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)
**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
**Links**: TC-8001 → Task 3 (Related); Task 3 → Task 4 (Blocks)

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (DoS).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (quinn-proto 0.11.9), 2.1.1 (quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: not determined during triage — verify direct vs transitive
- If the vulnerable dependency is dev-only or build-only, the remediation priority is
  Normal regardless of CVE severity. Add `dev-dependency` label to the task.

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

- Depends on: TC-8001 (parent tracking issue)
```

## Task 4 — 2.1.x downstream propagation (preemptive)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)
**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
**Links**: TC-8001 → Task 4 (Related); blocked by Task 3

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

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from <Task 3 key>.

The upstream backport (<Task 3 key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback
  approach), verify the pinning is reflected in the downstream build's
  lock file after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <Task 3 key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

## Post-creation steps (pending confirmation)

1. Description digest comment on each task (before links).
2. Links as listed above; TC-8001 → 2.2.x release Task (Related).
3. TC-8001 already in Assigned after Step 0.8 → In Progress transition skipped.
4. Comment on TC-8001: "Remediation tasks created: <Task 1> (dependency bump), <Task 2>
   (downstream propagation, blocked by <Task 1>)" plus preemptive task list for 2.1.x.
5. Add `ai-cve-triaged` label; post summary comment (impact table, Affects Versions
   correction RHTPA 2.0.0 → 2.2.0/2.2.1/2.2.2, tasks, release Jira refs, @mention of
   reporter, Comment Footnote).

## Pre-creation checklist

- [x] Task count per stream: 2 (Cargo = source dependency)
- [x] Cross-stream coverage: 2.1.x has preemptive tasks
- [x] Link types: Depend (2.2.x), Related (2.1.x preemptive), Blocks (upstream → downstream)
- [x] Preemptive labels on 2.1.x tasks
- [x] Coordination guidance: **omitted** — Deployment Context column absent (backward compatibility)
- [x] Release Jira linking: 2.2.x non-preemptive tasks → release Task (Blocks)
- [x] Dedup consistency: no Step 7.5.3 dedup (Upstream Affected Component field not configured)
