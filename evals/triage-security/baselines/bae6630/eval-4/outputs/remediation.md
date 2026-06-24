# Remediation -- TC-8004

## Triage Outcome

**Case A: Affected -- create remediation tasks** for the 2.1.x stream only.

The 2.2.x stream is NOT affected (all versions ship h2 >= 0.4.8), so no remediation tasks are needed for that stream. This is a mixed-impact scenario where only one of two streams requires remediation.

## Remediation Tasks (2.1.x stream only)

Since h2 is a **Cargo (source dependency)** ecosystem package, two tasks are required per the remediation template: an upstream backport task and a downstream propagation subtask.

---

### Task 1: Upstream Backport Task (2.1.x)

**Summary**: Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-33501`

#### Description

```markdown
## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: Memory exhaustion via CONTINUATION frames in h2 crate.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (build v0.3.8), RHTPA 2.1.1 (build v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- h2 is a transitive dependency via hyper -- the bump may require
  updating hyper or other intermediate crates
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

---

### Task 2: Downstream Propagation Subtask (2.1.x)

**Summary**: Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-33501`

#### Description

```markdown
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
```

---

## Jira Linkage

1. Link upstream task to TC-8004 with type "Depend"
2. Link downstream subtask to TC-8004 with type "Depend"
3. Link downstream subtask as blocked by upstream task with type "Blocks"
4. Transition TC-8004 to In Progress
5. Assign TC-8004 to current user
6. Add `ai-cve-triaged` label to TC-8004

## Cross-Stream Notice

No cross-stream remediation is needed. The 2.2.x stream is not affected -- all versions ship h2 >= 0.4.8, which is at or above the fix threshold. No proactive (preemptive) remediation tasks are required for the 2.2.x stream.

## Sibling / Duplicate Check

JQL search for sibling issues returned empty (no sibling Vulnerability issues exist for CVE-2026-33501). No duplicate or cross-stream companion issues to link.

## Post-Triage Summary Comment (to be posted to TC-8004)

```
Triage complete for CVE-2026-33501 (h2 -- memory exhaustion via CONTINUATION frames).

Version Impact:

| Version | h2 Version | Affected? | Notes |
|---------|------------|-----------|-------|
| 2.1.0   | 0.4.5      | YES       |       |
| 2.1.1   | 0.4.5      | YES       |       |
| 2.2.0   | 0.4.8      | NO        | at fix threshold |
| 2.2.1   | 0.4.8      | NO        |       |
| 2.2.2   | --         | NO        | retag of 2.2.1 |
| 2.2.3   | 0.4.9      | NO        |       |
| 2.2.4   | 0.4.9      | NO        |       |

Affects Versions corrected: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].
RHTPA 2.2.0 removed (not affected). RHTPA 2.1.1 added (affected).

Outcome: Remediation tasks created for the 2.1.x stream only.
- Upstream backport task: bump h2 to >= 0.4.8 on release/0.3.z
- Downstream propagation task: update backend ref in rhtpa-release.0.3.z (blocked by upstream task)

The 2.2.x stream requires no remediation -- all versions ship h2 >= 0.4.8.
```
