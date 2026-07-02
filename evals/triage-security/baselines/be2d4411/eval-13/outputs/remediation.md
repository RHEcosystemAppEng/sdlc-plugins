# Step 8 -- Remediation: CVE-2026-31812

## Triage Outcome

- **Issue scope**: 2.2.x stream (per `[rhtpa-2.2]` suffix)
- **Affected versions in scope**: 2.2.0, 2.2.1, 2.2.2
- **Ecosystem**: Cargo (source dependency) -- requires 2 tasks per stream (upstream backport + downstream propagation)
- **Cross-stream impact**: Stream 2.1.x is also affected (Case B -- preemptive remediation)

---

## Case A: Remediation Tasks for Stream 2.2.x (Scoped Stream)

### Task 1: Upstream Backport Task (2.2.x)

**Jira Creation Call:**

```
upstream_task_22 = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)",
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

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0, 2.2.1, 2.2.2
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

#### Description Digest Protocol for Upstream Backport Task (2.2.x)

After creating the upstream backport task, perform the following steps **before** creating any issue links or posting other comments:

1. **Re-fetch the task description from Jira** (do NOT hash the string passed to `create_issue` -- Jira normalizes content during storage):
   ```
   upstream_desc = jira.get_issue(<upstream-task-22-key>, fields=["description"])
   ```

2. **Write the re-fetched description to a temp file and compute the SHA-256 digest**:
   ```
   # Write description to /tmp/task-desc.md
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<64-char-hex> or sha256-adf:<64-char-hex>
   # (format tag depends on whether the API returned markdown or ADF)
   ```

3. **Post the digest comment** on the upstream backport task:
   ```
   jira.add_comment(<upstream-task-22-key>,
     "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py` (e.g., `sha256-md:a1b2c3...64chars`).

This digest comment is posted as a standalone comment, separate from any other comments. It uses ADF `contentFormat` with a single paragraph containing the marker and digest.

---

### Task 2: Downstream Propagation Subtask (2.2.x)

**Jira Creation Call:**

```
downstream_task_22 = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)",
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
CVE-2026-31812 fix from <upstream-task-22-key>.

The upstream backport (<upstream-task-22-key>) bumps quinn-proto to 0.11.14
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

- Depends on: <upstream-task-22-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Protocol for Downstream Propagation Subtask (2.2.x)

After creating the downstream propagation subtask, perform the following steps **before** creating any issue links or posting other comments:

1. **Re-fetch the task description from Jira**:
   ```
   downstream_desc = jira.get_issue(<downstream-task-22-key>, fields=["description"])
   ```

2. **Write the re-fetched description to a temp file and compute the SHA-256 digest**:
   ```
   # Write description to /tmp/task-desc.md
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<64-char-hex> or sha256-adf:<64-char-hex>
   ```

3. **Post the digest comment** on the downstream propagation subtask:
   ```
   jira.add_comment(<downstream-task-22-key>,
     "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

This digest comment is posted as a standalone comment before any links or other comments.

---

### Linkage for 2.2.x Tasks (After All Digest Comments)

Only after all digest comments are posted, create the issue links:

```
# Link upstream task to vulnerability issue
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <upstream-task-22-key>,
  type: "Depend"
)

# Link downstream task to vulnerability issue
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <downstream-task-22-key>,
  type: "Depend"
)

# Link downstream as blocked by upstream
jira.create_link(
  inwardIssue: <upstream-task-22-key>,
  outwardIssue: <downstream-task-22-key>,
  type: "Blocks"
)
```

---

## Case B: Preemptive Remediation Tasks for Stream 2.1.x (Cross-Stream Impact)

Stream 2.1.x is affected (all versions ship quinn-proto 0.11.9 < 0.11.14) but has no stream-specific CVE Jira (no sibling issue with suffix `[rhtpa-2.1]` found). Preemptive remediation tasks are created with the `security-preemptive` label and "Related" link type.

### Task 3: Preemptive Upstream Backport Task (2.1.x)

**Jira Creation Call:**

```
upstream_task_21 = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)",
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

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0, 2.1.1
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

- Depends on: TC-8001 (originating CVE tracking issue, cross-stream)
```

#### Description Digest Protocol for Preemptive Upstream Backport Task (2.1.x)

After creating the preemptive upstream backport task, perform the following steps **before** creating any issue links or posting other comments:

1. **Re-fetch the task description from Jira**:
   ```
   upstream_desc_21 = jira.get_issue(<upstream-task-21-key>, fields=["description"])
   ```

2. **Write the re-fetched description to a temp file and compute the SHA-256 digest**:
   ```
   # Write description to /tmp/task-desc.md
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<64-char-hex> or sha256-adf:<64-char-hex>
   ```

3. **Post the digest comment** on the preemptive upstream backport task:
   ```
   jira.add_comment(<upstream-task-21-key>,
     "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

This digest comment is posted as a standalone comment before any links or other comments.

---

### Task 4: Preemptive Downstream Propagation Subtask (2.1.x)

**Jira Creation Call:**

```
downstream_task_21 = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)",
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
CVE-2026-31812 fix from <upstream-task-21-key>.

The upstream backport (<upstream-task-21-key>) bumps quinn-proto to 0.11.14
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

- Depends on: <upstream-task-21-key> (upstream backport must merge first)
- Depends on: TC-8001 (originating CVE tracking issue, cross-stream)
```

#### Description Digest Protocol for Preemptive Downstream Propagation Subtask (2.1.x)

After creating the preemptive downstream propagation subtask, perform the following steps **before** creating any issue links or posting other comments:

1. **Re-fetch the task description from Jira**:
   ```
   downstream_desc_21 = jira.get_issue(<downstream-task-21-key>, fields=["description"])
   ```

2. **Write the re-fetched description to a temp file and compute the SHA-256 digest**:
   ```
   # Write description to /tmp/task-desc.md
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<64-char-hex> or sha256-adf:<64-char-hex>
   ```

3. **Post the digest comment** on the preemptive downstream propagation subtask:
   ```
   jira.add_comment(<downstream-task-21-key>,
     "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

This digest comment is posted as a standalone comment before any links or other comments.

---

### Linkage for 2.1.x Preemptive Tasks (After All Digest Comments)

Only after all digest comments are posted, create the issue links. Preemptive tasks use "Related" link type (not "Depend") to the originating CVE Jira:

```
# Link preemptive upstream task to originating CVE with "Related"
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <upstream-task-21-key>,
  type: "Related"
)

# Link preemptive downstream task to originating CVE with "Related"
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <downstream-task-21-key>,
  type: "Related"
)

# Link downstream as blocked by upstream
jira.create_link(
  inwardIssue: <upstream-task-21-key>,
  outwardIssue: <downstream-task-21-key>,
  type: "Blocks"
)
```

---

## Post-Triage Comment on TC-8001

After all tasks are created, linked, and digest comments posted:

1. **Add `ai-cve-triaged` label** to TC-8001.

2. **Post a summary comment** to TC-8001 documenting:
   - The version impact table
   - Affects Versions correction: RHTPA 2.0.0 -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
   - Remediation tasks created for 2.2.x: <upstream-task-22-key> (upstream backport), <downstream-task-22-key> (downstream propagation, blocked by <upstream-task-22-key>)
   - Preemptive tasks created for 2.1.x: <upstream-task-21-key> (upstream backport, security-preemptive), <downstream-task-21-key> (downstream propagation, security-preemptive)
   - @mention of the vulnerability issue reporter (using ADF mention node with the reporter's account ID from the Jira issue)

3. **Post a preemptive task summary comment** on TC-8001:
   ```
   Preemptive remediation tasks created for streams without CVE Jiras:
   - 2.1.x: <upstream-task-21-key> (security-preemptive)
   - 2.1.x: <downstream-task-21-key> (security-preemptive)

   These tasks use the "Related" link type and carry the security-preemptive
   label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
   reconciliation will link them and remove the label.
   ```

All comments MUST include the Comment Footnote:

```
---
This comment was AI-generated by sdlc-workflow/triage-security v0.11.1.
```

(Rendered in ADF with a rule node followed by a paragraph containing the linked plugin name and version.)

---

## Complete Sequencing Summary

The full sequence of Jira operations, in order:

1. Create upstream backport task (2.2.x)
2. Re-fetch description, compute digest, post digest comment on upstream task (2.2.x)
3. Create downstream propagation subtask (2.2.x)
4. Re-fetch description, compute digest, post digest comment on downstream task (2.2.x)
5. Create Depend link: TC-8001 -> upstream task (2.2.x)
6. Create Depend link: TC-8001 -> downstream task (2.2.x)
7. Create Blocks link: upstream task -> downstream task (2.2.x)
8. Create preemptive upstream backport task (2.1.x)
9. Re-fetch description, compute digest, post digest comment on preemptive upstream task (2.1.x)
10. Create preemptive downstream propagation subtask (2.1.x)
11. Re-fetch description, compute digest, post digest comment on preemptive downstream task (2.1.x)
12. Create Related link: TC-8001 -> preemptive upstream task (2.1.x)
13. Create Related link: TC-8001 -> preemptive downstream task (2.1.x)
14. Create Blocks link: preemptive upstream task -> preemptive downstream task (2.1.x)
15. Post cross-stream impact comment on TC-8001
16. Post preemptive task summary comment on TC-8001
17. Add `ai-cve-triaged` label to TC-8001
18. Post post-triage summary comment on TC-8001 (with @mention of reporter)
