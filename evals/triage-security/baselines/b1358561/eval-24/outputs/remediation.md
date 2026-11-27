# TC-8001 Remediation Plan (Step 8)

_Simulated: no Jira mutations were executed. Every action below would need engineer confirmation in interactive mode._

## Decision

- The issue is **scoped** to stream 2.2.x (`[rhtpa-2.2]`).
- In-scope versions 2.2.0, 2.2.1, and 2.2.2 (retag of 2.2.1) are affected. 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14. This gives **Case B** for 2.2.x.
- Out-of-scope stream 2.1.x is also affected (2.1.0 and 2.1.1 ship 0.11.9). This gives **Case A** for 2.1.x: a cross-stream comment plus **preemptive** tasks, because the run assumes no 2.1.x CVE Jira exists.
- The ecosystem is Cargo, a source dependency, so the plan has **2 tasks per stream**:
  - 2.2.x: the fix is already on `release/0.4.z`, so the plan uses the **dependency bump + downstream propagation** variant.
  - 2.1.x: the fix is not on `release/0.3.z` (v0.3.12 ships 0.11.9), so the plan uses the **upstream backport + downstream propagation** variant.
- **Coordination Guidance is omitted** from every task. The Source Repositories table in CLAUDE.md has no Deployment Context column. In that backward-compatibility case, `remediation-templates.md` says to omit the `### Coordination Guidance` subsection entirely. rhtpa-backend's internal default context is `upstream`, but the run does not emit guidance text for it.
- Dependency type: the inputs give no manifest evidence, so the type is listed as "to be confirmed" in each task (likely transitive via `quinn`).
- Security level: each create_issue would copy TC-8001's security level, read live from Jira; omit it only if TC-8001 has none.

**Engineer note:** for 2.2.x, the latest release (2.2.4) already ships the fix. The 2.2.x tasks therefore mainly confirm `release/0.4.z` stays at or above 0.11.14 and that the next 2.2.z build picks it up. The engineer may decide to decline them.

---

## Task 1 — 2.2.x dependency bump (standard, linked "Depend" to TC-8001)

**Summary:** Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)
**Labels:** ai-generated-jira, Security, CVE-2026-31812
**Security:** <TC-8001 security level>

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream —
a package manager update is sufficient.

Affected versions: RHTPA 2.2.0 (quinn-proto 0.11.9), RHTPA 2.2.1 (0.11.12), RHTPA 2.2.2 (same as 2.2.1 — retag)
Source commit(s): v0.4.5, v0.4.8 (backend tags from supportability matrix)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: to be confirmed (no manifest evidence available during triage; likely transitive via quinn)
- **Remediation action**: run the appropriate package manager update command:
  - **Cargo**: `cargo update -p quinn-proto` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update (tags v0.4.11 / v0.4.12
  already ship 0.11.14 — confirm release/0.4.z HEAD still does)
- If the vulnerable dependency is dev-only or build-only, the remediation priority
  is Normal regardless of CVE severity. Add `dev-dependency` label to the task.

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

## Task 2 — 2.2.x downstream propagation (standard, blocked by Task 1)

**Summary:** Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
**Labels:** ai-generated-jira, Security, CVE-2026-31812
**Security:** <TC-8001 security level>

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

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: to be confirmed — carried forward from upstream task
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

## Task 3 — 2.1.x upstream backport (PREEMPTIVE, linked "Related" to TC-8001)

**Summary:** Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)
**Labels:** ai-generated-jira, Security, CVE-2026-31812, security-preemptive
**Security:** <TC-8001 security level>

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

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (remote DoS).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (quinn-proto 0.11.9), RHTPA 2.1.1 (quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12 (backend tags from supportability matrix)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: to be confirmed (no manifest evidence available during triage; likely transitive via quinn)
- If the vulnerable dependency is dev-only or build-only, the remediation
  priority is Normal regardless of CVE severity. Add `dev-dependency` label to the task.

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (e.g., quinn / reqwest)
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

## Task 4 — 2.1.x downstream propagation (PREEMPTIVE, blocked by Task 3)

**Summary:** Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)
**Labels:** ai-generated-jira, Security, CVE-2026-31812, security-preemptive
**Security:** <TC-8001 security level>

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

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: to be confirmed — carried forward from upstream task
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

## Proposed Jira operations (in order, each needing confirmation)

1. Assign TC-8001 to the current user and transition New → Assigned (Step 0.8).
2. Set Affects Versions on TC-8001: [RHTPA 2.0.0] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2], plus a correction comment with the footnote. There is no ProdSec @mention because none is configured.
3. Release Jira for 2.2.x: find or create "RHTPA 2.2.5 Release Tasks" (Epic) and "RHTPA 2.2.5 CVE triage" (Task). This needs individual confirmation.
4. Create Task 1, then post its description digest.
5. Create Task 2, then post its description digest.
6. Links: TC-8001 → Task 1 (Depend), TC-8001 → Task 2 (Depend), Task 1 → Task 2 (Blocks), Task 1/Task 2 → release Task (Blocks), release Task → TC-8001 (Related).
7. Cross-stream comment on TC-8001: "Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x (2.1.0, 2.1.1 ship 0.11.9) based on lock file analysis. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage." The comment includes the footnote.
8. Create Task 3 (preemptive), then post its digest. Create Task 4 (preemptive), then post its digest.
9. Links: TC-8001 → Task 3 (Related), TC-8001 → Task 4 (Related), Task 3 → Task 4 (Blocks). Preemptive tasks are not linked to release Jira.
10. Comment on TC-8001 listing the preemptive tasks (2.1.x: Task 3, Task 4, security-preemptive), with the footnote.
11. Comment on TC-8001 listing the remediation tasks: "Remediation tasks created: <Task 1> (dependency bump), <Task 2> (downstream propagation, blocked by <Task 1>)". Include the footnote.
12. Add label `ai-cve-triaged` to TC-8001. Post the post-triage summary comment with the impact table, the AV correction, the outcome, task links, release Jira refs, "no dedup (field not configured)", an @mention of the TC-8001 reporter, and the Comment Footnote.

Transition to In Progress: skip it if TC-8001 is already in Assigned or a later indeterminate status.

## Pre-creation checklist

- [x] Task count per stream: Cargo is a source dependency, so 2 tasks for each of 2.2.x and 2.1.x
- [x] Cross-stream coverage: 2.1.x is covered by preemptive Tasks 3 and 4
- [x] Link types: Depend (own CVE), Related (preemptive), Blocks (upstream → downstream)
- [x] Preemptive labels: Tasks 3 and 4 carry `security-preemptive`
- [x] Coordination guidance: intentionally omitted because the Deployment Context column is absent (backward compatibility)
- [x] Release Jira linking: only non-preemptive Tasks 1 and 2 link to the 2.2.x release Task
- [x] Dedup consistency: no dedup was performed (Upstream Affected Component field not configured)
