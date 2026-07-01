# Step 8 -- Remediation

## Triage Decision

The version impact table shows affected versions exist within the issue's 2.2.x stream scope (2.2.0, 2.2.1, 2.2.2). Additionally, the 2.1.x stream (outside this issue's scope) is also affected (2.1.0, 2.1.1).

- **Case A applies**: Affected versions exist in the scoped stream (2.2.x) -- create remediation tasks.
- **Case B applies**: The 2.1.x stream is also affected (outside this issue's scope) -- post cross-stream impact comment. (Note: cross-stream remediation for 2.1.x would be handled per Case B rules, but the primary remediation tasks below are for the 2.2.x stream.)

## Ecosystem: Cargo (Source Dependency)

Since quinn-proto is a Cargo ecosystem dependency (source dependency), two tasks are created per Important Rule 8:

1. **Upstream backport task** -- fix in the source repo (rhtpa-backend)
2. **Downstream propagation subtask** -- update the reference in the Konflux release repo (rhtpa-release.0.4.z), blocked by the upstream task

---

## Task 1: Upstream Backport Task

### Proposed Jira Issue Creation

```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <see below>,
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

Remediate CVE-2026-31812: quinn-proto Panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (v0.4.5), RHTPA 2.2.1 (v0.4.8), RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8 (from supportability matrix)

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

### Description Digest Protocol (post-create)

After creating the upstream backport task, the following digest steps would be performed:

1. **Re-fetch the task description** from Jira after `create_issue` returns the new task key:
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```
   The digest is computed from the **re-fetched** description (via Jira API after create_issue), not from the description string passed to create_issue. This accounts for any Jira-side formatting transformations.

2. **Compute the SHA-256 digest** using `scripts/sha256-digest.py`:
   ```
   # Write re-fetched description to temp file
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<hex> or sha256-adf:<hex>
   ```

3. **Post the digest comment** with the marker `[sdlc-workflow] Description digest:` **BEFORE** creating issue links or other comments:
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

4. **Then** create the Depend link to TC-8001:
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <upstream-task-key>,
     type: "Depend"
   )
   ```

---

## Task 2: Downstream Propagation Subtask

### Proposed Jira Issue Creation

```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
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
CVE-2026-31812 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Description Digest Protocol (post-create)

After creating the downstream propagation subtask, the following digest steps would be performed:

1. **Re-fetch the task description** from Jira after `create_issue` returns the new task key:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```
   The digest is computed from the **re-fetched** description (via Jira API after create_issue), not from the description string passed to create_issue.

2. **Compute the SHA-256 digest** using `scripts/sha256-digest.py`:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<hex> or sha256-adf:<hex>
   ```

3. **Post the digest comment** with the marker `[sdlc-workflow] Description digest:` **BEFORE** creating issue links or other comments:
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

4. **Then** create the links:
   ```
   # Link downstream task to CVE issue
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )

   # Link downstream task as blocked by upstream task
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

---

## Linkage Summary

After both tasks are created and digest comments are posted:

| Link | From | To | Type |
|------|------|----|------|
| CVE -> Upstream | TC-8001 | <upstream-task-key> | Depend |
| CVE -> Downstream | TC-8001 | <downstream-task-key> | Depend |
| Upstream blocks Downstream | <upstream-task-key> | <downstream-task-key> | Blocks |

## Cross-Stream Impact Comment (Case B)

The 2.1.x stream is also affected but is outside this issue's scope (suffix `[rhtpa-2.2]`). The following comment would be proposed for TC-8001:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s)
2.1.x based on lock file analysis.
- 2.1.0 (tag v0.3.8): quinn-proto 0.11.9 -- affected
- 2.1.1 (tag v0.3.12): quinn-proto 0.11.9 -- affected

These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

---
_Posted by sdlc-workflow skill: triage-security_
```

## Post-Triage Summary

### Proposed: Add `ai-cve-triaged` label to TC-8001

```
jira.edit_issue("TC-8001", fields={
  "labels": ["CVE-2026-31812", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### Proposed: Post summary comment to TC-8001

The summary comment documents the triage outcome and includes an @mention of the vulnerability issue's reporter using an ADF mention node. The reporter's account ID is extracted from the Jira issue data fetched in Step 1.

```
Version impact analysis for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | |
| 2.1.1 | 0.11.9 | YES | |
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | |
| 2.2.4 | 0.11.14 | NO | |

Affects Versions corrected: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

Triage outcome: Remediation tasks created (Case A)
- <upstream-task-key> (upstream backport: bump quinn-proto to 0.11.14 on release/0.4.z)
- <downstream-task-key> (downstream propagation: update rhtpa-backend ref in rhtpa-release.0.4.z, blocked by <upstream-task-key>)

Cross-stream impact: 2.1.x stream also affected (see cross-stream comment).

@<reporter-name> (ADF mention node: {"type": "mention", "attrs": {"id": "<reporter-account-id>", "text": "@<reporter-name>"}})

---
_Posted by sdlc-workflow skill: triage-security_
```

Note: All actions above are **proposed** and require explicit engineer confirmation before execution. No Jira mutations are performed without approval (Guardrails).
