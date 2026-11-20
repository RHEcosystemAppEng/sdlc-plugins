# Step 8 – Remediation: TC-8001 / CVE-2026-31812 (quinn-proto < 0.11.14)

## Decision

- Embargo gate (Step 1.7): presented. Proceeding assumes the engineer answered **Yes**.
- The issue is **scoped** to 2.2.x, and 2.2.0–2.2.2 are affected, so this is **Case B** for 2.2.x.
- Stream 2.1.x, outside the scope, is also affected (2.1.0 and 2.1.1), so this is also **Case A**: a cross-stream comment plus preemptive tasks for 2.1.x. These tasks are needed only if Step 4 finds no 2.1.x sibling CVE Jira. In this eval the sibling search could not run, so the plan assumes there is no sibling.
- Ecosystem: Cargo, a source dependency, so **2 tasks per stream**.
  - 2.2.x: dependency-bump variant, because the fix is already on release/0.4.z and shipped in 2.2.3 and later. Then a downstream propagation task.
  - 2.1.x: upstream backport, because the fix has not been confirmed on release/0.3.z. Then a downstream propagation task.
- Steps 4–7 were not executed (they need Jira/JQL and the lifecycle page). Step 7.5 needs a release Epic and Task such as "RHTPA 2.2.5 Release Tasks" and "RHTPA 2.2.5 CVE triage" (default next patch after 2.2.4), confirmed individually. That is not executed here.
- Coordination Guidance is omitted. The Source Repositories table has no Deployment Context column (backward compatibility).
- Every Jira mutation below requires explicit engineer confirmation before it runs. Nothing was sent to Jira.

## Cross-stream impact comment (Case A) for TC-8001

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x
(RHTPA 2.1.0, 2.1.1 ship quinn-proto 0.11.9) based on lock file analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

---
_Posted by sdlc-workflow/triage-security_
```

---

## Task 1 – 2.2.x dependency bump (Case B)

- **Summary**: Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x)
- **Labels**: ai-generated-jira, Security, CVE-2026-31812
- **Links**: TC-8001 → Depend → this task. This task Blocks Task 2. This task Blocks the 2.2.x release Task (if Step 7.5 is active).

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
RHTPA 2.2.2 (retag of 2.2.1). RHTPA 2.2.3 and 2.2.4 already ship 0.11.14.
Source commit(s): v0.4.5, v0.4.8 (affected); v0.4.11, v0.4.12 (fixed)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: to be confirmed (expected transitive via quinn; verify with
  `cargo tree -i quinn-proto`)
- **Remediation action**: run `cargo update -p quinn-proto` to pull in the latest
  compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify Cargo.lock reflects >= 0.11.14 after the update. Released tags v0.4.11 and
  v0.4.12 already ship 0.11.14, so release/0.4.z HEAD is expected to be compliant;
  if so, confirm and record the fixing commit rather than making a new change.
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

## Task 2 – 2.2.x downstream propagation (Case B)

- **Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)
- **Labels**: ai-generated-jira, Security, CVE-2026-31812
- **Links**: TC-8001 → Depend → this task. Blocked by Task 1. This task Blocks the 2.2.x release Task (if Step 7.5 is active).

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <Task 1 key>.

The dependency bump (<Task 1 key>) ensures quinn-proto is 0.11.14
on release/0.4.z. Once that is confirmed/merged, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: to be confirmed — carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
  (must be v0.4.11 or later; current latest pin v0.4.12 already ships 0.11.14)
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

- Depends on: <Task 1 key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

## Task 3 – 2.1.x upstream backport (Case A, preemptive)

- **Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)
- **Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
- **Links**: TC-8001 → Related → this task. This task Blocks Task 4. No release-Task link, because the task is preemptive.

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

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (remote DoS via
crafted STREAMS frame). The vulnerable dependency (quinn-proto < 0.11.14) must be
updated to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (quinn-proto 0.11.9), RHTPA 2.1.1 (quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: to be confirmed (expected transitive via quinn; verify with
  `cargo tree -i quinn-proto`)
- If the vulnerable dependency is dev-only or build-only, the remediation priority
  is Normal regardless of CVE severity. Add `dev-dependency` label to the task.

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (likely quinn)
- Bump it to a version whose transitive closure includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes

**Fallback: pin the transitive dependency directly**
- Cargo: `cargo add quinn-proto@0.11.14` (or `cargo update -p quinn-proto --precise 0.11.14`)
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

## Task 4 – 2.1.x downstream propagation (Case A, preemptive)

- **Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)
- **Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
- **Links**: TC-8001 → Related → this task. Blocked by Task 3.

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
CVE-2026-31812 fix from <Task 3 key>.

The upstream backport (<Task 3 key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
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

- Depends on: <Task 3 key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

## Post-creation actions (each needs confirmation; not executed)

1. Post a description digest comment on each task (`[sdlc-workflow] Description digest: <tagged-digest>`), before any links.
2. Create the links listed above: Depend for Tasks 1–2, Related for Tasks 3–4, and Blocks from upstream to downstream. Link Tasks 1–2 to the 2.2.x release Task (Blocks), and link TC-8001 to the release Task (Related).
3. Update Affects Versions: RHTPA 2.0.0 → RHTPA 2.2.0, 2.2.1, 2.2.2.
4. Leave TC-8001 in Assigned (an indeterminate status), so no In Progress transition is needed.
5. Add a comment listing the preemptive tasks for 2.1.x (Tasks 3–4), with the Comment Footnote.
6. Add the `ai-cve-triaged` label.
7. Post a summary comment covering the impact table, the Affects Versions correction, the task links, the release Jira references, and an @mention of the reporter, plus the Comment Footnote.

## Pre-creation checklist

- [x] Task count per stream: 2 per stream (Cargo is a source dependency)
- [x] Cross-stream coverage: 2.1.x has preemptive tasks (pending the Step 4 sibling check)
- [x] Link types: Depend (own CVE), Related (preemptive), Blocks (upstream → downstream)
- [x] Preemptive labels on Tasks 3–4
- [x] Coordination guidance: omitted (no Deployment Context column)
- [ ] Release Jira linking: depends on Step 7.5, which was not executed
- [ ] Dedup consistency: depends on Step 7.5.3, which was not executed
