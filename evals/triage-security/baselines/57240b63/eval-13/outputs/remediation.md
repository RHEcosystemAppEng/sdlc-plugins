# Step 8 -- Remediation: CVE-2026-31812

## Triage Outcome

- **Case A**: Stream 2.2.x (scoped stream) has affected versions 2.2.0, 2.2.1, 2.2.2 -- create remediation tasks
- **Case B**: Stream 2.1.x (cross-stream) is also affected (2.1.0, 2.1.1) -- no sibling CVE Jira exists, create preemptive remediation tasks
- **Ecosystem**: Cargo (source dependency) -- each stream gets 2 tasks (upstream backport + downstream propagation)

Total tasks to create: 4 (2 for Case A + 2 for Case B preemptive)

---

## Case A: Remediation Tasks for Stream 2.2.x

### Task 1: Upstream Backport Task (2.2.x)

**PROPOSAL -- Jira Issue Creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task Description:**

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (DoS).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (quinn-proto 0.11.9), RHTPA 2.2.1 (quinn-proto 0.11.12), RHTPA 2.2.2 (retag of 2.2.1)
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

#### Description Digest Steps for Task 1 (Upstream Backport, 2.2.x)

After `jira.create_issue(...)` returns the new task key (e.g., TC-9001):

1. **Re-fetch the description from Jira** (do NOT hash the description string passed to create_issue -- Jira normalizes content during storage):
   ```
   upstream_desc = jira.get_issue("TC-9001", fields=["description"])
   ```

2. **Write the re-fetched description to a temp file:**
   - If using MCP (returns markdown): write the markdown text to `/tmp/task-desc.md`
   - If using REST API (returns ADF JSON): write the ADF JSON to `/tmp/task-desc.md`

3. **Compute the digest using the script** (do NOT compute SHA-256 manually):
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   - The script auto-detects the input format:
     - ADF JSON input produces: `sha256-adf:<64-char-hex-digest>`
     - Plain text (markdown) input produces: `sha256-md:<64-char-hex-digest>`
   - Check the exit code -- if non-zero, the input was empty and the digest is invalid

4. **Post the digest as a standalone comment** on TC-9001 using ADF contentFormat. This comment MUST be posted BEFORE creating issue links or any other comments:
   ```
   jira.add_comment("TC-9001", {
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
   })
   ```
   Note: Replace `sha256-md:<64-char-hex-digest>` with the actual full output from `scripts/sha256-digest.py`. The tag prefix (`sha256-md:` or `sha256-adf:`) is part of the digest value -- do not strip it. The hex digest is exactly 64 lowercase hexadecimal characters.

5. **Only after the digest comment is posted**, proceed to create issue links and other comments:
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: "TC-9001",
     type: "Depend"
   )
   ```

---

### Task 2: Downstream Propagation Subtask (2.2.x)

**PROPOSAL -- Jira Issue Creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see description below>,
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

#### Description Digest Steps for Task 2 (Downstream Propagation, 2.2.x)

After `jira.create_issue(...)` returns the new task key (e.g., TC-9002):

1. **Re-fetch the description from Jira** (always re-fetch, never hash the input string):
   ```
   downstream_desc = jira.get_issue("TC-9002", fields=["description"])
   ```

2. **Write the re-fetched description to a temp file:**
   - Write the returned description content (markdown or ADF JSON depending on access method) to `/tmp/task-desc.md`

3. **Compute the digest using the script:**
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   - Auto-detects format and outputs the tagged digest (e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`)
   - Verify exit code is 0

4. **Post the digest as a standalone comment** on TC-9002 using ADF contentFormat. This MUST be posted BEFORE creating issue links or other comments:
   ```
   jira.add_comment("TC-9002", {
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
   })
   ```
   Replace the placeholder with the actual full output from `scripts/sha256-digest.py` -- always the full 64-character hex digest with the format tag.

5. **Only after the digest comment is posted**, proceed to create issue links:
   ```
   # Link downstream subtask as blocked by upstream task
   jira.create_link(
     inwardIssue: "TC-9001",
     outwardIssue: "TC-9002",
     type: "Blocks"
   )

   # Link downstream subtask to the Vulnerability issue
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: "TC-9002",
     type: "Depend"
   )
   ```

---

## Case B: Preemptive Remediation Tasks for Stream 2.1.x

Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. No sibling CVE Jira exists for 2.1.x, so preemptive remediation tasks are created.

### Cross-Stream Impact Comment on TC-8001

**PROPOSAL:**
```
jira.add_comment("TC-8001", "Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s)
2.1.x based on lock file analysis. These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

[Comment Footnote]")
```

### Task 3: Preemptive Upstream Backport Task (2.1.x)

**PROPOSAL -- Jira Issue Creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task Description:**

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

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (DoS).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (quinn-proto 0.11.9), RHTPA 2.1.1 (quinn-proto 0.11.9)
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

#### Description Digest Steps for Task 3 (Preemptive Upstream Backport, 2.1.x)

After `jira.create_issue(...)` returns the new task key (e.g., TC-9003):

1. **Re-fetch the description from Jira** (the description must be re-fetched after creation because Jira normalizes content during storage -- never hash the input string passed to create_issue):
   ```
   preemptive_upstream_desc = jira.get_issue("TC-9003", fields=["description"])
   ```

2. **Write the re-fetched description to a temp file:**
   - Write the description content to `/tmp/task-desc.md`
   - The content will be markdown (if MCP) or ADF JSON (if REST API)

3. **Compute the digest using the script** (never compute SHA-256 manually or use example/hardcoded hashes):
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   - Output format: `sha256-md:<64-char-hex>` for markdown input, or `sha256-adf:<64-char-hex>` for ADF JSON input
   - The script exits non-zero if input is empty -- check the exit code

4. **Post the digest as a standalone comment** on TC-9003 using ADF contentFormat. This MUST be posted BEFORE creating issue links or any other comments on the task:
   ```
   jira.add_comment("TC-9003", {
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
   })
   ```
   Replace the placeholder with the actual output from `scripts/sha256-digest.py`. The digest is exactly 64 lowercase hexadecimal characters, prefixed by the format tag.

5. **Only after the digest comment is posted**, create issue links. Preemptive tasks use "Related" link type (not "Depend"):
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: "TC-9003",
     type: "Related"
   )
   ```

---

### Task 4: Preemptive Downstream Propagation Subtask (2.1.x)

**PROPOSAL -- Jira Issue Creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task Description:**

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

#### Description Digest Steps for Task 4 (Preemptive Downstream Propagation, 2.1.x)

After `jira.create_issue(...)` returns the new task key (e.g., TC-9004):

1. **Re-fetch the description from Jira** (always re-fetch after creation, never hash the input):
   ```
   preemptive_downstream_desc = jira.get_issue("TC-9004", fields=["description"])
   ```

2. **Write the re-fetched description to a temp file:**
   - Write the returned description content to `/tmp/task-desc.md`

3. **Compute the digest using the script:**
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   - Outputs: `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>` depending on input format
   - Check exit code is 0 before using the output

4. **Post the digest as a standalone comment** on TC-9004 using ADF contentFormat. This MUST be posted BEFORE creating issue links or any other comments:
   ```
   jira.add_comment("TC-9004", {
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
   })
   ```
   Replace the placeholder with the actual full output from `scripts/sha256-digest.py`.

5. **Only after the digest comment is posted**, create issue links. Both the "Related" link to the originating CVE and the "Blocks" link from the upstream task:
   ```
   # Link preemptive downstream subtask as blocked by preemptive upstream task
   jira.create_link(
     inwardIssue: "TC-9003",
     outwardIssue: "TC-9004",
     type: "Blocks"
   )

   # Link preemptive downstream subtask to originating CVE (Related, not Depend)
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: "TC-9004",
     type: "Related"
   )
   ```

---

## Preemptive Tasks Comment on TC-8001

**PROPOSAL:**
```
jira.add_comment("TC-8001", "Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: TC-9003 (upstream backport, security-preemptive), TC-9004 (downstream propagation, security-preemptive)

These tasks use the \"Related\" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.

[Comment Footnote]")
```

---

## Post-Task-Creation Linkage (Case A, 2.2.x)

After all digest comments are posted for Case A tasks:

```
# Link upstream backport to Vulnerability issue
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: "TC-9001",
  type: "Depend"
)

# Link downstream propagation as blocked by upstream backport
jira.create_link(
  inwardIssue: "TC-9001",
  outwardIssue: "TC-9002",
  type: "Blocks"
)

# Link downstream propagation to Vulnerability issue
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: "TC-9002",
  type: "Depend"
)

# Transition Vulnerability to In Progress
jira.transition_issue("TC-8001", <in-progress-transition-id>)

# Add remediation comment
jira.add_comment("TC-8001", "Remediation tasks created: TC-9001 (upstream backport),
TC-9002 (downstream propagation, blocked by TC-9001)

[Comment Footnote]")
```

---

## Post-Triage Summary

**PROPOSAL:**

1. Add the `ai-cve-triaged` label to TC-8001
2. Post a summary comment on TC-8001:

```
jira.add_comment("TC-8001", "## Triage Summary for CVE-2026-31812

### Version Impact Table

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | |
| 2.1.1 | 0.11.9 | YES | |
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 0.11.14 | NO | ships fixed version |

### Affects Versions Correction

Current: [RHTPA 2.0.0] -> Corrected: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

### Triage Outcome

Remediation tasks created (Case A, stream 2.2.x):
- TC-9001: Upstream backport -- bump quinn-proto to 0.11.14 (release/0.4.z)
- TC-9002: Downstream propagation -- update backend ref in rhtpa-release.0.4.z (blocked by TC-9001)

Preemptive remediation tasks created (Case B, stream 2.1.x):
- TC-9003: Upstream backport -- bump quinn-proto to 0.11.14 (release/0.3.z) [security-preemptive]
- TC-9004: Downstream propagation -- update backend ref in rhtpa-release.0.3.z (blocked by TC-9003) [security-preemptive]

@reporter-mention (ADF mention node with reporter's account ID from TC-8001)

[Comment Footnote: sdlc-workflow/triage-security vX.Y.Z]")
```

---

## Description Digest Protocol -- Summary of Key Rules

The following rules from `shared/description-digest-protocol.md` apply to every remediation task created above:

1. **Always re-fetch** the description from Jira after `create_issue` -- never hash the description string you passed in, because Jira normalizes content during storage
2. **Always use `scripts/sha256-digest.py`** to compute the hash -- never compute SHA-256 manually
3. **The digest comment must be posted BEFORE** creating issue links or other comments on the task
4. **The digest comment is standalone** -- do not embed it in other comments or the plan summary
5. **Use the full tagged output** from the script (e.g., `sha256-md:abcd1234...5678`) -- do not strip the format tag
6. **The hex digest is exactly 64 characters** -- never use abbreviated, placeholder, example, or hardcoded hashes
7. **Post using ADF contentFormat** with a single paragraph containing the marker and digest
8. **The marker string is fixed**: `[sdlc-workflow] Description digest:`
9. **One digest comment per task** -- if the task is re-created, the most recent digest comment wins (consumer selects by `created` timestamp)

### Execution Order Per Task

```
1. jira.create_issue(...)                           -> returns task key
2. jira.get_issue(<task-key>, fields=["description"]) -> re-fetch description
3. Write description to /tmp/task-desc.md
4. python3 scripts/sha256-digest.py /tmp/task-desc.md -> tagged digest output
5. jira.add_comment(<task-key>, digest comment)       -> standalone digest comment
6. jira.create_link(...)                              -> issue links (AFTER digest)
7. jira.add_comment(<parent>, remediation comment)    -> other comments (AFTER digest)
```

This order is critical: the digest comment must be the first comment on the task to ensure `/implement-task` can locate and verify description integrity in its Step 1.5.
