# Step 8 -- Remediation Tasks (Case A: Affected)

Issue TC-8001 is scoped to stream 2.2.x. Versions 2.2.0, 2.2.1, and 2.2.2 are affected (quinn-proto < 0.11.14). Ecosystem is Cargo (source dependency), so two tasks are created.

## Task 1: Upstream Backport Task

**PROPOSED Jira Issue Creation:**

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

```
## Repository

rhtpa-backend

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

- Target branch: release/0.4.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is shipped to customers. Coordinate with Product
Security for CVE assignment, advisory preparation, and formal
disclosure. Fix must be released via a security advisory with
explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

### Description Digest Protocol (Upstream Task)

After `jira.create_issue` returns the new task key:

1. **Re-fetch the description** from Jira: `jira.get_issue(<upstream-task-key>, fields=["description"])`
2. **Write the description** to a temp file: `/tmp/task-desc.md`
3. **Compute SHA-256 digest**: `python3 scripts/sha256-digest.py /tmp/task-desc.md` (outputs `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`)
4. **Post digest comment** (BEFORE creating issue links or other comments):
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
5. **Then** create the Depend link to TC-8001 and any other links/comments.

---

## Task 2: Downstream Propagation Subtask

**PROPOSED Jira Issue Creation:**

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

```
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
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product
Security for CVE assignment, advisory preparation, and formal
disclosure. Fix must be released via a security advisory with
explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Description Digest Protocol (Downstream Task)

After `jira.create_issue` returns the new task key:

1. **Re-fetch the description** from Jira: `jira.get_issue(<downstream-task-key>, fields=["description"])`
2. **Write the description** to a temp file: `/tmp/task-desc.md`
3. **Compute SHA-256 digest**: `python3 scripts/sha256-digest.py /tmp/task-desc.md` (outputs `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`)
4. **Post digest comment** (BEFORE creating issue links or other comments):
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
5. **Then** create the Blocks link from the upstream task and the Depend link to TC-8001.

---

## Jira Linkage (PROPOSED)

After both tasks and their digest comments are created:

1. Link upstream task to TC-8001: `jira.create_link(inwardIssue: TC-8001, outwardIssue: <upstream-task-key>, type: "Depend")`
2. Link downstream subtask as blocked by upstream: `jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")`
3. Link downstream task to TC-8001: `jira.create_link(inwardIssue: TC-8001, outwardIssue: <downstream-task-key>, type: "Depend")`
4. Transition TC-8001 to In Progress (if not already)
5. Add `ai-cve-triaged` label to TC-8001
6. Post summary comment on TC-8001 listing all created tasks

---
This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.12.3.
