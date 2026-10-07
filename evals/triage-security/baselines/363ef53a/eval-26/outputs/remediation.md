# Step 8 -- Remediation for TC-8050

## Triage Outcome

- **Case B**: Affected -- create remediation tasks for the 2.2.x stream
- **Case A**: Cross-stream impact -- 2.1.x stream is also affected (outside
  this issue's scope)

## Dev-Dependency Handling

criterion is a dev-only dependency (`[dev-dependencies]`). Per the dependency
scope decision tree:

- All remediation tasks carry the **`dev-dependency`** label
- Priority is overridden to **Normal** (not inherited from CVE severity)
- Task descriptions include: "This dependency is dev/build-only and is not
  shipped in production. Remediation priority is Normal (supply chain risk only)."

## Remediation Tasks -- 2.2.x Stream (Scoped)

Ecosystem: Cargo (source dependency). Upstream fix NOT available on
`release/0.4.z`. Two tasks required: upstream backport + downstream propagation.

### Task 1: Upstream Backport

**Summary**: Remediate CVE-2026-99001: bump criterion to 0.5.2 (rhtpa-2.2)
**Priority**: Normal (dev-dependency override)
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`
**Link**: Depend -> TC-8050

```
## Repository

backend

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
- **Dependency type**: direct (backend workspace -> criterion)
- **Dependency scope**: dev-only ([dev-dependencies] in backend/Cargo.toml)
  -- NOT shipped in production builds, used for benchmarks only

### Remediation approach (direct dependency)

- Update criterion dependency to >= 0.5.2 in backend/Cargo.toml
  [dev-dependencies] section
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

### Task 2: Downstream Propagation

**Summary**: Propagate CVE-2026-99001 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
**Priority**: Normal (dev-dependency override)
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`
**Links**: Depend -> TC-8050, Blocks -> upstream backport task (Task 1)

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99001 fix from the upstream backport task.

The upstream backport bumps criterion to 0.5.2 on release/0.4.z. Once
that PR merges, update the source pinning in this Konflux release repo
so the next build ships the fix.

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- **Dependency scope**: dev-only -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8050 (parent tracking issue)
```

## Case A: Cross-Stream Impact Comment

The following comment would be posted to TC-8050 to notify about cross-stream
impact:

```
Cross-stream impact: criterion < 0.5.2 also affects stream 2.1.x based on
lock file analysis. All 2.1.x versions (2.1.0, 2.1.1) ship criterion 0.5.1.

Note: criterion is a dev-only dependency ([dev-dependencies]) and is NOT
shipped in production. Supply chain risk only.

These streams are tracked by companion issues (see Related links) or may
require separate PSIRT triage.
```

For the 2.1.x stream, if no companion CVE Jira exists, preemptive remediation
tasks would be created with the `security-preemptive` label (in addition to
`dev-dependency`) and linked to TC-8050 with "Related" link type. Priority
would be Normal (dev-dependency override applies to preemptive tasks as well).

## Jira Linkage Summary

| Link Type | From | To | Purpose |
|-----------|------|----|---------|
| Depend | TC-8050 | Task 1 (upstream backport) | Standard remediation linkage |
| Depend | TC-8050 | Task 2 (downstream propagation) | Standard remediation linkage |
| Blocks | Task 1 (upstream backport) | Task 2 (downstream propagation) | Upstream must merge first |
| Blocks | Task 1 | Release Task (if active from Step 7.5) | Release Jira linkage |
| Blocks | Task 2 | Release Task (if active from Step 7.5) | Release Jira linkage |
| Related | Release Task | TC-8050 | CVE traceability |

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks for Cargo source dependency (upstream backport + downstream propagation) -- matches ecosystem classification table
- [x] **Cross-stream coverage**: 2.1.x stream identified as affected; Case A cross-stream comment prepared; preemptive tasks noted
- [x] **Link types**: Depend for tasks linked to TC-8050; Blocks for upstream -> downstream within stream
- [x] **Dev-dependency label**: all tasks carry `dev-dependency` label
- [x] **Priority override**: all tasks set to Normal (not inheriting CVE Medium severity)
- [x] **Coordination guidance**: omitted (no Deployment Context column in Source Repositories table -- backward compatibility)
