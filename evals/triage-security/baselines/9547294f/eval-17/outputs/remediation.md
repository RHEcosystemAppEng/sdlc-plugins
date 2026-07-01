# Step 8 -- Remediation

## Triage Decision

The issue is scoped to stream **2.2.x** (suffix `[rhtpa-2.2]`). Within this stream, versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 are not affected. This is **Case A** (affected versions exist) -- create remediation tasks.

The embargo check (Step 1.7) was completed -- engineer confirmed proceeding with triage after reviewing the embargo policy at https://example.com/security/embargo-policy.

Cross-stream impact: stream 2.1.x is also affected (2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). Since this is a scoped issue (`[rhtpa-2.2]`), a cross-stream impact notice would be posted (Case B), but remediation tasks are only created for the scoped stream (2.2.x).

## Ecosystem: Cargo (Source Dependency)

For source dependency ecosystems (Cargo), two tasks are created per Important Rule 8: an upstream backport task and a downstream propagation subtask with a Blocks dependency.

---

## Proposed Task 1: Upstream Backport Task

**Proposed Jira API call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z (from Ecosystem Mappings)
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

## Proposed Task 2: Downstream Propagation Subtask

**Proposed Jira API call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Proposed Jira Linkage

After task creation, the following links would be established:

1. **Upstream task -> Vulnerability issue**: `jira.create_link(inwardIssue: "TC-8001", outwardIssue: "<upstream-task-key>", type: "Depend")`
2. **Downstream subtask -> Vulnerability issue**: `jira.create_link(inwardIssue: "TC-8001", outwardIssue: "<downstream-task-key>", type: "Depend")`
3. **Downstream blocked by upstream**: `jira.create_link(inwardIssue: "<upstream-task-key>", outwardIssue: "<downstream-task-key>", type: "Blocks")`

## Proposed Post-Triage Actions

All actions below are **proposals** presented for engineer confirmation before execution:

1. **Propose** adding label `ai-cve-triaged` to TC-8001
2. **Propose** transitioning TC-8001 to In Progress
3. **Propose** assigning TC-8001 to current user
4. **Propose** posting a summary comment to TC-8001 documenting the version impact table, Affects Versions correction, triage outcome, and links to remediation tasks

## Cross-Stream Impact Notice (Case B)

**Proposed comment** on TC-8001:
```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. Stream 2.1.x versions (2.1.0, 2.1.1)
ship quinn-proto 0.11.9 which is within the affected range.
This stream is tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```
