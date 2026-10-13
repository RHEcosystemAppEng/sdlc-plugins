# Remediation — TC-8004 (CVE-2026-33501)

## Step 8: Remediation Decision

### Decision Tree

1. **Any supported versions affected?** YES — 2.1.0 and 2.1.1 (stream 2.1.x) are affected.
2. **Issue scoped to a single stream?** NO — issue is unscoped (no stream suffix).
3. **Case A (cross-stream impact)?** SKIPPED — unscoped issues cover all streams by definition; Case A applies only to scoped issues.
4. **Case B (create remediation tasks for affected streams):** Applies — create remediation tasks for stream 2.1.x only. Stream 2.2.x is not affected and requires no remediation.

### Ecosystem and Task Structure

- **Ecosystem**: Cargo (source dependency)
- **Upstream fix available on release/0.3.z?**: NO (latest tag v0.3.12 ships h2 0.4.5, below fix threshold 0.4.8)
- **Tasks per stream**: 2 (upstream backport + downstream propagation)
- **Affected stream**: 2.1.x only

---

## Remediation Task 1: Upstream Backport (Stream 2.1.x)

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

### Task Description

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 - Memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Versions of h2 before 0.4.8 are vulnerable to memory exhaustion caused by a peer
sending an excessive number of CONTINUATION frames following a HEADERS frame.

Affected versions: RHTPA 2.1.0 (v0.3.8), RHTPA 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: To be determined via Cargo.lock and Cargo.toml inspection.
  h2 is commonly a transitive dependency pulled in through hyper or tonic in Rust
  HTTP services. Inspect the lock file to confirm.

### Remediation approach (if direct dependency)

- Update h2 dependency to >= 0.4.8 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a code-level
  workaround is viable (see upstream changelog)

### Remediation approach (if transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in h2 (see dependency chain)
- Bump the direct dependency to a version whose transitive closure includes
  h2 >= 0.4.8
- Verify the bump does not introduce breaking API changes to the direct dependency

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable:
- Cargo: `cargo add h2@0.4.8` to add as a direct dependency, overriding the
  transitive resolution
- Document why the direct dep bump was not viable in the PR description

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)
```

### Post-creation: Description digest comment

After creating the task, post a description digest comment per the description-digest-protocol before creating any links.

### Jira Linkage

```
jira.create_link(
  inwardIssue: "TC-8004",
  outwardIssue: "<upstream-task-key>",
  type: "Depend"
)
```

---

## Remediation Task 2: Downstream Propagation (Stream 2.1.x)

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

### Task Description

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
- **Dependency type**: Carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback approach),
  verify the pinning is reflected in the downstream build's lock file after the
  source reference update
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

### Post-creation: Description digest comment

After creating the task, post a description digest comment per the description-digest-protocol before creating any links.

### Jira Linkage

```
# Link downstream task to CVE issue
jira.create_link(
  inwardIssue: "TC-8004",
  outwardIssue: "<downstream-task-key>",
  type: "Depend"
)

# Link downstream blocked by upstream
jira.create_link(
  inwardIssue: "<upstream-task-key>",
  outwardIssue: "<downstream-task-key>",
  type: "Blocks"
)
```

---

## Step 7.5: Release Jira Orchestration

_(Simulated — not calling Jira MCP in eval mode)_

For the affected 2.1.x stream, Step 7.5 would:
1. Search for an existing release Epic matching "RHTPA 2.1.* Release Tasks"
2. If found, use it; if not, propose creating one (e.g., "RHTPA 2.1.2 Release Tasks" based on next patch bump after 2.1.1)
3. Find or create a release Task "RHTPA 2.1.2 CVE triage" as a child of the Epic
4. After remediation task creation, link tasks to the release Task:

```
# Link remediation tasks to release Task (Blocks)
jira.create_link(inwardIssue: "<upstream-task-key>", outwardIssue: "<release-task-key>", type: "Blocks")
jira.create_link(inwardIssue: "<downstream-task-key>", outwardIssue: "<release-task-key>", type: "Blocks")

# Link CVE to release Task (Related)
jira.create_link(inwardIssue: "<release-task-key>", outwardIssue: "TC-8004", type: "Related")
```

Stream 2.2.x requires no release Jira orchestration since it is not affected.

---

## Pre-creation Checklist

- [x] **Task count per stream**: 2 tasks for 2.1.x stream (upstream backport + downstream propagation) -- matches Cargo source dependency ecosystem classification
- [x] **Cross-stream coverage**: N/A -- issue is unscoped, Case A is skipped. No preemptive tasks needed.
- [x] **Link types**: "Depend" for tasks linked to TC-8004, "Blocks" for upstream to downstream within stream 2.1.x
- [x] **Preemptive labels**: N/A -- no preemptive tasks created (issue is unscoped)
- [x] **Coordination guidance**: Included in each task's Implementation Notes with "upstream" deployment context guidance
- [x] **Release Jira linking**: Would link remediation Tasks to release Task (Blocks) and CVE to release Task (Related) after Step 7.5 resolution
- [x] **Dedup consistency**: N/A -- no dedup scenarios (Step 4.3 skipped, Step 7.5.3 would check at runtime)

## Post-Triage Summary

After all remediation tasks are created, the following post-triage actions would be performed:

### 1. Add `ai-cve-triaged` label to TC-8004

```
jira.edit_issue("TC-8004", fields={
  "labels": ["CVE-2026-33501", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### 2. Post summary comment on TC-8004

```
CVE-2026-33501 triage complete for TC-8004 (h2 - Memory exhaustion via CONTINUATION frames).

Version Impact:

| Version | Stream | h2 Version | Affected? |
|---------|--------|------------|-----------|
| 2.1.0   | 2.1.x  | 0.4.5      | YES       |
| 2.1.1   | 2.1.x  | 0.4.5      | YES       |
| 2.2.0   | 2.2.x  | 0.4.8      | NO        |
| 2.2.1   | 2.2.x  | 0.4.8      | NO        |
| 2.2.2   | 2.2.x  | (retag)    | NO        |
| 2.2.3   | 2.2.x  | 0.4.9      | NO        |
| 2.2.4   | 2.2.x  | 0.4.9      | NO        |

Affects Versions corrected: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]
- Removed RHTPA 2.2.0 (not affected: ships h2 0.4.8)
- Added RHTPA 2.1.1 (affected: ships h2 0.4.5)

Triage outcome: Remediation required for stream 2.1.x only. Stream 2.2.x ships h2 >= 0.4.8 (patched).

Remediation tasks created:
- <upstream-task-key>: Upstream backport — bump h2 to >= 0.4.8 on release/0.3.z (rhtpa-2.1)
- <downstream-task-key>: Downstream propagation — update backend ref in rhtpa-release.0.3.z (blocked by <upstream-task-key>)

No sibling issues found. No duplicate or overlap scenarios detected.
```

### 3. Transition TC-8004 to In Progress

```
jira.transition_issue("TC-8004", <in-progress-transition-id>)
```
