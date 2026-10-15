# Step 7/8 -- Remediation: TC-8004

## Step 7 -- Concurrent Triage Detection

**Skipped.** The Upstream Affected Component custom field is not configured in Security Configuration. Concurrent triage detection requires this field.

## Step 7.5 -- Release Jira Orchestration

Release Jira orchestration applies only to the **2.1.x stream** (the only affected stream). The 2.2.x stream is not affected and requires no remediation or release tracking.

### Proposed Action: Find or Create Release Epic for 2.1.x

Search for existing release Epic matching `"RHTPA 2.1.* Release Tasks"`. If none found, propose creating one based on the latest released version in the 2.1.x supportability matrix (2.1.1), defaulting to the next patch version (2.1.2):

```
Proposed: Create Epic "RHTPA 2.1.2 Release Tasks"
Labels: ["ai-generated-jira"]
```

### Proposed Action: Find or Create Release Task

Search for existing release Task under the release Epic. If none found:

```
Proposed: Create Task "RHTPA 2.1.2 CVE triage" as child of release Epic
Labels: ["ai-generated-jira"]
```

## Case Determination

- **Case A (Cross-stream impact)**: Not applicable. This issue is **unscoped** (no stream suffix). Case A only applies to stream-scoped issues. Skipping.
- **Case B (Affected -- create remediation tasks)**: Applies to the **2.1.x stream**. Both versions (2.1.0, 2.1.1) ship h2 0.4.5, which is below the fix threshold of 0.4.8.
- **Case C (No supported versions affected)**: Applies to the **2.2.x stream**. All versions in this stream ship h2 >= 0.4.8 and are NOT affected. No remediation needed for this stream.

Since the 2.2.x stream is entirely unaffected, no remediation tasks are created for it. The overall issue is NOT closed as Case C because the 2.1.x stream IS affected.

## Remediation Tasks -- 2.1.x Stream Only

Ecosystem: **Cargo** (source dependency). The h2 crate fix version 0.4.8 is a published release, so this is a **dependency bump** scenario (not an upstream backport requiring source code changes). Per the skill procedure, two tasks are created:

### Task 1: Dependency Bump -- bump h2 on release/0.3.z

**Proposed Jira Issue Creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: update h2 to 0.4.8 (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

**Task Description:**

```markdown
## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: bump h2 to 0.4.8 via dependency update.
The vulnerable dependency (h2 versions before 0.4.8) is already fixed upstream --
a package manager update is sufficient.

Affected versions: RHTPA 2.1.0 (build v0.3.8), RHTPA 2.1.1 (build v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: source dependency (Cargo crate)
- **Remediation action**: run `cargo update -p h2` to pull in h2 >= 0.4.8
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add h2@0.4.8`
- Verify the lock file reflects h2 >= 0.4.8 after the update

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)
```

**Post-creation actions:**
1. Post description digest comment on the new task
2. Link: `Depend` -- TC-8004 (inward) to new task (outward)
3. Link: `Blocks` -- new task (inward) to release Task (outward) _(if release Jira active)_

---

### Task 2: Downstream Propagation -- update backend ref in rhtpa-release.0.3.z

**Proposed Jira Issue Creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

**Task Description:**

```markdown
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from the upstream dependency bump task.

The upstream dependency bump task bumps h2 to 0.4.8
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: source dependency -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: [upstream dependency bump task key] (upstream bump must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

**Post-creation actions:**
1. Post description digest comment on the new task
2. Link: `Depend` -- TC-8004 (inward) to new task (outward)
3. Link: `Blocks` -- upstream bump task (inward) to downstream task (outward)
4. Link: `Blocks` -- new task (inward) to release Task (outward) _(if release Jira active)_

---

## 2.2.x Stream -- No Remediation Required

The 2.2.x stream is **not affected** by CVE-2026-33501. All versions in this stream ship h2 >= 0.4.8 (the fix threshold). No remediation tasks are created for this stream.

| Version | h2 version | Status |
|---------|------------|--------|
| 2.2.0 | 0.4.8 | Ships fixed version |
| 2.2.1 | 0.4.8 | Ships fixed version |
| 2.2.2 | 0.4.8 | Ships fixed version (retag of 2.2.1) |
| 2.2.3 | 0.4.9 | Ships version above fix threshold |
| 2.2.4 | 0.4.9 | Ships version above fix threshold |

## Release Jira Linkage (Proposed)

If release Jira orchestration produces a release Task for the 2.1.x stream:

1. Link each remediation Task to release Task: `Blocks` (remediation inward, release Task outward)
2. Link CVE TC-8004 to release Task: `Related` (release Task inward, TC-8004 outward)

No release Jira linkage for the 2.2.x stream (no remediation tasks created).

## Post-Triage Summary (Proposed)

### Proposed Action: Add `ai-cve-triaged` label to TC-8004

```
jira.edit_issue(TC-8004, fields={
  "labels": ["CVE-2026-33501", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### Proposed Action: Post summary comment on TC-8004

```
Triage summary for CVE-2026-33501 (h2 memory exhaustion via CONTINUATION frames):

Version Impact:

| Version | Stream | h2 version | Affected? |
|---------|--------|------------|-----------|
| 2.1.0   | 2.1.x  | 0.4.5      | YES       |
| 2.1.1   | 2.1.x  | 0.4.5      | YES       |
| 2.2.0   | 2.2.x  | 0.4.8      | NO        |
| 2.2.1   | 2.2.x  | 0.4.8      | NO        |
| 2.2.2   | 2.2.x  | 0.4.8      | NO (retag of 2.2.1) |
| 2.2.3   | 2.2.x  | 0.4.9      | NO        |
| 2.2.4   | 2.2.x  | 0.4.9      | NO        |

Affects Versions corrected: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]
- Removed RHTPA 2.2.0 (ships h2 0.4.8, not affected)
- Added RHTPA 2.1.1 (ships h2 0.4.5, affected)

Outcome: Remediation required for 2.1.x stream only.

Remediation tasks created:
- [upstream-bump-task-key] -- dependency bump: update h2 to 0.4.8 on release/0.3.z
- [downstream-task-key] -- downstream propagation: update backend ref in
  rhtpa-release.0.3.z (blocked by [upstream-bump-task-key])

2.2.x stream: not affected (all versions ship h2 >= 0.4.8). No remediation required.
```

### Proposed Action: Transition TC-8004 to In Progress

```
jira.transition_issue(TC-8004, <in-progress-transition-id>)
```

## Pre-Creation Checklist

- [x] **Task count per stream**: 2.1.x stream: 2 tasks (dependency bump + downstream propagation) -- matches Cargo source dependency classification. 2.2.x stream: 0 tasks (not affected).
- [x] **Cross-stream coverage**: Not applicable -- issue is unscoped and Case A is skipped.
- [x] **Link types**: "Depend" for tasks linked to TC-8004. "Blocks" for upstream bump to downstream propagation. "Blocks" for remediation tasks to release Task (if active).
- [x] **Preemptive labels**: Not applicable -- no preemptive tasks created (issue is unscoped).
- [x] **Coordination guidance**: Each task includes "upstream" deployment context guidance.
- [x] **Release Jira linking**: Proposed pending release Epic/Task creation for 2.1.x.
- [x] **Dedup consistency**: No dedup detected (Step 7.5.3 not applicable without Upstream Affected Component field).
