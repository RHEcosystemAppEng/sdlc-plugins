# Step 8 – Remediation: TC-8001 / CVE-2026-31812

Prerequisites carried forward:
- Step 1.7 embargo gate: the engineer answered "Yes" (simulated) before triage continued.
- Steps 4–7 were simulated. No Jira searches were run, so it is assumed that no sibling CVE Jira exists for 2.1.x and that there are no duplicates, already-fixed siblings, or existing preemptive tasks. Step 4.3 and Step 7 are skipped because the Upstream Affected Component field is not configured. Step 5: 2.1.x and 2.2.x are assumed to be in lifecycle; the engineer should verify this at https://access.example.com/product-life-cycle/rhtpa.
- Step 7.5: release Jira for 2.2.x and 2.1.x would be found or created with individual confirmation. That was not done in this eval, so release-Task links are shown as `<release-task-key>` placeholders.

## Decision

| Stream | Scope | Affected versions | Upstream fixed? | Case | Tasks |
|--------|-------|-------------------|-----------------|------|-------|
| 2.2.x | In scope (TC-8001) | 2.2.0, 2.2.1, 2.2.2 | YES (release/0.4.z; shipped in 2.2.3+) | Case B, dependency-bump variant | 2 (bump + downstream propagation) |
| 2.1.x | Out of scope | 2.1.0, 2.1.1 | NO (release/0.3.z at 0.11.9) | Case A, preemptive | 2 (upstream backport + downstream propagation), `security-preemptive` |

Not Case C, because supported versions are affected.

Engineer note for 2.2.x: 2.2.3 (v0.4.11) and 2.2.4 (v0.4.12) already ship quinn-proto 0.11.14. If release/0.4.z HEAD is confirmed at >= 0.11.14, the 2.2.x bump task only has to verify this. The downstream task makes sure the next 2.2.x build ships the fix, and the guidance for 2.2.0–2.2.2 is "upgrade to 2.2.3+". The engineer may choose to decline the 2.2.x tasks at the confirmation gate and instead record the upgrade path in the summary comment.

## Case A – Cross-stream impact comment (on TC-8001)

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x
(RHTPA 2.1.0, 2.1.1 ship quinn-proto 0.11.9) based on lock file analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

---
_[sdlc-workflow] triage-security_ (Comment Footnote)
```

---

## Task 1 (2.2.x): Dependency bump

- **Summary:** Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x)
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`
- **Links:** TC-8001 Depend -> this task; this task Blocks Task 2; this task Blocks `<release-task-key 2.2.x>`

```
## Repository

backend (rhtpa-backend)

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream —
a package manager update is sufficient. quinn-proto before 0.11.14 panics when a
remote peer sends a STREAMS frame requesting an excessive number of streams
(denial of service, CVSS 7.5).

Affected versions: RHTPA 2.2.0 (quinn-proto 0.11.9), RHTPA 2.2.1 (0.11.12),
RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8 (backend tags from supportability matrix)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend → quinn → quinn-proto) — to be confirmed from Cargo.lock
- **Remediation action**: run `cargo update -p quinn-proto` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify Cargo.lock reflects quinn-proto >= 0.11.14 after the update
- Note: release tags v0.4.11 and v0.4.12 already ship quinn-proto 0.11.14; if
  release/0.4.z HEAD already resolves >= 0.11.14, confirm and close with no change.

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

## Task 2 (2.2.x): Downstream propagation

- **Summary:** Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`
- **Links:** TC-8001 Depend -> this task; blocked by Task 1; this task Blocks `<release-task-key 2.2.x>`

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
- **Dependency type**: transitive — carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback
  approach), verify the pinning is reflected in the downstream build's
  lock file after the source reference update
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

## Task 3 (2.1.x, preemptive): Upstream backport

- **Summary:** Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- **Links:** TC-8001 Related -> this task (not Depend, because the originating CVE belongs to 2.2.x); this task Blocks Task 4. Preemptive tasks are not linked to a release Task.

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

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (DoS).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (quinn-proto 0.11.9), RHTPA 2.1.1 (quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12 (backend tags from supportability matrix)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: transitive (chain: backend → quinn → quinn-proto) — to be confirmed from Cargo.lock

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (see dependency chain above)
- Bump the direct dependency to a version whose transitive closure
  includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes to the direct dependency

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable (breaking API changes,
no release available with the fix):
- `cargo add quinn-proto@0.11.14` to add as a direct dependency, overriding
  the transitive resolution
- Document why the direct dep bump was not viable in the PR description

(If Cargo.lock analysis shows quinn-proto is a direct dependency instead:
update quinn-proto to >= 0.11.14 in Cargo.lock / Cargo.toml.)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

## Task 4 (2.1.x, preemptive): Downstream propagation

- **Summary:** Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- **Links:** TC-8001 Related -> this task; blocked by Task 3

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

The upstream backport (<Task 3 key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: transitive — carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback
  approach), verify the pinning is reflected in the downstream build's
  lock file after the source reference update
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

Coordination Guidance subsection: left out of all tasks, because the Source Repositories table has no Deployment Context column (backward-compatibility rule).

Each task gets a description digest comment (`[sdlc-workflow] Description digest: <tagged-digest>`) right after it is created, before any links or other comments.

## Follow-up comments and actions on TC-8001 (each needs confirmation; each comment includes the Comment Footnote)

1. Preemptive task list comment: "Preemptive remediation tasks created for streams without CVE Jiras: - 2.1.x: <Task 3 key>, <Task 4 key> (security-preemptive). These tasks use the "Related" link type and carry the security-preemptive label. When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link them and remove the label."
2. Remediation task comment: "Remediation tasks created: <Task 1 key> (dependency bump), <Task 2 key> (downstream propagation, blocked by <Task 1 key>)."
3. Link TC-8001 to `<release-task-key 2.2.x>` (Related). Link Tasks 1 and 2 to the release Task (Blocks).
4. Transition: skip if TC-8001 is already ASSIGNED or later (it was moved there in Step 0.8). Otherwise move it to In Progress.
5. Add the `ai-cve-triaged` label.
6. Post-triage summary comment: version impact table, the Affects Versions correction (RHTPA 2.0.0 -> RHTPA 2.2.0, 2.2.1, 2.2.2), the outcome (remediation created; 2.2.3+ already fixed), the task keys, release Jira keys, no dedup, an @mention of the TC-8001 reporter (ADF mention node), and the Comment Footnote.

## Pre-creation checklist

- [x] Task count per stream: Cargo is a source dependency, so 2 tasks per stream (2.2.x: bump + downstream; 2.1.x: backport + downstream)
- [x] Cross-stream coverage: 2.1.x is covered by preemptive tasks (assuming no sibling CVE Jira)
- [x] Link types: Depend (2.2.x tasks to TC-8001), Related (2.1.x preemptive tasks to TC-8001), Blocks (upstream to downstream)
- [x] Preemptive labels: `security-preemptive` on the 2.1.x tasks
- [x] Coordination guidance: left out because there is no Deployment Context column
- [x] Release Jira linking: non-preemptive 2.2.x tasks Block the release Task; the CVE is Related to it
- [x] Dedup consistency: no streams were deduplicated
