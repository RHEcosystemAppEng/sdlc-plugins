# Step 8 - Remediation: TC-8001

## Triage Determination

### Scoped stream: 2.2.x

**Case determination**: The 2.2.x stream has affected versions (2.2.0, 2.2.1, 2.2.2), but the fix is already present in 2.2.3+ and the development branch (`release/0.4.z`) already ships quinn-proto 0.11.14. No new remediation task is needed for this stream -- the fix was organically incorporated before CVE triage.

**Actions for 2.2.x**:
- Correct Affects Versions (remove RHTPA 2.0.0; add RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2)
- No remediation tasks created (fix already present in development stream and latest releases)

### Cross-stream: 2.1.x (Case B)

**Case determination**: The 2.1.x stream is outside this issue's scope but is also affected. Both versions (2.1.0, 2.1.1) ship quinn-proto 0.11.9, and the development branch (`release/0.3.z`) does NOT have the fix. No sibling CVE Jira exists for the 2.1.x stream (would be verified via JQL search for `CVE-2026-31812` label with `[rhtpa-2.1]` suffix).

**Actions for 2.1.x**:
1. Post cross-stream impact comment on TC-8001
2. Create preemptive remediation tasks for 2.1.x (upstream backport + downstream propagation)

---

## Cross-Stream Impact Comment

Posted to TC-8001:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on
lock file analysis (both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9).
This stream is not tracked by a companion CVE issue and may require
separate PSIRT triage.
```

---

## Preemptive Remediation Task 1: Upstream Backport (2.1.x)

### Jira Issue Creation

```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)",
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
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (ships quinn-proto 0.11.9), 2.1.1 (ships quinn-proto 0.11.9)
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

### Description Digest Protocol (after task creation)

After creating the upstream backport task, the description digest comment MUST be posted BEFORE creating issue links or any other comments. The steps are:

1. **Re-fetch the description** from Jira (do NOT hash the string passed to `create_issue` -- Jira normalizes content during storage):

   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```

2. **Write the re-fetched description to a temp file**:

   ```
   # Write the description content to /tmp/task-desc.md
   ```

3. **Compute the SHA-256 digest** using the project script:

   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```

   The script auto-detects the format:
   - If the description is returned as ADF JSON (REST API): outputs `sha256-adf:<64-char-hex>`
   - If the description is returned as markdown (MCP): outputs `sha256-md:<64-char-hex>`

4. **Post the digest comment** on the newly created task (BEFORE any links or other comments):

   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py` (e.g., `sha256-md:a1b2c3d4...` -- the full 64-character hex digest with format tag).

5. **Only after the digest comment is posted**, proceed to create issue links and other comments.

### Jira Linkage (after digest comment)

Link with "Related" (not "Depend") because this is a preemptive task for a cross-stream CVE:

```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <upstream-task-key>,
  type: "Related"
)
```

---

## Preemptive Remediation Task 2: Downstream Propagation (2.1.x)

### Jira Issue Creation

```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)",
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
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
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

### Description Digest Protocol (after task creation)

After creating the downstream propagation task, the description digest comment MUST be posted BEFORE creating issue links or any other comments. The steps are:

1. **Re-fetch the description** from Jira (do NOT hash the string passed to `create_issue` -- Jira normalizes content during storage):

   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```

2. **Write the re-fetched description to a temp file**:

   ```
   # Write the description content to /tmp/task-desc.md
   ```

3. **Compute the SHA-256 digest** using the project script:

   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```

   The script auto-detects the format:
   - If the description is returned as ADF JSON (REST API): outputs `sha256-adf:<64-char-hex>`
   - If the description is returned as markdown (MCP): outputs `sha256-md:<64-char-hex>`

4. **Post the digest comment** on the newly created task (BEFORE any links or other comments):

   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py` (e.g., `sha256-md:a1b2c3d4...` -- the full 64-character hex digest with format tag).

5. **Only after the digest comment is posted**, proceed to create issue links and other comments.

### Jira Linkage (after digest comment)

1. Link downstream task to the originating CVE with "Related":

   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <downstream-task-key>,
     type: "Related"
   )
   ```

2. Link downstream task as blocked by the upstream backport task:

   ```
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

---

## Preemptive Tasks Comment on TC-8001

After both tasks are created, linked, and digest comments posted, add a comment to TC-8001:

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <upstream-task-key> (upstream backport, security-preemptive)
- 2.1.x: <downstream-task-key> (downstream propagation, blocked by <upstream-task-key>, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

---

## Sequencing Summary

The complete sequence of Jira operations for each created task is:

### For each task (upstream backport, then downstream propagation):

1. `create_issue` -- create the remediation Task in Jira
2. `get_issue` -- re-fetch the description from the newly created task
3. `scripts/sha256-digest.py` -- compute SHA-256 digest from re-fetched description
4. `add_comment` -- post the digest comment: `[sdlc-workflow] Description digest: <tagged-digest>`
5. `create_link` -- create issue links (Related to TC-8001, and Blocks for downstream)

The digest comment (step 4) MUST occur BEFORE issue links (step 5) or any other comments. This ordering is mandated by the description digest protocol to ensure `/implement-task` can verify description integrity in its Step 1.5.

### Full operation sequence:

```
# --- Upstream Backport Task (2.1.x) ---
1. create_issue(upstream backport task)
2. get_issue(<upstream-task-key>, fields=["description"])
3. python3 scripts/sha256-digest.py /tmp/task-desc.md
4. add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
5. create_link(TC-8001 → <upstream-task-key>, type="Related")

# --- Downstream Propagation Task (2.1.x) ---
6. create_issue(downstream propagation task)
7. get_issue(<downstream-task-key>, fields=["description"])
8. python3 scripts/sha256-digest.py /tmp/task-desc.md
9. add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
10. create_link(TC-8001 → <downstream-task-key>, type="Related")
11. create_link(<upstream-task-key> → <downstream-task-key>, type="Blocks")

# --- Post-task comments ---
12. add_comment(TC-8001, "Preemptive remediation tasks created...")
```

### Key digest protocol rules:
- The digest is computed from the **re-fetched** description, NOT the string passed to `create_issue` (Jira normalizes content during storage)
- The digest comment is a **standalone** comment, not embedded in other comments
- The format tag (`sha256-md:` or `sha256-adf:`) is part of the digest value and must not be stripped
- The hex digest must be the full 64-character SHA-256 output -- never abbreviated
- Never use placeholder, example, or hardcoded hashes
