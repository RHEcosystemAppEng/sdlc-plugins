# Step 8 -- Remediation: TC-8050

CVE-2026-99001 (criterion < 0.5.2)

## Triage Outcome

**Case B: Affected -- create remediation tasks** for stream 2.2.x (issue scope).

All 2.2.x versions ship criterion 0.5.1 (below fix threshold 0.5.2). Criterion is a **dev-only dependency** ([dev-dependencies] in backend/Cargo.toml, not shipped in production). Remediation is still required for supply chain risk, but with the `dev-dependency` label and Normal priority override.

**Case A: Cross-stream impact** -- stream 2.1.x is also affected but is outside this issue's scope. A cross-stream impact comment would be posted, and preemptive remediation tasks created for 2.1.x if no sibling CVE Jira exists for that stream.

## Remediation Tasks for Stream 2.2.x

Ecosystem: Cargo (source dependency) -- 2 tasks: upstream backport + downstream propagation.

---

### Task 1: Upstream Backport (2.2.x)

**Summary:** Remediate CVE-2026-99001: bump criterion to 0.5.2 (2.2.x)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority:** Normal (overridden -- dev-only dependency, not shipped in production)

#### Task Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99001: path traversal in benchmark output in criterion.
The vulnerable dependency (criterion < 0.5.2) must be updated
to the fixed version (0.5.2+).

This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only).

Affected versions: 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4
Source commit(s): v0.4.5, v0.4.8, v0.4.11, v0.4.12

CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct dev-dependency (backend -> criterion)
- **Dependency scope**: dev-only ([dev-dependencies] in backend/Cargo.toml) -- not present in production builds, used for benchmarks only
- Priority is Normal regardless of CVE severity (dev-dependency override)

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update criterion dependency to >= 0.5.2 in backend/Cargo.toml [dev-dependencies]
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8050 (parent tracking issue)

---

### Task 2: Downstream Propagation (2.2.x)

**Summary:** Propagate CVE-2026-99001 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority:** Normal (overridden -- dev-only dependency, not shipped in production)

**Blocked by:** Task 1 (upstream backport must merge first)

#### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99001 fix from the upstream backport task.

The upstream backport bumps criterion to 0.5.2
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only).

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct dev-dependency -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8050 (parent tracking issue)

---

## Cross-Stream Impact (Case A)

Stream 2.1.x is also affected (all versions ship criterion 0.5.1 < 0.5.2). Since issue TC-8050 is scoped to 2.2.x, the following actions apply:

1. **Post cross-stream impact comment** on TC-8050:
   > Cross-stream impact: criterion < 0.5.2 also affects stream 2.1.x based on lock file analysis.
   > This stream is tracked by a companion issue (see Related links) or may require separate PSIRT triage.

2. **Check for existing sibling CVE Jira** for stream 2.1.x (search for Vulnerability issues with label CVE-2026-99001 and summary suffix [rhtpa-2.1]).

3. **If no sibling CVE Jira exists for 2.1.x**, create preemptive remediation tasks:
   - Upstream backport task for 2.1.x (release/0.3.z) with labels: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `security-preemptive`, `dev-dependency`
   - Downstream propagation task for 2.1.x (rhtpa-release.0.3.z) with labels: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `security-preemptive`, `dev-dependency`
   - Both tasks linked to TC-8050 with "Related" (not "Depend") link type
   - Priority: Normal (dev-dependency override)

4. **If a sibling CVE Jira exists for 2.1.x**, skip preemptive task creation -- that stream will be triaged through its own CVE issue.

## Jira Linkage Summary

| Link Type | From | To | Purpose |
|-----------|------|----|---------|
| Depend | TC-8050 | upstream backport task (2.2.x) | CVE -> remediation |
| Depend | TC-8050 | downstream propagation task (2.2.x) | CVE -> remediation |
| Blocks | upstream backport task (2.2.x) | downstream propagation task (2.2.x) | upstream -> downstream ordering |

## Post-Triage Actions

1. Add label `ai-cve-triaged` to TC-8050
2. Post summary comment on TC-8050 documenting:
   - Version impact table
   - Affects Versions correction (if any)
   - Triage outcome: remediation tasks created
   - Links to all remediation tasks
   - @mention of issue reporter
3. Transition TC-8050 status as appropriate

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks for 2.2.x (Cargo = source dependency: upstream backport + downstream propagation) -- matches ecosystem classification table
- [x] **Cross-stream coverage**: 2.1.x is affected and outside issue scope; preemptive tasks to be created if no sibling CVE Jira exists
- [x] **Link types**: "Depend" for tasks linked to TC-8050, "Related" for preemptive tasks, "Blocks" for upstream -> downstream within a stream
- [x] **Preemptive labels**: tasks for 2.1.x (if created) carry `security-preemptive` label
- [x] **Dev-dependency label**: all tasks carry `dev-dependency` label (criterion is dev-only)
- [x] **Priority override**: all tasks set to Normal priority (dev-dependency, not shipped in production)
- [x] **Coordination guidance**: included in Implementation Notes (deployment context: upstream)
