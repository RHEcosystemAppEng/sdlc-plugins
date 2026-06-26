# Step 7 - Remediation: CVE-2026-31812

## Triage Outcome

The issue TC-8001 is scoped to stream 2.2.x. Within that stream, versions 2.2.0, 2.2.1, and 2.2.2 are affected (quinn-proto < 0.11.14). Versions 2.2.3 and 2.2.4 already ship the fixed version.

Additionally, stream 2.1.x (all versions: 2.1.0, 2.1.1) is affected but outside scope (Case B - cross-stream impact).

Ecosystem: **Cargo** (source dependency) -- requires **two tasks** per affected stream:
1. Upstream backport task (fix in source repo rhtpa-backend)
2. Downstream propagation subtask (update reference in Konflux release repo)

---

## Case A: Remediation Tasks for Stream 2.2.x (In Scope)

### Task 1: Upstream Backport Task (2.2.x)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task description:**

```markdown
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0 (v0.4.5), 2.2.1 (v0.4.8), 2.2.2 (v0.4.9, retag of 2.2.1)
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

#### Description Digest Comment Procedure (Task 1)

After creating the upstream backport task (assume created as TC-9001):

1. **Re-fetch the task description from Jira:**
   ```
   upstream_desc = jira.get_issue("TC-9001", fields=["description"])
   ```

2. **Write the re-fetched description to a temp file:**
   ```
   Write the description content to /tmp/task-desc.md
   ```

3. **Compute the SHA-256 digest using the script:**
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This outputs a format-tagged digest, e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>` depending on the format returned by Jira.

4. **Post the digest comment on TC-9001 BEFORE creating any links or other comments:**
   ```
   jira.add_comment("TC-9001", "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py` (e.g., `sha256-md:a1b2c3d4...64chars`).

5. **Only after the digest comment is posted**, proceed to create issue links (Depend link to TC-8001) and other comments.

---

### Task 2: Downstream Propagation Subtask (2.2.x)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task description:**

```markdown
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

#### Description Digest Comment Procedure (Task 2)

After creating the downstream propagation task (assume created as TC-9002):

1. **Re-fetch the task description from Jira:**
   ```
   downstream_desc = jira.get_issue("TC-9002", fields=["description"])
   ```

2. **Write the re-fetched description to a temp file:**
   ```
   Write the description content to /tmp/task-desc.md
   ```

3. **Compute the SHA-256 digest using the script:**
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This outputs a format-tagged digest, e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`.

4. **Post the digest comment on TC-9002 BEFORE creating any links or other comments:**
   ```
   jira.add_comment("TC-9002", "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py`.

5. **Only after the digest comment is posted**, proceed to create issue links:
   - Depend link: TC-8001 (inward) -> TC-9002 (outward), type "Depend"
   - Blocks link: TC-9001 (inward) -> TC-9002 (outward), type "Blocks"

---

## Jira Linkage for Stream 2.2.x Tasks

After all digest comments are posted, create the following links:

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

# Link downstream task as blocked by upstream task
jira.create_link(
  inwardIssue: "TC-9001",
  outwardIssue: "TC-9002",
  type: "Blocks"
)
```

---

## Case B: Cross-Stream Impact - Preemptive Remediation for Stream 2.1.x

Stream 2.1.x is affected (all versions ship quinn-proto 0.11.9) but has no stream-specific CVE Jira for this CVE. Preemptive remediation tasks are created with the `security-preemptive` label and "Related" link type.

### Task 3: Preemptive Upstream Backport Task (2.1.x)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task description:**

```markdown
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

Affected versions: 2.1.0 (v0.3.8), 2.1.1 (v0.3.12)
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

#### Description Digest Comment Procedure (Task 3)

After creating the preemptive upstream backport task (assume created as TC-9003):

1. **Re-fetch the task description from Jira:**
   ```
   preemptive_upstream_desc = jira.get_issue("TC-9003", fields=["description"])
   ```

2. **Write the re-fetched description to a temp file:**
   ```
   Write the description content to /tmp/task-desc.md
   ```

3. **Compute the SHA-256 digest using the script:**
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```

4. **Post the digest comment on TC-9003 BEFORE creating any links or other comments:**
   ```
   jira.add_comment("TC-9003", "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

5. **Only after the digest comment is posted**, proceed to create the "Related" link to TC-8001.

---

### Task 4: Preemptive Downstream Propagation Subtask (2.1.x)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task description:**

```markdown
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

#### Description Digest Comment Procedure (Task 4)

After creating the preemptive downstream propagation task (assume created as TC-9004):

1. **Re-fetch the task description from Jira:**
   ```
   preemptive_downstream_desc = jira.get_issue("TC-9004", fields=["description"])
   ```

2. **Write the re-fetched description to a temp file:**
   ```
   Write the description content to /tmp/task-desc.md
   ```

3. **Compute the SHA-256 digest using the script:**
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```

4. **Post the digest comment on TC-9004 BEFORE creating any links or other comments:**
   ```
   jira.add_comment("TC-9004", "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

5. **Only after the digest comment is posted**, proceed to create links:
   - Related link: TC-8001 (inward) -> TC-9004 (outward), type "Related"
   - Blocks link: TC-9003 (inward) -> TC-9004 (outward), type "Blocks"

---

## Jira Linkage for Stream 2.1.x Preemptive Tasks

After all digest comments are posted for preemptive tasks, create the following links:

```
# Link preemptive upstream task to originating CVE Jira (Related, not Depend)
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: "TC-9003",
  type: "Related"
)

# Link preemptive downstream task to originating CVE Jira (Related, not Depend)
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: "TC-9004",
  type: "Related"
)

# Link preemptive downstream task as blocked by preemptive upstream task
jira.create_link(
  inwardIssue: "TC-9003",
  outwardIssue: "TC-9004",
  type: "Blocks"
)
```

---

## Cross-Stream Impact Comment

Post the following comment to TC-8001:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis.
Stream 2.1.x ships quinn-proto 0.11.9 in all versions (2.1.0, 2.1.1).
This stream is tracked by preemptive remediation tasks (see below).

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: TC-9003 (upstream backport, security-preemptive), TC-9004 (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

---

## Description Digest Protocol Summary

The description digest protocol ensures integrity between task creation and implementation. For every remediation task created:

1. **Create the task** via `jira.create_issue()`
2. **Re-fetch** the created task's description from Jira (do NOT hash the description string passed to `create_issue` -- Jira normalizes content during storage)
3. **Compute digest** using `python3 scripts/sha256-digest.py /tmp/task-desc.md` which auto-detects format and outputs `sha256-md:<hex>` or `sha256-adf:<hex>`
4. **Post digest comment** with marker `[sdlc-workflow] Description digest: <tagged-digest>` as a standalone comment
5. **Only then** create issue links (Depend, Blocks, Related) or other comments

This ordering is critical: digest comments MUST be posted BEFORE creating issue links or other comments on each task. This ensures `/implement-task` can verify description integrity in its Step 1.5.

### Order of Operations (Complete)

1. Create TC-9001 (upstream backport, 2.2.x)
2. Re-fetch TC-9001 description, compute digest, post digest comment on TC-9001
3. Create TC-9002 (downstream propagation, 2.2.x)
4. Re-fetch TC-9002 description, compute digest, post digest comment on TC-9002
5. Create TC-9003 (preemptive upstream backport, 2.1.x)
6. Re-fetch TC-9003 description, compute digest, post digest comment on TC-9003
7. Create TC-9004 (preemptive downstream propagation, 2.1.x)
8. Re-fetch TC-9004 description, compute digest, post digest comment on TC-9004
9. Create all Depend links (TC-8001 -> TC-9001, TC-8001 -> TC-9002)
10. Create Blocks link (TC-9001 -> TC-9002)
11. Create all Related links (TC-8001 -> TC-9003, TC-8001 -> TC-9004)
12. Create Blocks link (TC-9003 -> TC-9004)
13. Transition TC-8001 to In Progress
14. Assign TC-8001 to current user
15. Add ai-cve-triaged label to TC-8001
16. Post remediation summary comment on TC-8001 (including cross-stream impact notice)
