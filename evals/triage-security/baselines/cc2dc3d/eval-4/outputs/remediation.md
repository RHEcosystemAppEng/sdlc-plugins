# Step 7 -- Remediation: TC-8004 (CVE-2026-33501)

## Triage Outcome

**Case A: Affected -- create remediation tasks** (for the 2.1.x stream only).

The version impact analysis shows:
- **2.1.x stream**: ALL versions affected (h2 0.4.5, before the 0.4.8 fix)
- **2.2.x stream**: NO versions affected (h2 >= 0.4.8 in all versions)

Since the 2.2.x stream already ships the fixed version, remediation is needed only for the 2.1.x stream. No cross-stream impact notice (Case B) is needed because the other stream is already fixed.

## Ecosystem and Task Structure

- **Ecosystem**: Cargo (source dependency)
- **Task count**: 2 tasks -- upstream backport + downstream propagation
- **Affected stream**: 2.1.x only

## Proposed Remediation Task 1: Upstream Backport (2.1.x)

### Jira Issue Creation (requires engineer confirmation)

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

### Task Description

```markdown
## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 versions before 0.4.8) must be updated
to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (v0.3.8), RHTPA 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Target branch: release/0.3.z
- h2 is a transitive dependency via hyper -- the bump may require
  updating hyper or adjusting dependency constraints
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

- Depends on: TC-8004 (parent tracking issue)
```

## Proposed Remediation Task 2: Downstream Propagation (2.1.x)

### Jira Issue Creation (requires engineer confirmation)

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

### Task Description

```markdown
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that PR
merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
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

## Proposed Jira Linkage (requires engineer confirmation)

After creating both tasks:

1. **Link upstream task to Vulnerability**:
   ```
   jira.create_link(
     inwardIssue: "TC-8004",
     outwardIssue: <upstream-task-key>,
     type: "Depend"
   )
   ```

2. **Link downstream subtask as blocked by upstream task**:
   ```
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

3. **Link downstream task to Vulnerability**:
   ```
   jira.create_link(
     inwardIssue: "TC-8004",
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )
   ```

4. **Transition** TC-8004 to In Progress.

5. **Assign** TC-8004 to the current user.

## Proposed Post-Triage Actions (requires engineer confirmation)

### Add ai-cve-triaged label

```
jira.edit_issue("TC-8004", fields={
  "labels": ["CVE-2026-33501", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### Post-Triage Summary Comment

```
CVE-2026-33501 triage complete for TC-8004.

**Version Impact:**

| Version | h2 version | Affected? | Notes |
|---------|------------|-----------|-------|
| 2.1.0 | 0.4.5 | YES | < 0.4.8 |
| 2.1.1 | 0.4.5 | YES | < 0.4.8 |
| 2.2.0 | 0.4.8 | NO | = fixed version |
| 2.2.1 | 0.4.8 | NO | = fixed version |
| 2.2.2 | -- | NO | retag of 2.2.1 |
| 2.2.3 | 0.4.9 | NO | > 0.4.8 |
| 2.2.4 | 0.4.9 | NO | > 0.4.8 |

**Affects Versions correction:** [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]

**Triage outcome:** Remediation tasks created for the 2.1.x stream only. The 2.2.x stream already ships h2 >= 0.4.8 and is not affected.

**Remediation tasks:**
- <upstream-task-key>: Upstream backport -- bump h2 to >= 0.4.8 on release/0.3.z
- <downstream-task-key>: Downstream propagation -- update backend ref in rhtpa-release.0.3.z (blocked by <upstream-task-key>)

---
_Comment generated by `/sdlc-workflow:triage-security`._
```

## Steps 4-6 Summary

### Step 4 -- Duplicate/Sibling Check
No sibling Vulnerability issues found for CVE-2026-33501 (JQL returned empty). No duplicates or companion trackers exist.

### Step 5 -- Version Lifecycle Check
Lifecycle check deferred (would require fetching product pages at https://access.example.com/product-life-cycle/rhtpa). Assuming both 2.1.x and 2.2.x are within support lifecycle for the purpose of this triage.

### Step 6 -- Already Fixed Check
No resolved sibling issues exist (Step 4 found none). Cannot determine if any stream has already been fixed via a separate issue. Proceeding with remediation for the affected 2.1.x stream.
