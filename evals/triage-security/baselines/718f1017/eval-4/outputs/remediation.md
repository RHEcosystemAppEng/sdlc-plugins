# Step 7 -- Remediation: TC-8004

## Triage Outcome

**Case A: Affected -- create remediation tasks** for the 2.1.x stream only.

The version impact table shows:
- **2.1.x stream**: AFFECTED (all versions ship h2 0.4.5, below fix threshold 0.4.8)
- **2.2.x stream**: NOT affected (all versions ship h2 >= 0.4.8)

Since the issue is unscoped (covers all streams), remediation is created only for the actually affected stream (2.1.x). The 2.2.x stream requires no remediation -- it already ships the patched version.

This is NOT Case B (cross-stream impact / proactive remediation) because the other stream (2.2.x) is not affected. Case B applies when other streams outside the issue's scope ARE affected and need proactive remediation. Here, 2.2.x ships h2 >= 0.4.8 so no remediation is needed for it.

## Ecosystem

**Cargo** (source dependency ecosystem) -- requires **two** tasks per affected stream:
1. Upstream backport task (fix in the source repo)
2. Downstream propagation subtask (update reference in the Konflux release repo)

## Remediation Tasks for 2.1.x Stream

### Task 1: Upstream Backport Task

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

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Target branch: release/0.3.z
- h2 is a transitive dependency via hyper -- the bump may require
  updating hyper or adjusting version constraints in Cargo.toml
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

**Jira creation**:
```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (rhtpa-2.1)",
  description: <upstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

**Description digest comment** (posted before links or other comments):
```
[sdlc-workflow] Description digest: sha256-md:<computed-64-char-hex-digest>
```
(Digest computed via `python3 scripts/sha256-digest.py` on the re-fetched description)

### Task 2: Downstream Propagation Subtask

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

The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that
PR merges, update the source pinning in this Konflux release repo so
the next build ships the fix.

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

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

**Jira creation**:
```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <downstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

**Description digest comment** (posted before links or other comments):
```
[sdlc-workflow] Description digest: sha256-md:<computed-64-char-hex-digest>
```

## Jira Linkage

After creating both tasks:

```
# Link upstream task to Vulnerability issue
jira.create_link(
  inwardIssue: "TC-8004",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)

# Link downstream subtask as blocked by upstream task
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)

# Link downstream task to Vulnerability issue
jira.create_link(
  inwardIssue: "TC-8004",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)

# Transition Vulnerability to In Progress
jira.transition_issue("TC-8004", status: "In Progress")

# Assign Vulnerability to current user
jira.edit_issue("TC-8004", fields={"assignee": {"accountId": "<current-user-id>"}})
```

## No Remediation Needed for 2.2.x Stream

The 2.2.x stream is NOT affected -- all versions ship h2 >= 0.4.8 (the fix threshold). No remediation tasks are created for this stream.

- 2.2.0 ships h2 0.4.8 (exactly at fix threshold -- not vulnerable)
- 2.2.1 ships h2 0.4.8
- 2.2.2 is a retag of 2.2.1 (same as 2.2.1)
- 2.2.3 ships h2 0.4.9
- 2.2.4 ships h2 0.4.9

## Post-Triage Summary

### 1. Add `ai-cve-triaged` label

```
jira.edit_issue("TC-8004", fields={
  "labels": ["CVE-2026-33501", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### 2. Post summary comment to TC-8004

```
CVE-2026-33501 triage complete for h2 (memory exhaustion via CONTINUATION frames).

Version Impact:

| Stream | Version | h2 version | Affected? | Notes |
|--------|---------|------------|-----------|-------|
| 2.1.x | 2.1.0 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.1.x | 2.1.1 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.2.x | 2.2.0 | 0.4.8 | NO | 0.4.8 >= 0.4.8 |
| 2.2.x | 2.2.1 | 0.4.8 | NO | 0.4.8 >= 0.4.8 |
| 2.2.x | 2.2.2 | -- | NO | retag of 2.2.1 |
| 2.2.x | 2.2.3 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.x | 2.2.4 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

Affects Versions corrected: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]
RHTPA 2.2.0 removed (ships h2 0.4.8, not vulnerable). RHTPA 2.1.1 added (ships h2 0.4.5, vulnerable).

Remediation tasks created for 2.1.x stream only:
- <upstream-task-key> (upstream backport: bump h2 to 0.4.8 on release/0.3.z)
- <downstream-task-key> (downstream propagation: update rhtpa-backend ref in rhtpa-release.0.3.z, blocked by <upstream-task-key>)

No remediation needed for 2.2.x stream -- all versions ship h2 >= 0.4.8.

@<reporter-name> (reporter mention via ADF mention node with reporter account ID from issue data)

---
This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/mrizzi/sdlc-plugins) v0.11.0.
```

The summary comment includes:
1. Version impact table showing mixed impact across streams
2. Affects Versions correction with evidence
3. Triage outcome (remediation for 2.1.x only, 2.2.x not affected)
4. Links to remediation tasks (upstream + downstream for Cargo ecosystem)
5. @mention of the issue reporter (mandatory per methodology)
6. Comment footnote with skill name and plugin version (mandatory per shared/comment-footnote.md)
