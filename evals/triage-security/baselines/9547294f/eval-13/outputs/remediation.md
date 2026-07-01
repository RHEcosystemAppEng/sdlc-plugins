# Step 8 -- Remediation (Case A: Affected)

The version impact analysis shows that versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream are affected by CVE-2026-31812 (quinn-proto < 0.11.14). Since the ecosystem is **Cargo** (a source dependency ecosystem), two remediation tasks are proposed: an upstream backport task and a downstream propagation subtask.

## Proposed Remediation Tasks

All actions below are presented as proposals for engineer confirmation before execution. No Jira mutations are performed without explicit approval.

---

### Task 1: Upstream Backport Task

**Proposed Jira create_issue call:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <upstream-task-description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task Description:**

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto - Panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is retag of v0.4.8)

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

#### Description Digest Protocol for Upstream Backport Task

After `create_issue` returns the new task key (e.g., TC-XXXX), the following digest procedure is performed **before** creating any issue links or other comments on the task:

1. **Re-fetch the description from Jira API** -- The description is re-fetched from Jira after creation because Jira normalizes content during storage. The description string passed to `create_issue` is NOT used for hashing.

   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```

2. **Write the re-fetched description to a temp file** and compute the SHA-256 digest using `scripts/sha256-digest.py`:

   ```bash
   # Write the re-fetched description content to a temp file
   # (the content comes from the Jira API response, not the original input string)
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<64-char-hex-digest> (or sha256-adf:<64-char-hex-digest>)
   ```

   The script auto-detects the input format (ADF JSON vs markdown) and outputs the appropriate format-tagged digest.

3. **Post the digest comment** to the upstream task. The comment uses the exact marker prefix `[sdlc-workflow] Description digest:`:

   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py` (e.g., `sha256-md:a1b2c3d4...64 hex chars`).

   The ADF format of this comment is:
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
             "text": "[sdlc-workflow] Description digest: sha256-md:<64-char-hex>"
           }
         ]
       }
     ]
   }
   ```

4. **Only after the digest comment is posted**, proceed to create issue links and other comments:

   ```
   # NOW create the Depend link to the Vulnerability issue
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <upstream-task-key>,
     type: "Depend"
   )
   ```

**Sequencing summary for upstream task:**
1. `create_issue` (create the task)
2. `get_issue` (re-fetch description from Jira)
3. `sha256-digest.py` (compute digest from re-fetched description)
4. `add_comment` (post `[sdlc-workflow] Description digest: <tagged-digest>`)
5. `create_link` (Depend link to TC-8001) -- AFTER digest comment
6. Any other comments -- AFTER digest comment

---

### Task 2: Downstream Propagation Subtask

**Proposed Jira create_issue call:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <downstream-task-description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task Description:**

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

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
- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Protocol for Downstream Propagation Subtask

After `create_issue` returns the new downstream task key (e.g., TC-YYYY), the following digest procedure is performed **before** creating any issue links (Depend to TC-8001, Blocks from upstream task) or other comments on the task:

1. **Re-fetch the description from Jira API** -- The description is re-fetched from Jira after creation because Jira normalizes content during storage. The description string passed to `create_issue` is NOT used for hashing.

   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```

2. **Write the re-fetched description to a temp file** and compute the SHA-256 digest using `scripts/sha256-digest.py`:

   ```bash
   # Write the re-fetched description content to a temp file
   # (the content comes from the Jira API response, not the original input string)
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<64-char-hex-digest> (or sha256-adf:<64-char-hex-digest>)
   ```

   The script auto-detects the input format (ADF JSON vs markdown) and outputs the appropriate format-tagged digest.

3. **Post the digest comment** to the downstream task. The comment uses the exact marker prefix `[sdlc-workflow] Description digest:`:

   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py` (e.g., `sha256-md:a1b2c3d4...64 hex chars`).

   The ADF format of this comment is:
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
             "text": "[sdlc-workflow] Description digest: sha256-md:<64-char-hex>"
           }
         ]
       }
     ]
   }
   ```

4. **Only after the digest comment is posted**, proceed to create issue links and other comments:

   ```
   # NOW create the Depend link to the Vulnerability issue
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )

   # NOW create the Blocks link from upstream to downstream
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

**Sequencing summary for downstream task:**
1. `create_issue` (create the task)
2. `get_issue` (re-fetch description from Jira)
3. `sha256-digest.py` (compute digest from re-fetched description)
4. `add_comment` (post `[sdlc-workflow] Description digest: <tagged-digest>`)
5. `create_link` (Depend link to TC-8001) -- AFTER digest comment
6. `create_link` (Blocks link from upstream task) -- AFTER digest comment
7. Any other comments -- AFTER digest comment

---

## Complete Remediation Procedure Sequence

The full end-to-end sequence for both tasks, showing digest comments are posted before any links or other comments:

```
# === UPSTREAM BACKPORT TASK ===

# 1. Create the upstream task
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <upstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)

# 2. Re-fetch description from Jira (NOT from the input string)
upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])

# 3. Compute digest from re-fetched description
# Write re-fetched description to /tmp/task-desc.md
python3 scripts/sha256-digest.py /tmp/task-desc.md  # -> sha256-md:<hex> or sha256-adf:<hex>

# 4. Post digest comment BEFORE any links
jira.add_comment(<upstream-task-key>,
  "[sdlc-workflow] Description digest: <tagged-digest>")

# 5. NOW create links (after digest comment)
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)

# === DOWNSTREAM PROPAGATION SUBTASK ===

# 6. Create the downstream task
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <downstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)

# 7. Re-fetch description from Jira (NOT from the input string)
downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])

# 8. Compute digest from re-fetched description
python3 scripts/sha256-digest.py /tmp/task-desc.md  # -> sha256-md:<hex> or sha256-adf:<hex>

# 9. Post digest comment BEFORE any links
jira.add_comment(<downstream-task-key>,
  "[sdlc-workflow] Description digest: <tagged-digest>")

# 10. NOW create links (after digest comment)
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)

# === POST-TRIAGE ===

# 11. Transition Vulnerability to In Progress
# 12. Add ai-cve-triaged label to TC-8001
# 13. Post summary comment to TC-8001
```

## Key Protocol Properties

1. **Digest is computed from the re-fetched description** (via `jira.get_issue` after `create_issue`), NOT from the description string passed to `create_issue`. This is because Jira normalizes content during storage, so the stored representation may differ from the input.

2. **The digest comment uses the exact marker prefix** `[sdlc-workflow] Description digest:` so that consumers (e.g., `/implement-task`) can locate it among all issue comments.

3. **Digest comments are posted BEFORE issue links** (Depend, Blocks) or other comments. This sequencing is mandated by `shared/description-digest-protocol.md` Rules: "Producers must post the digest comment immediately after creating the task issue, before creating issue links or other comments."

4. **The digest is computed using `scripts/sha256-digest.py`**, which auto-detects the input format (ADF JSON vs markdown) and produces a format-tagged digest (`sha256-md:<hex>` or `sha256-adf:<hex>`).

5. **Both tasks receive their own independent digest comment** -- the upstream backport task and the downstream propagation subtask each go through the full re-fetch, compute, and post cycle independently.
