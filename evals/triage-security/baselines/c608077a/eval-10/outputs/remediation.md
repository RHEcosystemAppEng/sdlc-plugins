# TC-8020 — Remediation (Steps 7.5 and 8)

## Decision

- Supported versions are affected, so this is not Case C.
- The issue is **scoped** (`[rhtpa-2.2]`) and another stream (**rhtpa-2.1**) is also affected. That triggers **Case A**: a cross-stream comment, then preemptive tasks for streams without a CVE Jira.
- The current stream rhtpa-2.2 is affected, which triggers **Case B**: standard remediation tasks.
- Ecosystem is Cargo, a source dependency, so each stream gets **2 tasks**. Upstream fix status is unknown, so the upstream backport variant is used.
- Totals: **4 tasks**. Two are standard (rhtpa-2.2) and two are preemptive (rhtpa-2.1).

Task keys below are placeholders (`<TASK-A>` and so on) because no Jira writes are made in this eval.

---

## Step 7.5 – Release Jira orchestration (rhtpa-2.2 only)

Preemptive tasks are not linked to release Jira ("All non-preemptive remediation types are linked to release Jira"), so release orchestration runs only for stream 2.2.x.

- 7.5.1: Search `project = TC AND issuetype = Epic AND summary ~ 'RHTPA 2.2' AND summary ~ 'Release Tasks'`. If nothing is found, the default version is the next patch after the latest matrix release 2.2.4, which is **RHTPA 2.2.5**. Prompt: Accept / Specify / Skip. Then create Epic `RHTPA 2.2.5 Release Tasks` (labels `ai-generated-jira`) and post its digest comment.
- 7.5.2: Find or create Task `RHTPA 2.2.5 CVE triage` as a child of the Epic (individual confirmation), then post its digest comment. Its key is referred to below as `<RELEASE-TASK>`.
- 7.5.3: Cross-CVE dedup is **skipped** because the Upstream Affected Component field is not configured. No stream is dedup'd.

---

## Case B — Standard remediation tasks for rhtpa-2.2 (current stream)

### Task A — Upstream backport (rhtpa-2.2)

- **Summary**: `Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)`
- **Issue type**: Task, project TC
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`
- **Description**:

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: tokio use-after-free when a spawned task is aborted
while holding a borrowed reference (memory corruption / potential code execution).
The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed version (1.42.0+).

Affected versions: RHTPA 2.2.0 (tokio 1.41.1), RHTPA 2.2.1 (tokio 1.41.1),
RHTPA 2.2.2 (retag of 2.2.1); RHTPA 2.2.3 / 2.2.4 pending verification
Source commit(s): backend v0.4.5, v0.4.8 (from security-matrix.md)

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: undetermined (no dependency-chain evidence available during
  triage), so confirm with `cargo tree -i tokio`
- tokio is a runtime dependency (not dev-only or build-only), so standard priority applies.

### Remediation approach (direct dependency)

- Update tokio dependency to >= 1.42.0 in Cargo.lock (and Cargo.toml if the version
  requirement excludes 1.42.0)
- If a direct bump introduces breaking changes, assess whether a code-level
  workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in tokio
- Bump it to a version whose transitive closure includes tokio >= 1.42.0
- Verify the bump does not introduce breaking API changes

**Fallback: pin the transitive dependency directly**
- Cargo: `cargo add tokio@1.42.0` to override the transitive resolution
- Document why the direct dep bump was not viable in the PR description

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8020 (parent tracking issue)
```

### Task B — Downstream propagation (rhtpa-2.2)

- **Summary**: `Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)`
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`
- **Description**:

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-55123 fix from <TASK-A>.

The upstream backport (<TASK-A>) bumps tokio to 1.42.0 on release/0.4.z.
Once that PR merges, update the source pinning in this Konflux release repo
so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: undetermined, carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback approach),
  verify the pinning is reflected in the downstream build's lock file
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <TASK-A> (upstream backport must merge first)
- Depends on: TC-8020 (parent tracking issue)
```

### Case B creation and linkage sequence (after confirmation)

1. Create Task A, then post the description digest comment (`[sdlc-workflow] Description digest: sha256-...`).
2. Create Task B, then post its description digest comment.
3. Link `TC-8020` → `<TASK-A>` with type **Depend**.
4. Link `TC-8020` → `<TASK-B>` with type **Depend**.
5. Link `<TASK-A>` → `<TASK-B>` with type **Blocks** (upstream blocks downstream).
6. Link `<TASK-A>` → `<RELEASE-TASK>` with **Blocks**, and `<TASK-B>` → `<RELEASE-TASK>` with **Blocks**.
7. Link `<RELEASE-TASK>` → `TC-8020` with **Related**.
8. Transition TC-8020 to In Progress. Skip this if it is already Assigned, which counts as an equivalent indeterminate status.
9. Comment on TC-8020: "Remediation tasks created: <TASK-A> (upstream backport), <TASK-B> (downstream propagation, blocked by <TASK-A>)", with the Comment Footnote.

---

## Case A — Preemptive remediation tasks for rhtpa-2.1 (no CVE Jira)

The Step 4 JQL for sibling CVE-2026-55123 issues returned **no rhtpa-2.1 issue**. Stream rhtpa-2.1 is affected (tokio 1.40.0 < 1.42.0), so preemptive tasks are created. These use the same templates with a preemptive prefix, the `security-preemptive` label, and a **Related** link to TC-8020 instead of Depend. They are not linked to a release Task.

### Task C — Upstream backport (rhtpa-2.1, preemptive)

- **Summary**: `Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)`
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`
- **Description**:

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
while holding a borrowed reference (memory corruption / potential code execution).
The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed version (1.42.0+).

Affected versions: RHTPA 2.1.0 (tokio 1.40.0), RHTPA 2.1.1 (tokio 1.40.0)
Source commit(s): backend v0.3.8, v0.3.12 (from security-matrix.md)

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: undetermined (no dependency-chain evidence available during
  triage), so confirm with `cargo tree -i tokio`
- tokio is a runtime dependency (not dev-only or build-only), so standard priority applies.
- Note: 1.40.0 → 1.42.0 crosses two minor versions; check the tokio changelog for MSRV
  or behaviour changes on the 0.3.z branch.

### Remediation approach (direct dependency)

- Update tokio dependency to >= 1.42.0 in Cargo.lock (and Cargo.toml if needed)
- If a direct bump introduces breaking changes, assess whether a code-level
  workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in tokio
- Bump it to a version whose transitive closure includes tokio >= 1.42.0
- Verify the bump does not introduce breaking API changes

**Fallback: pin the transitive dependency directly**
- Cargo: `cargo add tokio@1.42.0` to override the transitive resolution
- Document why the direct dep bump was not viable in the PR description

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8020 (originating CVE Jira, stream rhtpa-2.2; preemptive, no rhtpa-2.1 CVE Jira yet)
```

### Task D — Downstream propagation (rhtpa-2.1, preemptive)

- **Summary**: `Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)`
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`
- **Description**:

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
CVE-2026-55123 fix from <TASK-C>.

The upstream backport (<TASK-C>) bumps tokio to 1.42.0 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release repo
so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: undetermined, carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback approach),
  verify the pinning is reflected in the downstream build's lock file
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <TASK-C> (upstream backport must merge first)
- Related to: TC-8020 (originating CVE Jira, stream rhtpa-2.2)
```

### Case A creation and linkage sequence (after confirmation)

1. Post the cross-stream impact comment on TC-8020 (see `cross-stream.md`).
2. Create Task C, then post its description digest comment.
3. Create Task D, then post its description digest comment.
4. Link `TC-8020` → `<TASK-C>` with type **Related** (not Depend).
5. Link `TC-8020` → `<TASK-D>` with type **Related** (not Depend).
6. Link `<TASK-C>` → `<TASK-D>` with type **Blocks**.
7. Do not link these tasks to a release Task, because they are preemptive.
8. Post the preemptive-task listing comment on TC-8020 (see `cross-stream.md`).

No Vulnerability issue is created for rhtpa-2.1, because PSIRT owns that.

---

## Pre-creation checklist

- [x] **Task count per stream**: Cargo (source dependency) gets 2 per stream: A+B for 2.2, C+D for 2.1.
- [x] **Cross-stream coverage**: rhtpa-2.1 has no sibling CVE Jira, so it gets preemptive tasks C+D.
- [x] **Link types**: Depend for TC-8020→A/B; Related for TC-8020→C/D; Blocks for A→B and C→D; Blocks for A/B→release Task; Related for release Task→TC-8020.
- [x] **Preemptive labels**: C and D carry `security-preemptive`. A and B do not.
- [x] **Coordination guidance**: omitted, because the Deployment Context column is absent from Source Repositories (backward-compatibility rule).
- [x] **Release Jira linking**: only the non-preemptive tasks A and B are linked to `<RELEASE-TASK>`. TC-8020 is linked Related.
- [x] **Dedup consistency**: 7.5.3 was skipped (field not configured) and no stream is dedup'd.

## Post-triage (after all actions)

- Add the label `ai-cve-triaged` to TC-8020.
- Post a summary comment covering: the version impact table; the Affects Versions correction (2.2.0, 2.2.1 → plus 2.2.2); the outcome (remediation created for rhtpa-2.2 and preemptive remediation for rhtpa-2.1); task links A–D; release Epic and Task keys (RHTPA 2.2.5); dedup (none); an @mention of the TC-8020 reporter via an ADF mention node; and the Comment Footnote (`This comment was AI-generated by sdlc-workflow/triage-security v0.14.0.`).

## Open items for the engineer

1. Verify tokio in 2.2.3 (`v0.4.11`) and 2.2.4 (`v0.4.12`) Cargo.lock. If either is < 1.42.0, add it to Affects Versions.
2. Check the upstream branches `release/0.4.z` and `release/0.3.z`. If tokio is already >= 1.42.0, switch Tasks A and C to the dependency-bump variant.
3. The matrix is 145 days stale. Consider refreshing it.
4. The due date (2026-08-15) has passed. Consider prioritising this work.
