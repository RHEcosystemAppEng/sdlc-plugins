# Step 2 -- Version Impact Analysis (Summary)

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | |
| 2.2.4 | 2.2.x | 0.11.14 | NO | |

Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency
  Profile: production (quinn-proto is a runtime dependency)

---

# Step 7.5 -- Release Jira Orchestration

**Proposed actions (not executed -- eval mode):**

Release Jira orchestration would search for an existing release Epic matching the pattern "RHTPA 2.2.* Release Tasks" for the 2.2.x stream. If found, the existing Epic is reused; if not found, the engineer is prompted to confirm the release version (default: next patch bump from the latest released version in the supportability matrix) before creating a new Epic and child Task ("RHTPA <version> CVE triage").

Since external tools are not available in this eval, release orchestration confirmations are pending. The following work would be performed upon confirmation:

1. **Resolve stream-to-version mapping**: Parse stream rhtpa-2.2 -> 2.2.x release family. Search for existing release Epic.
2. **Find or create release Task**: Search for existing "RHTPA <version> CVE triage" Task under the release Epic. Create if not found (after engineer confirmation).
3. **Cross-CVE dedup check**: Inspect the release Task's Blocks links for existing remediation Tasks covering the same upstream component (quinn-proto). Upstream Affected Component custom field is not configured in this CLAUDE.md, so dedup is skipped.

Release evidence and confirmation are unavailable in this eval context. Release linking is reported as pending work rather than claiming creation.

---

# Step 8 -- Remediation

## Triage Outcome: Case A/B -- Affected versions exist, create remediation tasks

The version impact table shows that versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream are affected (ship quinn-proto < 0.11.14). Versions 2.2.3 and 2.2.4 are not affected (ship quinn-proto 0.11.14).

### Cross-Stream Impact (Case A)

The issue is scoped to stream 2.2.x via the `[rhtpa-2.2]` suffix. The version impact analysis also reveals that stream 2.1.x is affected (versions 2.1.0 and 2.1.1 ship quinn-proto 0.11.9). A cross-stream impact comment would be posted:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x based on lock file analysis. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.

A search for sibling CVE Jiras with label CVE-2026-31812 and stream suffix [rhtpa-2.1] would determine whether preemptive remediation tasks need to be created for the 2.1.x stream.

### Remediation Tasks for Stream 2.2.x (Case B)

Ecosystem: **Cargo** (source dependency) -> **2 tasks**: upstream backport + downstream propagation.

---

## Task 1: Upstream Backport Task

**Proposed Jira Issue (not executed -- eval mode):**

- **Project**: TC
- **Issue Type**: Task
- **Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

### Task Description

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto Panic on large stream counts.
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

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
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
```

### Post-Creation Steps (proposed)

1. **Description digest**: After creating the task, re-fetch the description from Jira via `jira.get_issue(<upstream-task-key>, fields=["description"])`, write it to a temp file, compute the digest using `python3 scripts/sha256-digest.py /tmp/task-desc.md`, and post a digest comment: `[sdlc-workflow] Description digest: <tagged-digest>` -- this is posted BEFORE creating any issue links or other comments.

2. **Issue links** (after digest comment):
   - `jira.create_link(inwardIssue: TC-8001, outwardIssue: <upstream-task-key>, type: "Depend")` -- link to parent CVE
   - If release Task exists: `jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <release-task-key>, type: "Blocks")` -- link to release Task

---

## Task 2: Downstream Propagation Subtask

**Proposed Jira Issue (not executed -- eval mode):**

- **Project**: TC
- **Issue Type**: Task
- **Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

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
```

### Post-Creation Steps (proposed)

1. **Description digest**: After creating the task, re-fetch the description from Jira via `jira.get_issue(<downstream-task-key>, fields=["description"])`, write it to a temp file, compute the digest using `python3 scripts/sha256-digest.py /tmp/task-desc.md`, and post a digest comment: `[sdlc-workflow] Description digest: <tagged-digest>` -- this is posted BEFORE creating any issue links or other comments.

2. **Issue links** (after digest comment):
   - `jira.create_link(inwardIssue: TC-8001, outwardIssue: <downstream-task-key>, type: "Depend")` -- link to parent CVE
   - `jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")` -- upstream blocks downstream
   - If release Task exists: `jira.create_link(inwardIssue: <downstream-task-key>, outwardIssue: <release-task-key>, type: "Blocks")` -- link to release Task

---

## Post-Triage Summary

**Proposed actions (not executed -- eval mode):**

1. **Add label**: `ai-cve-triaged` to TC-8001
2. **Transition**: TC-8001 to In Progress
3. **Post summary comment** on TC-8001 documenting:
   - Version impact table (2.2.0 YES, 2.2.1 YES, 2.2.2 YES retag, 2.2.3 NO, 2.2.4 NO)
   - Affects Versions correction: Current [RHTPA 2.0.0] -> Proposed [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
   - Triage outcome: remediation tasks created for stream 2.2.x
   - Cross-stream impact: 2.1.x also affected
   - Links to upstream backport task and downstream propagation subtask
   - @mention of the vulnerability issue's reporter using ADF mention node
   - Comment Footnote: "This comment was AI-generated by sdlc-workflow/triage-security v0.13.10."

---

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks for 2.2.x stream (Cargo = source dependency ecosystem: upstream backport + downstream propagation)
- [x] **Cross-stream coverage**: 2.1.x is also affected; sibling CVE Jira search and preemptive task creation pending
- [x] **Link types**: "Depend" for tasks linked to TC-8001, "Blocks" for upstream -> downstream within 2.2.x stream
- [x] **Coordination guidance**: each task's Implementation Notes includes the customer-shipped guidance based on the rhtpa-backend repository's deployment context
- [x] **Release Jira linking**: pending release orchestration confirmation (Step 7.5)
