# Step 8 -- Remediation for CVE-2026-31812 (TC-8001)

## Triage Outcome: Case A + Case B

- **Case A (Affected)**: Stream 2.2.x has affected versions (2.2.0, 2.2.1, 2.2.2) -- create remediation tasks.
- **Case B (Cross-stream impact)**: Stream 2.1.x is also affected (2.1.0, 2.1.1) -- post cross-stream impact comment.

Since quinn-proto is a **Cargo** (source dependency) ecosystem, create **two tasks** for the 2.2.x stream:
1. Upstream backport task (fix in source repo)
2. Downstream propagation subtask (update reference in Konflux release repo)

Coordination guidance is **omitted** because the Source Repositories table does not have a Deployment Context column (backward compatibility).

---

## Task 1: Upstream Backport Task (2.2.x stream)

### Jira Issue Creation

```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)",
  description: <upstream-task-description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0 (ships 0.11.9), 2.2.1 (ships 0.11.12), 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z
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
```

### Description Digest Protocol (Upstream Task)

After creating the upstream task, perform the following description digest steps **before** creating any issue links or other comments:

**Step 1: Re-fetch description from Jira**

```
upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
```

This re-fetches the description as stored by Jira after `create_issue`. The re-fetched content is used for hashing -- NOT the input string passed to `create_issue` -- because Jira normalizes content during storage (whitespace, ADF conversion, etc.).

**Step 2: Write description to temp file and compute SHA-256 digest**

```bash
# Write the re-fetched description to a temp file
# (content written to /tmp/task-desc.md)

python3 scripts/sha256-digest.py /tmp/task-desc.md
```

The script auto-detects the input format:
- If the re-fetched description is ADF JSON (REST API path) -> outputs `sha256-adf:<64-char-hex>`
- If the re-fetched description is markdown text (MCP path) -> outputs `sha256-md:<64-char-hex>`

**Step 3: Post digest comment with marker**

```
jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
```

Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py` (e.g., `sha256-md:a1b2c3d4...64chars...`).

The comment is posted as ADF format:
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
          "text": "[sdlc-workflow] Description digest: <tagged-digest>"
        }
      ]
    }
  ]
}
```

**Critical ordering**: This digest comment is posted BEFORE creating issue links (Depend link to TC-8001, Blocks link to downstream task) or any other comments on the task.

---

## Task 2: Downstream Propagation Subtask (2.2.x stream)

### Jira Issue Creation

```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)",
  description: <downstream-task-description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Description Digest Protocol (Downstream Task)

After creating the downstream propagation task, perform the following description digest steps **before** creating any issue links or other comments:

**Step 1: Re-fetch description from Jira**

```
downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
```

This re-fetches the description as stored by Jira after `create_issue`. The re-fetched content is used for hashing -- NOT the input string passed to `create_issue` -- because Jira normalizes content during storage.

**Step 2: Write description to temp file and compute SHA-256 digest**

```bash
# Write the re-fetched description to a temp file
# (content written to /tmp/task-desc.md)

python3 scripts/sha256-digest.py /tmp/task-desc.md
```

The script auto-detects the input format:
- If the re-fetched description is ADF JSON (REST API path) -> outputs `sha256-adf:<64-char-hex>`
- If the re-fetched description is markdown text (MCP path) -> outputs `sha256-md:<64-char-hex>`

**Step 3: Post digest comment with marker**

```
jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
```

Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py` (e.g., `sha256-md:a1b2c3d4...64chars...`).

The comment is posted as ADF format:
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
          "text": "[sdlc-workflow] Description digest: <tagged-digest>"
        }
      ]
    }
  ]
}
```

**Critical ordering**: This digest comment is posted BEFORE creating issue links (Blocks link from upstream task, Depend link to TC-8001) or any other comments on the task.

---

## Jira Linkage (after both digest comments are posted)

After both tasks have their digest comments posted, create the issue links:

```
# 1. Link upstream task to Vulnerability issue
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)

# 2. Link downstream task as blocked by upstream task
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)

# 3. Link downstream task to Vulnerability issue
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)
```

---

## Complete Sequence of Operations (per task)

### Upstream task sequence:
1. `jira.create_issue(...)` -- create the upstream backport task
2. `jira.get_issue(<upstream-task-key>, fields=["description"])` -- re-fetch description from Jira
3. `python3 scripts/sha256-digest.py /tmp/task-desc.md` -- compute SHA-256 digest from re-fetched content
4. `jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")` -- post digest comment
5. _(links created after both tasks have digests -- see Jira Linkage above)_

### Downstream task sequence:
1. `jira.create_issue(...)` -- create the downstream propagation task
2. `jira.get_issue(<downstream-task-key>, fields=["description"])` -- re-fetch description from Jira
3. `python3 scripts/sha256-digest.py /tmp/task-desc.md` -- compute SHA-256 digest from re-fetched content
4. `jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")` -- post digest comment
5. _(links created after both tasks have digests -- see Jira Linkage above)_

---

## Key Digest Protocol Rules

1. **Re-fetch, do not reuse**: The digest is computed from the description as re-fetched from Jira after `create_issue`, NOT from the input string. Jira normalizes content during storage.
2. **Use the script**: Always use `python3 scripts/sha256-digest.py` to compute the digest. Never compute SHA-256 manually or use hardcoded/example hashes.
3. **Full 64-character hex**: The SHA-256 digest must be exactly 64 lowercase hexadecimal characters. No abbreviation.
4. **Preserve the format tag**: The output includes `sha256-md:` or `sha256-adf:` prefix. Post the full tagged value.
5. **Digest before links**: Post the digest comment BEFORE creating any issue links or other comments on the task.
6. **Single-line comment**: The comment body is exactly one line: `[sdlc-workflow] Description digest: <tagged-digest>`.
7. **Standalone comment**: The digest comment is independent -- not appended to any other comment.
