# Step 8 -- Remediation

## Triage Outcome

**Case A: Affected -- create remediation tasks** for the 2.2.x stream.

All versions in the 2.2.x stream ship criterion 0.5.1 (vulnerable). The fixed
version is 0.5.2. Remediation tasks are required.

**Dev-dependency override**: criterion is a dev-only dependency (identified in
Step 2.3.5). Per the dependency scope decision tree:
- Label `dev-dependency` is added to all remediation tasks
- Priority is set to **Normal** regardless of CVE severity (CVSS 5.3 Medium)
- Tasks include a note that the dependency is not shipped in production

**Ecosystem**: Cargo (source dependency) -- two tasks are created:
1. Upstream backport task (fix in the source repo)
2. Downstream propagation subtask (update reference in Konflux release repo)

---

## Task 1: Upstream Backport Task

**Summary**: Remediate CVE-2026-99001: bump criterion to 0.5.2 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority**: Normal

### Task Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99001: path traversal in benchmark output in criterion.
The vulnerable dependency (criterion versions before 0.5.2) must be updated
to the fixed version (0.5.2+).

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

Affected versions: RHTPA 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4
Source commit(s): v0.4.5, v0.4.8, v0.4.11, v0.4.12

Upstream fix: (none available in remote links)
Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
- **Dependency scope**: dev-only ([dev-dependencies] in backend/Cargo.toml) -- not shipped in production builds, used for benchmarks only

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update criterion dependency to >= 0.5.2 in backend/Cargo.toml
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8050 (parent tracking issue)

---

## Task 2: Downstream Propagation Subtask

**Summary**: Propagate CVE-2026-99001 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority**: Normal

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99001 fix from the upstream backport task.

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

The upstream backport bumps criterion to 0.5.2
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

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

---

## Jira Linkage (proposed)

1. Link upstream backport task to TC-8050 with link type "Depend"
2. Link downstream propagation task to TC-8050 with link type "Depend"
3. Link downstream propagation task as blocked by upstream backport task with link type "Blocks"
4. Transition TC-8050 to In Progress
5. Add `ai-cve-triaged` label to TC-8050

## Cross-Stream Impact (Case B check)

The issue is scoped to stream 2.2.x. The 2.1.x stream also ships criterion
0.5.1 at all versions, meaning it is also affected. In a real triage:
- Check for existing CVE Jira for CVE-2026-99001 in the 2.1.x stream
- If none exists, create preemptive remediation tasks with `security-preemptive` label
- Post cross-stream impact comment on TC-8050

## Post-Triage Summary (proposed comment)

Version impact analysis for CVE-2026-99001 (criterion < 0.5.2):

All 2.2.x versions ship criterion 0.5.1 (affected). criterion is a dev-only
dependency ([dev-dependencies]) and is NOT present in production builds.

Remediation tasks created with `dev-dependency` label and Normal priority:
- Upstream backport task (bump criterion to >= 0.5.2 on release/0.4.z)
- Downstream propagation task (update backend ref in rhtpa-release.0.4.z)
