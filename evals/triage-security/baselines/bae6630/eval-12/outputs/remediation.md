# Step 7 -- Remediation

## Triage Outcome: Case C (No Supported Versions Affected in Scoped Stream)

The version impact analysis (Step 2) shows that **no versions in the 2.2.x stream** (the issue's scope) ship a vulnerable version of h2. All 2.2.x versions ship h2 >= 0.4.8, which is at or above the enriched fix threshold from Step 1.5.

### Proposed Action: Close as Not a Bug

**Recommendation**: Close TC-8030 as Not a Bug (not affected).

Proposed Jira actions (pending engineer confirmation):

1. **Add comment** to TC-8030:

   > No supported versions in the 2.2.x stream ship a vulnerable version of h2.
   > Version impact analysis (using enriched fix threshold 0.4.8 from MITRE CVE API
   > and OSV.dev cross-validation):
   >
   > | Version | h2 version | Affected? |
   > |---------|-----------|-----------|
   > | 2.2.0 | 0.4.8 | NO |
   > | 2.2.1 | 0.4.8 | NO |
   > | 2.2.2 | 0.4.8 | NO (retag of 2.2.1) |
   > | 2.2.3 | 0.4.9 | NO |
   > | 2.2.4 | 0.4.9 | NO |
   >
   > All 2.2.x versions ship h2 >= 0.4.8, which is outside the affected range (< 0.4.8).
   >
   > Note: Cross-stream analysis shows the 2.1.x stream IS affected (h2 0.4.5 < 0.4.8).
   > This is tracked separately -- see cross-stream impact notice below.

2. **Transition** TC-8030 to Closed with resolution "Not a Bug".

3. **Set VEX Justification** (customfield_12345) to **"Component not Present"** -- the vulnerable version of h2 (< 0.4.8) is not shipped in any 2.2.x product version.

4. **Assign** to current user.

5. **Add label** `ai-cve-triaged` to TC-8030.

## Cross-Stream Impact Notice (Case B)

The version impact analysis reveals that the **2.1.x stream** (outside this issue's scope) is affected:

- 2.1.0: h2 0.4.5 (affected, < 0.4.8)
- 2.1.1: h2 0.4.5 (affected, < 0.4.8)

### Proposed Cross-Stream Comment

Post to TC-8030:

> Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file
> analysis. Stream 2.1.x versions ship h2 0.4.5. This stream is tracked by a
> companion issue (see Related links) or may require separate PSIRT triage.

### Preemptive Remediation for 2.1.x

If no sibling CVE Jira exists for stream 2.1.x (confirmed via JQL search for label `CVE-2026-48901` with stream suffix `[rhtpa-2.1]`), create proactive preemptive remediation tasks:

#### Preemptive Upstream Backport Task (2.1.x)

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-48901: bump h2 to 0.4.8 (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-48901", "security-preemptive"]
)
```

**Task Description:**

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream rhtpa-2.2). No stream-specific CVE Jira
> exists yet for this stream. When PSIRT creates one, this task will be linked
> and the `security-preemptive` label removed.

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: 2.1.0 (v0.3.8), 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Target branch: release/0.3.z
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

#### Preemptive Downstream Propagation Subtask (2.1.x)

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-48901 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-48901", "security-preemptive"]
)
```

**Task Description:**

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream rhtpa-2.2). No stream-specific CVE Jira
> exists yet for this stream. When PSIRT creates one, this task will be linked
> and the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-48901 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that PR merges,
update the source pinning in this Konflux release repo so the next build ships the fix.

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

### Linkage for Preemptive Tasks

Preemptive tasks are linked to TC-8030 with **"Related"** link type (not "Depend"), because TC-8030 belongs to a different stream (rhtpa-2.2):

```
jira.create_link(
  inwardIssue: "TC-8030",
  outwardIssue: <preemptive-upstream-task-key>,
  type: "Related"
)
```

The downstream propagation subtask is blocked by the upstream backport task:

```
jira.create_link(
  inwardIssue: <preemptive-upstream-task-key>,
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Blocks"
)
```
