# Step 7 -- Remediation Recommendations for TC-8030

## Triage Outcome: Case C (No Supported Versions Affected in Scoped Stream)

The version impact analysis shows that **no versions in the 2.2.x stream** (the issue's scoped stream) ship a vulnerable version of h2:

| Version | h2 version | Affected? |
|---------|------------|-----------|
| 2.2.0 | 0.4.8 | NO (at fix threshold) |
| 2.2.1 | 0.4.8 | NO (at fix threshold) |
| 2.2.2 | -- | NO (retag of 2.2.1) |
| 2.2.3 | 0.4.9 | NO (above fix threshold) |
| 2.2.4 | 0.4.9 | NO (above fix threshold) |

Fix threshold (from Step 1.5 enrichment): h2 >= 0.4.8

## Proposed Actions (Requiring Engineer Confirmation)

### Action 1: Close TC-8030 as Not a Bug

**Rationale**: No supported versions within the 2.2.x stream ship a vulnerable version of h2. All 2.2.x versions ship h2 >= 0.4.8, which is at or above the enriched fix threshold established by cross-validated MITRE CVE API and OSV.dev data.

**Proposed Jira mutations** (pending engineer approval):

1. **Add comment** to TC-8030:
   > No supported versions in the 2.2.x stream ship a vulnerable version of h2.
   > Version impact analysis (fix threshold h2 < 0.4.8, source: MITRE CVE API + OSV.dev):
   >
   > | Version | h2 version | Affected? |
   > |---------|------------|-----------|
   > | 2.2.0 | 0.4.8 | NO |
   > | 2.2.1 | 0.4.8 | NO |
   > | 2.2.2 | -- | NO (retag of 2.2.1) |
   > | 2.2.3 | 0.4.9 | NO |
   > | 2.2.4 | 0.4.9 | NO |
   >
   > All 2.2.x versions ship h2 0.4.8+, which is outside the affected range (< 0.4.8).
   >
   > Note: The Jira description did not provide a precise fix threshold ("versions prior to the fix" / "see advisory"). The threshold h2 < 0.4.8 was established via external CVE data enrichment -- both MITRE CVE API (lessThan: 0.4.8) and OSV.dev (fixed: 0.4.8) agree.

2. **Transition** TC-8030 to Closed with resolution **Not a Bug**.

3. **Set VEX Justification** (customfield_12345) to **Component not Present** -- the vulnerable version of h2 (< 0.4.8) is not shipped in any 2.2.x release.

4. **Assign** TC-8030 to current user.

5. **Add label** `ai-cve-triaged` to TC-8030.

### Action 2: Cross-Stream Impact Notice

**Rationale**: The version impact analysis reveals that the **2.1.x stream IS affected** (both 2.1.0 and 2.1.1 ship h2 0.4.5, which is below the 0.4.8 fix threshold). This is outside TC-8030's scope (which is 2.2.x only), but should be reported for PSIRT awareness.

**Proposed comment** on TC-8030:
> Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file analysis.
> - 2.1.0 (tag v0.3.8): h2 0.4.5 -- AFFECTED
> - 2.1.1 (tag v0.3.12): h2 0.4.5 -- AFFECTED
>
> The 2.1.x stream is tracked by a separate Konflux release repo (rhtpa-release.0.3.z).
> If no companion CVE Jira exists for stream 2.1.x, consider creating preemptive remediation tasks per Step 7 Case B.

### Action 3: Preemptive Remediation for 2.1.x (Case B -- if no companion CVE Jira exists)

If JQL search confirms no sibling CVE Jira exists for CVE-2026-48901 with stream suffix `[rhtpa-2.1]`, create preemptive remediation tasks for the 2.1.x stream:

#### Preemptive Upstream Backport Task (2.1.x)

**Proposed Jira issue creation**:

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-48901: bump h2 to 0.4.8 (rhtpa-2.1)",
  labels: ["ai-generated-jira", "Security", "CVE-2026-48901", "security-preemptive"]
)
```

**Task description**:

## Repository

backend (rhtpa-backend)

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: 2.1.0 (h2 0.4.5), 2.1.1 (h2 0.4.5)
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

**Link type**: Related (not Depend) -- preemptive task linked to originating CVE from a different stream.

#### Preemptive Downstream Propagation Task (2.1.x)

**Proposed Jira issue creation**:

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-48901 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  labels: ["ai-generated-jira", "Security", "CVE-2026-48901", "security-preemptive"]
)
```

**Task description**:

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-48901 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8+ on release/0.3.z. Once that PR merges,
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

**Link type**: Related (not Depend) -- preemptive task linked to originating CVE from a different stream.
**Blocked by**: upstream backport task (Blocks link type).

## No Remediation Tasks for 2.2.x Stream

No remediation tasks are created for the 2.2.x stream because all versions already ship h2 >= 0.4.8. The issue is recommended for closure as Not a Bug.
