# Remediation -- TC-8004

## Triage Outcome

**Case A: Affected -- create remediation tasks** for the 2.1.x stream only.

The issue is **unscoped** (covers all streams). Version impact analysis shows:
- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1 ship h2 0.4.5)
- **2.2.x stream**: NO versions affected (all ship h2 >= 0.4.8)

Per the skill definition, Case B (cross-stream impact) is skipped for unscoped issues -- they cover all streams by definition. Remediation tasks are created only for the affected stream (2.1.x).

Since the ecosystem is **Cargo** (source dependency), two tasks are created: an upstream backport task and a downstream propagation subtask.

No sibling issues exist (JQL returns empty), so Steps 4.1 and 4.2 produce no findings.

---

## Task 1: Upstream Backport (2.1.x stream)

**Summary**: Remediate CVE-2026-33501: bump h2 to 0.4.8 (rhtpa-2.1)
**Labels**: ai-generated-jira, Security, CVE-2026-33501
**Issue Type**: Task

### Task Description

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 versions before 0.4.8) must be updated
to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update h2 dependency to >= 0.4.8 in Cargo.lock (and Cargo.toml if version-pinned)
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

### Jira Linkage

```
jira.create_link(
  inwardIssue: "TC-8004",
  outwardIssue: "<upstream-task-key>",
  type: "Depend"
)
```

---

## Task 2: Downstream Propagation (2.1.x stream)

**Summary**: Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)
**Labels**: ai-generated-jira, Security, CVE-2026-33501
**Issue Type**: Task

### Task Description

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps h2 to 0.4.8
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

### Jira Linkage

```
# Link downstream task as blocked by upstream task
jira.create_link(
  inwardIssue: "<upstream-task-key>",
  outwardIssue: "<downstream-task-key>",
  type: "Blocks"
)

# Link downstream task to the Vulnerability issue
jira.create_link(
  inwardIssue: "TC-8004",
  outwardIssue: "<downstream-task-key>",
  type: "Depend"
)
```

---

## Why No Tasks for 2.2.x

The 2.2.x stream ships h2 0.4.8 or later at every version (2.2.0 through 2.2.4). Since 0.4.8 is the fix version for CVE-2026-33501, no remediation is needed for the 2.2.x stream. No tasks are created.

---

## Post-Triage Actions

1. **Add label**: `ai-cve-triaged` to TC-8004
2. **Post summary comment** to TC-8004 with:
   - Version impact table (mixed impact: 2.1.x affected, 2.2.x not affected)
   - Affects Versions correction: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]
   - Triage outcome: remediation tasks created for 2.1.x stream only
   - Links to upstream backport task and downstream propagation task
   - @mention of the reporter (PSIRT analyst)
3. **Transition** TC-8004 to In Progress
