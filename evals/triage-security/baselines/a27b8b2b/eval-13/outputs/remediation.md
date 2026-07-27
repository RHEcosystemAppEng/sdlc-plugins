# Step 8 -- Remediation

## Triage Outcome: Case B (Affected) + Case A (Cross-Stream Impact)

The version impact table shows that versions 2.2.0, 2.2.1, and 2.2.2 in the scoped 2.2.x stream are affected. Since quinn-proto is a Cargo ecosystem (source dependency), two remediation tasks are created per the ecosystem classification table: an upstream backport task and a downstream propagation subtask.

Additionally, Case A applies because stream 2.1.x is also affected but outside the scope of this issue.

---

## Task 1: Upstream Backport Task (2.2.x stream)

### Proposed Jira creation

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

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8 (2.2.2 is retag of 2.2.1)

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

### Description Digest Protocol (Task 1 -- Upstream Backport)

After `create_issue` returns the upstream task key (e.g., TC-XXXX), perform the following steps **before creating any issue links or other comments**:

1. **Re-fetch the task description from Jira** (do NOT use the description string passed to `create_issue` -- Jira normalizes content during storage, so the stored description may differ from the input):

   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```

2. **Write the re-fetched description to a temporary file and compute the SHA-256 digest** using the `scripts/sha256-digest.py` script. The script auto-detects the input format (ADF JSON or markdown) and produces a format-tagged digest:

   ```bash
   # Write re-fetched description to temp file
   echo "<re-fetched-description>" > /tmp/task-desc.md
   
   # Compute digest
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<64-char-hex> or sha256-adf:<64-char-hex>
   ```

3. **Post the digest comment** on the upstream task. The comment uses the exact marker prefix `[sdlc-workflow] Description digest:` followed by the tagged digest:

   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py` (e.g., `sha256-md:a1b2c3...64-chars...`). The format tag is part of the digest value and must not be stripped.

4. **Only after the digest comment is posted**, proceed to create issue links and other comments:

   ```
   # NOW create the Depend link to the Vulnerability issue
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <upstream-task-key>,
     type: "Depend"
   )
   ```

**Why re-fetch?** The Jira API normalizes content during storage (e.g., markdown-to-ADF conversion, whitespace normalization). Hashing the input string would produce a different digest than what `implement-task` computes when it re-fetches the description later for verification. The digest must be computed from the stored representation, not the input.

---

## Task 2: Downstream Propagation Subtask (2.2.x stream)

### Proposed Jira creation

```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <downstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

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

### Description Digest Protocol (Task 2 -- Downstream Propagation)

After `create_issue` returns the downstream task key (e.g., TC-YYYY), perform the following steps **before creating any issue links or other comments**:

1. **Re-fetch the task description from Jira** (do NOT use the description string passed to `create_issue` -- Jira normalizes content during storage):

   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```

2. **Write the re-fetched description to a temporary file and compute the SHA-256 digest** using `scripts/sha256-digest.py`:

   ```bash
   # Write re-fetched description to temp file
   echo "<re-fetched-description>" > /tmp/task-desc.md
   
   # Compute digest
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<64-char-hex> or sha256-adf:<64-char-hex>
   ```

3. **Post the digest comment** on the downstream task with the exact marker prefix:

   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py` (e.g., `sha256-adf:e4f5a6...64-chars...`).

4. **Only after the digest comment is posted**, proceed to create issue links and other comments:

   ```
   # NOW create the Depend link to the Vulnerability issue
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )
   
   # NOW create the Blocks link (downstream blocked by upstream)
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

**Why re-fetch?** Same reason as the upstream task -- the digest must be computed from the re-fetched description (the version Jira actually stored), not from the description string originally passed to `create_issue`. Jira normalizes content during storage, so the stored description may differ. The `scripts/sha256-digest.py` script auto-detects whether the re-fetched description is ADF JSON (from REST API) or markdown (from MCP) and produces the appropriately tagged digest (`sha256-adf:` or `sha256-md:`).

---

## Complete Procedure Sequence (Both Tasks)

The full ordered procedure for creating both remediation tasks, including digest comments, is:

### Phase 1: Create Upstream Backport Task

1. `jira.create_issue(...)` -- create the upstream task
2. `jira.get_issue(<upstream-task-key>, fields=["description"])` -- re-fetch description from Jira
3. `python3 scripts/sha256-digest.py /tmp/task-desc.md` -- compute SHA-256 digest from re-fetched description
4. `jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")` -- post digest comment
5. `jira.create_link(inwardIssue: "TC-8001", outwardIssue: <upstream-task-key>, type: "Depend")` -- link to CVE issue

### Phase 2: Create Downstream Propagation Subtask

6. `jira.create_issue(...)` -- create the downstream task
7. `jira.get_issue(<downstream-task-key>, fields=["description"])` -- re-fetch description from Jira
8. `python3 scripts/sha256-digest.py /tmp/task-desc.md` -- compute SHA-256 digest from re-fetched description
9. `jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")` -- post digest comment
10. `jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-key>, type: "Depend")` -- link to CVE issue
11. `jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")` -- downstream blocked by upstream

### Phase 3: Post-Triage Actions

12. Transition TC-8001 to In Progress
13. Add `ai-cve-triaged` label to TC-8001
14. Post summary comment on TC-8001 listing all created tasks (with Comment Footnote)

**Critical sequencing rule**: For each task, the digest comment (steps 4 and 9) MUST be posted BEFORE any issue links (steps 5, 10, 11) or other comments. This is mandated by `shared/description-digest-protocol.md` Rules: "Producers must post the digest comment immediately after creating the task issue, before creating issue links or other comments."

---

## Post-Triage Summary Comment (proposed)

A summary comment would be posted on TC-8001 documenting:

1. Version impact table (from Step 2)
2. Affects Versions correction: Current [RHTPA 2.0.0] -> Proposed [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
3. Triage outcome: Remediation tasks created for 2.2.x stream
4. Links to remediation tasks: <upstream-task-key> (upstream backport), <downstream-task-key> (downstream propagation, blocked by <upstream-task-key>)
5. @mention of the vulnerability issue reporter using ADF mention node:
   ```json
   { "type": "mention", "attrs": { "id": "<reporter-account-id>", "text": "@<reporter-name>" } }
   ```

The comment MUST include the Comment Footnote:
```
---
This comment was AI-generated by sdlc-workflow/triage-security v0.13.6.
```
