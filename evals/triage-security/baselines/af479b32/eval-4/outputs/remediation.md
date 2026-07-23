# Remediation — TC-8004 (CVE-2026-33501)

## Triage Outcome

**Case A: Affected -- create remediation tasks** for the 2.1.x stream only.

The issue is unscoped, so all streams were analyzed. Only the **2.1.x stream** is affected (all versions ship h2 0.4.5, which is below the fix threshold of 0.4.8). The **2.2.x stream** is NOT affected (all versions ship h2 >= 0.4.8). Remediation tasks are created only for the affected stream.

Case B (cross-stream impact) does not apply because the issue is unscoped -- it covers all streams by definition.

## Duplicate / Sibling Check

No sibling Vulnerability issues found for CVE-2026-33501 (JQL returned empty). No duplicates or companion trackers to reconcile.

## Remediation Tasks (2.1.x stream)

Since h2 is a Cargo (source) dependency, two tasks are required per the skill's ecosystem rules:

### Task 1: Upstream Backport

**Summary**: Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-33501`

```markdown
## Repository

backend

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
- **Dependency type**: to be determined via Cargo.toml inspection (direct or transitive)
- Update h2 dependency to >= 0.4.8 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)
- The fix adds a configurable maximum header list size defaulting to 16 KiB

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

**Summary**: Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-33501`

```markdown
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from the upstream backport task.

The upstream backport bumps h2 to >= 0.4.8 on release/0.3.z. Once that
PR merges, update the source pinning in this Konflux release repo so
the next build ships the fix.

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

## Jira Linkage

After task creation:

1. Link upstream backport task to TC-8004 with type "Depend"
2. Link downstream propagation task to TC-8004 with type "Depend"
3. Link downstream propagation task as blocked by upstream backport task with type "Blocks"
4. Transition TC-8004 to In Progress
5. Add `ai-cve-triaged` label to TC-8004

## Post-Triage Summary Comment

The following summary comment would be posted to TC-8004:

```
Version Impact for CVE-2026-33501 (h2 < 0.4.8):

| Version | Stream | h2 version | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0   | 2.1.x  | 0.4.5      | YES       |       |
| 2.1.1   | 2.1.x  | 0.4.5      | YES       |       |
| 2.2.0   | 2.2.x  | 0.4.8      | NO        | ships fixed version |
| 2.2.1   | 2.2.x  | 0.4.8      | NO        | ships fixed version |
| 2.2.2   | 2.2.x  | --         | NO        | retag of 2.2.1 |
| 2.2.3   | 2.2.x  | 0.4.9      | NO        | above fix threshold |
| 2.2.4   | 2.2.x  | 0.4.9      | NO        | above fix threshold |

Affects Versions corrected: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]

Triage outcome: Remediation required for stream 2.1.x only. Stream 2.2.x
ships h2 >= 0.4.8 (fixed) across all versions -- no action needed.

Remediation tasks created:
- [upstream-task-key] (upstream backport: bump h2 to >= 0.4.8 on release/0.3.z)
- [downstream-task-key] (downstream propagation: update backend ref in rhtpa-release.0.3.z, blocked by [upstream-task-key])
```

## Why No Remediation for 2.2.x

The 2.2.x stream is completely unaffected:

- 2.2.0 ships h2 0.4.8 (the exact fix version)
- 2.2.1 ships h2 0.4.8
- 2.2.2 is a retag of 2.2.1 (same h2 0.4.8)
- 2.2.3 ships h2 0.4.9 (above fix threshold)
- 2.2.4 ships h2 0.4.9 (above fix threshold)

No remediation tasks are created for 2.2.x because no version in that stream ships a vulnerable h2 version.
