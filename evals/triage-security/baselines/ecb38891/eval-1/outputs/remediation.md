# Remediation — TC-8001 (CVE-2026-31812)

## Step 8 — Remediation Task Creation

### Triage Outcome: Case B (Affected) + Case A (Cross-stream impact)

The version impact analysis shows:
- **2.2.x stream (in scope):** Versions 2.2.0, 2.2.1, 2.2.2 are affected
- **2.1.x stream (out of scope):** Versions 2.1.0, 2.1.1 are also affected

Since the issue is scoped to 2.2.x, remediation tasks are created for the
2.2.x stream only. Cross-stream impact for the 2.1.x stream is reported
via a comment (Case A).

The ecosystem is **Cargo** (source dependency), so **two tasks** are created
for the 2.2.x stream: an upstream backport task and a downstream propagation
subtask with a Blocks dependency between them.

---

## Task 1: Upstream Backport Task

**Proposed Jira creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto - Panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
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

### Description Digest Protocol (Task 1)

After creating the upstream backport task, the following digest steps are performed
before creating any issue links or other comments:

1. **Re-fetch the task description from Jira** (the description as stored by Jira,
   not the string passed to `create_issue`, since Jira normalizes content during storage):

   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```

2. **Write the description to a temp file and compute the SHA-256 digest:**

   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```

   The script auto-detects the format (ADF JSON or markdown) and outputs a
   format-tagged digest (e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`).

3. **Post the digest comment** with the marker `[sdlc-workflow] Description digest:`:

   ```
   jira.add_comment(<upstream-task-key>,
     "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

   This digest comment is posted BEFORE creating the Depend link to TC-8001
   or any other comments on the task.

---

## Task 2: Downstream Propagation Subtask

**Proposed Jira creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps quinn-proto to 0.11.14
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

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Description Digest Protocol (Task 2)

After creating the downstream propagation subtask, the following digest steps are
performed before creating any issue links or other comments:

1. **Re-fetch the task description from Jira:**

   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```

2. **Compute the SHA-256 digest:**

   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```

3. **Post the digest comment:**

   ```
   jira.add_comment(<downstream-task-key>,
     "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

   This digest comment is posted BEFORE creating the Blocks link from the
   upstream task or the Depend link to TC-8001 or any other comments.

---

## Proposed Jira Linkage

After creating both tasks and posting their digest comments:

1. **Link upstream task to TC-8001** (Depend):

   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <upstream-task-key>,
     type: "Depend"
   )
   ```

2. **Link downstream task to TC-8001** (Depend):

   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )
   ```

3. **Link downstream blocked by upstream** (Blocks):

   ```
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

4. **Propose transitioning TC-8001 to In Progress** (if not already).

5. **Propose adding the `ai-cve-triaged` label** to TC-8001.

---

## Case A: Cross-Stream Impact Comment

The issue is scoped to 2.2.x, but the version impact analysis shows that
stream 2.1.x is also affected (versions 2.1.0 and 2.1.1 ship quinn-proto
0.11.9, which is within the affected range < 0.11.14).

**Proposed cross-stream impact comment** on TC-8001:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s)
2.1.x based on lock file analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

---
This comment was AI-generated by sdlc-workflow/triage-security v0.13.7.
```

---

## Post-Triage Summary

**Proposed summary comment** on TC-8001:

```
## Triage Summary for CVE-2026-31812

### Version Impact

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | |
| 2.2.4 | 2.2.x | 0.11.14 | NO | |

### Affects Versions Correction

Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

### Triage Outcome

Remediation tasks created (Cargo, source dependency -- 2 tasks):
- <upstream-task-key> — upstream backport: bump quinn-proto to 0.11.14 (release/0.4.z)
- <downstream-task-key> — downstream propagation: update backend ref in rhtpa-release.0.4.z (blocked by <upstream-task-key>)

Cross-stream impact: 2.1.x stream also affected (2.1.0, 2.1.1).

@<reporter-name> (ADF mention node with reporter account ID from Jira issue)

---
This comment was AI-generated by sdlc-workflow/triage-security v0.13.7.
```

The @mention of the vulnerability reporter uses an ADF mention node:

```json
{ "type": "mention", "attrs": { "id": "<reporter-account-id>", "text": "@<reporter-name>" } }
```

The reporter account ID is extracted from the Jira issue's `reporter` field
(always available on the issue, no configuration needed).
