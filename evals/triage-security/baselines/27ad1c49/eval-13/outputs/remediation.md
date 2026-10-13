# Step 8 -- Remediation for TC-8001 (CVE-2026-31812)

## Triage Decision Tree

### Scoped Stream: 2.2.x

- Versions 2.2.0, 2.2.1, 2.2.2 are affected (quinn-proto < 0.11.14)
- Versions 2.2.3, 2.2.4 are NOT affected (quinn-proto = 0.11.14)
- Upstream branch `release/0.4.z` already ships the fix
- Latest Konflux releases (2.2.3, 2.2.4) already include the fix
- **Result**: Fix already present in this stream. No remediation tasks needed for 2.2.x.
- Affects Versions correction: `RHTPA 2.0.0` -> `[RHTPA 2.2.0, RHTPA 2.2.1]` (scoped to 2.2.x; 2.2.2 is a retag of 2.2.1; 2.2.3+ are not affected)

### Cross-Stream Impact: 2.1.x (Case A)

- Both 2.1.0 and 2.1.1 are affected (quinn-proto 0.11.9 < 0.11.14)
- Upstream branch `release/0.3.z` does NOT have the fix
- No sibling CVE Jira exists for the 2.1.x stream (no issue with suffix `[rhtpa-2.1]` found)
- **Result**: Case A applies. Create **preemptive** remediation tasks for the 2.1.x stream.
- Ecosystem: Cargo (source dependency, fix NOT available upstream) -> 2 tasks: upstream backport + downstream propagation
- Labels include `security-preemptive` since no stream-specific CVE Jira exists for 2.1.x
- Link type: "Related" to originating CVE TC-8001 (not "Depend", since TC-8001 is scoped to a different stream)

---

## Preemptive Remediation Task 1: Upstream Backport (2.1.x stream)

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)",
  description: <see task description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

### Task Description

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (v0.3.8), RHTPA 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

### Description Digest Comment (posted after task creation)

After creating the upstream backport task, the following steps are performed to post the description digest:

1. **Re-fetch the description** from Jira after creation (Jira normalizes content during storage):
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```

2. **Write the description to a temp file** and compute the digest using the script:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The script auto-detects the input format (ADF JSON or markdown) and outputs a format-tagged digest, e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`.

3. **Post the digest comment** on the newly created task (before creating any links or other comments):
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from `sha256-digest.py` (e.g., `sha256-md:a1b2c3...64 hex chars`).

   The comment body in ADF format:
   ```json
   {
     "type": "doc",
     "version": 1,
     "content": [
       {
         "type": "paragraph",
         "content": [
           {
             "type": "text",
             "text": "[sdlc-workflow] Description digest: sha256-md:<64-char-hex-digest>"
           }
         ]
       }
     ]
   }
   ```

4. **After the digest comment is posted**, proceed to create issue links.

### Jira Linkage (after digest comment)

Link the preemptive task to the originating CVE with "Related" (not "Depend"):

```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <upstream-task-key>,
  type: "Related"
)
```

---

## Preemptive Remediation Task 2: Downstream Propagation (2.1.x stream)

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see task description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

### Task Description

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Description Digest Comment (posted after task creation)

1. **Re-fetch the description** from Jira after creation:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```

2. **Compute the digest**:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```

3. **Post the digest comment** on the newly created task (before creating any links or other comments):
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

   The comment body in ADF format:
   ```json
   {
     "type": "doc",
     "version": 1,
     "content": [
       {
         "type": "paragraph",
         "content": [
           {
             "type": "text",
             "text": "[sdlc-workflow] Description digest: sha256-md:<64-char-hex-digest>"
           }
         ]
       }
     ]
   }
   ```

4. **After the digest comment is posted**, proceed to create issue links.

### Jira Linkage (after digest comment)

1. Link the downstream task to the originating CVE with "Related" (preemptive):
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <downstream-task-key>,
     type: "Related"
   )
   ```

2. Link the downstream task as blocked by the upstream task:
   ```
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

---

## Cross-Stream Impact Comment

After creating the preemptive tasks, post a comment on TC-8001 documenting the cross-stream impact:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis at pinned commits v0.3.8 and v0.3.12.

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <upstream-task-key> (upstream backport, security-preemptive)
- 2.1.x: <downstream-task-key> (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

---

## Post-Triage Summary

After all triage actions are complete, the following actions would be performed on TC-8001:

### 1. Add the `ai-cve-triaged` label

```
jira.edit_issue("TC-8001", fields={
  "labels": ["CVE-2026-31812", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### 2. Post a summary comment

```
Post-triage summary for TC-8001 (CVE-2026-31812):

Version Impact Table:

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0   | 2.1.x  | 0.11.9     | YES       |       |
| 2.1.1   | 2.1.x  | 0.11.9     | YES       |       |
| 2.2.0   | 2.2.x  | 0.11.9     | YES       |       |
| 2.2.1   | 2.2.x  | 0.11.12    | YES       |       |
| 2.2.2   | 2.2.x  | --         | YES       | retag of 2.2.1 |
| 2.2.3   | 2.2.x  | 0.11.14    | NO        |       |
| 2.2.4   | 2.2.x  | 0.11.14    | NO        |       |

Affects Versions correction: RHTPA 2.0.0 -> [RHTPA 2.2.0, RHTPA 2.2.1]
(scoped to 2.2.x stream per issue suffix; 2.2.3+ already ship the fix)

Triage outcome:
- 2.2.x stream: Fix already present in versions 2.2.3+ (quinn-proto 0.11.14).
  No new remediation tasks needed for this stream.
- 2.1.x stream: Preemptive remediation tasks created:
  - <upstream-task-key>: upstream backport (bump quinn-proto to 0.11.14 on release/0.3.z)
  - <downstream-task-key>: downstream propagation (update backend ref in rhtpa-release.0.3.z)
  Both tasks carry the security-preemptive label and are linked via "Related".

@<reporter-name> (reporter mention via ADF mention node with reporter account ID)
```

The summary comment MUST include the Comment Footnote per `shared/comment-footnote.md` using skill name `triage-security`.

---

## Pre-Creation Checklist

- [x] **Task count per stream**: 2.1.x stream gets 2 tasks (upstream backport + downstream propagation) -- matches Cargo source dependency classification. 2.2.x stream gets 0 tasks (fix already present).
- [x] **Cross-stream coverage**: 2.1.x (outside issue scope) has preemptive tasks created. No sibling CVE Jira exists for 2.1.x.
- [x] **Link types**: "Related" for preemptive tasks linked to TC-8001 (originating CVE from a different stream). "Blocks" for upstream -> downstream within the 2.1.x stream.
- [x] **Preemptive labels**: Both 2.1.x tasks carry the `security-preemptive` label.
- [x] **Coordination guidance**: Each task includes upstream coordination guidance (deployment context = `upstream`, the default since no Deployment Context column is present in Source Repositories).
- [x] **Dedup consistency**: No dedup scenarios apply (no release Jira or existing remediation tasks found).

## Description Digest Protocol Summary

For each remediation task created, the description digest protocol requires:

1. **Timing**: The digest comment MUST be posted immediately after task creation, BEFORE creating any issue links or other comments on the task.
2. **Computation**: Always re-fetch the description from Jira after creation (Jira normalizes content during storage). Write to a temp file and compute via `python3 scripts/sha256-digest.py /tmp/task-desc.md`.
3. **Format**: The digest comment is a single line: `[sdlc-workflow] Description digest: sha256-md:<64-char-hex>` (or `sha256-adf:<64-char-hex>` if using REST API path). The format tag is part of the digest value.
4. **Standalone**: The digest comment must be an independent comment, not appended to any other comment.
5. **Purpose**: Enables `/implement-task` to verify description integrity in its Step 1.5, detecting any modification between planning and implementation.
