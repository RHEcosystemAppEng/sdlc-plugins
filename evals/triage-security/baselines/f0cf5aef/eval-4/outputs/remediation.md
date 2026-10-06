# Step 8 -- Remediation

## Triage Outcome: Case B (Affected -- create remediation tasks)

### Decision Logic

1. **Any supported versions affected?** YES -- 2.1.0 and 2.1.1 are affected.
2. **Issue scoped to a single stream?** NO -- TC-8004 is unscoped (no stream suffix).
3. **Unscoped path**: Skip Case A (cross-stream notice) entirely. Create remediation tasks for affected streams only.
4. **Affected streams**: Only 2.1.x is affected. The 2.2.x stream ships h2 >= 0.4.8 in all versions and requires no remediation.
5. **Ecosystem**: Cargo (source dependency) -- 2 tasks for the affected stream.

### Why No Cross-Stream Notice

Per the skill instructions (Case A guard): "Case A applies exclusively to stream-scoped issues (those whose summary contains a stream suffix). Unscoped issues cover all streams by definition -- there are no 'other streams outside this issue's scope,' so the cross-stream impact check is not applicable."

TC-8004 is unscoped, so Case A is skipped. No cross-stream notice is posted.

### Why No 2.2.x Remediation

The version impact analysis shows that all 2.2.x versions ship h2 >= 0.4.8 (the fixed version). No remediation tasks are created for unaffected streams.

---

## Remediation Tasks for Stream 2.1.x

### Task 1: Upstream Backport

**Summary**: Remediate CVE-2026-33501: bump h2 to 0.4.8 (rhtpa-2.1)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

**Description**:

```
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed
version (0.4.8+).

Affected versions: RHTPA 2.1.0 (v0.3.8), RHTPA 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: h2 is likely a transitive dependency (chain: backend workspace -> [hyper/reqwest] -> h2)
- Current h2 version on release/0.3.z: 0.4.5
- Required h2 version: >= 0.4.8

### Remediation approach (transitive dependency)

The h2 crate is typically pulled in through hyper or reqwest as a
transitive dependency. Use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in h2 (likely hyper or reqwest)
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

**Jira creation call**:
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (rhtpa-2.1)",
  description: <upstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

### Task 2: Downstream Propagation (blocked by Task 1)

**Summary**: Propagate CVE-2026-33501 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

**Description**:

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from the upstream backport task.

The upstream backport bumps h2 to >= 0.4.8 on release/0.3.z. Once that
PR merges, update the source pinning in this Konflux release repo so
the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: transitive -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

**Jira creation call**:
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <downstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

### Linkage

```
# Link upstream task to CVE
jira.create_link(inwardIssue: "TC-8004", outwardIssue: <upstream-task-key>, type: "Depend")

# Link downstream task to CVE
jira.create_link(inwardIssue: "TC-8004", outwardIssue: <downstream-task-key>, type: "Depend")

# Block downstream on upstream
jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
```

---

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks for 2.1.x (Cargo = source dependency ecosystem) -- matches classification table
- [x] **Cross-stream coverage**: Not applicable -- unscoped issue; Case A skipped. 2.2.x is not affected so no remediation needed.
- [x] **Link types**: "Depend" for tasks linked to TC-8004; "Blocks" for upstream -> downstream within 2.1.x stream
- [x] **Preemptive labels**: Not applicable -- no preemptive tasks created (issue is unscoped)
- [x] **Coordination guidance**: Omitted -- Source Repositories table has no Deployment Context column (backward compatibility)

## Sibling/Duplicate Check (Step 4)

JQL search for sibling Vulnerability issues with label CVE-2026-33501 returned **empty** (no siblings exist). No duplicate or cross-stream coordination actions needed.

## Post-Triage Summary

After task creation, the following actions would be performed on TC-8004:

1. Add label `ai-cve-triaged` to TC-8004
2. Post summary comment documenting:
   - Version impact table (mixed: 2.1.x affected, 2.2.x not affected)
   - Affects Versions correction: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]
   - Remediation: 2 tasks created for stream 2.1.x only
   - No remediation for 2.2.x (all versions ship h2 >= 0.4.8)
   - @mention of the issue reporter
