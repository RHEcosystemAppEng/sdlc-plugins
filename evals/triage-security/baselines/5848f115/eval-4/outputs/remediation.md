# Step 8 -- Remediation: TC-8004

## Triage Decision

**Case B: Affected -- create remediation tasks** for the 2.1.x stream only.

### Decision Rationale

- The issue is **unscoped** (no stream suffix), so Case A (cross-stream impact comment) does not apply. Per the skill methodology: "Unscoped issues cover all streams by definition -- there are no 'other streams outside this issue's scope,' so the cross-stream impact check is not applicable. For unscoped issues, skip Case A entirely and proceed directly to Case B task creation for all affected streams."
- The version impact table shows the **2.1.x stream is affected** (all versions ship h2 0.4.5, which is < 0.4.8).
- The **2.2.x stream is NOT affected** (all versions ship h2 >= 0.4.8). No remediation tasks are created for 2.2.x.
- h2 is a **Cargo** (source dependency) ecosystem, so **2 tasks** are created for the affected 2.1.x stream: upstream backport + downstream propagation.
- No sibling issues exist (JQL returns empty).
- No Deployment Context column in Source Repositories table (backward compatibility), so coordination guidance is omitted.

## Remediation Tasks for 2.1.x Stream

### Task 1: Upstream Backport

**Summary**: Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-33501`

**Description**:

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- The h2 crate is a direct dependency of the backend workspace

### Remediation approach (direct dependency)

- Update h2 dependency to >= 0.4.8 in Cargo.toml
- Run `cargo update -p h2` to update Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog for 0.4.8)
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

**Jira Creation**:
```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)",
  description: <upstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

**Linkage**:
```
jira.create_link(
  inwardIssue: "TC-8004",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)
```

---

### Task 2: Downstream Propagation (blocked by Task 1)

**Summary**: Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-33501`

**Description**:

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-33501
fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps h2 to 0.4.8 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release repo so
the next build ships the fix.

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

**Jira Creation**:
```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <downstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

**Linkage**:
```
# Link downstream to CVE issue
jira.create_link(
  inwardIssue: "TC-8004",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)

# Block downstream on upstream
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)
```

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks for 2.1.x (Cargo = source dependency: upstream backport + downstream propagation) -- matches ecosystem classification table
- [x] **Cross-stream coverage**: Not applicable -- issue is unscoped; 2.2.x is not affected so no tasks needed
- [x] **Link types**: "Depend" for tasks linked to TC-8004; "Blocks" for upstream -> downstream within 2.1.x stream
- [x] **Preemptive labels**: Not applicable -- no preemptive tasks needed (issue is unscoped and 2.2.x is not affected)
- [x] **Coordination guidance**: Omitted -- no Deployment Context column in Source Repositories table (backward compatibility)

## Post-Triage Actions

1. **Add label**: `ai-cve-triaged` to TC-8004
2. **Post summary comment** to TC-8004 with:
   - Version impact table
   - Affects Versions correction: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]
   - Triage outcome: remediation tasks created for 2.1.x stream; 2.2.x stream not affected
   - Links to upstream and downstream remediation tasks
   - @mention of the issue reporter (PSIRT analyst)
3. **Transition** TC-8004 to In Progress

## Summary

| Stream | Affected? | Tasks Created | Reason |
|--------|-----------|---------------|--------|
| 2.1.x | YES | 2 (upstream backport + downstream propagation) | Ships h2 0.4.5 (< 0.4.8) |
| 2.2.x | NO | 0 | Ships h2 >= 0.4.8 (already fixed) |
