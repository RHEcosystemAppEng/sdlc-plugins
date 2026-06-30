# Step 7 — Remediation: CVE-2026-55123

## Triage Outcome

The version impact analysis confirms affected versions in **two streams**:

- **Stream rhtpa-2.2** (in-scope): RHTPA 2.2.0, RHTPA 2.2.1 — tokio 1.41.1 < 1.42.0
- **Stream rhtpa-2.1** (out-of-scope): RHTPA 2.1.0, RHTPA 2.1.1 — tokio 1.40.0 < 1.42.0

This triggers both **Case A** (remediation for the current stream) and **Case B** (preemptive remediation for the other stream).

---

## Case A: Remediation Tasks for Stream rhtpa-2.2 (Current Stream)

Ecosystem: Cargo (source dependency) — **two tasks** required: upstream backport + downstream propagation.

### Task 1: Upstream Backport Task

**Summary**: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`

**Description**:

> ## Repository
>
> rhtpa-backend
>
> ## Target Branch
>
> release/0.4.z
>
> ## Description
>
> Remediate CVE-2026-55123: use-after-free in task abort in the tokio crate.
> The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed version (1.42.0+).
>
> Affected versions: RHTPA 2.2.0, RHTPA 2.2.1
> Source commit(s): v0.4.5 (2.2.0), v0.4.8 (2.2.1)
>
> Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
> Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp
>
> ## Implementation Notes
>
> - Update tokio dependency to >= 1.42.0 in Cargo.lock
> - Target branch: release/0.4.z
> - Check for pinned versions or transitive dependency constraints
>   that might prevent the bump
> - If a direct bump introduces breaking changes, assess whether a
>   code-level workaround is viable (see upstream changelog)
>
> ## Acceptance Criteria
>
> - [ ] tokio dependency is >= 1.42.0
> - [ ] No other dependency conflicts introduced
> - [ ] Existing tests pass
>
> ## Test Requirements
>
> - [ ] Existing test suite passes with the updated dependency
>
> ## Dependencies
>
> - Depends on: TC-8020 (parent tracking issue)

**Linkage**: Link to TC-8020 with type "Depend"

---

### Task 2: Downstream Propagation Subtask

**Summary**: Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`

**Description**:

> ## Repository
>
> rhtpa-release.0.4.z
>
> ## Target Branch
>
> main
>
> ## Description
>
> Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
> CVE-2026-55123 fix from the upstream backport task.
>
> The upstream backport bumps tokio to 1.42.0 on release/0.4.z. Once that
> PR merges, update the source pinning in this Konflux release repo so the
> next build ships the fix.
>
> ## Implementation Notes
>
> - Source pinning method: artifacts.lock.yaml (download URL contains tag)
> - Update the rhtpa-backend reference to the merged commit or new release tag
> - Verify the Konflux build pipeline triggers successfully
>
> ## Acceptance Criteria
>
> - [ ] rhtpa-backend reference updated to include the fix
> - [ ] Konflux rebuild triggers new container image
>
> ## Test Requirements
>
> - [ ] Container image builds successfully with the updated reference
>
> ## Dependencies
>
> - Depends on: upstream backport task (upstream backport must merge first)
> - Depends on: TC-8020 (parent tracking issue)

**Linkage**:
- Link to TC-8020 with type "Depend"
- Link downstream subtask as blocked by upstream task with type "Blocks"

---

## Case B: Preemptive Remediation Tasks for Stream rhtpa-2.1

Stream rhtpa-2.1 is affected (tokio 1.40.0 < 1.42.0) but has **no CVE Jira** for this CVE. Preemptive remediation tasks are created with the `security-preemptive` label and "Related" link type.

### Preemptive Task 1: Upstream Backport Task (rhtpa-2.1)

**Summary**: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`

**Description**:

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.
>
> ## Repository
>
> rhtpa-backend
>
> ## Target Branch
>
> release/0.3.z
>
> ## Description
>
> Remediate CVE-2026-55123: use-after-free in task abort in the tokio crate.
> The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed version (1.42.0+).
>
> Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
> Source commit(s): v0.3.8 (2.1.0), v0.3.12 (2.1.1)
>
> Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
> Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp
>
> ## Implementation Notes
>
> - Update tokio dependency to >= 1.42.0 in Cargo.lock
> - Target branch: release/0.3.z
> - Check for pinned versions or transitive dependency constraints
>   that might prevent the bump
> - If a direct bump introduces breaking changes, assess whether a
>   code-level workaround is viable (see upstream changelog)
>
> ## Acceptance Criteria
>
> - [ ] tokio dependency is >= 1.42.0
> - [ ] No other dependency conflicts introduced
> - [ ] Existing tests pass
>
> ## Test Requirements
>
> - [ ] Existing test suite passes with the updated dependency
>
> ## Dependencies
>
> - Depends on: TC-8020 (originating CVE Jira — cross-stream)

**Linkage**: Link to TC-8020 with type "Related" (not "Depend" — different stream)

---

### Preemptive Task 2: Downstream Propagation Subtask (rhtpa-2.1)

**Summary**: Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`

**Description**:

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.
>
> ## Repository
>
> rhtpa-release.0.3.z
>
> ## Target Branch
>
> main
>
> ## Description
>
> Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
> CVE-2026-55123 fix from the upstream backport task.
>
> The upstream backport bumps tokio to 1.42.0 on release/0.3.z. Once that
> PR merges, update the source pinning in this Konflux release repo so the
> next build ships the fix.
>
> ## Implementation Notes
>
> - Source pinning method: artifacts.lock.yaml (download URL contains tag)
> - Update the rhtpa-backend reference to the merged commit or new release tag
> - Verify the Konflux build pipeline triggers successfully
>
> ## Acceptance Criteria
>
> - [ ] rhtpa-backend reference updated to include the fix
> - [ ] Konflux rebuild triggers new container image
>
> ## Test Requirements
>
> - [ ] Container image builds successfully with the updated reference
>
> ## Dependencies
>
> - Depends on: preemptive upstream backport task (upstream backport must merge first)
> - Depends on: TC-8020 (originating CVE Jira — cross-stream)

**Linkage**:
- Link to TC-8020 with type "Related" (not "Depend" — different stream)
- Link downstream subtask as blocked by upstream preemptive task with type "Blocks"

---

## Post-Triage Actions

1. **Add label** `ai-cve-triaged` to TC-8020
2. **Transition** TC-8020 to In Progress
3. **Assign** TC-8020 to current user
4. **Post summary comment** to TC-8020 documenting the version impact table, Affects Versions correction, and all created remediation tasks (both Case A and Case B)
