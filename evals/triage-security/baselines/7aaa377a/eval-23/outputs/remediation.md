# Step 8 -- Remediation

## Version Impact Summary

Based on the version impact analysis (Step 2), the following versions in the 2.2.x stream are affected:

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | |
| 2.2.4 | 0.11.14 | NO | |

Cross-stream check (2.1.x):

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | |
| 2.1.1 | 0.11.9 | YES | |

**Triage decision**: Case B -- affected versions exist within the scoped stream (2.2.x). Also, Case A applies because the 2.1.x stream is also affected (cross-stream impact for this scoped issue).

## Ecosystem Classification

quinn-proto is a **Cargo** (source dependency) ecosystem package. Per the ecosystem classification table, this requires **two tasks** per affected stream:
1. Upstream backport task (fix in source repo)
2. Downstream propagation subtask (update reference in Konflux release repo)

## Remediation Task Descriptions

### Task 1: Upstream Backport Task (2.2.x stream)

**Proposed Jira create_issue call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task description:**

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (v0.4.5), RHTPA 2.2.1 (v0.4.8), RHTPA 2.2.2 (v0.4.8, retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock / Cargo.toml

### Remediation approach (direct dependency)

The vulnerable package quinn-proto is a direct dependency of the workspace:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
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

---

**Post-creation procedure for upstream task:**

1. Re-fetch the task description from Jira after create_issue:
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```
2. Write the re-fetched description to a temp file and compute the SHA-256 digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The script auto-detects the format (ADF or markdown) and outputs a tagged digest (e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`).
3. Post the description digest comment **before** creating issue links or other comments:
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
4. After the digest comment is posted, create the Depend link:
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <upstream-task-key>, type: "Depend")
   ```

---

### Task 2: Downstream Propagation Subtask (2.2.x stream)

**Proposed Jira create_issue call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task description:**

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

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

**Post-creation procedure for downstream subtask:**

1. Re-fetch the task description from Jira after create_issue:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```
2. Write the re-fetched description to a temp file and compute the SHA-256 digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The script auto-detects the format and outputs a tagged digest.
3. Post the description digest comment **before** creating issue links or other comments:
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
4. After the digest comment is posted, create links:
   - Depend link to CVE: `jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-key>, type: "Depend")`
   - Blocks link from upstream: `jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")`

---

## Post-Triage Summary

After remediation tasks are created, the following post-triage actions are proposed:

1. **Add `ai-cve-triaged` label** to TC-8001
2. **Post summary comment** to TC-8001 documenting:
   - Version impact table
   - Affects Versions correction (Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1])
   - Triage outcome: remediation tasks created
   - Links to upstream task and downstream subtask
   - @mention of the vulnerability reporter using ADF mention node:
     ```json
     { "type": "mention", "attrs": { "id": "<reporter-account-id>", "text": "@<reporter-name>" } }
     ```
   - Comment Footnote: "This comment was AI-generated by sdlc-workflow/triage-security v0.13.7."
3. **Transition TC-8001** to In Progress

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks for 2.2.x stream (Cargo = source dependency -> upstream backport + downstream propagation)
- [x] **Cross-stream coverage**: 2.1.x stream is also affected -- Case A cross-stream impact comment to be posted; preemptive tasks or sibling CVE Jira check applies
- [x] **Link types**: "Depend" for tasks linked to TC-8001, "Blocks" for upstream -> downstream within 2.2.x stream
- [x] **Coordination guidance**: each task's Implementation Notes includes customer-shipped guidance based on rhtpa-backend's deployment context
