# Step 8 -- Remediation

## Triage Outcome

Versions 2.2.0, 2.2.1, and 2.2.2 in stream 2.2.x are affected by CVE-2026-99010 (h2 < 0.4.5). Versions 2.2.3 and 2.2.4 ship h2 0.4.5, which is at or above the fix threshold.

Cross-stream check: stream 2.1.x is NOT affected (all versions ship h2 >= 0.4.5). No cross-stream impact notice (Case A) is needed.

**Decision: Case B** -- affected versions exist within the issue's scoped stream. Create remediation tasks for stream 2.2.x.

Ecosystem: Cargo (source dependency) -- create **two tasks**: upstream backport + downstream propagation.

---

## Remediation Task 1: Upstream Backport Task

### Proposed Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-99010: bump h2 to 0.4.5 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99010"]
)
```

### Task Description

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99010: h2 - Memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.5) must be updated to the fixed version (0.4.5+).

Affected versions: 2.2.0 (v0.4.5), 2.2.1 (v0.4.8), 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/hyperium/h2/pull/800
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99010

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend -> reqwest -> hyper -> h2, 3 levels deep)

### Remediation approach (transitive dependency)

The vulnerable package h2 is a **transitive** dependency pulled in through
intermediate packages. Use a two-tier approach:

**Preferred: bump the direct dependency (reqwest)**
- reqwest is the direct dependency that ultimately pulls in h2 through
  reqwest -> hyper -> h2
- Bump reqwest to a version whose transitive closure includes h2 >= 0.4.5
- Verify the bump does not introduce breaking API changes to reqwest
- Check reqwest's changelog and dependency tree to confirm a version
  exists that resolves h2 >= 0.4.5 transitively

**Fallback: pin h2 directly**
If bumping reqwest is not viable (breaking API changes, no release
available with the fix):
- Run: `cargo add h2@0.4.5` to add h2 as a direct dependency,
  overriding the transitive resolution
- This forces Cargo to resolve h2 to at least 0.4.5 regardless of
  what reqwest/hyper request
- Document why the direct dep bump (reqwest) was not viable in the
  PR description

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.5
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8060 (parent tracking issue)
```

### Post-Creation Steps (Upstream Backport Task)

1. **Description digest comment** (posted BEFORE issue links or other comments):
   - Re-fetch the task description from Jira after create_issue:
     ```
     upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
     ```
   - Write the re-fetched description to a temp file
   - Compute the SHA-256 digest using the digest script:
     ```
     python3 scripts/sha256-digest.py /tmp/task-desc.md
     ```
     This produces a format-tagged digest (e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`)
   - Post the digest comment:
     ```
     jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
     ```

2. **Issue link** (Depend -- posted AFTER digest comment):
   ```
   jira.create_link(
     inwardIssue: "TC-8060",
     outwardIssue: <upstream-task-key>,
     type: "Depend"
   )
   ```

---

## Remediation Task 2: Downstream Propagation Subtask

### Proposed Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-99010 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99010"]
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
CVE-2026-99010 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps h2 to 0.4.5
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: transitive (chain: backend -> reqwest -> hyper -> h2) -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- If the upstream fix pinned h2 directly (fallback approach via cargo add h2@0.4.5),
  verify the pinning is reflected in the downstream build's Cargo.lock after
  the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8060 (parent tracking issue)
```

### Post-Creation Steps (Downstream Propagation Subtask)

1. **Description digest comment** (posted BEFORE issue links or other comments):
   - Re-fetch the task description from Jira after create_issue:
     ```
     downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
     ```
   - Write the re-fetched description to a temp file
   - Compute the SHA-256 digest using the digest script:
     ```
     python3 scripts/sha256-digest.py /tmp/task-desc.md
     ```
     This produces a format-tagged digest (e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`)
   - Post the digest comment:
     ```
     jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
     ```

2. **Issue links** (posted AFTER digest comment):
   - Depend link to CVE:
     ```
     jira.create_link(
       inwardIssue: "TC-8060",
       outwardIssue: <downstream-task-key>,
       type: "Depend"
     )
     ```
   - Blocks link (upstream blocks downstream):
     ```
     jira.create_link(
       inwardIssue: <upstream-task-key>,
       outwardIssue: <downstream-task-key>,
       type: "Blocks"
     )
     ```

---

## Post-Triage Summary

After remediation task creation, the following post-triage actions are proposed:

1. **Add `ai-cve-triaged` label** to TC-8060:
   ```
   jira.edit_issue("TC-8060", fields={"labels": ["CVE-2026-99010", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]})
   ```

2. **Transition TC-8060 to In Progress** (if not already):
   ```
   jira.get_transitions("TC-8060")
   jira.transition_issue("TC-8060", <in-progress-transition-id>)
   ```

3. **Post summary comment** on TC-8060 with @mention of the reporter (psirt-analyst):

   The comment includes:
   - Version impact table
   - Affects Versions correction (Current: [RHTPA 2.2.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2])
   - Triage outcome: remediation tasks created
   - Links to upstream and downstream tasks
   - @mention of the reporter using ADF mention node:
     ```json
     { "type": "mention", "attrs": { "id": "557058:psirt-analyst-mock-id", "text": "@psirt-analyst" } }
     ```
   - Comment Footnote (sdlc-workflow/triage-security v0.13.7)

   ```
   Remediation tasks created:
   - <upstream-task-key> (upstream backport: bump h2 to 0.4.5 in backend on release/0.4.z)
   - <downstream-task-key> (downstream propagation: update backend ref in rhtpa-release.0.4.z, blocked by <upstream-task-key>)

   Note: h2 is a transitive dependency (backend -> reqwest -> hyper -> h2, 3 levels deep).
   Preferred remediation: bump reqwest to a version whose transitive closure includes h2 >= 0.4.5.
   Fallback: pin h2 directly via cargo add h2@0.4.5.

   @psirt-analyst [ADF mention node with account ID 557058:psirt-analyst-mock-id]

   ---
   This comment was AI-generated by sdlc-workflow/triage-security v0.13.7.
   ```

All actions above are proposed -- each requires explicit engineer confirmation before execution.
