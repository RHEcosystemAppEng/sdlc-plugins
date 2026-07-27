# Step 8 -- Remediation

## Triage Decision

**Case B: Affected -- create remediation tasks** for affected streams only.

The issue is **unscoped** (no stream suffix), so it covers all streams by definition. There is no "cross-stream impact" check (Case A) for unscoped issues -- Case A applies only to scoped issues. Since the issue is unscoped, **no cross-stream impact notice is generated**.

**Stream-by-stream assessment:**
- **Stream 2.1.x: AFFECTED** -- all versions (2.1.0, 2.1.1) ship h2 0.4.5, below fix threshold 0.4.8. Remediation tasks are required.
- **Stream 2.2.x: NOT AFFECTED** -- all versions ship h2 >= 0.4.8 (at or above fix threshold). No remediation tasks needed.

**Ecosystem**: Cargo (source dependency) -- per the ecosystem classification table, this produces **2 tasks per affected stream** (upstream backport + downstream propagation with Blocks dependency).

Remediation tasks are created **only for stream 2.1.x**. Stream 2.2.x already ships the patched version and requires no action.

---

## Task 1: Upstream Backport (Stream 2.1.x)

### Proposed Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (rhtpa-2.1)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

### Task Description

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (tag v0.3.8, h2 0.4.5), RHTPA 2.1.1 (tag v0.3.12, h2 0.4.5)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- Update h2 dependency to >= 0.4.8 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)

### Post-Creation Procedures

1. **Description digest comment** (posted BEFORE creating issue links or other comments):
   - Re-fetch the task description from Jira: `jira.get_issue(<upstream-task-key>, fields=["description"])`
   - Write the re-fetched description to a temp file
   - Compute the digest: `python3 scripts/sha256-digest.py /tmp/task-desc.md`
   - Post the digest comment: `jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`
   - The digest is computed from the re-fetched description (via Jira API after create_issue), NOT from the description string passed to create_issue

2. **Link to Vulnerability issue** (after digest comment):
   ```
   jira.create_link(
     inwardIssue: "TC-8004",
     outwardIssue: <upstream-task-key>,
     type: "Depend"
   )
   ```

---

## Task 2: Downstream Propagation Subtask (Stream 2.1.x)

### Proposed Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

### Task Description

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-33501 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps h2 to 0.4.8 on release/0.3.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
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
- Depends on: TC-8004 (parent tracking issue)

### Post-Creation Procedures

1. **Description digest comment** (posted BEFORE creating issue links or other comments):
   - Re-fetch the task description from Jira: `jira.get_issue(<downstream-task-key>, fields=["description"])`
   - Write the re-fetched description to a temp file
   - Compute the digest: `python3 scripts/sha256-digest.py /tmp/task-desc.md`
   - Post the digest comment: `jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`
   - The digest is computed from the re-fetched description (via Jira API after create_issue), NOT from the description string passed to create_issue

2. **Link to Vulnerability issue** (after digest comment):
   ```
   jira.create_link(
     inwardIssue: "TC-8004",
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )
   ```

3. **Blocks dependency** -- downstream subtask is blocked by upstream task (after digest comment):
   ```
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

---

## Post-Triage Summary

After all remediation tasks are created:

1. **Add `ai-cve-triaged` label** to TC-8004.

2. **Transition TC-8004 to In Progress** (if not already).

3. **Post summary comment** to TC-8004:

```
Triage complete for CVE-2026-33501 (h2 < 0.4.8).

Version Impact:

| Version | Stream | h2 version | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.4.5 | YES | |
| 2.1.1 | 2.1.x | 0.4.5 | YES | |
| 2.2.0 | 2.2.x | 0.4.8 | NO | at fix threshold |
| 2.2.1 | 2.2.x | 0.4.8 | NO | at fix threshold |
| 2.2.2 | 2.2.x | -- | NO | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.4.9 | NO | |
| 2.2.4 | 2.2.x | 0.4.9 | NO | |

Affects Versions corrected: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]

Triage outcome: Remediation required for stream 2.1.x only.
Stream 2.2.x already ships h2 >= 0.4.8 -- no remediation needed.

Remediation tasks created (stream 2.1.x, Cargo -- 2 tasks):
- <upstream-task-key> (upstream backport: bump h2 to 0.4.8 on release/0.3.z)
- <downstream-task-key> (downstream propagation: update backend ref in rhtpa-release.0.3.z, blocked by <upstream-task-key>)

@<reporter-name> [ADF mention node: {"type": "mention", "attrs": {"id": "<reporter-account-id>", "text": "@<reporter-name>"}}]

---
This comment was AI-generated by sdlc-workflow/triage-security v0.13.6.
```

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks for stream 2.1.x (Cargo = source dependency). 0 tasks for stream 2.2.x (not affected).
- [x] **Cross-stream coverage**: not applicable -- issue is unscoped, so Case A is skipped entirely. No cross-stream impact notice generated.
- [x] **Link types**: "Depend" for tasks linked to TC-8004 (their own CVE Jira). "Blocks" for upstream -> downstream within stream 2.1.x.
- [x] **Preemptive labels**: not applicable -- issue is unscoped, no preemptive tasks needed.
- [x] **Coordination guidance**: omitted -- no Deployment Context column in Source Repositories table (backward compatibility, all repos default to upstream).
