# Step 8 -- Remediation: TC-8004 (CVE-2026-33501)

## Triage Outcome: Case B -- Create remediation tasks for affected stream(s) only

### Decision Rationale

- **Issue scope**: Unscoped (no stream suffix) -- covers all streams
- **Case A (cross-stream impact)**: SKIPPED -- Case A applies exclusively to stream-scoped issues. This issue is unscoped, so cross-stream impact analysis is not applicable.
- **Affected streams**: 2.1.x only (2.2.x ships h2 >= 0.4.8, not affected)
- **Ecosystem**: Cargo (source dependency) -- 2 tasks per affected stream
- **Total tasks to create**: 2 (upstream backport + downstream propagation for 2.1.x only)

No remediation tasks are needed for the 2.2.x stream because all 2.2.x versions ship h2 0.4.8 or later, which is at or above the fix threshold.

---

## Remediation Task 1: Upstream Backport (2.1.x stream)

**Summary**: Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

### Task Description

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed
version (0.4.8+).

Affected versions: RHTPA 2.1.0 (tag v0.3.8), RHTPA 2.1.1 (tag v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: to be confirmed via Cargo.toml analysis (direct or transitive)

### Remediation approach (direct dependency)

When h2 is a direct dependency of a workspace member:

- Update h2 dependency to >= 0.4.8 in Cargo.toml
- Run `cargo update -p h2` to update Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

When h2 is a transitive dependency (pulled in through intermediate packages),
use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in h2 (see dependency chain)
- Bump the direct dependency to a version whose transitive closure
  includes h2 >= 0.4.8
- Verify the bump does not introduce breaking API changes

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable:
- `cargo add h2@0.4.8` to add as a direct dependency, overriding the
  transitive resolution
- Document why the direct dep bump was not viable in the PR description

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

## Remediation Task 2: Downstream Propagation (2.1.x stream)

**Summary**: Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

**Blocked by**: Upstream backport task (Task 1 above)

### Task Description

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from the upstream backport task.

The upstream backport bumps h2 to >= 0.4.8 on release/0.3.z. Once that
PR merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the backend reference to the merged commit or new release tag
  that includes h2 >= 0.4.8
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: [upstream-backport-task-key] (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

---

## Jira Linkage Plan

1. **Link upstream backport task** to TC-8004 with type "Depend"
2. **Link downstream propagation task** to TC-8004 with type "Depend"
3. **Link downstream propagation task** as blocked by upstream backport task with type "Blocks"
4. **Transition** TC-8004 to In Progress
5. **Add label** `ai-cve-triaged` to TC-8004
6. **Post summary comment** to TC-8004 listing both remediation tasks

## Post-Triage Summary Comment (to be posted on TC-8004)

```
CVE-2026-33501 triage complete for h2 (memory exhaustion via CONTINUATION frames).

Version Impact:

| Version | h2 version | Affected? | Notes |
|---------|------------|-----------|-------|
| 2.1.0   | 0.4.5      | YES       |       |
| 2.1.1   | 0.4.5      | YES       |       |
| 2.2.0   | 0.4.8      | NO        | ships fixed version |
| 2.2.1   | 0.4.8      | NO        | ships fixed version |
| 2.2.2   | --         | NO        | retag of 2.2.1 |
| 2.2.3   | 0.4.9      | NO        | ships version above fix threshold |
| 2.2.4   | 0.4.9      | NO        | ships version above fix threshold |

Affects Versions corrected: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]

Triage outcome: Remediation tasks created for 2.1.x stream only (2.2.x not affected).
- [upstream-task-key] -- upstream backport: bump h2 to >= 0.4.8 on release/0.3.z
- [downstream-task-key] -- downstream propagation: update backend ref in rhtpa-release.0.3.z
  (blocked by upstream task)

No remediation needed for 2.2.x stream -- all versions ship h2 >= 0.4.8.
```
