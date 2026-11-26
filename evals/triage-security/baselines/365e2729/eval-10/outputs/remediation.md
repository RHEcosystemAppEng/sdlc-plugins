# TC-8020 — Remediation (Step 8)

## Decision

| Check | Result |
|---|---|
| Any supported versions affected? | Yes |
| Issue scoped to a single stream? | Yes, `[rhtpa-2.2]` (2.2.x) |
| Other streams affected? | Yes, rhtpa-2.1 (2.1.x): tokio 1.40.0 < 1.42.0 |
| Sibling CVE Jira for rhtpa-2.1? | **None** (JQL returned no results) |
| Ecosystem | Cargo, a source dependency, so 2 tasks per stream |
| Upstream fix confirmed on branch? | No, so use upstream backport + downstream propagation |

**Outcome:** Case A, because the issue is scoped and another stream is affected:
- Post the cross-stream comment (see cross-stream.md).
- Create **preemptive** tasks for rhtpa-2.1, which has no CVE Jira.
- Create Case B standard remediation tasks for the in-scope stream rhtpa-2.2.

Total: **4 Tasks**: 2 standard (rhtpa-2.2) and 2 preemptive (rhtpa-2.1). No Vulnerability issues are created.

The parent security level is copied from TC-8020's `security` field to every created Task. It is omitted only if TC-8020 has none.

---

# Part 1 — Current stream rhtpa-2.2: standard tasks (Case B, triggered via Case A)

## Task 1 — Upstream backport (rhtpa-2.2)

- **Project**: TC | **Type**: Task
- **Summary**: `Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)`
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`
- **Security**: <TC-8020 security level>
- **Ref**: `upstream-rhtpa-2.2`

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: tokio use-after-free when a spawned task is aborted
while holding a borrowed reference (memory corruption / potential code execution, CVSS 8.1).
The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed version (1.42.0+).

Affected versions: RHTPA 2.2.0 (tokio 1.41.1), RHTPA 2.2.1 (tokio 1.41.1), RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (verify with `cargo tree -i tokio`)
- Runtime dependency, not dev-only. No `dev-dependency` label.

### Remediation approach (direct dependency)

- Update tokio dependency to >= 1.42.0 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

If tokio turns out to be transitive:
**Preferred: bump the direct dependency** whose transitive closure includes tokio >= 1.42.0.
**Fallback:** `cargo add tokio@1.42.0` to override the transitive resolution, and document
in the PR why the direct dependency bump was not viable.

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8020 (parent tracking issue)
```

## Task 2 — Downstream propagation (rhtpa-2.2)

- **Summary**: `Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)`
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`
- **Security**: <TC-8020 security level>
- **Ref**: `downstream-rhtpa-2.2`

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-55123 fix from {{upstream-rhtpa-2.2.key}}.

The upstream backport ({{upstream-rhtpa-2.2.key}}) bumps tokio to 1.42.0
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: direct, carried forward from the upstream task
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

- Depends on: {{upstream-rhtpa-2.2.key}} (upstream backport must merge first)
- Depends on: TC-8020 (parent tracking issue)
```

## rhtpa-2.2 operation order (needs confirmation)
1. Create Task 1. Post the description digest comment `[sdlc-workflow] Description digest: sha256-...` before any links.
2. Create Task 2. Post its description digest comment.
3. Link TC-8020 (inward) to Task 1 (outward), type **Depend**.
4. Link TC-8020 (inward) to Task 2 (outward), type **Depend**.
5. Link Task 1 (inward) to Task 2 (outward), type **Blocks** (upstream blocks downstream).
6. Release Jira, if Step 7.5 confirms "RHTPA 2.2.5 CVE triage":
   - Task 1 to release Task, type **Blocks**
   - Task 2 to release Task, type **Blocks**
   - Release Task (inward) to TC-8020 (outward), type **Related**
7. TC-8020 is already Assigned after Step 0.8, which counts as an in-progress-equivalent status, so the transition is skipped.
8. Comment on TC-8020: "Remediation tasks created: {{upstream-rhtpa-2.2.key}} (upstream backport), {{downstream-rhtpa-2.2.key}} (downstream propagation, blocked by {{upstream-rhtpa-2.2.key}})", followed by the footnote.

---

# Part 2 — Other stream rhtpa-2.1: preemptive tasks (Case A, step 3)

These tasks exist because rhtpa-2.1 is affected (tokio 1.40.0, threshold 1.42.0) and **no CVE Jira exists** for CVE-2026-55123 in that stream. Differences from standard tasks:
- They carry the extra label `security-preemptive`.
- The Description has a preemptive prefix.
- They link to TC-8020 with **Related**, not Depend.
- They are not linked to release Jira.

## Task 3 — Upstream backport, preemptive (rhtpa-2.1)

- **Summary**: `Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)`
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`
- **Security**: <TC-8020 security level>
- **Ref**: `preemptive-upstream-rhtpa-2.1`

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
while holding a borrowed reference (memory corruption / potential code execution, CVSS 8.1).
The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed version (1.42.0+).

Affected versions: RHTPA 2.1.0 (tokio 1.40.0), RHTPA 2.1.1 (tokio 1.40.0)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (verify with `cargo tree -i tokio`)
- Runtime dependency, not dev-only. No `dev-dependency` label.
- The jump from 1.40.0 to 1.42.0 crosses two minor versions. Review the tokio changelog for MSRV
  and behavior changes on the older 0.3.z branch.

### Remediation approach (direct dependency)

- Update tokio dependency to >= 1.42.0 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

If tokio turns out to be transitive:
**Preferred: bump the direct dependency** whose transitive closure includes tokio >= 1.42.0.
**Fallback:** `cargo add tokio@1.42.0` to override the transitive resolution, and document
in the PR why the direct dependency bump was not viable.

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8020 (originating CVE Jira, stream rhtpa-2.2; no rhtpa-2.1 CVE Jira yet)
```

## Task 4 — Downstream propagation, preemptive (rhtpa-2.1)

- **Summary**: `Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)`
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`
- **Security**: <TC-8020 security level>
- **Ref**: `preemptive-downstream-rhtpa-2.1`

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
CVE-2026-55123 fix from {{preemptive-upstream-rhtpa-2.1.key}}.

The upstream backport ({{preemptive-upstream-rhtpa-2.1.key}}) bumps tokio to 1.42.0
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: direct, carried forward from the upstream task
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

- Depends on: {{preemptive-upstream-rhtpa-2.1.key}} (upstream backport must merge first)
- Related to: TC-8020 (originating CVE Jira, stream rhtpa-2.2)
```

## rhtpa-2.1 operation order (needs confirmation)
1. Create Task 3. Post its description digest comment before any links.
2. Create Task 4. Post its description digest comment.
3. Link TC-8020 (inward) to Task 3 (outward), type **Related**.
4. Link TC-8020 (inward) to Task 4 (outward), type **Related**.
5. Link Task 3 (inward) to Task 4 (outward), type **Blocks**.
6. **No** release Jira linking, because the tasks are preemptive.
7. Post the preemptive task list comment on TC-8020 (see cross-stream.md).

---

## Pre-creation checklist

- [x] Task count per stream: Cargo is a source dependency, so 2 per stream (2.2.x: 2, 2.1.x: 2)
- [x] Cross-stream coverage: rhtpa-2.1 has no sibling CVE Jira, so it gets preemptive tasks
- [x] Link types: Depend (2.2 tasks to TC-8020), Related (2.1 preemptive tasks to TC-8020), Blocks (upstream to downstream within each stream)
- [x] Preemptive labels: `security-preemptive` on Tasks 3 and 4 only
- [x] Coordination guidance: the Deployment Context column is absent, so it is omitted per backward compatibility
- [x] Release Jira linking: only the non-preemptive Tasks 1 and 2 link to the release Task, plus the TC-8020 Related link to the release Task
- [x] Dedup consistency: dedup was skipped (field not configured) and no streams are marked dedup'd
- [x] No Vulnerability issues are created

## Post-triage (needs confirmation)
- Add label `ai-cve-triaged` to TC-8020.
- Post the summary comment. It includes the impact table, the Affects Versions correction, the outcome, the 4 task keys, the release Epic/Task keys, a "Dedup: not applicable" note, an ADF @mention of the TC-8020 **reporter** (account ID taken from the issue data), and the footnote.
- Note: the due date 2026-08-15 has already passed. Flag this to the engineer for prioritization.
