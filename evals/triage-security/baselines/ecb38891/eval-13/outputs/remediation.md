# Step 8 -- Remediation

## Triage Outcome: Case B (Affected -- create remediation tasks)

The version impact table shows versions 2.2.0, 2.2.1, and 2.2.2 are affected within the scoped 2.2.x stream. Versions 2.2.3 and 2.2.4 already ship the fixed version (0.11.14). Remediation tasks are needed for the affected versions.

Since quinn-proto is a **Cargo** ecosystem dependency (source dependency category), **two tasks** are created per the ecosystem classification table: an upstream backport task and a downstream propagation subtask.

---

## Task 1: Upstream Backport Task

### Proposed Jira Issue

```
jira.create_issue(
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

Remediate CVE-2026-31812: quinn-proto denial of service via excessive stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is retag of v0.4.8)

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

### Description Digest Protocol for Upstream Backport Task

After the `create_issue` call returns the new task key (e.g., `TC-XXXX`), the following description digest steps are performed **before** creating any issue links or posting any other comments:

1. **Re-fetch the task description from Jira** -- the description is re-fetched from the Jira API after `create_issue`, not reused from the description string that was passed to `create_issue`. This is critical because Jira normalizes content during storage, so the stored description may differ from what was submitted.

   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```

2. **Write the re-fetched description to a temporary file** and compute the SHA-256 digest using the project's digest script:

   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```

   The script auto-detects the format (ADF JSON or markdown) and outputs a format-tagged digest (e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`).

3. **Post the digest comment** on the newly created upstream task using the marker string `[sdlc-workflow] Description digest:`:

   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

   The comment is posted as an ADF document:

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
   - Create `Depend` link: TC-8001 (Vulnerability) -> TC-XXXX (upstream task)
   - Create `Blocks` link: TC-XXXX (upstream task) -> TC-YYYY (downstream subtask)
   - Post any additional comments

This sequencing ensures that `/implement-task` can verify description integrity in its Step 1.5 before beginning implementation.

---

## Task 2: Downstream Propagation Subtask

### Proposed Jira Issue

```
jira.create_issue(
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
CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Description Digest Protocol for Downstream Propagation Subtask

After the `create_issue` call returns the new subtask key (e.g., `TC-YYYY`), the following description digest steps are performed **before** creating any issue links or posting any other comments:

1. **Re-fetch the subtask description from Jira** -- the description is re-fetched from the Jira API after `create_issue`, not reused from the description string that was passed to `create_issue`. Jira normalizes content during storage, so the stored version is the authoritative one for digest computation.

   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```

2. **Write the re-fetched description to a temporary file** and compute the SHA-256 digest using the project's digest script:

   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```

   The script auto-detects the format (ADF JSON or markdown) and outputs a format-tagged digest (e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`).

3. **Post the digest comment** on the newly created downstream subtask using the marker string `[sdlc-workflow] Description digest:`:

   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

   The comment is posted as an ADF document:

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
   - Create `Depend` link: TC-8001 (Vulnerability) -> TC-YYYY (downstream subtask)
   - Create `Blocks` link: TC-XXXX (upstream task) -> TC-YYYY (downstream subtask)
   - Post any additional comments

This sequencing ensures that `/implement-task` can verify description integrity in its Step 1.5 before beginning implementation.

---

## Full Remediation Procedure (ordered)

The complete sequence of Jira operations for both tasks, showing exactly when digest comments are posted relative to links and comments:

### Phase 1: Create upstream backport task

1. `jira.create_issue(...)` -- create the upstream task (returns key TC-XXXX)
2. `jira.get_issue(TC-XXXX, fields=["description"])` -- re-fetch the description from Jira (NOT from the string passed to create_issue)
3. Write re-fetched description to `/tmp/task-desc.md`
4. `python3 scripts/sha256-digest.py /tmp/task-desc.md` -- compute the format-tagged digest
5. `jira.add_comment(TC-XXXX, "[sdlc-workflow] Description digest: <tagged-digest>")` -- post digest comment

### Phase 2: Create downstream propagation subtask

6. `jira.create_issue(...)` -- create the downstream subtask (returns key TC-YYYY)
7. `jira.get_issue(TC-YYYY, fields=["description"])` -- re-fetch the description from Jira (NOT from the string passed to create_issue)
8. Write re-fetched description to `/tmp/task-desc.md`
9. `python3 scripts/sha256-digest.py /tmp/task-desc.md` -- compute the format-tagged digest
10. `jira.add_comment(TC-YYYY, "[sdlc-workflow] Description digest: <tagged-digest>")` -- post digest comment

### Phase 3: Create issue links (AFTER all digest comments are posted)

11. `jira.create_link(inwardIssue: TC-8001, outwardIssue: TC-XXXX, type: "Depend")` -- link upstream task to Vulnerability
12. `jira.create_link(inwardIssue: TC-8001, outwardIssue: TC-YYYY, type: "Depend")` -- link downstream subtask to Vulnerability
13. `jira.create_link(inwardIssue: TC-XXXX, outwardIssue: TC-YYYY, type: "Blocks")` -- downstream blocked by upstream

### Phase 4: Transition and label

14. Transition TC-8001 to In Progress (if not already)
15. Add `ai-cve-triaged` label to TC-8001

### Phase 5: Post-triage summary comment

16. `jira.add_comment(TC-8001, <post-triage summary including version impact table, remediation task links, and reporter @mention>)`

---

## Cross-Stream Impact (Case A)

The 2.1.x stream is also affected (versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). Since the current issue is scoped to 2.2.x, a cross-stream impact comment would be proposed:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x based on lock file analysis. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.

Whether preemptive remediation tasks are created for 2.1.x depends on whether a sibling CVE Jira exists for that stream (Step 4 / Case A check).
