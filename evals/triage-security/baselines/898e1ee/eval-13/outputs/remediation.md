# Step 7 -- Remediation: TC-8001

## Triage Outcome

This issue is stream-scoped to 2.2.x. The version impact analysis shows:

- **Stream 2.2.x (in scope)**: Versions 2.2.0, 2.2.1, 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fixed quinn-proto 0.11.14. Since the latest released versions (2.2.3, 2.2.4) already contain the fix, the vulnerability is already resolved in the current builds of this stream. The Affects Versions correction documents the historical exposure.
- **Stream 2.1.x (cross-stream)**: All versions (2.1.0, 2.1.1) are affected with quinn-proto 0.11.9. No version in this stream ships the fix. This triggers Case B (cross-stream impact).

Since stream 2.2.x already has the fix in its latest builds (2.2.3+), the primary remediation for that stream is already done. However, stream 2.1.x still needs remediation. Because this issue is scoped to 2.2.x, the 2.1.x remediation is handled via Case B preemptive tasks.

## Remediation Tasks

Since quinn-proto is a Cargo (source dependency) ecosystem, each affected stream requires **two tasks**: an upstream backport task and a downstream propagation subtask.

---

### Task 1: Upstream Backport Task (Stream 2.1.x -- Preemptive)

**Jira API call:**

```
upstream_task = jira.create_issue(
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
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8, quinn-proto 0.11.9), 2.1.1 (v0.3.12, quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.3.z
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

#### Description Digest Comment Flow for Upstream Task

After creating the upstream task (assume it gets key TC-9001), the following steps are performed **before** creating any issue links or other comments:

1. **Re-fetch the description from Jira:**
   ```
   upstream_desc = jira.get_issue("TC-9001", fields=["description"])
   ```
   This returns the description as Jira stored it (which may differ from what was passed to `create_issue` due to Jira's internal normalization). The re-fetched description is used for hashing, NOT the original description string.

2. **Write the re-fetched description to a temp file:**
   ```
   # Write the re-fetched description content to /tmp/task-desc.md
   ```

3. **Compute the SHA-256 digest using the script:**
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The script auto-detects whether the input is ADF JSON or markdown text:
   - If the Jira API returned ADF JSON: outputs `sha256-adf:<64-char-hex-digest>`
   - If the Jira API returned markdown: outputs `sha256-md:<64-char-hex-digest>`

4. **Post the digest comment on the upstream task:**
   ```
   jira.add_comment("TC-9001", "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the exact output from step 3 (e.g., `sha256-md:a3b4c5d6...` -- full 64-char hex). The comment is posted as a standalone comment using ADF contentFormat:
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

5. **Only after the digest comment is posted**, proceed to create issue links:
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: "TC-9001",
     type: "Related"
   )
   ```
   Note: Preemptive tasks use "Related" link type (not "Depend") because the originating CVE belongs to a different stream.

---

### Task 2: Downstream Propagation Subtask (Stream 2.1.x -- Preemptive)

**Jira API call:**

```
downstream_task = jira.create_issue(
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
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from TC-9001.

The upstream backport (TC-9001) bumps quinn-proto to 0.11.14
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

- Depends on: TC-9001 (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Comment Flow for Downstream Task

After creating the downstream task (assume it gets key TC-9002), the following steps are performed **before** creating any issue links or other comments:

1. **Re-fetch the description from Jira:**
   ```
   downstream_desc = jira.get_issue("TC-9002", fields=["description"])
   ```
   This returns the description as Jira stored it after normalization. The re-fetched description is what gets hashed -- never the description string originally passed to `create_issue`.

2. **Write the re-fetched description to a temp file:**
   ```
   # Write the re-fetched description content to /tmp/task-desc.md
   ```

3. **Compute the SHA-256 digest using the script:**
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The script auto-detects the format and outputs the appropriately tagged digest:
   - ADF JSON input: `sha256-adf:<64-char-hex-digest>`
   - Markdown text input: `sha256-md:<64-char-hex-digest>`

4. **Post the digest comment on the downstream task:**
   ```
   jira.add_comment("TC-9002", "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the exact full output from step 3. The comment is posted as a standalone ADF comment:
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

5. **Only after the digest comment is posted**, proceed to create issue links:
   ```
   # Link downstream as blocked by upstream
   jira.create_link(
     inwardIssue: "TC-9001",
     outwardIssue: "TC-9002",
     type: "Blocks"
   )

   # Link downstream to originating CVE (preemptive: "Related")
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: "TC-9002",
     type: "Related"
   )
   ```

---

## Summary of Description Digest Protocol

For both the upstream backport task and the downstream propagation subtask, the description digest comment flow is identical:

1. **Create the task** via `jira.create_issue(...)`.
2. **Re-fetch the description** from Jira using `jira.get_issue(<task-key>, fields=["description"])`. This is critical because Jira normalizes content during storage, so the stored description may differ from what was passed to `create_issue`.
3. **Write the re-fetched description** to a temp file (e.g., `/tmp/task-desc.md`).
4. **Compute the digest** using `python3 scripts/sha256-digest.py /tmp/task-desc.md`. The script auto-detects format (ADF JSON vs markdown) and outputs a format-tagged digest (`sha256-adf:<hex>` or `sha256-md:<hex>`).
5. **Post the digest comment** as a standalone comment on the task: `[sdlc-workflow] Description digest: <tagged-digest>`.
6. **Only then** create issue links (`Depend`, `Blocks`, `Related`) and post any other comments.

Key rules:
- The digest is computed from the **re-fetched** description, never from the description string passed to `create_issue`.
- The digest comment must be posted **before** creating issue links or other comments.
- Both the upstream and downstream tasks receive their own digest comment.
- The digest comment is a standalone comment -- not appended to any other comment.
- The full 64-character hex digest must be included (no abbreviations).
- The format tag (`sha256-md:` or `sha256-adf:`) must be preserved from the script output.
- The marker string `[sdlc-workflow] Description digest:` is fixed and must not be varied.

## Post-Task-Creation Actions

After both tasks are created and their digest comments posted:

1. **Post preemptive tasks comment** on TC-8001:
   ```
   Preemptive remediation tasks created for streams without CVE Jiras:
   - 2.1.x: TC-9001 (upstream backport), TC-9002 (downstream propagation) (security-preemptive)

   These tasks use the "Related" link type and carry the security-preemptive
   label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
   reconciliation will link them and remove the label.
   ```

2. **Post cross-stream impact comment** on TC-8001:
   ```
   Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s)
   2.1.x based on lock file analysis.
   These streams are tracked by companion issues (see Related links)
   or may require separate PSIRT triage.
   ```

3. **Add `ai-cve-triaged` label** to TC-8001.

4. **Post summary comment** on TC-8001 with version impact table, Affects Versions correction, triage outcome, task links, and @mention of the reporter.

All Jira comments include the Comment Footnote per `shared/comment-footnote.md` with skill name `triage-security`.
