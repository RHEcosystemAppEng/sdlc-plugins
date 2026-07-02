# Remediation -- TC-8004

## Triage Outcome

**Case A: Affected** -- the 2.1.x stream ships vulnerable h2 (0.4.5 < 0.4.8). Remediation tasks are required for the 2.1.x stream only.

The 2.2.x stream is NOT affected (ships h2 >= 0.4.8) and requires no remediation.

## Ecosystem

Cargo (source dependency) -- requires **two** tasks:
1. Upstream backport task (fix in the source repo on the 2.1.x upstream branch)
2. Downstream propagation subtask (update the reference in the Konflux release repo)

## Task 1: Upstream Backport (2.1.x stream)

**Summary**: Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

### Description

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: memory exhaustion via CONTINUATION frames in h2 crate.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (backend v0.3.8), RHTPA 2.1.1 (backend v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
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

---

## Task 2: Downstream Propagation (2.1.x stream)

**Summary**: Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

### Description

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from the upstream backport task.

The upstream backport bumps h2 to >= 0.4.8 on release/0.3.z. Once that PR
merges, update the source pinning in this Konflux release repo so the next
build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
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

## Jira Linkage (proposed)

1. Link upstream backport task to TC-8004 with link type "Depend"
2. Link downstream propagation task to TC-8004 with link type "Depend"
3. Link downstream propagation task as blocked by upstream backport task with link type "Blocks"
4. Transition TC-8004 to In Progress
5. Add ai-cve-triaged label to TC-8004

## Streams Not Requiring Remediation

**2.2.x stream**: No remediation needed. All versions in this stream (2.2.0 through 2.2.4) ship h2 >= 0.4.8, which is at or above the fix threshold. No tasks created for this stream.

## Post-Triage Summary

Version impact analysis for CVE-2026-33501 (h2 < 0.4.8) shows mixed impact across streams:

- **2.1.x stream**: AFFECTED -- all versions ship h2 0.4.5 (vulnerable)
- **2.2.x stream**: NOT AFFECTED -- all versions ship h2 >= 0.4.8 (fixed)

Affects Versions corrected: removed RHTPA 2.2.0 (not affected), added RHTPA 2.1.1 (affected but missing from PSIRT assignment).

Remediation tasks created for 2.1.x stream only:
- Upstream backport task: bump h2 to >= 0.4.8 on release/0.3.z
- Downstream propagation task: update backend ref in rhtpa-release.0.3.z (blocked by upstream task)

No sibling issues found (JQL returned empty).
