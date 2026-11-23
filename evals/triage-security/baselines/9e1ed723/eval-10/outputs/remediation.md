# TC-8020 — Step 8 Remediation

## Decision path

1. Supported versions affected? **Yes** (2.2.0, 2.2.1, 2.2.2 in scope; 2.1.0, 2.1.1 out of scope).
2. Issue scoped to one stream? **Yes**: `[rhtpa-2.2]`.
3. Other streams also affected? **Yes**: rhtpa-2.1. That triggers the cross-stream branch. It also runs the standard remediation for the current stream.
4. Ecosystem: Cargo (source dependency) with the upstream fix not confirmed, so **2 tasks per stream**: upstream backport plus downstream propagation.

> Labelling note: this file follows the eval prompt's split. "Case A" here means the standard tasks for the current stream. "Case B" means the preemptive tasks for the other stream. In SKILL.md the names are swapped: SKILL.md Case B is the standard remediation within scope, and SKILL.md Case A is the cross-stream impact comment plus preemptive tasks. The content is the same either way.

No Vulnerability issues are created. PSIRT owns those, so only Tasks are created.

---

## Case A — Standard remediation tasks for the current stream (rhtpa-2.2 / 2.2.x)

### Task A1 — Upstream backport

- **Project**: TC · **Type**: Task
- **Summary**: `Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)`
- **Labels**: `["ai-generated-jira", "Security", "CVE-2026-55123"]`
- **Links**: TC-8020 → A1, **Depend**. A1 → release Task "RHTPA 2.2.5 CVE triage", **Blocks** (if Step 7.5 is confirmed).

```
## Repository

backend (rhtpa-backend)

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: tokio use-after-free when a spawned task is aborted
while holding a borrowed reference (CVSS 8.1, High).
The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed
version (1.42.0+).

Affected versions: RHTPA 2.2.0 (tokio 1.41.1), RHTPA 2.2.1 (tokio 1.41.1),
RHTPA 2.2.2 (retag of 2.2.1); RHTPA 2.2.3 / 2.2.4 pending lock-file verification
Source commit(s): v0.4.5, v0.4.8 (backend tags from security-matrix.md)

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: not determined during triage (no manifest evidence) —
  confirm whether tokio is a direct workspace dependency or transitive
- Production runtime dependency assumed; not a dev-only dependency.

### Remediation approach (direct dependency)

- Update tokio dependency to >= 1.42.0 in Cargo.lock (and Cargo.toml if pinned)
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in tokio
- Bump it to a version whose transitive closure includes tokio >= 1.42.0
- Verify the bump does not introduce breaking API changes

**Fallback: pin the transitive dependency directly**
- `cargo add tokio@1.42.0` to override the transitive resolution
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

Post-creation: a description digest comment, `[sdlc-workflow] Description digest: <tagged-digest>`, is posted before any links.

### Task A2 — Downstream propagation

- **Summary**: `Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)`
- **Labels**: `["ai-generated-jira", "Security", "CVE-2026-55123"]`
- **Links**: TC-8020 → A2, **Depend**. A1 → A2, **Blocks** (A2 is blocked by A1). A2 → release Task "RHTPA 2.2.5 CVE triage", **Blocks** (if Step 7.5 is confirmed).

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-55123 fix from <A1-key>.

The upstream backport (<A1-key>) bumps tokio to 1.42.0 on release/0.4.z.
Once that PR merges, update the source pinning in this Konflux release repo
so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: carried forward from upstream task <A1-key>
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

- Depends on: <A1-key> (upstream backport must merge first)
- Depends on: TC-8020 (parent tracking issue)
```

Post-creation: a description digest comment, posted before any links.

### Release Jira linkage (Case A tasks only)

- A1 → "RHTPA 2.2.5 CVE triage", **Blocks**
- A2 → "RHTPA 2.2.5 CVE triage", **Blocks**
- "RHTPA 2.2.5 CVE triage" → TC-8020, **Related**

### Vulnerability housekeeping

- TC-8020 is already moved to Assigned by Step 0.8, an indeterminate-category status, so the In Progress transition is skipped.
- Comment on TC-8020:
  > Remediation tasks created: <A1-key> (upstream backport), <A2-key> (downstream propagation, blocked by <A1-key>)
  > ---
  > This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0.

---

## Case B — Preemptive remediation tasks for the other stream (rhtpa-2.1 / 2.1.x)

Trigger: rhtpa-2.1 is affected (tokio 1.40.0 < 1.42.0 in 2.1.0 and 2.1.1), and the sibling JQL for CVE-2026-55123 found **no CVE Jira** for rhtpa-2.1. So the **Preemptive Task Variant** applies:

- Label `security-preemptive` is added alongside the standard labels.
- The link to TC-8020 is **Related**, not Depend, because TC-8020 belongs to stream rhtpa-2.2.
- The description starts with the preemptive remediation prefix.
- There is no release Jira linkage, because these tasks are preemptive.

### Task B1 — Upstream backport (preemptive)

- **Summary**: `Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)`
- **Labels**: `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]`
- **Links**: TC-8020 → B1, **Related**

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
while holding a borrowed reference (CVSS 8.1, High).
The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed
version (1.42.0+).

Affected versions: RHTPA 2.1.0 (tokio 1.40.0), RHTPA 2.1.1 (tokio 1.40.0)
Source commit(s): v0.3.8, v0.3.12 (backend tags from security-matrix.md)

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: not determined during triage (no manifest evidence) —
  confirm whether tokio is a direct workspace dependency or transitive
- Note: 1.40.0 → 1.42.0 crosses two minor releases; review the tokio
  changelog for MSRV or behavior changes on the older 0.3.z branch.

### Remediation approach (direct dependency)

- Update tokio dependency to >= 1.42.0 in Cargo.lock (and Cargo.toml if pinned)
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in tokio
- Bump it to a version whose transitive closure includes tokio >= 1.42.0

**Fallback: pin the transitive dependency directly**
- `cargo add tokio@1.42.0` to override the transitive resolution
- Document why the direct dep bump was not viable in the PR description

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8020 (originating CVE Jira, stream rhtpa-2.2)
```

Post-creation: a description digest comment, posted before any links.

### Task B2 — Downstream propagation (preemptive)

- **Summary**: `Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)`
- **Labels**: `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]`
- **Links**: TC-8020 → B2, **Related**. B1 → B2, **Blocks**.

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
CVE-2026-55123 fix from <B1-key>.

The upstream backport (<B1-key>) bumps tokio to 1.42.0 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release repo
so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: carried forward from upstream task <B1-key>
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <B1-key> (upstream backport must merge first)
- Related to: TC-8020 (originating CVE Jira, stream rhtpa-2.2)
```

Post-creation: a description digest comment, posted before any links.

---

## Link topology summary

| From (inward) | To (outward) | Type | Purpose |
|---|---|---|---|
| TC-8020 | A1 | Depend | standard remediation, own CVE |
| TC-8020 | A2 | Depend | standard remediation, own CVE |
| A1 | A2 | Blocks | upstream → downstream (2.2.x) |
| A1 | RHTPA 2.2.5 CVE triage | Blocks | release linkage |
| A2 | RHTPA 2.2.5 CVE triage | Blocks | release linkage |
| RHTPA 2.2.5 CVE triage | TC-8020 | Related | CVE ↔ release |
| TC-8020 | B1 | **Related** | preemptive, cross-stream |
| TC-8020 | B2 | **Related** | preemptive, cross-stream |
| B1 | B2 | Blocks | upstream → downstream (2.1.x) |

## Pre-creation checklist

- [x] Task count per stream: Cargo is a source dependency, so 2 tasks for 2.2.x (A1, A2) and 2 for 2.1.x (B1, B2).
- [x] Cross-stream coverage: rhtpa-2.1 has no CVE Jira and gets preemptive tasks B1 and B2.
- [x] Link types: Depend for A1/A2 to TC-8020; Related for B1/B2 to TC-8020; Blocks from upstream to downstream in each stream.
- [x] Preemptive labels: `security-preemptive` on B1 and B2 only.
- [x] Coordination guidance: omitted, because Source Repositories has no Deployment Context column.
- [x] Release Jira linking: only A1 and A2 are linked to "RHTPA 2.2.5 CVE triage" (Blocks); TC-8020 is Related. Preemptive tasks are excluded.
- [x] Dedup consistency: 7.5.3 was skipped (field not configured), so no stream was deduplicated.

## Post-triage (proposed)

- Add label `ai-cve-triaged` to TC-8020.
- Post a summary comment on TC-8020. It covers: the version impact table; the Affects Versions correction (+RHTPA 2.2.2); the outcome (remediation created); A1, A2, B1, B2 with keys; release Epic/Task keys; no dedup; an @mention of the TC-8020 reporter (ADF mention node with the reporter's account ID); and the Comment Footnote (`sdlc-workflow/triage-security v0.14.0`).

All Jira mutations above need explicit engineer confirmation. None were executed in this eval.
