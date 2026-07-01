# Step 8 -- Remediation

## Triage Outcome: Case A -- Affected, create remediation tasks

Version 2.2.0 in the 2.2.x stream ships h2 0.4.5, which is below the enriched fix threshold of 0.4.8 (from Step 1.5 external CVE data enrichment). Remediation tasks are required.

The ecosystem is **Cargo** (source dependency), so two tasks are created: an upstream backport task and a downstream propagation subtask.

---

## Task 1: Upstream Backport Task

**Proposed Jira create_issue call:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-48901: bump h2 to 0.4.8 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-48901"]
)
```

### Task Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated
to the fixed version (0.4.8+).

Affected versions: RHTPA 2.2.0
Source commit(s): v0.4.5

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Target branch: release/0.4.z
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

- Depends on: TC-8030 (parent tracking issue)

---

## Task 2: Downstream Propagation Subtask

**Proposed Jira create_issue call:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-48901 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-48901"]
)
```

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-48901 fix from the upstream backport task.

The upstream backport task bumps h2 to 0.4.8
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
- Depends on: TC-8030 (parent tracking issue)

---

## Proposed Jira Linkage

After task creation, the following links would be created:

1. **Upstream task --> Vulnerability issue**: `jira.create_link(inwardIssue: "TC-8030", outwardIssue: "<upstream-task-key>", type: "Depend")`
2. **Downstream subtask --> Vulnerability issue**: `jira.create_link(inwardIssue: "TC-8030", outwardIssue: "<downstream-task-key>", type: "Depend")`
3. **Downstream subtask blocked by upstream task**: `jira.create_link(inwardIssue: "<upstream-task-key>", outwardIssue: "<downstream-task-key>", type: "Blocks")`

## Proposed Affects Versions Correction

Current: [RHTPA 2.2.0] --> Proposed: [RHTPA 2.2.0] (no change needed -- only 2.2.0 is affected, and PSIRT already assigned it correctly)

## Proposed Post-Triage Actions

1. Add label `ai-cve-triaged` to TC-8030
2. Transition TC-8030 to In Progress
3. Post summary comment documenting version impact, enrichment results, and remediation tasks

All Jira mutations are presented as proposals for engineer confirmation -- no changes are executed without explicit approval.
