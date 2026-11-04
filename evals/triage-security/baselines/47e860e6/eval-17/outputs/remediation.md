# TC-8001 — Steps 4–8 and Remediation Task Descriptions

## Steps 4–7 (not executed against Jira in this eval)
- **Step 4 (duplicates and siblings):** the JQL for `labels = CVE-2026-31812` was not run. For this plan, assume no sibling 2.1.x CVE Jira exists. The engineer must confirm this in a live run.
- **Step 4.3 and Step 7:** skipped, because the Upstream Affected Component field is not configured.
- **Step 5 (lifecycle):** the product pages were not fetched. 2.1.x and 2.2.x are treated as supported.
- **Step 6 (already fixed):** no resolved siblings are known.
- **Step 7.5 (release Jira):** the release Epic/Task search and creation were not run. Each would need individual confirmation in a live run. Release-Task linking below is marked as conditional.

## Step 8 decision
- The issue is **scoped** (2.2.x), and 2.2.0–2.2.2 are affected, so **Case B** applies to 2.2.x.
- Another stream (2.1.x) is also affected, so **Case A** applies: a cross-stream comment plus preemptive tasks for 2.1.x, since it has no CVE Jira of its own.
- The ecosystem is Cargo (source dependency), so each stream gets 2 tasks.
  - 2.2.x: release/0.4.z already ships quinn-proto 0.11.14, so the **dependency bump + downstream propagation** variant is used.
  - 2.1.x: release/0.3.z is still at 0.11.9 as of v0.3.12, so the **upstream backport + downstream propagation** variant is used, with the preemptive label.

> Note for the engineer at the confirmation gate: in 2.2.x the fix already shipped in 2.2.3
> (v0.4.11) and 2.2.4 (v0.4.12). The 2.2.x tasks therefore mostly verify that the fix holds and
> ensure the Konflux reference stays at or above v0.4.11. You may decide they are unnecessary.

### Case A cross-stream comment (to be posted on TC-8001 after confirmation)
```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x
(2.1.0, 2.1.1 ship quinn-proto 0.11.9) based on lock file analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

---
_Posted by sdlc-workflow/triage-security_
```

---

## Task 1 — 2.2.x dependency bump (standard, linked to TC-8001 with "Depend")

**Summary:** Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x)
**Labels:** ai-generated-jira, Security, CVE-2026-31812

```
## Repository

backend (rhtpa-backend)

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream —
a package manager update is sufficient.

Affected versions: 2.2.0 (v0.4.5, quinn-proto 0.11.9), 2.2.1 (v0.4.8, 0.11.12),
2.2.2 (retag of 2.2.1, v0.4.8)
Source commit(s): v0.4.5, v0.4.8
Not affected: 2.2.3 (v0.4.11) and 2.2.4 (v0.4.12) already ship quinn-proto 0.11.14

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: to be confirmed — likely transitive (chain: backend → quinn → quinn-proto); verify with `cargo tree -i quinn-proto`
- **Remediation action**: `cargo update -p quinn-proto`
- If the update pulls a version still < 0.11.14, pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify Cargo.lock reflects quinn-proto >= 0.11.14 after the update
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

**Summary:** Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)
**Labels:** ai-generated-jira, Security, CVE-2026-31812

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
- **Dependency type**: to be confirmed (likely transitive) — carried forward from upstream task
- Update the backend reference to the merged commit or new release tag (must be >= v0.4.11)
- If the upstream fix pinned a transitive dependency directly (fallback approach),
  verify the pinning is reflected in the downstream build's lock file
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

## Task 3 — 2.1.x upstream backport (PREEMPTIVE, linked to TC-8001 with "Related")

**Summary:** Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)
**Labels:** ai-generated-jira, Security, CVE-2026-31812, security-preemptive

```
## Repository

backend (rhtpa-backend)

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic (DoS) on excessive stream counts
in a QUIC STREAMS frame. The vulnerable dependency (quinn-proto < 0.11.14) must
be updated to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8, quinn-proto 0.11.9), 2.1.1 (v0.3.12, quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: to be confirmed — likely transitive (chain: backend → quinn → quinn-proto)
- If the vulnerable dependency is dev-only or build-only, the remediation priority
  is Normal regardless of CVE severity. Add `dev-dependency` label to the task.

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level
  workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (e.g., quinn / reqwest)
- Bump it to a version whose transitive closure includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes

**Fallback: pin the transitive dependency directly**
- `cargo add quinn-proto@0.11.14` to override the transitive resolution
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

**Summary:** Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)
**Labels:** ai-generated-jira, Security, CVE-2026-31812, security-preemptive

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

The upstream backport (<Task 3 key>) bumps quinn-proto to 0.11.14 on
release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: to be confirmed (likely transitive) — carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback approach),
  verify the pinning is reflected in the downstream build's lock file
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

## Planned Jira operations (each requires engineer confirmation; none executed)
1. Create each task, then post its description digest comment (`[sdlc-workflow] Description digest: <sha256>`) before any links or comments on that task.
2. Links:
   - TC-8001 → Task 1 and TC-8001 → Task 2 (Depend).
   - TC-8001 → Task 3 and TC-8001 → Task 4 (Related, preemptive).
   - Task 1 Blocks Task 2. Task 3 Blocks Task 4.
3. If Step 7.5 produced an RHTPA 2.2.x release Task: Tasks 1 and 2 Block the release Task, and TC-8001 is Related to it. The preemptive tasks are not release-linked.
4. Set Affects Versions to RHTPA 2.2.0, 2.2.1, 2.2.2, replacing RHTPA 2.0.0.
5. Transition TC-8001 to In Progress, using the status discovered from the live workflow.
6. Post a comment listing the tasks (standard and preemptive), add the `ai-cve-triaged` label, and post the post-triage summary comment. The summary includes the impact table, the Affects Versions correction, links to the tasks, an @mention of the reporter, and the comment footnote.

## Pre-creation checklist
- [x] Task count per stream: Cargo gives 2 tasks for 2.2.x and 2 tasks for 2.1.x
- [x] Cross-stream coverage: 2.1.x has preemptive tasks (assuming no sibling CVE Jira)
- [x] Link types: Depend for own CVE, Related for preemptive, Blocks for upstream to downstream
- [x] Preemptive labels on the 2.1.x tasks
- [x] Coordination guidance omitted, because the Deployment Context column is absent (backward compatibility)
- [ ] Release Jira linking: depends on Step 7.5 (not run)
- [x] Dedup consistency: no dedup'd streams (Step 7.5.3 not applicable without the Upstream Affected Component field)
