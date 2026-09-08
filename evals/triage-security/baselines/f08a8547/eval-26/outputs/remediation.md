# Step 8 -- Remediation

## Triage Decision

- **Case B: Affected -- create remediation tasks** (scoped to 2.2.x stream)
- All 2.2.x versions (2.2.0 through 2.2.4) ship criterion 0.5.1, which is
  within the affected range (< 0.5.2).
- **Case A also applies**: the 2.1.x stream is also affected but is outside
  this issue's scope. A cross-stream impact comment would be posted, and
  preemptive remediation tasks would be created for the 2.1.x stream if no
  sibling CVE Jira exists for that stream.

## Dev-Dependency Overrides

criterion is a dev-only dependency (declared in `[dev-dependencies]`). Per the
dependency scope decision tree:

- **Label**: `dev-dependency` added to all remediation tasks
- **Priority**: Normal (overrides CVE severity -- supply chain risk only)
- **Note in description**: "This dependency is dev/build-only and is not
  shipped in production. Remediation priority is Normal (supply chain risk only)."

## Remediation Tasks (2.2.x stream)

### Task 1: Upstream backport task

**Summary**: Remediate CVE-2026-99001: bump criterion to 0.5.2 (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority**: Normal

#### Description

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99001: path traversal in benchmark output in criterion.
The vulnerable dependency (criterion < 0.5.2) must be updated to the fixed
version (0.5.2+).

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

Affected versions: 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4
Source commit(s): v0.4.5, v0.4.8, v0.4.11, v0.4.12

CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct dev-dependency
- **Dependency scope**: dev-only ([dev-dependencies] in backend/Cargo.toml).
  criterion is used for benchmarks only and is NOT shipped in production builds.
  Remediation priority is Normal regardless of CVE severity.

### Remediation approach (direct dependency)

- Update criterion dependency to >= 0.5.2 in backend/Cargo.toml [dev-dependencies]
- Run `cargo update -p criterion` to update Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8050 (parent tracking issue)
```

### Task 2: Downstream propagation subtask

**Summary**: Propagate CVE-2026-99001 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority**: Normal

#### Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99001 fix from the upstream backport task.

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

The upstream backport bumps criterion to 0.5.2 on release/0.4.z. Once that
PR merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct dev-dependency -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8050 (parent tracking issue)
```

## Jira Linkage (would be executed)

1. Link upstream task to TC-8050 with "Depend"
2. Link downstream task to TC-8050 with "Depend"
3. Link downstream task as blocked by upstream task with "Blocks"
4. Add `ai-cve-triaged` label to TC-8050

## Cross-Stream Impact (Case A)

The 2.1.x stream is also affected (criterion 0.5.1 at tags v0.3.8 and v0.3.12).
In a real triage:
- A cross-stream impact comment would be posted to TC-8050
- A JQL search would check for sibling CVE Jiras with label CVE-2026-99001 and
  suffix [rhtpa-2.1]
- If no sibling exists, preemptive remediation tasks would be created for the
  2.1.x stream with the `security-preemptive` label and "Related" link type

## Post-Triage Summary

Triage outcome for TC-8050 (CVE-2026-99001 -- criterion path traversal):

- **All 2.2.x versions affected**: 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 ship
  criterion 0.5.1 (affected range: < 0.5.2)
- **Dependency scope**: dev-only ([dev-dependencies]) -- not shipped in production
- **Priority override**: Normal (supply chain risk only)
- **Remediation**: 2 tasks created for 2.2.x stream (upstream backport +
  downstream propagation), both with `dev-dependency` label and Normal priority
- **Cross-stream**: 2.1.x stream also affected -- handled via Case A
  (cross-stream impact comment + preemptive tasks if no sibling CVE Jira exists)
