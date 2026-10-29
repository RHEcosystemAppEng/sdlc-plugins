# Step 8 -- Remediation Plan for TC-8001 (CVE-2026-31812)

## Triage Decision Tree

1. **Any supported versions affected?** YES -- versions 2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2 are affected.
2. **Issue scoped to a single stream?** YES -- scoped to 2.2.x (from `[rhtpa-2.2]` suffix).
3. **Other streams also affected?** YES -- stream 2.1.x is also affected.
4. **Result**: Case A (cross-stream impact) followed by Case B (create remediation tasks).

## Case A: Cross-Stream Impact

### PROPOSAL: Post cross-stream impact comment on TC-8001

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis (2.1.0 ships 0.11.9, 2.1.1 ships 0.11.9).
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

### PROPOSAL: Create preemptive remediation tasks for stream 2.1.x

Since no sibling CVE Jira exists for stream 2.1.x (no `[rhtpa-2.1]` scoped issue found), create preemptive tasks with the `security-preemptive` label and "Related" link type to TC-8001.

The upstream fix is NOT available on `release/0.3.z` (still ships 0.11.9), so the upstream backport + downstream propagation pattern is used.

---

## Case B: Remediation Tasks for Stream 2.2.x (In-Scope)

The upstream fix IS available on `release/0.4.z` (ships 0.11.14 at v0.4.12), so the **dependency bump** variant is used.

### Task 1: Dependency Bump Task (2.2.x)

**PROPOSAL: Create Jira Task**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

#### Task Description

```markdown
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream --
a package manager update is sufficient.

Affected versions: 2.2.0 (0.11.9), 2.2.1 (0.11.12), 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
- **Remediation action**: run the appropriate package manager update command:
  - **Cargo**: `cargo update -p quinn-proto` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Comment Steps (Task 1)

After creating the dependency bump task, perform the following description digest steps **before** creating any issue links or other comments:

1. **Re-fetch the created task's description from Jira:**
   ```
   task_desc = jira.get_issue(<bump-task-key>, fields=["description"])
   ```

2. **Write the description to a temporary file:**
   ```
   Write the description content to /tmp/task-desc.md
   ```

3. **Compute the digest using the script:**
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The script auto-detects the format (ADF JSON or markdown) and outputs a tagged digest, e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`.

4. **Post the digest comment on the created task:**
   ```
   jira.add_comment(<bump-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from the script (e.g., `sha256-md:a1b2c3...64 hex chars`).

   The comment is posted using ADF contentFormat:
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

5. **Only after the digest comment is posted**, proceed to create issue links (Depend link to TC-8001, Blocks link from this task to the downstream propagation task, etc.).

---

### Task 2: Downstream Propagation Task (2.2.x)

**PROPOSAL: Create Jira Task**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

#### Task Description

```markdown
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <bump-task-key>.

The dependency bump (<bump-task-key>) bumps quinn-proto to 0.11.14
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

- Depends on: <bump-task-key> (dependency bump must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Comment Steps (Task 2)

After creating the downstream propagation task, perform the following steps **before** creating any issue links or other comments:

1. **Re-fetch the created task's description from Jira:**
   ```
   task_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```

2. **Write the description to a temporary file:**
   ```
   Write the description content to /tmp/task-desc.md
   ```

3. **Compute the digest using the script:**
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```

4. **Post the digest comment on the created task:**
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

   The comment is posted as a standalone ADF comment:
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

5. **Only after the digest comment is posted**, proceed to create issue links:
   - Link downstream task to TC-8001 (Depend): `jira.create_link(inwardIssue: TC-8001, outwardIssue: <downstream-task-key>, type: "Depend")`
   - Link downstream task as blocked by bump task (Blocks): `jira.create_link(inwardIssue: <bump-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")`

---

## Jira Linkage for Stream 2.2.x Tasks

After all digest comments are posted:

1. **Depend link** -- bump task to CVE:
   ```
   jira.create_link(inwardIssue: TC-8001, outwardIssue: <bump-task-key>, type: "Depend")
   ```

2. **Depend link** -- downstream task to CVE:
   ```
   jira.create_link(inwardIssue: TC-8001, outwardIssue: <downstream-task-key>, type: "Depend")
   ```

3. **Blocks link** -- downstream blocked by bump task:
   ```
   jira.create_link(inwardIssue: <bump-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
   ```

4. **Release Jira links** (if Step 7.5 produced a release Task for 2.2.x):
   - Blocks: `jira.create_link(inwardIssue: <bump-task-key>, outwardIssue: <release-task-key>, type: "Blocks")`
   - Blocks: `jira.create_link(inwardIssue: <downstream-task-key>, outwardIssue: <release-task-key>, type: "Blocks")`
   - Related: `jira.create_link(inwardIssue: <release-task-key>, outwardIssue: TC-8001, type: "Related")`

---

## Case A Preemptive Tasks: Stream 2.1.x

Since stream 2.1.x is affected and has no sibling CVE Jira, preemptive tasks are created. The upstream fix is NOT available on `release/0.3.z`, so the upstream backport + downstream propagation pattern is used.

### Preemptive Task 3: Upstream Backport (2.1.x)

**PROPOSAL: Create Jira Task**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

#### Task Description

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

Affected versions: 2.1.0 (0.11.9), 2.1.1 (0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (originating tracking issue -- cross-stream)
```

#### Description Digest Comment Steps (Preemptive Task 3)

After creating the preemptive upstream backport task, perform the following steps **before** creating any issue links:

1. **Re-fetch the created task's description from Jira:**
   ```
   task_desc = jira.get_issue(<preemptive-upstream-task-key>, fields=["description"])
   ```

2. **Write the description to a temporary file:**
   ```
   Write the description content to /tmp/task-desc.md
   ```

3. **Compute the digest using the script:**
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```

4. **Post the digest comment on the created task:**
   ```
   jira.add_comment(<preemptive-upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

   Posted as standalone ADF comment:
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

5. **Only after the digest comment is posted**, create the "Related" link:
   ```
   jira.create_link(inwardIssue: TC-8001, outwardIssue: <preemptive-upstream-task-key>, type: "Related")
   ```

---

### Preemptive Task 4: Downstream Propagation (2.1.x)

**PROPOSAL: Create Jira Task**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

#### Task Description

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
CVE-2026-31812 fix from <preemptive-upstream-task-key>.

The upstream backport (<preemptive-upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
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

- Depends on: <preemptive-upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (originating tracking issue -- cross-stream)
```

#### Description Digest Comment Steps (Preemptive Task 4)

After creating the preemptive downstream propagation task, perform the following steps **before** creating any issue links:

1. **Re-fetch the created task's description from Jira:**
   ```
   task_desc = jira.get_issue(<preemptive-downstream-task-key>, fields=["description"])
   ```

2. **Write the description to a temporary file:**
   ```
   Write the description content to /tmp/task-desc.md
   ```

3. **Compute the digest using the script:**
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```

4. **Post the digest comment on the created task:**
   ```
   jira.add_comment(<preemptive-downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

   Posted as standalone ADF comment:
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

5. **Only after the digest comment is posted**, create the links:
   - Related link to TC-8001: `jira.create_link(inwardIssue: TC-8001, outwardIssue: <preemptive-downstream-task-key>, type: "Related")`
   - Blocks link (upstream blocks downstream): `jira.create_link(inwardIssue: <preemptive-upstream-task-key>, outwardIssue: <preemptive-downstream-task-key>, type: "Blocks")`

---

## Preemptive Tasks Comment on TC-8001

### PROPOSAL: Post comment on TC-8001

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <preemptive-upstream-task-key> (upstream backport, security-preemptive),
         <preemptive-downstream-task-key> (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

---

## Post-Triage Summary

### PROPOSAL: Add `ai-cve-triaged` label to TC-8001

```
jira.edit_issue(TC-8001, labels: add "ai-cve-triaged")
```

### PROPOSAL: Post summary comment on TC-8001

The summary comment would include:

1. **Version impact table** (from Step 2)
2. **Affects Versions correction**: removed RHTPA 2.0.0, added RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
3. **Triage outcome**: remediation tasks created for 2.2.x (in-scope) and preemptive tasks for 2.1.x (cross-stream)
4. **Remediation tasks created**:
   - 2.2.x: <bump-task-key> (dependency bump), <downstream-task-key> (downstream propagation, blocked by bump task)
   - 2.1.x (preemptive): <preemptive-upstream-task-key> (upstream backport), <preemptive-downstream-task-key> (downstream propagation)
5. **Release Jira references** (if created in Step 7.5)
6. **Reporter @mention**: ADF mention node for the issue reporter
7. **Comment Footnote**: per shared/comment-footnote.md with skill name `triage-security`

---

## Description Digest Protocol Summary

The description digest protocol is applied identically to all four remediation tasks. The key rules are:

1. **Timing**: The digest comment MUST be posted immediately after task creation, BEFORE creating any issue links or other comments on the task.
2. **Re-fetch required**: The digest is computed from the description as stored by Jira (re-fetched via API), NOT from the description string passed to `create_issue`, because Jira normalizes content during storage.
3. **Tool-based computation**: Always use `python3 scripts/sha256-digest.py` to compute the digest. The script auto-detects the input format and outputs a format-tagged digest (`sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`).
4. **Standalone comment**: The digest comment is a separate, independent comment -- never appended to other comments.
5. **Format tag preserved**: The full tagged output from the script is posted as-is. The tag tells consumers which description format was hashed.
6. **No placeholders**: The digest must be the actual 64-character hex hash computed from the real description content.
7. **Comment format**: ADF `contentFormat` with a single paragraph containing the marker and digest.

### Order of operations per task:
1. Create the Jira Task (`jira.create_issue`)
2. Re-fetch the task description (`jira.get_issue`)
3. Write description to temp file
4. Compute digest (`python3 scripts/sha256-digest.py /tmp/task-desc.md`)
5. Post digest comment (`jira.add_comment` with marker `[sdlc-workflow] Description digest: <tagged-digest>`)
6. Create issue links (`jira.create_link`)
7. Create any other comments

This sequence is repeated for each of the four remediation tasks before proceeding to the post-triage summary.
