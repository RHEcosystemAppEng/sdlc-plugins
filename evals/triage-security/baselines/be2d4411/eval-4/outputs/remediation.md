# Step 8 -- Remediation

## Triage Outcome: Case A -- Affected (create remediation tasks for 2.1.x only)

The version impact analysis shows that only the **2.1.x stream** is affected. The **2.2.x stream** already ships h2 >= 0.4.8 and requires no remediation.

Since the issue is **unscoped**, no cross-stream impact notice (Case B) is generated -- the unscoped issue already covers all streams, so there is no "other stream outside scope" to notify about.

Remediation tasks are created only for the **2.1.x stream**.

## Ecosystem: Cargo (Source Dependency) -- Two Tasks

Since h2 is a Cargo (source) dependency, two tasks are created per the remediation templates:
1. **Upstream backport task** -- bump h2 in the source repository
2. **Downstream propagation subtask** -- update the source reference in the Konflux release repo

---

## Task 1: Upstream Backport (2.1.x)

**Summary**: Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-33501`

### Task Description

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: memory exhaustion via CONTINUATION frames in h2.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (v0.3.8), RHTPA 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock (and Cargo.toml if directly specified)
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)
- The fix adds a configurable maximum header list size that defaults to 16 KiB

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)

---

## Task 2: Downstream Propagation (2.1.x)

**Summary**: Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-33501`

### Task Description

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-33501 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)

---

## Jira Linkage

After task creation:

1. Link upstream backport task to TC-8004 with type "Depend"
2. Link downstream propagation task to TC-8004 with type "Depend"
3. Link downstream propagation task as blocked by upstream backport task with type "Blocks"
4. Post description digest comments on both tasks
5. Transition TC-8004 to In Progress
6. Assign TC-8004 to current user

## Post-Triage Summary

### Label Addition

Add `ai-cve-triaged` label to TC-8004.

### Summary Comment

```
Triage summary for CVE-2026-33501 (h2 < 0.4.8):

Version Impact:

| Version | h2 version | Affected? | Notes |
|---------|------------|-----------|-------|
| 2.1.0   | 0.4.5      | YES       | < 0.4.8 |
| 2.1.1   | 0.4.5      | YES       | < 0.4.8 |
| 2.2.0   | 0.4.8      | NO        | >= 0.4.8 (fixed) |
| 2.2.1   | 0.4.8      | NO        | >= 0.4.8 (fixed) |
| 2.2.2   | --         | NO        | retag of 2.2.1 |
| 2.2.3   | 0.4.9      | NO        | >= 0.4.8 (fixed) |
| 2.2.4   | 0.4.9      | NO        | >= 0.4.8 (fixed) |

Affects Versions corrected: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]

Outcome: Remediation tasks created for 2.1.x stream only.
- <upstream-task-key> (upstream backport: bump h2 to 0.4.8 on release/0.3.z)
- <downstream-task-key> (downstream propagation: update backend ref in rhtpa-release.0.3.z, blocked by <upstream-task-key>)

No remediation needed for 2.2.x -- all versions already ship h2 >= 0.4.8.

No sibling issues found (JQL returned empty).

@<reporter-name> (reporter mention)

---
This comment was AI-generated by sdlc-workflow/triage-security v0.11.1.
```
