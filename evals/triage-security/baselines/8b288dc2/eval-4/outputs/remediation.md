# Remediation — TC-8004

## Triage Outcome

**Case A: Affected** — stream 2.1.x has affected versions. Stream 2.2.x is NOT affected (all versions ship h2 >= 0.4.8).

Remediation tasks are created for **stream 2.1.x only**. No remediation needed for stream 2.2.x.

No cross-stream impact notice is required because this issue is unscoped (covers all streams). There are no "other streams outside the issue's scope" since the issue has no scope restriction.

## Ecosystem

Cargo (source dependency) — requires **two tasks**: upstream backport + downstream propagation.

## Task 1: Upstream Backport (2.1.x)

### Jira Issue Creation

```
upstream_task = jira.create_issue(
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

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (h2 0.4.5), RHTPA 2.1.1 (h2 0.4.5)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

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

- Depends on: TC-8004 (parent tracking issue)
```

## Task 2: Downstream Propagation (2.1.x)

### Jira Issue Creation

```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)",
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

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that PR
merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

## Jira Linkage

After creating both tasks:

1. Link upstream task to TC-8004:
   ```
   jira.create_link(
     inwardIssue: "TC-8004",
     outwardIssue: <upstream-task-key>,
     type: "Depend"
   )
   ```

2. Link downstream task as blocked by upstream task:
   ```
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

3. Link downstream task to TC-8004:
   ```
   jira.create_link(
     inwardIssue: "TC-8004",
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )
   ```

4. Transition TC-8004 to In Progress.
5. Assign TC-8004 to current user.
6. Add `ai-cve-triaged` label to TC-8004.

## Post-Triage Summary Comment

```
Triage complete for CVE-2026-33501 (h2 < 0.4.8).

Version impact:

| Version | Stream | h2 version | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0   | 2.1.x  | 0.4.5      | YES       | |
| 2.1.1   | 2.1.x  | 0.4.5      | YES       | |
| 2.2.0   | 2.2.x  | 0.4.8      | NO        | ships fix version |
| 2.2.1   | 2.2.x  | 0.4.8      | NO        | |
| 2.2.2   | 2.2.x  | 0.4.8      | NO        | retag of 2.2.1 |
| 2.2.3   | 2.2.x  | 0.4.9      | NO        | |
| 2.2.4   | 2.2.x  | 0.4.9      | NO        | |

Affects Versions corrected: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].
RHTPA 2.2.0 removed (not affected). RHTPA 2.1.1 added (affected).

Remediation tasks created (stream 2.1.x only):
- <upstream-task-key> (upstream backport: bump h2 to 0.4.8 on release/0.3.z)
- <downstream-task-key> (downstream propagation: update rhtpa-backend ref in rhtpa-release.0.3.z, blocked by <upstream-task-key>)

Stream 2.2.x: no remediation needed — all versions ship h2 >= 0.4.8.
```

## Notes

- No sibling issues found (JQL returned empty) — no duplicate/cross-stream coordination needed.
- No cross-stream impact notice posted because the issue is unscoped (covers all streams). Case B does not apply to unscoped issues since there are no "other streams outside the issue's scope."
- Coordination guidance omitted from task descriptions because the Source Repositories table has no Deployment Context column (backward compatibility).
