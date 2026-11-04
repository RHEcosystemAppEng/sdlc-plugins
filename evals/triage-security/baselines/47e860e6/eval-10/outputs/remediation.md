# Step 8 – Remediation: TC-8020 (CVE-2026-55123, tokio < 1.42.0)

## Decision

- Supported versions are affected, so this is not Case C.
- The issue is **scoped** (`[rhtpa-2.2]`) and another stream (2.1.x / rhtpa-2.1) is also affected, so **Case A** applies: post the cross-stream impact comment and create preemptive tasks for 2.1.x, which has no CVE Jira.
- Stream 2.2.x, which is in scope, gets **Case B** standard remediation.
- Ecosystem: Cargo, a source dependency, so **2 tasks per stream**. Step 2.5 did not confirm an upstream fix, so each stream uses the upstream backport task plus the downstream propagation task.
- Total: **4 remediation Tasks** (2 standard for rhtpa-2.2, 2 preemptive for rhtpa-2.1).
- No Vulnerability issues are created. PSIRT owns those.

All Jira mutations below need engineer confirmation. None were executed in this eval.

---

## Case B – Stream 2.2.x (rhtpa-2.2): standard remediation tasks

### Task 1 – Upstream backport (2.2.x)

- **Summary:** `Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)`
- **Issue type:** Task, project TC
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-55123`
- **Links:** TC-8020 → task (**Depend**); task → release Task "RHTPA <2.2.z> CVE triage" (**Blocks**), if Step 7.5 is active

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: tokio use-after-free when a spawned task is aborted
while holding a borrowed reference (memory corruption / potential code execution).
The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed version (1.42.0+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 (retag of 2.2.1); RHTPA 2.2.3 / 2.2.4 pending lock file verification
Source commit(s): v0.4.5, v0.4.8 (tokio 1.41.1)

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (to be confirmed with `cargo tree -i tokio`)
- tokio is a runtime dependency (not dev-only) — priority follows CVE severity.

### Remediation approach (direct dependency)

- Update tokio dependency to >= 1.42.0 in Cargo.lock (`cargo update -p tokio`, raising the Cargo.toml requirement if needed)
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

If `cargo tree` shows tokio is only pulled transitively:
- Preferred: bump the direct dependency to a version whose transitive closure includes tokio >= 1.42.0
- Fallback: `cargo add tokio@1.42.0` to override the transitive resolution; document why in the PR

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8020 (parent tracking issue)
```

### Task 2 – Downstream propagation (2.2.x)

- **Summary:** `Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-55123`
- **Links:** TC-8020 → task (**Depend**); Task 1 → Task 2 (**Blocks**); task → release Task (**Blocks**), if active

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-55123 fix from <Task 1 key>.

The upstream backport (<Task 1 key>) bumps tokio to 1.42.0 on release/0.4.z.
Once that PR merges, update the source pinning in this Konflux release repo so
the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: direct — carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly, verify it is reflected in the downstream build's lock file
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <Task 1 key> (upstream backport must merge first)
- Depends on: TC-8020 (parent tracking issue)
```

---

## Case A – Stream 2.1.x (rhtpa-2.1): preemptive tasks

Sibling JQL found **no CVE Jira** for CVE-2026-55123 in rhtpa-2.1, so preemptive tasks are created using the Preemptive Task Variant.

### Task 3 – Upstream backport (2.1.x, preemptive)

- **Summary:** `Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`
- **Links:** TC-8020 → task (**Related**, not Depend). Not linked to release Jira.

```
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-55123: tokio use-after-free when a spawned task is aborted
while holding a borrowed reference. The vulnerable dependency (tokio < 1.42.0)
must be updated to the fixed version (1.42.0+).

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
Source commit(s): v0.3.8, v0.3.12 (tokio 1.40.0)

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (to be confirmed with `cargo tree -i tokio`)
- tokio is a runtime dependency (not dev-only) — priority follows CVE severity.
- Note: 1.40.0 → 1.42.0 spans two minor releases; check MSRV and API changes on the 0.3.z branch.

### Remediation approach (direct dependency)

- Update tokio dependency to >= 1.42.0 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable

### Remediation approach (transitive dependency)

- Preferred: bump the direct dependency whose closure includes tokio >= 1.42.0
- Fallback: `cargo add tokio@1.42.0`; document why in the PR

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8020 (originating CVE Jira, stream rhtpa-2.2)
```

### Task 4 – Downstream propagation (2.1.x, preemptive)

- **Summary:** `Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`
- **Links:** TC-8020 → task (**Related**); Task 3 → Task 4 (**Blocks**). Not linked to release Jira.

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-55123 fix from <Task 3 key>.

The upstream backport (<Task 3 key>) bumps tokio to 1.42.0 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release repo so
the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: direct — carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <Task 3 key> (upstream backport must merge first)
- Related to: TC-8020 (originating CVE Jira, stream rhtpa-2.2)
```

---

## Execution order (after confirmation)

1. Create Task 1, then post its description digest comment (`[sdlc-workflow] Description digest: sha256-...`) before any links.
2. Create Task 2, then post its digest.
3. Links: TC-8020 → Task 1 (Depend), TC-8020 → Task 2 (Depend), Task 1 → Task 2 (Blocks), Tasks 1 and 2 → release Task (Blocks), release Task → TC-8020 (Related).
4. Create Task 3, then post its digest. Create Task 4, then post its digest.
5. Links: TC-8020 → Task 3 (Related), TC-8020 → Task 4 (Related), Task 3 → Task 4 (Blocks).
6. Comments on TC-8020: the task-list comment, the cross-stream impact comment, and the preemptive task list (see cross-stream.md). Each ends with the footnote.
7. Move TC-8020 to In Progress, or skip if it is already in Assigned or a later indeterminate status. Assign it to the current user.
8. Add the `ai-cve-triaged` label and post the summary comment, including an @mention of the reporter and the footnote.

Task-list comment for TC-8020:

```
Remediation tasks created: <Task 1 key> (upstream backport), <Task 2 key> (downstream propagation, blocked by <Task 1 key>)

---
This comment was AI-generated by sdlc-workflow/triage-security v0.13.10.
```

## Pre-creation checklist

- [x] Task count per stream: Cargo, so 2 tasks per stream (2.2.x: 2, 2.1.x: 2)
- [x] Cross-stream coverage: 2.1.x has no sibling CVE Jira, so it gets preemptive tasks
- [x] Link types: Depend for the 2.2.x tasks to TC-8020; Related for the 2.1.x preemptive tasks to TC-8020; Blocks from upstream to downstream within each stream
- [x] Preemptive labels: `security-preemptive` on Tasks 3 and 4 only
- [x] Coordination guidance: omitted, because Source Repositories has no Deployment Context column
- [x] Release Jira linking: only the non-preemptive 2.2.x tasks are linked to the release Task (Blocks), and TC-8020 is linked to it (Related)
- [x] Dedup consistency: Step 7.5.3 found no dedup (Upstream Affected Component field not configured)
