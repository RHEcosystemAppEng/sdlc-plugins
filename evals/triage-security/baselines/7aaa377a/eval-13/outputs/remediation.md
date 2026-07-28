# Step 8 -- Remediation

## Triage Decision

The version impact table shows that versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream
(the scoped stream) are affected. This is **Case B: Affected -- create remediation tasks**.

Additionally, the 2.1.x stream is also affected (versions 2.1.0, 2.1.1), triggering
**Case A: Cross-stream impact** (a cross-stream impact comment would be posted).

Since quinn-proto is a **Cargo** ecosystem (source dependency), **two tasks** are created
per affected stream: an upstream backport task and a downstream propagation subtask.

---

## Remediation Tasks for Stream 2.2.x (In Scope)

### Task 1: Upstream Backport Task

**Jira creation call:**

```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <upstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task description:**

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is retag of v0.4.8)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
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

#### Description Digest Protocol for Upstream Backport Task

After creating the upstream backport task, the following description digest steps
are performed **before** creating any issue links (Depend, Blocks) or posting any
other comments on the task:

1. **Re-fetch the task description from Jira API** (do NOT use the description
   string that was passed to `create_issue` -- Jira normalizes content during
   storage, so the stored version may differ from the input):

   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```

2. **Write the re-fetched description to a temporary file**:

   ```
   Write the description content from the Jira API response to /tmp/task-desc.md
   ```

3. **Compute the SHA-256 digest using scripts/sha256-digest.py**:

   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```

   The script auto-detects the input format (ADF JSON vs markdown) and outputs
   a format-tagged digest: either `sha256-adf:<64-char-hex>` or
   `sha256-md:<64-char-hex>`.

4. **Post the digest comment on the task** using the exact marker prefix
   `[sdlc-workflow] Description digest:`:

   ```
   jira.add_comment(<upstream-task-key>,
     "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py`
   (e.g., `sha256-md:a1b2c3d4...` -- the full 64-character hex digest with
   format tag). The comment body is exactly one line containing the marker
   and digest.

5. **Only after the digest comment is posted**, proceed to create issue links
   and other comments:

   ```
   # Link upstream task to CVE Vulnerability issue
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <upstream-task-key>,
     type: "Depend"
   )
   ```

---

### Task 2: Downstream Propagation Subtask

**Jira creation call:**

```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <downstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task description:**

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
- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Protocol for Downstream Propagation Subtask

After creating the downstream propagation subtask, the following description digest
steps are performed **before** creating any issue links (Depend, Blocks) or posting
any other comments on the task:

1. **Re-fetch the task description from Jira API** (do NOT use the description
   string that was passed to `create_issue` -- Jira normalizes content during
   storage, so the stored version may differ from the input):

   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```

2. **Write the re-fetched description to a temporary file**:

   ```
   Write the description content from the Jira API response to /tmp/task-desc.md
   ```

3. **Compute the SHA-256 digest using scripts/sha256-digest.py**:

   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```

   The script auto-detects the input format (ADF JSON vs markdown) and outputs
   a format-tagged digest: either `sha256-adf:<64-char-hex>` or
   `sha256-md:<64-char-hex>`.

4. **Post the digest comment on the task** using the exact marker prefix
   `[sdlc-workflow] Description digest:`:

   ```
   jira.add_comment(<downstream-task-key>,
     "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py`
   (e.g., `sha256-md:a1b2c3d4...` -- the full 64-character hex digest with
   format tag). The comment body is exactly one line containing the marker
   and digest.

5. **Only after the digest comment is posted**, proceed to create issue links
   and other comments:

   ```
   # Link downstream subtask as blocked by upstream task
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )

   # Link downstream subtask to CVE Vulnerability issue
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )
   ```

---

## Complete Remediation Procedure (Ordered)

The full sequence of operations for creating remediation tasks, with the description
digest protocol integrated, is as follows. The digest comment is always posted
**before** issue links or other comments on each task.

### 1. Create Upstream Backport Task

```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <upstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### 1a. Post Description Digest for Upstream Task (BEFORE links/comments)

```
# Re-fetch description from Jira (not the string we passed to create_issue)
upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])

# Write re-fetched description to temp file and compute digest
python3 scripts/sha256-digest.py /tmp/task-desc.md
# Output: sha256-md:<64-char-hex> or sha256-adf:<64-char-hex>

# Post digest comment with exact marker prefix
jira.add_comment(<upstream-task-key>,
  "[sdlc-workflow] Description digest: <tagged-digest>")
```

### 1b. Create Issue Links for Upstream Task (AFTER digest comment)

```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)
```

### 2. Create Downstream Propagation Subtask

```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <downstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### 2a. Post Description Digest for Downstream Subtask (BEFORE links/comments)

```
# Re-fetch description from Jira (not the string we passed to create_issue)
downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])

# Write re-fetched description to temp file and compute digest
python3 scripts/sha256-digest.py /tmp/task-desc.md
# Output: sha256-md:<64-char-hex> or sha256-adf:<64-char-hex>

# Post digest comment with exact marker prefix
jira.add_comment(<downstream-task-key>,
  "[sdlc-workflow] Description digest: <tagged-digest>")
```

### 2b. Create Issue Links for Downstream Subtask (AFTER digest comment)

```
# Blocks link: upstream blocks downstream
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)

# Depend link: downstream depends on CVE issue
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)
```

### 3. Transition CVE Issue and Post Summary

```
# Transition TC-8001 to In Progress
jira.transition_issue("TC-8001", <in-progress-transition-id>)

# Add ai-cve-triaged label
jira.edit_issue("TC-8001", fields={
  "labels": ["CVE-2026-31812", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})

# Post summary comment (with Comment Footnote)
jira.add_comment("TC-8001", "Triage complete for CVE-2026-31812 (quinn-proto).
Version impact: 2.2.0, 2.2.1, 2.2.2 affected; 2.2.3, 2.2.4 not affected.
Remediation tasks created:
- <upstream-task-key> (upstream backport: bump quinn-proto to 0.11.14)
- <downstream-task-key> (downstream propagation, blocked by <upstream-task-key>)

Cross-stream impact: 2.1.x stream also affected (2.1.0, 2.1.1).

---
This comment was AI-generated by sdlc-workflow/triage-security v0.13.7.")
```

---

## Key Protocol Details

### Why re-fetch the description?

The digest is computed from the **re-fetched** description (via Jira API after
`create_issue`), NOT from the description string passed to `create_issue`. This
is critical because Jira normalizes content during storage -- the stored
representation may differ from the input. The `scripts/sha256-digest.py` script
auto-detects whether the re-fetched content is ADF JSON or markdown and produces
the appropriate format-tagged digest (`sha256-adf:` or `sha256-md:`).

### Why digest before links?

Per `shared/description-digest-protocol.md` Rules: "Producers must post the digest
comment immediately after creating the task issue, before creating issue links or
other comments." This ensures the digest comment has the earliest timestamp among
all task comments, making it unambiguous for consumers (`/implement-task`) to
locate.

### Marker string

The exact marker prefix is `[sdlc-workflow] Description digest:` -- this is a
fixed string used by both producers and consumers. The full comment line is:

```
[sdlc-workflow] Description digest: sha256-md:<64-char-hex>
```

or

```
[sdlc-workflow] Description digest: sha256-adf:<64-char-hex>
```
