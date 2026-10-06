# Remediation -- TC-8004

## Step 8 -- Remediation Decision

### Triage Outcome: Case B (Affected -- create remediation tasks)

The version impact analysis shows:
- **2.1.x stream**: AFFECTED (all versions ship h2 0.4.5 < 0.4.8)
- **2.2.x stream**: NOT AFFECTED (all versions ship h2 >= 0.4.8)

Since this is an **unscoped** issue and the 2.1.x stream has affected versions,
remediation tasks are created for the **2.1.x stream only**. The 2.2.x stream
requires no remediation. Case A (cross-stream impact) does not apply because the
issue is unscoped -- unscoped issues cover all streams by definition, so there
are no "other streams outside this issue's scope."

### Ecosystem Classification

- Ecosystem: **Cargo** (source dependency)
- Tasks per stream: **2** (upstream backport + downstream propagation)
- Downstream blocked by upstream

### Task 1: Upstream Backport (2.1.x stream)

**Summary**: Remediate CVE-2026-33501: bump h2 to 0.4.8 (rhtpa-2.1)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

```markdown
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 - Memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version
(0.4.8+).

Affected versions: RHTPA 2.1.0 (build v0.3.8), RHTPA 2.1.1 (build v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (h2 is a direct Cargo dependency)
- Update h2 dependency to >= 0.4.8 in Cargo.toml and regenerate Cargo.lock
- The fix adds a configurable maximum header list size that defaults to 16 KiB

### Remediation approach (direct dependency)

- Update h2 dependency to >= 0.4.8 in Cargo.toml
- Run `cargo update -p h2` to update Cargo.lock
- If bumping to 0.4.8 introduces breaking API changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)
```

### Task 2: Downstream Propagation (2.1.x stream)

**Summary**: Propagate CVE-2026-33501 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

**Blocked by**: Task 1 (upstream backport)

```markdown
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that PR
merges, update the source pinning in this Konflux release repo so the next
build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-backport-task-key> (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

### Jira Linkage (proposed)

1. Link Task 1 (upstream) to TC-8004 with link type "Depend"
2. Link Task 2 (downstream) to TC-8004 with link type "Depend"
3. Link Task 2 as blocked by Task 1 with link type "Blocks"
4. Transition TC-8004 to In Progress
5. Add `ai-cve-triaged` label to TC-8004

### Post-Triage Summary Comment (proposed)

```
Triage complete for CVE-2026-33501 (h2 < 0.4.8).

Version impact:

| Version | Stream | h2 version | Affected? |
|---------|--------|------------|-----------|
| 2.1.0 | 2.1.x | 0.4.5 | YES |
| 2.1.1 | 2.1.x | 0.4.5 | YES |
| 2.2.0 | 2.2.x | 0.4.8 | NO |
| 2.2.1 | 2.2.x | 0.4.8 | NO |
| 2.2.2 | 2.2.x | -- | NO (retag of 2.2.1) |
| 2.2.3 | 2.2.x | 0.4.9 | NO |
| 2.2.4 | 2.2.x | 0.4.9 | NO |

Affects Versions corrected: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]
- Removed RHTPA 2.2.0 (ships h2 0.4.8, not affected)
- Added RHTPA 2.1.1 (ships h2 0.4.5, affected)

Remediation tasks created for 2.1.x stream:
- <upstream-task-key>: upstream backport (bump h2 to >= 0.4.8 on release/0.3.z)
- <downstream-task-key>: downstream propagation (update rhtpa-backend ref in
  rhtpa-release.0.3.z, blocked by <upstream-task-key>)

No remediation needed for 2.2.x stream -- all versions ship h2 >= 0.4.8.

No sibling issues found (JQL returned empty).
```
