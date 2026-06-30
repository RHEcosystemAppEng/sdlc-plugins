# Remediation -- TC-8004

## Step 7 -- Triage Outcome

**Case A: Affected -- create remediation tasks** for the 2.1.x stream only.

The 2.2.x stream is NOT affected (all versions ship h2 >= 0.4.8) and requires no remediation.

Since the ecosystem is **Cargo** (source dependency), two tasks are needed for the affected 2.1.x stream:
1. Upstream backport task (fix in the source repo)
2. Downstream propagation subtask (update reference in Konflux release repo)

---

## Proposed Remediation Task 1: Upstream Backport (2.1.x)

### Jira Issue Creation

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

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: Memory exhaustion via CONTINUATION frames in h2 crate.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (v0.3.8, h2 0.4.5), RHTPA 2.1.1 (v0.3.12, h2 0.4.5)
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
- h2 is likely a transitive dependency (via hyper/reqwest); may need
  to bump intermediate crates or use a [patch] override

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)
```

### Post-Creation Actions

1. Post description digest comment on the upstream task
2. Link to TC-8004 with type "Depend"

---

## Proposed Remediation Task 2: Downstream Propagation (2.1.x)

### Jira Issue Creation

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

```
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

- Depends on: <upstream-backport-task-key> (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

### Post-Creation Actions

1. Post description digest comment on the downstream task
2. Link to TC-8004 with type "Depend"
3. Link downstream task as blocked by upstream task with type "Blocks"

---

## No Remediation Needed for 2.2.x

The 2.2.x stream does NOT require remediation. All versions in this stream ship h2 >= 0.4.8:

| Version | h2 version | Status |
|---------|------------|--------|
| 2.2.0 | 0.4.8 | At fix threshold -- not affected |
| 2.2.1 | 0.4.8 | At fix threshold -- not affected |
| 2.2.2 | (retag) | Same as 2.2.1 -- not affected |
| 2.2.3 | 0.4.9 | Above fix threshold -- not affected |
| 2.2.4 | 0.4.9 | Above fix threshold -- not affected |

No tasks are created for the 2.2.x stream.

---

## Proposed Jira Linkage

After creating the remediation tasks:

```
# Link upstream task to CVE
jira.create_link(
  inwardIssue: "TC-8004",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)

# Link downstream task to CVE
jira.create_link(
  inwardIssue: "TC-8004",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)

# Link downstream as blocked by upstream
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)

# Transition CVE to In Progress
jira.transition_issue("TC-8004", status="In Progress")

# Assign CVE to current user
jira.edit_issue("TC-8004", fields={"assignee": {"accountId": "<current-user-id>"}})
```

## Post-Triage Summary

### Proposed Label Addition

Add `ai-cve-triaged` label to TC-8004.

### Proposed Summary Comment on TC-8004

```
## Triage Summary -- CVE-2026-33501 (h2 < 0.4.8)

### Version Impact

| Stream | Version | h2 version | Affected? | Notes |
|--------|---------|------------|-----------|-------|
| 2.1.x | 2.1.0 | 0.4.5 | YES | |
| 2.1.x | 2.1.1 | 0.4.5 | YES | |
| 2.2.x | 2.2.0 | 0.4.8 | NO | at fix threshold |
| 2.2.x | 2.2.1 | 0.4.8 | NO | |
| 2.2.x | 2.2.2 | -- | NO | retag of 2.2.1 |
| 2.2.x | 2.2.3 | 0.4.9 | NO | |
| 2.2.x | 2.2.4 | 0.4.9 | NO | |

### Affects Versions Correction

[RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]
- Removed RHTPA 2.2.0 (not affected, ships h2 0.4.8)
- Added RHTPA 2.1.1 (affected, ships h2 0.4.5)

### Triage Outcome

Remediation tasks created for the 2.1.x stream (Cargo ecosystem, 2 tasks):
- <upstream-task-key>: Upstream backport -- bump h2 to >= 0.4.8 on release/0.3.z
- <downstream-task-key>: Downstream propagation -- update backend ref in rhtpa-release.0.3.z (blocked by upstream task)

No remediation needed for the 2.2.x stream (all versions ship h2 >= 0.4.8).

@<reporter-name> (reporter)

---
_This comment was generated by the triage-security skill of the sdlc-workflow plugin._
```
