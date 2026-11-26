# Step 8 – Remediation: TC-8020 (CVE-2026-55123, tokio < 1.42.0)

## Decision path

1. Step 7: no concurrent triage, so proceed.
2. Step 7.5: release Jira for 2.2.x is found or created. Step 7.5.3 found no cross-CVE dedup (no existing remediation Task covers `tokio`).
3. Are any supported versions affected? **Yes.**
4. Is the issue scoped to a single stream? **Yes**, `[rhtpa-2.2]`, so 2.2.x.
5. Are other streams also affected? **Yes**, 2.1.x (tokio 1.40.0). This triggers **Case A**: post the cross-stream impact comment and check for CVE Jiras in the other streams.
6. 2.1.x has no CVE Jira, so it gets **preemptive** remediation tasks (Case B templates with the preemptive variant).
7. 2.2.x (this issue's scope) gets standard remediation tasks under **Case B**.
8. Ecosystem: Cargo, which is a source dependency. Upstream fix availability is not confirmed, so each stream gets **2 tasks: upstream backport + downstream propagation**.

Total: **4 remediation Tasks**. Two are standard (2.2.x) and two are preemptive (2.1.x).

All creation actions copy the parent Vulnerability's (TC-8020) `security` level. Every task gets a description digest comment (`[sdlc-workflow] Description digest: sha256-...`) right after it is created, before any links or other comments.

---

## Case B: standard remediation for stream 2.2.x (in scope)

### Task 1: upstream backport (2.2.x)

- **Summary**: `Remediate CVE-2026-55123: bump tokio to 1.42.0 (2.2.x)`
- **Issue type**: Task, project TC
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`
- **Security**: same level as TC-8020
- **Links**: TC-8020 → Task 1 (**Depend**); Task 1 → Task 2 (**Blocks**); Task 1 → 2.2.x release Task (**Blocks**)

```
## Repository

backend (rhtpa-backend)

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: tokio use-after-free when a spawned task is aborted
while holding a borrowed reference (memory corruption, potential code execution).
The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed version
(1.42.0+).

Affected versions: RHTPA 2.2.0 (tokio 1.41.1), RHTPA 2.2.1 (tokio 1.41.1),
RHTPA 2.2.2 (retag of 2.2.1); RHTPA 2.2.3 / 2.2.4 pending lock file verification
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (backend workspace → tokio), to be confirmed with `cargo tree -i tokio`
- If the vulnerable dependency is dev-only or build-only, the remediation
  priority is Normal regardless of CVE severity. Add `dev-dependency` label.
  (tokio is a runtime dependency, so this is not expected to apply.)

### Remediation approach (direct dependency)

- Update tokio dependency to >= 1.42.0 in Cargo.lock (and Cargo.toml if the
  version requirement excludes 1.42.0)
- If a direct bump introduces breaking changes, assess whether a code-level
  workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

If tokio is found to be transitive: prefer bumping the direct dependency whose
transitive closure includes tokio >= 1.42.0; fall back to
`cargo add tokio@1.42.0` and document why in the PR description.

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if
the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8020 (parent tracking issue)
```

### Task 2: downstream propagation (2.2.x)

- **Summary**: `Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)`
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`
- **Security**: same level as TC-8020
- **Links**: TC-8020 → Task 2 (**Depend**); blocked by Task 1 (**Blocks**); Task 2 → 2.2.x release Task (**Blocks**)

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
- **Dependency type**: direct, carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback
  approach), verify the pinning is reflected in the downstream build's lock file
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if
the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <Task 1 key> (upstream backport must merge first)
- Depends on: TC-8020 (parent tracking issue)
```

### Release Jira linkage (2.2.x)

- Task 1 → release Task "RHTPA <2.2.z> CVE triage": **Blocks**
- Task 2 → release Task: **Blocks**
- Release Task ↔ TC-8020: **Related**

---

## Case A → preemptive remediation for stream 2.1.x (no CVE Jira)

The sibling JQL (`labels = 'CVE-2026-55123'`, stream rhtpa-2.1) returned no results, so preemptive tasks are created. They differ from the standard tasks in four ways:
- They add the `security-preemptive` label.
- They link to TC-8020 with **Related**, not Depend. The originating CVE belongs to a different stream.
- Their descriptions start with a preemptive prefix.
- They are not linked to release Jira, because release linking covers non-preemptive remediation only.

### Task 3: preemptive upstream backport (2.1.x)

- **Summary**: `Remediate CVE-2026-55123: bump tokio to 1.42.0 (2.1.x)`
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`
- **Security**: same level as TC-8020
- **Links**: TC-8020 → Task 3 (**Related**); Task 3 → Task 4 (**Blocks**)

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
while holding a borrowed reference (memory corruption, potential code execution).
The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed version
(1.42.0+).

Affected versions: RHTPA 2.1.0 (tokio 1.40.0), RHTPA 2.1.1 (tokio 1.40.0)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (backend workspace → tokio), to be confirmed with `cargo tree -i tokio`
- tokio 1.40.0 → 1.42.0 spans two minor releases; check the tokio changelog
  and MSRV for the 0.3.z branch toolchain
- If the vulnerable dependency is dev-only or build-only, the remediation
  priority is Normal regardless of CVE severity. Add `dev-dependency` label.

### Remediation approach (direct dependency)

- Update tokio dependency to >= 1.42.0 in Cargo.lock (and Cargo.toml if needed)
- If a direct bump introduces breaking changes, assess whether a code-level
  workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

If tokio is found to be transitive: prefer bumping the direct dependency whose
transitive closure includes tokio >= 1.42.0; fall back to
`cargo add tokio@1.42.0` and document why in the PR description.

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if
the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8020 (originating CVE Jira, stream rhtpa-2.2)
```

### Task 4: preemptive downstream propagation (2.1.x)

- **Summary**: `Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)`
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`
- **Security**: same level as TC-8020
- **Links**: TC-8020 → Task 4 (**Related**); blocked by Task 3 (**Blocks**)

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
- **Dependency type**: direct, carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if
the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

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

## Link topology summary

| From | To | Type | Notes |
|---|---|---|---|
| TC-8020 | Task 1 (2.2.x upstream) | Depend | own CVE |
| TC-8020 | Task 2 (2.2.x downstream) | Depend | own CVE |
| Task 1 | Task 2 | Blocks | upstream → downstream |
| Task 1, Task 2 | 2.2.x release Task | Blocks | release linkage |
| 2.2.x release Task | TC-8020 | Related | traceability |
| TC-8020 | Task 3 (2.1.x upstream, preemptive) | Related | originating CVE in another stream |
| TC-8020 | Task 4 (2.1.x downstream, preemptive) | Related | originating CVE in another stream |
| Task 3 | Task 4 | Blocks | upstream → downstream |

## Pre-creation checklist

- [x] Task count per stream: Cargo is a source dependency, so 2 tasks for 2.2.x and 2 tasks for 2.1.x
- [x] Cross-stream coverage: 2.1.x (affected, outside scope) has preemptive tasks. It has no sibling CVE Jira
- [x] Link types: Depend (2.2.x to TC-8020), Related (2.1.x preemptive to TC-8020), Blocks (upstream → downstream)
- [x] Preemptive labels: `security-preemptive` on Tasks 3 and 4 only
- [x] Coordination guidance: `upstream` default context in every task
- [x] Release Jira linking: non-preemptive Tasks 1 and 2 → 2.2.x release Task (Blocks); TC-8020 → release Task (Related)
- [x] Dedup consistency: no stream is dedup'd

## Other proposed mutations (all require engineer confirmation)

1. Assign TC-8020 to the current user and transition it New → Assigned (Step 0.8).
2. Affects Versions: `[RHTPA 2.2.0, RHTPA 2.2.1]` → `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`, and add 2.2.3/2.2.4 only if verification shows they are affected. Post a correction comment with the footnote.
3. Post the cross-stream impact comment and the preemptive-task comment. See cross-stream.md.
4. Post the task-list comment: "Remediation tasks created: <Task 1> (upstream backport), <Task 2> (downstream propagation, blocked by <Task 1>)".
5. Add the label `ai-cve-triaged` to TC-8020 and post the post-triage summary comment. The comment includes the impact table, the AV correction, the 4 task keys, the release Epic/Task keys, an @mention of the reporter (ADF mention node), and the footnote.

## Open items for the engineer

- The matrix is 151 days stale. Consider refreshing it, because new 2.1.z/2.2.z releases may be missing.
- tokio versions at v0.4.11 (2.2.3) and v0.4.12 (2.2.4) were not provided and must be verified.
- Upstream branch HEADs (release/0.3.z, release/0.4.z) were not checked. If either already has tokio >= 1.42.0, switch that stream's Task 1/Task 3 to the dependency-bump variant.
- The due date (2026-08-15) has passed. Consider escalating priority (CVSS 8.1 High).
