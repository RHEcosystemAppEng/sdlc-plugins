# TC-8001 — Step 8 Remediation (CVE-2026-31812, quinn-proto < 0.11.14)

> Eval mode: none of these Jira mutations were executed. Task keys are placeholders.
> In interactive mode each creation, digest comment, link, and comment requires engineer confirmation.

## Decision

- Issue scope: **2.2.x** (summary suffix `[rhtpa-2.2]`).
- 2.2.x affected: 2.2.0, 2.2.1, 2.2.2 (retag of 2.2.1). 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14.
- Other affected stream: **2.1.x** (2.1.0 and 2.1.1 ship 0.11.9). It has no sibling CVE Jira (assumed, since Step 4 JQL was not run).
- Ecosystem: **Cargo**, a source dependency, so **2 tasks per stream**.
- Affected repository deployment context: **rhtpa-backend → `customer-shipped`**. Every task below gets the customer-shipped Coordination Guidance subsection.
- Outcome: **Case A** (cross-stream comment plus preemptive tasks for 2.1.x) and **Case B** (standard tasks for 2.2.x).

| # | Stream | Task | Variant | Labels | Link to CVE |
|---|--------|------|---------|--------|-------------|
| 1 | 2.2.x | Dependency bump in rhtpa-backend `release/0.4.z` | Fix available upstream | ai-generated-jira, Security, CVE-2026-31812 | Depend (TC-8001 → task) |
| 2 | 2.2.x | Downstream propagation in rhtpa-release.0.4.z | Blocked by #1 | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 3 | 2.1.x | Upstream backport in rhtpa-backend `release/0.3.z` | Preemptive | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |
| 4 | 2.1.x | Downstream propagation in rhtpa-release.0.3.z | Preemptive, blocked by #3 | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |

Note for the engineer on 2.2.x: the latest 2.2.x releases (2.2.3 and 2.2.4) already ship the fix. Task #1 may therefore be a verification-only change if `release/0.4.z` HEAD already has quinn-proto >= 0.11.14. Task #2 makes sure the next 2.2.x build stays pinned to a fixed backend ref, and gives the advisory a fixed build to reference for customers on 2.2.0–2.2.2. You may decide that "upgrade to 2.2.3+" is sufficient and decline #1 and #2.

---

## Task 1 — Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x)

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream —
a package manager update is sufficient. quinn-proto before 0.11.14 allows a
remote attacker to cause a panic (DoS) via a QUIC frame creating an excessive
number of streams.

Affected versions: RHTPA 2.2.0 (0.11.9), RHTPA 2.2.1 (0.11.12), RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8
Not affected: RHTPA 2.2.3 (v0.4.11), RHTPA 2.2.4 (v0.4.12) — ship quinn-proto 0.11.14

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (unverified — confirm via `cargo tree -i quinn-proto`; typical chain: backend → reqwest/quinn → quinn-proto)
- **Remediation action**: run `cargo update -p quinn-proto` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify Cargo.lock reflects quinn-proto >= 0.11.14 after the update (tags v0.4.11/v0.4.12 already do; if HEAD already does, record that and close as no change needed)
- Dependency is production/runtime scope (not dev-only); no `dev-dependency` label

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE
assignment, advisory preparation, and formal disclosure. Fix must be released via
a security advisory with explicit CVE-to-component mapping.

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

## Task 2 — Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <TASK-1-KEY>.

The dependency bump (<TASK-1-KEY>) brings quinn-proto to 0.11.14 on
release/0.4.z. Once that PR merges (or is confirmed already present), update
the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: transitive (unverified) — carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag (must be >= v0.4.11, which already ships quinn-proto 0.11.14)
- If the upstream fix pinned a transitive dependency directly (fallback
  approach), verify the pinning is reflected in the downstream build's
  lock file after the source reference update
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE
assignment, advisory preparation, and formal disclosure. Fix must be released via
a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <TASK-1-KEY> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

## Task 3 (preemptive) — Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

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

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (remote DoS).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (0.11.9), RHTPA 2.1.1 (0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: transitive (unverified — confirm via `cargo tree -i quinn-proto`)
- Dependency is production/runtime scope; no `dev-dependency` label

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto
- Bump it to a version whose transitive closure includes quinn-proto >= 0.11.14
  (0.11.9 → 0.11.14 is semver-compatible, so `cargo update -p quinn-proto` may suffice)
- Verify the bump does not introduce breaking API changes to the direct dependency

**Fallback: pin the transitive dependency directly**
- Cargo: `cargo add quinn-proto@0.11.14` to override the transitive resolution
- Document why the direct dep bump was not viable in the PR description

(If `cargo tree` shows quinn-proto is a direct dependency, simply update it to
>= 0.11.14 in Cargo.lock.)

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE
assignment, advisory preparation, and formal disclosure. Fix must be released via
a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (originating tracking issue, stream 2.2.x — Related link)
```

## Task 4 (preemptive) — Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)

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
CVE-2026-31812 fix from <TASK-3-KEY>.

The upstream backport (<TASK-3-KEY>) bumps quinn-proto to 0.11.14 on
release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: transitive (unverified) — carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback
  approach), verify the pinning is reflected in the downstream build's
  lock file after the source reference update
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE
assignment, advisory preparation, and formal disclosure. Fix must be released via
a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <TASK-3-KEY> (upstream backport must merge first)
- Depends on: TC-8001 (originating tracking issue — Related link)
```

---

## Planned Jira operations (order; all require confirmation)

1. Create Task 1 → post description digest comment.
2. Create Task 2 → post description digest comment.
3. Links: TC-8001 → Task 1 (Depend), TC-8001 → Task 2 (Depend), Task 1 → Task 2 (Blocks).
4. Release linking (Step 7.5, 2.2.x release Task): Task 1 and Task 2 → release Task (Blocks). Release Task → TC-8001 (Related).
5. Create Task 3 and Task 4 (preemptive) → digest comment on each. Links: TC-8001 → Task 3/4 (Related), Task 3 → Task 4 (Blocks). Preemptive tasks are not linked to release Jira.
6. Cross-stream impact comment on TC-8001:
   "Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x based on lock file analysis. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage."
7. Preemptive task-list comment on TC-8001 ("Preemptive remediation tasks created for streams without CVE Jiras: 2.1.x: <TASK-3-KEY>, <TASK-4-KEY> (security-preemptive) ...").
8. Remediation task-list comment: "Remediation tasks created: <TASK-1-KEY> (dependency bump), <TASK-2-KEY> (downstream propagation, blocked by <TASK-1-KEY>)".
9. TC-8001: already assigned and in Assigned (an indeterminate status) from Step 0.8, so the In Progress transition is skipped.
10. Add label `ai-cve-triaged`. Post the post-triage summary with the version impact table, the Affects Versions correction (RHTPA 2.0.0 → RHTPA 2.2.0, 2.2.1, 2.2.2), task links, release Jira refs, and an @mention of the reporter.

Every comment ends with the `triage-security` Comment Footnote (`shared/comment-footnote.md`).

## Pre-creation checklist

- [x] Task count per stream: 2 per stream (Cargo, a source dependency)
- [x] Cross-stream coverage: 2.1.x is covered by preemptive tasks #3 and #4
- [x] Link types: Depend (own CVE), Related (preemptive), Blocks (upstream → downstream)
- [x] Preemptive labels: `security-preemptive` on #3 and #4
- [x] Coordination guidance: the **customer-shipped** subsection is in the Implementation Notes of all 4 tasks (rhtpa-backend deployment context)
- [x] Release Jira linking: only the non-preemptive tasks #1 and #2 link to the release Task
- [x] Dedup consistency: no Step 7.5.3 dedup (Upstream Affected Component field not configured)
