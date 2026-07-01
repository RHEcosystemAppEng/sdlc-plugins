# Step 8 -- Remediation (Case A: Affected)

## Triage Outcome

The issue is scoped to the **2.2.x** stream (suffix `[rhtpa-2.2]`). Within this stream, versions **2.2.0, 2.2.1, and 2.2.2** are affected by CVE-2026-31812 (quinn-proto < 0.11.14). Versions 2.2.3 and 2.2.4 already ship the fixed version.

Since quinn-proto is a **Cargo** (source dependency) ecosystem, remediation requires **two tasks**: an upstream backport task and a downstream propagation subtask.

Additionally, the 2.1.x stream is also affected (cross-stream impact -- Case B), but remediation tasks for the 2.1.x stream would be handled separately via the cross-stream impact flow. This output focuses on the 2.2.x stream remediation and the description digest protocol.

---

## Proposed Remediation Task 1: Upstream Backport Task

### Jira Issue Creation

```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <upstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

```markdown
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto Panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
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

### Description Digest Protocol (Upstream Backport Task)

After creating the upstream backport task, the following description digest steps are performed **before** creating any issue links or other comments:

**Step 1: Re-fetch the description from Jira**

After `jira.create_issue` returns the new task key (e.g., `TC-9100`), re-fetch the task description from the Jira API. This is mandatory because Jira normalizes content during storage -- the description returned from the API may differ from the string passed to `create_issue`.

```
upstream_desc = jira.get_issue("TC-9100", fields=["description"])
```

Write the fetched description content to a temporary file:

```bash
# Write the re-fetched description to a temp file
cat > /tmp/task-desc.md << 'EOF'
<re-fetched description content from Jira API>
EOF
```

**Step 2: Compute the SHA-256 digest**

Run `scripts/sha256-digest.py` on the re-fetched description. The script auto-detects the input format (ADF JSON or markdown) and outputs a format-tagged digest:

```bash
python3 scripts/sha256-digest.py /tmp/task-desc.md
# Output: sha256-md:<64-char-hex-digest>  (if markdown)
# or:     sha256-adf:<64-char-hex-digest> (if ADF JSON)
```

**Step 3: Post the digest comment**

Post a standalone comment on the upstream backport task with the digest. This comment uses the exact marker prefix `[sdlc-workflow] Description digest:`:

```
jira.add_comment("TC-9100", "[sdlc-workflow] Description digest: sha256-md:<64-char-hex-digest>")
```

The comment body is exactly one line: `[sdlc-workflow] Description digest: <tagged-digest>`. No extra text, timestamps, or metadata is appended.

**Step 4: THEN create issue links and other comments**

Only after the digest comment is posted, proceed to create links:

```
# Link upstream task to the Vulnerability issue
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: "TC-9100",
  type: "Depend"
)
```

### Sequencing Summary for Upstream Backport Task

1. `jira.create_issue(...)` -- create the task
2. `jira.get_issue(<task-key>, fields=["description"])` -- re-fetch description
3. `python3 scripts/sha256-digest.py /tmp/task-desc.md` -- compute digest from re-fetched description
4. `jira.add_comment(<task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")` -- post digest comment
5. `jira.create_link(...)` -- create Depend link to TC-8001
6. Other comments (if any)

---

## Proposed Remediation Task 2: Downstream Propagation Subtask

### Jira Issue Creation

```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <downstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

```markdown
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from TC-9100.

The upstream backport (TC-9100) bumps quinn-proto to 0.11.14
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

- Depends on: TC-9100 (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Description Digest Protocol (Downstream Propagation Subtask)

After creating the downstream propagation subtask, the same description digest steps are performed **before** creating any issue links or other comments:

**Step 1: Re-fetch the description from Jira**

After `jira.create_issue` returns the new task key (e.g., `TC-9101`), re-fetch the task description from the Jira API. The digest must be computed from the re-fetched description, not the description string passed to `create_issue`, because Jira normalizes content during storage.

```
downstream_desc = jira.get_issue("TC-9101", fields=["description"])
```

Write the fetched description content to a temporary file:

```bash
cat > /tmp/task-desc.md << 'EOF'
<re-fetched description content from Jira API>
EOF
```

**Step 2: Compute the SHA-256 digest**

Run `scripts/sha256-digest.py` on the re-fetched description:

```bash
python3 scripts/sha256-digest.py /tmp/task-desc.md
# Output: sha256-md:<64-char-hex-digest>  (if markdown)
# or:     sha256-adf:<64-char-hex-digest> (if ADF JSON)
```

**Step 3: Post the digest comment**

Post a standalone comment on the downstream propagation subtask with the digest marker:

```
jira.add_comment("TC-9101", "[sdlc-workflow] Description digest: sha256-md:<64-char-hex-digest>")
```

The comment uses the exact marker prefix `[sdlc-workflow] Description digest:` as a single-line comment with no additional text.

**Step 4: THEN create issue links and other comments**

Only after the digest comment is posted, proceed to create links:

```
# Link downstream task to the Vulnerability issue
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: "TC-9101",
  type: "Depend"
)

# Link downstream task as blocked by the upstream task
jira.create_link(
  inwardIssue: "TC-9100",
  outwardIssue: "TC-9101",
  type: "Blocks"
)
```

### Sequencing Summary for Downstream Propagation Subtask

1. `jira.create_issue(...)` -- create the subtask
2. `jira.get_issue(<task-key>, fields=["description"])` -- re-fetch description
3. `python3 scripts/sha256-digest.py /tmp/task-desc.md` -- compute digest from re-fetched description
4. `jira.add_comment(<task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")` -- post digest comment
5. `jira.create_link(inward: "TC-8001", outward: <task-key>, type: "Depend")` -- link to CVE Jira
6. `jira.create_link(inward: "TC-9100", outward: <task-key>, type: "Blocks")` -- blocked-by upstream task
7. Other comments (if any)

---

## Critical Protocol Rules

The description digest protocol follows these rules for **both** the upstream backport task and the downstream propagation subtask:

1. **Re-fetch, do not reuse**: The digest is computed from the re-fetched description (via `jira.get_issue` after `create_issue`), NOT from the description string passed to `create_issue`. Jira normalizes content during storage, so the stored description may differ from the submitted one.

2. **Digest before links**: The digest comment MUST be posted BEFORE creating issue links (`Depend`, `Blocks`) or any other comments on the task. This ensures `/implement-task` can verify description integrity from the earliest possible point.

3. **Use scripts/sha256-digest.py**: The digest is computed using `scripts/sha256-digest.py`, which auto-detects input format (ADF JSON vs markdown) and outputs a format-tagged digest (`sha256-adf:<hex>` or `sha256-md:<hex>`).

4. **Exact marker string**: The comment uses the exact marker prefix `[sdlc-workflow] Description digest:` so that `/implement-task` can locate it among all issue comments.

5. **Standalone comment**: The digest comment is posted as an independent comment, not appended to the post-triage summary or any other comment.

---

## Post-Creation Actions

After both remediation tasks are created and their digest comments are posted:

1. **Transition** TC-8001 to In Progress
2. **Assign** TC-8001 to the current user
3. **Add the `ai-cve-triaged` label** to TC-8001
4. **Post a summary comment** to TC-8001 documenting:
   - The version impact table
   - The Affects Versions correction (RHTPA 2.0.0 -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2)
   - The triage outcome (remediation tasks created)
   - Links to: TC-9100 (upstream backport), TC-9101 (downstream propagation, blocked by TC-9100)
   - The summary comment includes the Comment Footnote
