# Step 7 -- Remediation: CVE-2026-31812

## Triage Outcome

This is **Case A + Case B**: The scoped stream (2.2.x) has affected versions requiring remediation tasks, AND cross-stream impact on 2.1.x requires preemptive remediation tasks.

Since quinn-proto is a **Cargo** (source dependency) ecosystem, each affected stream requires **two tasks**: an upstream backport task and a downstream propagation subtask.

---

## Case A: Scoped Stream 2.2.x -- Standard Remediation Tasks

### Task 1: Upstream Backport Task (2.2.x)

**Jira API call:**

```
upstream_task = jira.create_issue(
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

Affected versions: 2.2.0 (v0.4.5, quinn-proto 0.11.9), 2.2.1 (v0.4.8, quinn-proto 0.11.12), 2.2.2 (retag of 2.2.1)
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
- Note: upstream fix already landed on release/0.4.z as of v0.4.11

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Flow for Upstream Task (2.2.x)

After creating the upstream task (assume it gets key TC-9001):

**Step 1 -- Re-fetch the created task description from Jira:**

```
upstream_desc = jira.get_issue("TC-9001", fields=["description"])
```

This re-fetches the description as stored by Jira, which may differ from the string passed to `create_issue` due to Jira-side formatting normalization.

**Step 2 -- Write re-fetched description to temp file and compute SHA-256 digest:**

```bash
# Write the re-fetched description to a temp file
cat > /tmp/task-desc.md << 'DESCRIPTION'
<content of the re-fetched description from jira.get_issue>
DESCRIPTION

# Compute digest using the project script
python3 scripts/sha256-digest.py /tmp/task-desc.md
# Output: sha256-md:<64-char-hex-digest>  (or sha256-adf:<64-char-hex-digest> if REST API returned ADF JSON)
```

The script auto-detects the format (markdown vs ADF JSON) and outputs the appropriately tagged digest.

**Step 3 -- Post digest comment on the created task (BEFORE creating any issue links):**

```
jira.add_comment("TC-9001", "[sdlc-workflow] Description digest: sha256-md:<64-char-hex-digest>")
```

The comment uses the exact marker prefix `[sdlc-workflow] Description digest:` followed by the full tagged digest value from the script output. This comment is posted as a standalone comment, not appended to any other comment.

**Step 4 -- Only after the digest comment is posted, proceed to create issue links and other comments.**

---

### Task 2: Downstream Propagation Subtask (2.2.x)

**Jira API call:**

```
downstream_task = jira.create_issue(
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
CVE-2026-31812 fix from TC-9001.

The upstream backport (TC-9001) bumps quinn-proto to 0.11.14
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

- Depends on: TC-9001 (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Flow for Downstream Task (2.2.x)

After creating the downstream task (assume it gets key TC-9002):

**Step 1 -- Re-fetch the created task description from Jira:**

```
downstream_desc = jira.get_issue("TC-9002", fields=["description"])
```

This re-fetches the description as stored by Jira, accounting for any Jira-side formatting changes applied during storage.

**Step 2 -- Write re-fetched description to temp file and compute SHA-256 digest:**

```bash
# Write the re-fetched description to a temp file
cat > /tmp/task-desc.md << 'DESCRIPTION'
<content of the re-fetched description from jira.get_issue>
DESCRIPTION

# Compute digest using the project script
python3 scripts/sha256-digest.py /tmp/task-desc.md
# Output: sha256-md:<64-char-hex-digest>  (or sha256-adf:<64-char-hex-digest> if REST API returned ADF JSON)
```

**Step 3 -- Post digest comment on the created task (BEFORE creating any issue links):**

```
jira.add_comment("TC-9002", "[sdlc-workflow] Description digest: sha256-md:<64-char-hex-digest>")
```

**Step 4 -- Only after the digest comment is posted, proceed to create issue links:**

```
# Link downstream task to vulnerability issue
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: "TC-9002",
  type: "Depend"
)

# Link downstream task as blocked by upstream task
jira.create_link(
  inwardIssue: "TC-9001",
  outwardIssue: "TC-9002",
  type: "Blocks"
)
```

---

## Linkage for Case A Tasks (2.2.x)

After both digest comments are posted:

```
# Link upstream task to vulnerability issue
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: "TC-9001",
  type: "Depend"
)

# Link downstream task to vulnerability issue
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: "TC-9002",
  type: "Depend"
)

# Link downstream blocked by upstream
jira.create_link(
  inwardIssue: "TC-9001",
  outwardIssue: "TC-9002",
  type: "Blocks"
)
```

---

## Case B: Cross-Stream Impact -- 2.1.x Preemptive Remediation Tasks

The 2.1.x stream is also affected (all versions ship quinn-proto 0.11.9) but has no stream-specific CVE Jira. Preemptive remediation tasks are created with the `security-preemptive` label and "Related" link type.

### Task 3: Upstream Backport Task (2.1.x, preemptive)

**Jira API call:**

```
preemptive_upstream_task = jira.create_issue(
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
- Note: upstream fix has NOT landed on release/0.3.z yet -- backport required

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Flow for Preemptive Upstream Task (2.1.x)

After creating the preemptive upstream task (assume it gets key TC-9003):

**Step 1 -- Re-fetch the created task description from Jira:**

```
preemptive_upstream_desc = jira.get_issue("TC-9003", fields=["description"])
```

This re-fetches the description as stored by Jira. The re-fetch is critical because Jira may normalize the blockquote formatting, whitespace, or markdown syntax during storage, producing a different byte sequence than the string passed to `create_issue`.

**Step 2 -- Write re-fetched description to temp file and compute SHA-256 digest:**

```bash
# Write the re-fetched description to a temp file
cat > /tmp/task-desc.md << 'DESCRIPTION'
<content of the re-fetched description from jira.get_issue>
DESCRIPTION

# Compute digest using the project script
python3 scripts/sha256-digest.py /tmp/task-desc.md
# Output: sha256-md:<64-char-hex-digest>  (or sha256-adf:<64-char-hex-digest> if REST API returned ADF JSON)
```

**Step 3 -- Post digest comment on the created task (BEFORE creating any issue links):**

```
jira.add_comment("TC-9003", "[sdlc-workflow] Description digest: sha256-md:<64-char-hex-digest>")
```

**Step 4 -- Only after the digest comment is posted, create the "Related" link to the originating CVE:**

```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: "TC-9003",
  type: "Related"
)
```

---

### Task 4: Downstream Propagation Subtask (2.1.x, preemptive)

**Jira API call:**

```
preemptive_downstream_task = jira.create_issue(
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
CVE-2026-31812 fix from TC-9003.

The upstream backport (TC-9003) bumps quinn-proto to 0.11.14
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

- Depends on: TC-9003 (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Flow for Preemptive Downstream Task (2.1.x)

After creating the preemptive downstream task (assume it gets key TC-9004):

**Step 1 -- Re-fetch the created task description from Jira:**

```
preemptive_downstream_desc = jira.get_issue("TC-9004", fields=["description"])
```

**Step 2 -- Write re-fetched description to temp file and compute SHA-256 digest:**

```bash
# Write the re-fetched description to a temp file
cat > /tmp/task-desc.md << 'DESCRIPTION'
<content of the re-fetched description from jira.get_issue>
DESCRIPTION

# Compute digest using the project script
python3 scripts/sha256-digest.py /tmp/task-desc.md
# Output: sha256-md:<64-char-hex-digest>  (or sha256-adf:<64-char-hex-digest> if REST API returned ADF JSON)
```

**Step 3 -- Post digest comment on the created task (BEFORE creating any issue links):**

```
jira.add_comment("TC-9004", "[sdlc-workflow] Description digest: sha256-md:<64-char-hex-digest>")
```

**Step 4 -- Only after the digest comment is posted, create links:**

```
# Related link to originating CVE (preemptive, not Depend)
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: "TC-9004",
  type: "Related"
)

# Blocks link: downstream blocked by upstream
jira.create_link(
  inwardIssue: "TC-9003",
  outwardIssue: "TC-9004",
  type: "Blocks"
)
```

---

## Summary of Description Digest Protocol

For every remediation task created (both standard and preemptive), the description digest flow is:

1. **Create the task** via `jira.create_issue()`
2. **Re-fetch the description** via `jira.get_issue(<task-key>, fields=["description"])` -- this is critical because Jira normalizes content during storage, so the stored description may differ from what was passed to `create_issue`
3. **Write the re-fetched description to a temp file** and **compute the SHA-256 digest** using `python3 scripts/sha256-digest.py /tmp/task-desc.md` -- the script auto-detects format (markdown vs ADF JSON) and outputs a tagged digest like `sha256-md:<64-hex-chars>` or `sha256-adf:<64-hex-chars>`
4. **Post the digest comment** on the task using the exact marker: `[sdlc-workflow] Description digest: <tagged-digest>` -- this comment MUST be posted BEFORE creating any issue links (Depend, Blocks, Related) or other comments on the task
5. **Only then** proceed to create issue links and other comments

This ensures that `/implement-task` can later verify description integrity by re-fetching the description, computing its digest, and comparing against the stored digest comment.

---

## All Created Tasks Summary

| Task Key | Type | Stream | Role | Labels | Link to TC-8001 |
|----------|------|--------|------|--------|-----------------|
| TC-9001 | Upstream backport | 2.2.x | Standard remediation | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| TC-9002 | Downstream propagation | 2.2.x | Standard remediation | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| TC-9003 | Upstream backport | 2.1.x | Preemptive remediation | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |
| TC-9004 | Downstream propagation | 2.1.x | Preemptive remediation | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |

## Cross-Stream Impact Comment on TC-8001

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x based on lock file analysis.
These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: TC-9003 (upstream backport), TC-9004 (downstream propagation) (security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive label.
When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link them and remove the label.
```
