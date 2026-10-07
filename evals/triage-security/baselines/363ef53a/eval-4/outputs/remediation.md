# Remediation — TC-8004

## Triage Outcome

**Case B: Affected — create remediation tasks** for the 2.1.x stream only.

The issue is **unscoped** (no stream suffix), so Case A (cross-stream impact) is skipped entirely. Remediation tasks are created only for streams where the version impact analysis shows affected versions. The 2.2.x stream is NOT affected (ships h2 >= 0.4.8) and receives no remediation tasks.

## Affected Stream Summary

| Stream | Affected? | Remediation Required? |
|--------|-----------|----------------------|
| 2.1.x | YES (h2 0.4.5 < 0.4.8) | YES — 2 tasks (upstream backport + downstream propagation) |
| 2.2.x | NO (h2 >= 0.4.8) | NO |

## Ecosystem Classification

- **Ecosystem**: Cargo (source dependency)
- **Tasks per stream**: 2 (upstream backport + downstream propagation)
- **Upstream fix available on release/0.3.z?**: NO (latest tag v0.3.12 ships h2 0.4.5)
- **Remediation variant**: Upstream backport (not dependency bump, since the fix is not yet on the upstream branch)

## Task 1: Upstream Backport (2.1.x stream)

**Jira creation call (proposed):**

```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

**Task description:**

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 - Memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: 2.1.0 (v0.3.8), 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (or verify via Cargo.lock dependency chain)

### Remediation approach (direct dependency)

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)
```

## Task 2: Downstream Propagation (2.1.x stream)

**Jira creation call (proposed):**

```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

**Task description:**

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that PR
merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct — carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

## Jira Linkage (proposed)

1. **Upstream task -> CVE**: Link upstream task to TC-8004 with type "Depend"
2. **Downstream task -> CVE**: Link downstream task to TC-8004 with type "Depend"
3. **Upstream -> Downstream**: Link upstream task to downstream task with type "Blocks" (downstream is blocked by upstream)
4. **Release Jira linking** (if Step 7.5 produced a release Task): Link both remediation tasks to the release Task with type "Blocks", and link TC-8004 to the release Task with type "Related"

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks for 2.1.x stream (Cargo source dependency = upstream backport + downstream propagation). 0 tasks for 2.2.x stream (not affected).
- [x] **Cross-stream coverage**: Not applicable — issue is unscoped, Case A skipped. 2.2.x is not affected so no remediation needed.
- [x] **Link types**: "Depend" for tasks linked to TC-8004. "Blocks" for upstream -> downstream within the 2.1.x stream.
- [x] **Preemptive labels**: Not applicable — issue is unscoped, no preemptive tasks created.
- [x] **Coordination guidance**: Omitted — Source Repositories table has no Deployment Context column.
- [x] **Release Jira linking**: Would be linked if Step 7.5 produced a release Task for the 2.1.x stream.
- [x] **Dedup consistency**: No sibling issues exist (JQL returned empty). No dedup applies.

## No Remediation for 2.2.x

The 2.2.x stream ships h2 0.4.8 or later across all versions (2.2.0 through 2.2.4). All 2.2.x versions are at or above the fix threshold of 0.4.8. No remediation tasks are created for this stream.
