# Step 8 -- Remediation

## Version Impact Summary

Based on the version impact analysis from Step 2, the following versions in the 2.2.x stream (the issue's scoped stream) are affected:

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.11.14 | NO | >= 0.11.14 |
| 2.2.4 | 0.11.14 | NO | >= 0.11.14 |

Versions 2.2.0 through 2.2.2 are affected. This triggers **Case A: Affected -- create remediation tasks**.

## Triage Decision

Since the ecosystem is **Cargo** (a source dependency ecosystem), two remediation tasks are created:

1. **Upstream backport task** -- fix in the source repo (rhtpa-backend)
2. **Downstream propagation subtask** -- update the source reference in the Konflux release repo

---

## Remediation Task 1: Upstream Backport Task

### Proposed Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto Panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (v0.4.5), RHTPA 2.2.1 (v0.4.8), RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z (from Ecosystem Mappings)
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

### Description Digest Protocol (Post-Creation)

After creating this task:

1. **Re-fetch the task description** from Jira using the newly created issue key:
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```
2. **Write the re-fetched description** to a temp file (the description as returned by Jira, not the string passed to create_issue):
   ```
   Write re-fetched description to /tmp/task-desc.md
   ```
3. **Compute the SHA-256 digest** from the re-fetched description:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This produces a tagged digest in format `sha256-md:<hex>` or `sha256-adf:<hex>`.
4. **Post the digest comment** (BEFORE creating issue links or other comments):
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
5. **Then create the Depend link** to TC-8001:
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
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
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

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

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

### Description Digest Protocol (Post-Creation)

After creating this task:

1. **Re-fetch the task description** from Jira using the newly created issue key:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```
2. **Write the re-fetched description** to a temp file (the description as returned by Jira, not the string passed to create_issue):
   ```
   Write re-fetched description to /tmp/task-desc.md
   ```
3. **Compute the SHA-256 digest** from the re-fetched description:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This produces a tagged digest in format `sha256-md:<hex>` or `sha256-adf:<hex>`.
4. **Post the digest comment** (BEFORE creating issue links or other comments):
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
5. **Then create the Blocks link** to the upstream task and Depend link to TC-8001:
   ```
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )
   ```

---

## Linkage Summary

After both tasks are created and digest comments are posted:

1. **Upstream backport task** is linked to TC-8001 with "Depend"
2. **Downstream propagation subtask** is linked to:
   - The upstream backport task with "Blocks" (downstream is blocked by upstream)
   - TC-8001 with "Depend" (parent tracking issue)

## Post-Triage Actions (Proposed)

The following Jira mutations are proposed (require engineer confirmation):

1. **Add label** `ai-cve-triaged` to TC-8001
2. **Transition** TC-8001 to "In Progress"
3. **Assign** TC-8001 to the current user
4. **Post summary comment** to TC-8001 documenting:
   - The version impact table
   - The Affects Versions correction
   - The triage outcome (remediation tasks created)
   - Links to both remediation tasks
   - @mention of the vulnerability issue's reporter using ADF mention node

---

## Key Observations

### Coordination Guidance Inclusion

Both remediation task descriptions include a **Coordination Guidance** subsection under Implementation Notes. This is because the affected repository (`rhtpa-backend`) has a deployment context of **customer-shipped** configured in the Source Repositories table of the CLAUDE.md Security Configuration.

The customer-shipped guidance text instructs the engineer to:
- Coordinate with Product Security for CVE assignment
- Prepare an advisory
- Follow formal disclosure procedures
- Ensure the fix is released via a security advisory with explicit CVE-to-component mapping

This guidance is appended to the Implementation Notes section of each remediation task (both upstream backport and downstream propagation) to ensure the engineer is aware of the customer-facing implications of the fix.
