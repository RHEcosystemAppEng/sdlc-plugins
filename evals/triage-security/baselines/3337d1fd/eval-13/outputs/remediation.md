# Step 8 -- Remediation for CVE-2026-31812 (TC-8001)

## Triage Outcome Summary

- **Issue stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Ecosystem**: Cargo (source dependency)
- **2.2.x stream**: Fix already shipped in versions 2.2.3+ (quinn-proto 0.11.14). No new remediation task needed.
- **2.1.x stream**: All versions affected (quinn-proto 0.11.9). Fix NOT present on upstream branch `release/0.3.z`. Remediation required.
- **Case determination**: Case B (cross-stream impact) -- the 2.1.x stream is affected but is outside this issue's scope.

## Case B: Cross-Stream Impact

### Cross-stream impact comment (posted on TC-8001)

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. Stream 2.1.x is tracked by companion
issues (see Related links) or may require separate PSIRT triage.
```

### Preemptive remediation task check

Search for existing CVE Jiras for the 2.1.x stream with JQL:
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8001
```

Assuming no sibling CVE Jira exists for the 2.1.x stream, preemptive remediation tasks are created.

Since this is a Cargo (source dependency) ecosystem, **two** preemptive tasks are created for the 2.1.x stream.

---

## Preemptive Task 1: Upstream Backport (2.1.x stream)

### Jira Issue Creation

```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)",
  description: <upstream-task-description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

### Task Description

```markdown
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (DoS).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (quinn-proto 0.11.9), RHTPA 2.1.1 (quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct or transitive (verify via `Cargo.lock` inspection at `v0.3.12`)

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

When the vulnerable package is a **transitive** dependency (pulled in
through intermediate packages), use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (see dependency
  chain above)
- Bump the direct dependency to a version whose transitive closure
  includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes to the
  direct dependency

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable (breaking API changes,
no release available with the fix):
- Cargo: `cargo add quinn-proto@0.11.14` to add as a direct
  dependency, overriding the transitive resolution
- Document why the direct dep bump was not viable in the PR description

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

### Description Digest Comment (posted immediately after task creation)

After creating the upstream backport task, the description digest protocol is followed:

1. **Re-fetch the description** from Jira to get the stored/normalized version:
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```

2. **Write the description to a temp file** and compute the digest:
   ```bash
   # Write the fetched description to a temp file
   # (content comes from the Jira API response, not the input string)
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The script auto-detects the format:
   - If the API returned ADF JSON, the output is `sha256-adf:<64-char-hex>`
   - If the API returned markdown text, the output is `sha256-md:<64-char-hex>`

3. **Post the digest comment** on the newly created task (before any links or other comments):
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py` (e.g., `sha256-md:a1b2c3d4...` -- full 64-character hex digest).

   The comment is posted in ADF format:
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

4. **Link the task** to the originating CVE Jira with "Related" (preemptive variant):
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <upstream-task-key>,
     type: "Related"
   )
   ```

---

## Preemptive Task 2: Downstream Propagation Subtask (2.1.x stream)

### Jira Issue Creation

```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <downstream-task-description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

### Task Description

```markdown
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: direct or transitive -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback
  approach), verify the pinning is reflected in the downstream build's
  lock file after the source reference update
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

### Description Digest Comment (posted immediately after task creation)

After creating the downstream propagation task, the description digest protocol is followed:

1. **Re-fetch the description** from Jira to get the stored/normalized version:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```

2. **Write the description to a temp file** and compute the digest:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The script auto-detects the format and outputs `sha256-adf:<64-char-hex>` or `sha256-md:<64-char-hex>`.

3. **Post the digest comment** on the newly created task (before any links or other comments):
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py` (full 64-character hex digest with format tag).

   The comment is posted in ADF format:
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

4. **Link the task** to the originating CVE Jira with "Related" (preemptive variant):
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <downstream-task-key>,
     type: "Related"
   )
   ```

5. **Link the downstream subtask as blocked by the upstream task**:
   ```
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

---

## Post-Creation: Preemptive Task Comment on TC-8001

After both preemptive tasks are created and their digest comments posted, add a comment to the originating CVE Jira (TC-8001):

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <upstream-task-key> (upstream backport, security-preemptive),
  <downstream-task-key> (downstream propagation, security-preemptive,
  blocked by <upstream-task-key>)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

---

## 2.2.x Stream: No Remediation Needed

For the issue-scoped 2.2.x stream, no new remediation task is created because:

1. The upstream branch `release/0.4.z` already includes the fix (quinn-proto 0.11.14 since tag `v0.4.11`).
2. The Konflux releases 2.2.3 (build 0.4.11) and 2.2.4 (build 0.4.12) already ship the fixed version.
3. The affected versions (2.2.0, 2.2.1, 2.2.2) are superseded by the fixed releases.

The Affects Versions are corrected to `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]` to record the historical vulnerability, but no code change is required.

---

## Post-Triage Summary

### 1. Add the `ai-cve-triaged` label to TC-8001

### 2. Post a summary comment on TC-8001

The summary comment would document:

1. The version impact table (all streams)
2. The Affects Versions correction: `RHTPA 2.0.0` -> `RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2`
3. Triage outcome:
   - 2.2.x stream: fix already shipped in 2.2.3+ (no remediation task needed)
   - 2.1.x stream: preemptive remediation tasks created (Case B cross-stream impact)
4. Links to all remediation tasks: <upstream-task-key> (upstream backport), <downstream-task-key> (downstream propagation, blocked by <upstream-task-key>)
5. @mention of the Vulnerability issue reporter (using ADF mention node with reporter's account ID from the Jira issue data)

The summary comment includes the Comment Footnote per `shared/comment-footnote.md` with skill name `triage-security`.

---

## Description Digest Protocol Summary

The description digest protocol is applied to every remediation task created. The key steps are:

1. **Create the task** via `jira.create_issue(...)`.
2. **Re-fetch the description** from Jira immediately after creation (`jira.get_issue(<key>, fields=["description"])`). This is essential because Jira normalizes content during storage -- the stored description may differ from the input.
3. **Write the fetched description to a temp file** and compute the SHA-256 digest using `python3 scripts/sha256-digest.py /tmp/task-desc.md`. The script auto-detects the format (ADF JSON or markdown) and outputs a tagged digest.
4. **Post the digest comment** as a standalone comment on the task, using the exact marker format: `[sdlc-workflow] Description digest: <tagged-digest>`. This comment must be posted BEFORE creating issue links or other comments on the task.
5. **Proceed with links and other comments** only after the digest comment is posted.

The digest enables `/implement-task` to verify description integrity in its Step 1.5 -- if the description was modified after triage, the consumer will detect the mismatch and warn the engineer.
