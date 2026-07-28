# Step 8 -- Remediation

## Triage Outcome: Case B -- Affected (create remediation tasks)

All 2.2.x versions ship criterion 0.5.1 (< 0.5.2). Remediation tasks are required.

**Dev-dependency handling applied**: criterion is a dev-only dependency (declared
in `[dev-dependencies]`). Per the dependency scope decision tree:
- Tasks carry the `dev-dependency` label
- Priority is overridden to **Normal** (regardless of CVE severity CVSS 5.3 Medium)
- Task descriptions include a note that the dependency is dev/build-only

Since criterion is a **Cargo** (source dependency) ecosystem, two tasks are
created per stream: upstream backport + downstream propagation.

---

## Task 1: Upstream Backport Task

**Proposed Jira issue creation** (requires confirmation):

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

```markdown
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99001: path traversal in benchmark output in criterion.
The vulnerable dependency (criterion < 0.5.2) must be updated to the fixed
version (0.5.2+).

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

Affected versions: RHTPA 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4
Source commit(s): v0.4.5, v0.4.8, v0.4.11, v0.4.12

CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (dev-dependency)
- **Dependency scope**: dev-only ([dev-dependencies] in backend/Cargo.toml) --
  NOT shipped in production. Used for benchmarks only.

### Remediation approach (direct dependency)

- Update criterion dependency to >= 0.5.2 in backend/Cargo.toml [dev-dependencies]
- Run `cargo update -p criterion` to update Cargo.lock
- If the direct bump introduces breaking API changes to benchmark code,
  assess whether benchmark code adjustments are viable (see upstream changelog)

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8050 (parent tracking issue)
```

### Post-creation steps (proposed):

1. **Description digest comment** (before links or other comments):
   - Re-fetch the task description from Jira after `create_issue`:
     `jira.get_issue(<upstream-task-key>, fields=["description"])`
   - Write the description content to a temp file
   - Compute the digest: `python3 scripts/sha256-digest.py /tmp/task-desc.md`
   - Post the digest comment:
     `jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`

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

**Proposed Jira issue creation** (requires confirmation):

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

```markdown
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99001 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps criterion to 0.5.2
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct (dev-dependency) -- carried forward from upstream task
- **Dependency scope**: dev-only -- NOT shipped in production
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

### Post-creation steps (proposed):

1. **Description digest comment** (before links or other comments):
   - Re-fetch the task description from Jira after `create_issue`:
     `jira.get_issue(<downstream-task-key>, fields=["description"])`
   - Write the description content to a temp file
   - Compute the digest: `python3 scripts/sha256-digest.py /tmp/task-desc.md`
   - Post the digest comment:
     `jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`

2. **Link downstream subtask to Vulnerability issue** (after digest comment):
   ```
   jira.create_link(
     inwardIssue: "TC-8050",
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )
   ```

3. **Link downstream subtask as blocked by upstream task**:
   ```
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

---

## Post-Triage Summary

After creating both remediation tasks, the following post-triage actions are proposed:

1. **Add `ai-cve-triaged` label** to TC-8050
2. **Transition TC-8050 to In Progress** (if not already)
3. **Post summary comment** on TC-8050 documenting:
   - Version impact table (all 2.2.x versions affected, criterion 0.5.1 < 0.5.2)
   - Dependency scope: dev-only (not shipped in production)
   - Affects Versions correction: Current [RHTPA 2.2.0] -> Proposed [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2, RHTPA 2.2.3, RHTPA 2.2.4]
   - Remediation tasks created: <upstream-task-key> (upstream backport),
     <downstream-task-key> (downstream propagation, blocked by <upstream-task-key>)
   - Both tasks carry the `dev-dependency` label with Normal priority
   - @mention of the vulnerability issue's reporter using ADF mention node:
     ```json
     { "type": "mention", "attrs": { "id": "<reporter-account-id>", "text": "@<reporter-name>" } }
     ```
   - Comment Footnote:
     ```
     ---
     This comment was AI-generated by sdlc-workflow/triage-security v0.13.7.
     ```

---

## Summary of Dev-Dependency Modifications

| Aspect | Standard | Dev-Dependency (applied) |
|--------|----------|--------------------------|
| Labels | ai-generated-jira, Security, CVE-2026-99001 | ai-generated-jira, Security, CVE-2026-99001, **dev-dependency** |
| Priority | Inherits CVE severity (Medium) | **Normal** (override) |
| Task count | 2 (upstream + downstream) | 2 (unchanged) |
| Description note | (none) | "This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only)." |
