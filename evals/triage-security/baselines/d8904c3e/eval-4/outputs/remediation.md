# Step 8 -- Remediation

## Triage Outcome

**Case B: Affected -- create remediation tasks** for the 2.1.x stream only.

The issue is unscoped (covers all streams). The version impact analysis shows:

- **2.1.x stream**: AFFECTED -- all versions (2.1.0, 2.1.1) ship h2 0.4.5 (vulnerable)
- **2.2.x stream**: NOT AFFECTED -- all versions ship h2 >= 0.4.8 (fixed)

Since this is an unscoped issue, Case A (cross-stream impact) does not apply --
unscoped issues cover all streams by definition and there are no "other streams
outside this issue's scope."

Remediation tasks are created only for the affected 2.1.x stream. No tasks are
needed for the 2.2.x stream since it already ships the fixed version.

## Ecosystem Classification

- **Ecosystem**: Cargo (source dependency)
- **Tasks per stream**: 2 (upstream backport + downstream propagation)

## Duplicate / Sibling Check (Step 4)

JQL search for sibling issues with label CVE-2026-33501 returned empty -- no
duplicate or sibling Vulnerability issues exist.

## Remediation Tasks for Stream 2.1.x

### Task 1: Upstream Backport

**Summary**: Remediate CVE-2026-33501: bump h2 to 0.4.8 (rhtpa-2.1)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

```markdown
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed
version (0.4.8+).

Affected versions: RHTPA 2.1.0 (build v0.3.8), RHTPA 2.1.1 (build v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- h2 is a direct dependency of the backend workspace

### Remediation approach (direct dependency)

- Update h2 dependency to >= 0.4.8 in Cargo.toml
- Run `cargo update -p h2` to update Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)
- The fix adds a configurable maximum header list size defaulting to 16 KiB

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

### Task 2: Downstream Propagation

**Summary**: Propagate CVE-2026-33501 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

```markdown
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that PR
merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

## Jira Linkage

1. Link upstream backport task to TC-8004 with type "Depend"
2. Link downstream propagation task to TC-8004 with type "Depend"
3. Link downstream propagation task as blocked by upstream backport task with type "Blocks"
4. Transition TC-8004 to In Progress
5. Add ai-cve-triaged label to TC-8004

## Post-Triage Summary

```
Version impact analysis for CVE-2026-33501 (h2 < 0.4.8):

| Version | h2 version | Affected? |
|---------|------------|-----------|
| 2.1.0   | 0.4.5      | YES       |
| 2.1.1   | 0.4.5      | YES       |
| 2.2.0   | 0.4.8      | NO        |
| 2.2.1   | 0.4.8      | NO        |
| 2.2.2   | --         | NO (retag of 2.2.1) |
| 2.2.3   | 0.4.9      | NO        |
| 2.2.4   | 0.4.9      | NO        |

Affects Versions corrected: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]

Triage outcome: Remediation tasks created for stream 2.1.x (the only affected stream).
Stream 2.2.x ships h2 >= 0.4.8 and is not affected.

Remediation tasks:
- Upstream backport: bump h2 to >= 0.4.8 on release/0.3.z
- Downstream propagation: update rhtpa-backend ref in rhtpa-release.0.3.z (blocked by upstream task)
```
