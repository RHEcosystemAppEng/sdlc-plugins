# Step 8 -- Remediation (Case B: Affected)

All versions in the 2.2.x stream are affected. Remediation tasks are required.

## Dev-Dependency Handling

criterion is a **dev-only** dependency (declared in `[dev-dependencies]`). Per the dependency scope decision tree:

- Remediation tasks are still created (supply chain risk -- compromised dev deps can inject malicious code during builds)
- The `dev-dependency` label is added to all remediation tasks
- Priority is overridden to **Normal** regardless of the CVE severity (CVSS 5.3 Medium)
- A note is included in the task description indicating the dependency is dev/build-only

## Ecosystem Classification

Cargo is a **source dependency** ecosystem. Per the classification table, two tasks are created per stream:
1. Upstream backport task (fix in the source repo)
2. Downstream propagation subtask (update reference in Konflux release repo)

---

## Task 1: Upstream Backport Task

**Proposed Jira API call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-99001: bump criterion to 0.5.2 (rhtpa-2.2)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99001", "dev-dependency"],
  priority: "Normal"
)
```

### Task Description

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only).

Remediate CVE-2026-99001: path traversal in benchmark output in criterion.
The vulnerable dependency (criterion < 0.5.2) must be updated
to the fixed version (0.5.2+).

Affected versions: RHTPA 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4
Source commit(s): v0.4.5, v0.4.8, v0.4.11, v0.4.12

CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (dev-dependency)
- **Dependency scope**: dev-only ([dev-dependencies] in backend/Cargo.toml) -- NOT shipped in production, used for benchmarks only
- This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only).

### Remediation approach (direct dependency)

criterion is a direct dev-dependency of the backend workspace:

- Update criterion dependency to >= 0.5.2 in backend/Cargo.toml ([dev-dependencies] section)
- Run `cargo update -p criterion` to update Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass (criterion is used for benchmarks)

## Test Requirements

- [ ] Existing test suite passes with the updated dependency
- [ ] Benchmarks compile and run successfully with the new criterion version

## Dependencies

- Depends on: TC-8050 (parent tracking issue)
```

### Post-Creation Steps (Upstream Backport Task)

1. **Description digest comment** (posted BEFORE issue links or other comments):
   - Re-fetch the task description from Jira after create_issue:
     ```
     upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
     ```
   - Write the re-fetched description to a temp file
   - Compute the SHA-256 digest using the script:
     ```
     python3 scripts/sha256-digest.py /tmp/task-desc.md
     ```
   - Post the digest comment:
     ```
     jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
     ```
   Note: The digest is computed from the re-fetched description (via Jira API after create_issue), not from the description string passed to create_issue.

2. **Link to Vulnerability issue** (after digest comment):
   ```
   jira.create_link(
     inwardIssue: "TC-8050",
     outwardIssue: <upstream-task-key>,
     type: "Depend"
   )
   ```

---

## Task 2: Downstream Propagation Subtask

**Proposed Jira API call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-99001 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99001", "dev-dependency"],
  priority: "Normal"
)
```

### Task Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only).

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99001 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps criterion to 0.5.2
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct (dev-dependency) -- carried forward from upstream task
- **Dependency scope**: dev-only -- NOT shipped in production (supply chain risk only)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8050 (parent tracking issue)
```

### Post-Creation Steps (Downstream Propagation Subtask)

1. **Description digest comment** (posted BEFORE issue links or other comments):
   - Re-fetch the task description from Jira after create_issue:
     ```
     downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
     ```
   - Write the re-fetched description to a temp file
   - Compute the SHA-256 digest using the script:
     ```
     python3 scripts/sha256-digest.py /tmp/task-desc.md
     ```
   - Post the digest comment:
     ```
     jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
     ```
   Note: The digest is computed from the re-fetched description (via Jira API after create_issue), not from the description string passed to create_issue.

2. **Link to Vulnerability issue** (after digest comment):
   ```
   jira.create_link(
     inwardIssue: "TC-8050",
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )
   ```

3. **Link downstream as blocked by upstream** (after digest comment):
   ```
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

---

## Post-Triage Summary

After task creation, the following post-triage actions are proposed:

1. **Add `ai-cve-triaged` label** to TC-8050
2. **Transition TC-8050 to In Progress**
3. **Post summary comment** on TC-8050 documenting:
   - Version impact table (all 2.2.x versions affected, criterion 0.5.1 < 0.5.2)
   - Affects Versions correction (proposed: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2, RHTPA 2.2.3, RHTPA 2.2.4)
   - Triage outcome: remediation tasks created with dev-dependency handling
   - Links to upstream backport task and downstream propagation subtask
   - @mention of the vulnerability issue reporter (ADF mention node with reporter's account ID)
   - Comment Footnote: "This comment was AI-generated by sdlc-workflow/triage-security v0.13.6."

---

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks (source dependency ecosystem -- Cargo) -- upstream backport + downstream propagation
- [x] **Cross-stream coverage**: Issue is scoped to 2.2.x; no cross-stream impact analysis performed in this output (would be handled by Case A if other streams affected)
- [x] **Link types**: "Depend" for tasks linked to TC-8050, "Blocks" for upstream -> downstream within stream
- [x] **Dev-dependency label**: Both tasks carry `dev-dependency` label
- [x] **Priority override**: Both tasks set to Normal priority (not inheriting CVSS 5.3 Medium)
- [x] **Coordination guidance**: Omitted -- Source Repositories table has no Deployment Context column
