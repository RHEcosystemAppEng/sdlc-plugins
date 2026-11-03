# TC-8020 — Remediation Plan (Step 8)

Ecosystem: Cargo (source dependency) → 2 tasks per affected stream.
Upstream fix not confirmed on either upstream branch → upstream backport + downstream propagation.

Summary of tasks to create (4 total):

| # | Stream | Task | Labels | Link to TC-8020 | Other links |
|---|---|---|---|---|---|
| 1 | 2.2.x (rhtpa-2.2) — Case B (in scope) | Upstream backport: bump tokio to 1.42.0 | ai-generated-jira, Security, CVE-2026-55123 | **Depend** | Blocks → Task 2; Blocks → 2.2.x release Task |
| 2 | 2.2.x (rhtpa-2.2) — Case B (in scope) | Downstream propagation in rhtpa-release.0.4.z | ai-generated-jira, Security, CVE-2026-55123 | **Depend** | blocked by Task 1; Blocks → 2.2.x release Task |
| 3 | 2.1.x (rhtpa-2.1) — Case A preemptive | Upstream backport: bump tokio to 1.42.0 | ai-generated-jira, Security, CVE-2026-55123, **security-preemptive** | **Related** | Blocks → Task 4 |
| 4 | 2.1.x (rhtpa-2.1) — Case A preemptive | Downstream propagation in rhtpa-release.0.3.z | ai-generated-jira, Security, CVE-2026-55123, **security-preemptive** | **Related** | blocked by Task 3 |

After each task is created, a description digest comment (`[sdlc-workflow] Description digest: <sha256-md:...>`) is posted per `shared/description-digest-protocol.md` **before** any links or other comments.

No Vulnerability issue is created for 2.1.x — PSIRT owns Vulnerability issue creation.

---

## Case B — current stream (rhtpa-2.2 / 2.2.x)

### Task 1 — Upstream backport (2.2.x)

**Summary:** Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-55123`

```
## Repository

backend (rhtpa-backend)

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: tokio use-after-free when a spawned task is aborted
while holding a borrowed reference (memory corruption, potential code execution).
The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed version (1.42.0+).

Affected versions: RHTPA 2.2.0 (tokio 1.41.1), RHTPA 2.2.1 (tokio 1.41.1),
RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: to be confirmed with `cargo tree -i tokio` (direct or transitive)
- tokio is a runtime dependency (not dev-only); standard priority applies.

### Remediation approach (direct dependency)

- Update tokio dependency to >= 1.42.0 in Cargo.lock (and Cargo.toml constraint if needed)
- If a direct bump introduces breaking changes, assess whether a code-level
  workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency** that pulls in tokio to a version whose
transitive closure includes tokio >= 1.42.0.

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

### Task 2 — Downstream propagation (2.2.x)

**Summary:** Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-55123`

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-55123 fix from <Task-1-key>.

The upstream backport (<Task-1-key>) bumps tokio to 1.42.0 on release/0.4.z.
Once that PR merges, update the source pinning in this Konflux release repo so
the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned tokio directly (fallback approach), verify the
  pinning is reflected in the downstream build's lock file
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <Task-1-key> (upstream backport must merge first)
- Depends on: TC-8020 (parent tracking issue)
```

### Case B linkage

1. `create_link(inward: TC-8020, outward: <Task-1>, type: Depend)`
2. `create_link(inward: TC-8020, outward: <Task-2>, type: Depend)`
3. `create_link(inward: <Task-1>, outward: <Task-2>, type: Blocks)`
4. `create_link(inward: <Task-1>, outward: <2.2.x release Task>, type: Blocks)` and same for `<Task-2>` (if release Jira active from Step 7.5)
5. `create_link(inward: <2.2.x release Task>, outward: TC-8020, type: Related)`
6. Transition TC-8020 to In Progress; ensure it is assigned to the current user.
7. Comment on TC-8020: "Remediation tasks created: <Task-1> (upstream backport), <Task-2> (downstream propagation, blocked by <Task-1>)" + Comment Footnote.

---

## Case A — other stream (rhtpa-2.1 / 2.1.x), preemptive tasks

Stream 2.1.x is affected (tokio 1.40.0 < 1.42.0) and the JQL sibling search found **no CVE Jira for rhtpa-2.1**, so preemptive tasks are created. Details in `cross-stream.md`.

### Task 3 — Preemptive upstream backport (2.1.x)

**Summary:** Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`

```
## Repository

backend (rhtpa-backend)

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-55123: tokio use-after-free when a spawned task is aborted
while holding a borrowed reference.
The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed version (1.42.0+).

Affected versions: RHTPA 2.1.0 (tokio 1.40.0), RHTPA 2.1.1 (tokio 1.40.0)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: to be confirmed with `cargo tree -i tokio` (direct or transitive)
- tokio 1.40.0 → 1.42.0 is a minor bump within 1.x; check MSRV compatibility on release/0.3.z.

### Remediation approach (direct dependency)

- Update tokio dependency to >= 1.42.0 in Cargo.lock

### Remediation approach (transitive dependency)

**Preferred:** bump the direct dependency that pulls in tokio.
**Fallback:** `cargo add tokio@1.42.0`; document why in the PR description.

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8020 (originating CVE Jira, stream rhtpa-2.2)
```

### Task 4 — Preemptive downstream propagation (2.1.x)

**Summary:** Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`

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
CVE-2026-55123 fix from <Task-3-key>.

The upstream backport (<Task-3-key>) bumps tokio to 1.42.0 on release/0.3.z.
Once that PR merges, update the source pinning so the next 2.1.x build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <Task-3-key> (upstream backport must merge first)
- Related to: TC-8020 (originating CVE Jira, stream rhtpa-2.2)
```

### Case A linkage

1. `create_link(inward: TC-8020, outward: <Task-3>, type: Related)`
2. `create_link(inward: TC-8020, outward: <Task-4>, type: Related)`
3. `create_link(inward: <Task-3>, outward: <Task-4>, type: Blocks)`
4. No release Jira linking for preemptive tasks.

---

## Pre-creation checklist

- [x] Task count per stream: 2 for 2.2.x, 2 for 2.1.x (Cargo = source dependency)
- [x] Cross-stream coverage: 2.1.x has preemptive tasks (no sibling CVE Jira exists)
- [x] Link types: Depend (2.2.x tasks → TC-8020), Related (2.1.x preemptive → TC-8020), Blocks (upstream → downstream)
- [x] Preemptive labels: Tasks 3 and 4 carry `security-preemptive`
- [x] Coordination guidance: omitted (no Deployment Context column configured)
- [x] Release Jira linking: only non-preemptive 2.2.x tasks linked (pending Step 7.5 release Task)
- [x] Dedup consistency: no dedup'd streams

## Post-triage

- Add label `ai-cve-triaged` to TC-8020.
- Post summary comment on TC-8020: version impact table, Affects Versions outcome, remediation tasks (Tasks 1–4), release Jira references, matrix staleness note, @mention of the PSIRT reporter (ADF mention node with reporter account ID from Step 1), Comment Footnote ("This comment was AI-generated by sdlc-workflow/triage-security v0.13.10.").
- All mutations above require engineer confirmation before execution.
