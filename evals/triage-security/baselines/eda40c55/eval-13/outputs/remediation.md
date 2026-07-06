# Step 8 -- Remediation: TC-8001 (CVE-2026-31812)

## Triage Outcome

- **Stream 2.2.x (scoped)**: Case A -- affected versions exist (2.2.0, 2.2.1, 2.2.2). Create standard remediation tasks.
- **Stream 2.1.x (cross-stream)**: Case B -- all versions affected (2.1.0, 2.1.1), no stream-specific CVE Jira exists. Create preemptive remediation tasks.

Ecosystem: **Cargo** (source dependency) -- each stream gets **two tasks**: upstream backport + downstream propagation.

---

## Stream 2.2.x -- Standard Remediation Tasks (Case A)

### Task 1: Upstream Backport (2.2.x)

**Jira creation call:**
```
upstream_task_2_2 = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)",
  description: <see description below>,
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

Affected versions: 2.2.0 (0.11.9), 2.2.1 (0.11.12), 2.2.2 (0.11.12, retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8, v0.4.9

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z
- Note: upstream branch release/0.4.z already has the fix at HEAD
  (v0.4.11+ ships quinn-proto 0.11.14). Verify the fix is present
  on the branch; if so, this task may already be resolved.
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

#### Description Digest Protocol for Task 1 (Upstream Backport 2.2.x)

The following steps are performed **immediately after** `jira.create_issue` returns, and **before** creating any issue links (Depend to TC-8001) or posting any other comments:

1. **Re-fetch the description from Jira:**
   ```
   upstream_desc = jira.get_issue(<upstream_task_2_2_key>, fields=["description"])
   ```
   Write the returned description content to a temporary file `/tmp/task-desc.md`.
   The description is re-fetched because Jira normalizes content during storage --
   the string passed to `create_issue` may differ from what Jira actually stored.

2. **Compute the SHA-256 digest using the script:**
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The script auto-detects whether the input is ADF JSON or markdown text and
   outputs a format-tagged digest, e.g., `sha256-md:<64-char-hex>` or
   `sha256-adf:<64-char-hex>`.

3. **Post the digest comment to the newly created task:**
   ```
   jira.add_comment(<upstream_task_2_2_key>,
     "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from step 2 (e.g.,
   `sha256-md:a3b7c9d1e4f5...` -- the complete 64-character hex digest with
   format tag). The comment is a single line with the exact marker prefix
   `[sdlc-workflow] Description digest:`.

4. **Only after the digest comment is posted**, proceed to create issue links:
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <upstream_task_2_2_key>,
     type: "Depend"
   )
   ```

---

### Task 2: Downstream Propagation (2.2.x)

**Jira creation call:**
```
downstream_task_2_2 = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)",
  description: <see description below>,
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
CVE-2026-31812 fix from <upstream_task_2_2_key>.

The upstream backport (<upstream_task_2_2_key>) bumps quinn-proto to 0.11.14
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

- Depends on: <upstream_task_2_2_key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Protocol for Task 2 (Downstream Propagation 2.2.x)

The following steps are performed **immediately after** `jira.create_issue` returns, and **before** creating any issue links (Blocks from upstream task, Depend to TC-8001) or posting any other comments:

1. **Re-fetch the description from Jira:**
   ```
   downstream_desc = jira.get_issue(<downstream_task_2_2_key>, fields=["description"])
   ```
   Write the returned description content to a temporary file `/tmp/task-desc.md`.
   The description is re-fetched because Jira normalizes content during storage --
   the string passed to `create_issue` may differ from what Jira actually stored.

2. **Compute the SHA-256 digest using the script:**
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The script auto-detects the input format and outputs a format-tagged digest
   (e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`).

3. **Post the digest comment to the newly created task:**
   ```
   jira.add_comment(<downstream_task_2_2_key>,
     "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from step 2 (the complete
   64-character hex digest with format tag). The comment is a single line
   with the exact marker prefix `[sdlc-workflow] Description digest:`.

4. **Only after the digest comment is posted**, proceed to create issue links:
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <downstream_task_2_2_key>,
     type: "Depend"
   )
   jira.create_link(
     inwardIssue: <upstream_task_2_2_key>,
     outwardIssue: <downstream_task_2_2_key>,
     type: "Blocks"
   )
   ```

---

## Stream 2.1.x -- Preemptive Remediation Tasks (Case B)

Cross-stream impact detected: stream 2.1.x is also affected (all versions ship quinn-proto 0.11.9).

Before creating preemptive tasks, search for existing CVE Jiras for 2.1.x:
```
jira.search_jql(
  jql: "project = TC AND issuetype = 10024 AND labels = CVE-2026-31812 AND summary ~ 'rhtpa-2.1'",
  fields: ["summary", "status"],
  maxResults: 5
)
```

Assuming no stream-specific CVE Jira exists for 2.1.x, create preemptive tasks with `security-preemptive` label and "Related" link type.

### Task 3: Preemptive Upstream Backport (2.1.x)

**Jira creation call:**
```
upstream_task_2_1 = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task description:**

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for this stream. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (0.11.9), 2.1.1 (0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.3.z
- Note: upstream branch release/0.3.z does NOT yet have the fix
  (v0.3.12 ships quinn-proto 0.11.9). An upstream PR is required
  to bump the dependency on this branch.
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

#### Description Digest Protocol for Task 3 (Preemptive Upstream Backport 2.1.x)

The following steps are performed **immediately after** `jira.create_issue` returns, and **before** creating any issue links (Related to TC-8001) or posting any other comments:

1. **Re-fetch the description from Jira:**
   ```
   upstream_desc_2_1 = jira.get_issue(<upstream_task_2_1_key>, fields=["description"])
   ```
   Write the returned description content to a temporary file `/tmp/task-desc.md`.
   The description is re-fetched because Jira normalizes content during storage --
   the string passed to `create_issue` may differ from what Jira actually stored.

2. **Compute the SHA-256 digest using the script:**
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The script auto-detects the input format and outputs a format-tagged digest
   (e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`).

3. **Post the digest comment to the newly created task:**
   ```
   jira.add_comment(<upstream_task_2_1_key>,
     "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from step 2 (the complete
   64-character hex digest with format tag). The comment is a single line
   with the exact marker prefix `[sdlc-workflow] Description digest:`.

4. **Only after the digest comment is posted**, proceed to create the issue link.
   Preemptive tasks use "Related" (not "Depend") because the originating CVE
   belongs to a different stream:
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <upstream_task_2_1_key>,
     type: "Related"
   )
   ```

---

### Task 4: Preemptive Downstream Propagation (2.1.x)

**Jira creation call:**
```
downstream_task_2_1 = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task description:**

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for this stream. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from <upstream_task_2_1_key>.

The upstream backport (<upstream_task_2_1_key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

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

- Depends on: <upstream_task_2_1_key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Protocol for Task 4 (Preemptive Downstream Propagation 2.1.x)

The following steps are performed **immediately after** `jira.create_issue` returns, and **before** creating any issue links (Related to TC-8001, Blocks from upstream task) or posting any other comments:

1. **Re-fetch the description from Jira:**
   ```
   downstream_desc_2_1 = jira.get_issue(<downstream_task_2_1_key>, fields=["description"])
   ```
   Write the returned description content to a temporary file `/tmp/task-desc.md`.
   The description is re-fetched because Jira normalizes content during storage --
   the string passed to `create_issue` may differ from what Jira actually stored.

2. **Compute the SHA-256 digest using the script:**
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The script auto-detects the input format and outputs a format-tagged digest
   (e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`).

3. **Post the digest comment to the newly created task:**
   ```
   jira.add_comment(<downstream_task_2_1_key>,
     "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from step 2 (the complete
   64-character hex digest with format tag). The comment is a single line
   with the exact marker prefix `[sdlc-workflow] Description digest:`.

4. **Only after the digest comment is posted**, proceed to create issue links.
   Preemptive tasks use "Related" (not "Depend"):
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <downstream_task_2_1_key>,
     type: "Related"
   )
   jira.create_link(
     inwardIssue: <upstream_task_2_1_key>,
     outwardIssue: <downstream_task_2_1_key>,
     type: "Blocks"
   )
   ```

---

## Summary of Digest Protocol Sequencing

For **every** remediation task (both standard and preemptive, both upstream and downstream), the description digest protocol follows the same sequence:

```
1. jira.create_issue(...)                           -- create the task
2. jira.get_issue(<new-task-key>, fields=["description"])  -- RE-FETCH description
3. python3 scripts/sha256-digest.py /tmp/task-desc.md      -- compute tagged digest
4. jira.add_comment(<new-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
5. jira.create_link(...)                            -- ONLY NOW create issue links
6. (any other comments)                             -- ONLY AFTER digest comment
```

Key rules:
- The digest is computed from the **re-fetched** description, NOT from the string originally passed to `create_issue`. Jira normalizes content during storage.
- The digest comment MUST be posted **before** any issue links (Depend, Blocks, Related) or other comments.
- The `scripts/sha256-digest.py` script auto-detects the format (ADF JSON vs markdown) and outputs a format-tagged digest (e.g., `sha256-md:<64-hex>` or `sha256-adf:<64-hex>`).
- The format tag is part of the digest value -- do not strip it.
- The digest is exactly 64 lowercase hexadecimal characters (SHA-256). Never use abbreviated, placeholder, or example hashes.
- The comment body is a single line: `[sdlc-workflow] Description digest: sha256-md:<64-char-hex>` (or `sha256-adf:<64-char-hex>`).

## Post-Task-Creation Linkage Summary

After all four tasks are created and their digest comments are posted:

### Standard tasks (2.2.x):
- `<upstream_task_2_2_key>` --[Depend]--> TC-8001
- `<downstream_task_2_2_key>` --[Depend]--> TC-8001
- `<upstream_task_2_2_key>` --[Blocks]--> `<downstream_task_2_2_key>`

### Preemptive tasks (2.1.x):
- `<upstream_task_2_1_key>` --[Related]--> TC-8001
- `<downstream_task_2_1_key>` --[Related]--> TC-8001
- `<upstream_task_2_1_key>` --[Blocks]--> `<downstream_task_2_1_key>`

## Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8001.
2. Post summary comment to TC-8001 documenting:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 removed, RHTPA 2.2.0/2.2.1/2.2.2 added)
   - Remediation tasks created (all four task keys)
   - Cross-stream impact notice for 2.1.x with preemptive task keys
   - @mention of the reporter (using ADF mention node with reporter account ID)
   - Comment Footnote: "This comment was AI-generated by sdlc-workflow/triage-security v0.12.2."
3. Post cross-stream impact comment to TC-8001:
   ```
   Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
   based on lock file analysis. Preemptive remediation tasks created:
   - 2.1.x: <upstream_task_2_1_key> (upstream), <downstream_task_2_1_key> (downstream)
   (security-preemptive)
   ```
   With Comment Footnote appended.
