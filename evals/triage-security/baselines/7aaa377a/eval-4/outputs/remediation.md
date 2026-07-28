# Step 8 -- Remediation

## Triage Decision

This is an **unscoped** issue (no stream suffix in summary). The version impact
table shows mixed results:

- **2.1.x stream**: AFFECTED (all versions ship h2 0.4.5, below fix threshold 0.4.8)
- **2.2.x stream**: NOT AFFECTED (all versions ship h2 >= 0.4.8, the fixed version)

**Case B applies for the 2.1.x stream** -- affected versions exist, create
remediation tasks.

**No remediation for 2.2.x** -- all 2.2.x versions already ship the patched h2
version (0.4.8 or later). No tasks are created for this stream.

**Cross-stream impact notice (Case A) is NOT applicable** -- this issue is unscoped,
meaning it covers all streams by definition. There are no "other streams outside
this issue's scope," so the cross-stream impact check does not apply. The issue
is handled entirely through Case B, creating remediation tasks only for actually
affected streams.

## Pre-Creation Checklist

- [x] **Task count per stream**: Cargo is a source dependency ecosystem -> 2 tasks
  for the 2.1.x stream (upstream backport + downstream propagation)
- [x] **Cross-stream coverage**: N/A -- issue is unscoped, all streams are in scope
- [x] **Link types**: "Depend" for tasks linked to TC-8004, "Blocks" for upstream
  -> downstream within the 2.1.x stream
- [x] **Preemptive labels**: N/A -- no preemptive tasks needed (issue is unscoped)
- [x] **Coordination guidance**: omitted -- no Deployment Context column in Source
  Repositories table

---

## Remediation Tasks for 2.1.x Stream

### Task 1: Upstream Backport Task

**Proposed Jira create_issue:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

**Task Description:**

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 - Memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version
(0.4.8+).

Affected versions: RHTPA 2.1.0 (v0.3.8), RHTPA 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

- Update h2 dependency to >= 0.4.8 in Cargo.toml / Cargo.lock
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

**Post-creation steps:**

1. Re-fetch the task description from Jira after create_issue:
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```
2. Write the re-fetched description to a temp file and compute digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
3. Post digest comment (BEFORE creating issue links or other comments):
   ```
   jira.add_comment(<upstream-task-key>,
     "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
4. Create Depend link to the Vulnerability issue:
   ```
   jira.create_link(
     inwardIssue: "TC-8004",
     outwardIssue: <upstream-task-key>,
     type: "Depend"
   )
   ```

---

### Task 2: Downstream Propagation Subtask

**Proposed Jira create_issue:**

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

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-33501
fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps h2 to 0.4.8 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
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

**Post-creation steps:**

1. Re-fetch the task description from Jira after create_issue:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```
2. Write the re-fetched description to a temp file and compute digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
3. Post digest comment (BEFORE creating issue links or other comments):
   ```
   jira.add_comment(<downstream-task-key>,
     "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
4. Create Depend link to the Vulnerability issue:
   ```
   jira.create_link(
     inwardIssue: "TC-8004",
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )
   ```
5. Create Blocks link from upstream to downstream:
   ```
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

---

## No Tasks for 2.2.x Stream

The 2.2.x stream does not require remediation. All versions in this stream ship
h2 >= 0.4.8, which is at or above the fix threshold:

| Version | h2 Version | Affected? |
|---------|------------|-----------|
| 2.2.0 | 0.4.8 | NO |
| 2.2.1 | 0.4.8 | NO |
| 2.2.2 | (retag of 2.2.1) | NO |
| 2.2.3 | 0.4.9 | NO |
| 2.2.4 | 0.4.9 | NO |

No remediation tasks are created for this stream.

---

## Post-Triage Actions

### 1. Add ai-cve-triaged label

Proposed action: add the `ai-cve-triaged` label to TC-8004.

### 2. Transition to In Progress

Proposed action: transition TC-8004 to In Progress status.

### 3. Post summary comment

Proposed post-triage summary comment on TC-8004:

```
Triage complete for CVE-2026-33501 (h2 < 0.4.8).

Version impact:
| Version | h2 | Affected? | Notes |
|---------|-----|-----------|-------|
| 2.1.0 | 0.4.5 | YES | |
| 2.1.1 | 0.4.5 | YES | |
| 2.2.0 | 0.4.8 | NO | ships fixed version |
| 2.2.1 | 0.4.8 | NO | ships fixed version |
| 2.2.2 | -- | NO | retag of 2.2.1 |
| 2.2.3 | 0.4.9 | NO | |
| 2.2.4 | 0.4.9 | NO | |

Affects Versions corrected: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]

Remediation tasks created (2.1.x stream only):
- <upstream-task-key> (upstream backport: bump h2 to 0.4.8 on release/0.3.z)
- <downstream-task-key> (downstream propagation, blocked by <upstream-task-key>)

2.2.x stream: no remediation needed -- all versions ship h2 >= 0.4.8.

@<reporter-name> (ADF mention node: {"type": "mention", "attrs": {"id": "<reporter-account-id>", "text": "@<reporter-name>"}})

---
This comment was AI-generated by sdlc-workflow/triage-security v0.13.7.
```

All proposed actions require engineer confirmation before execution.
