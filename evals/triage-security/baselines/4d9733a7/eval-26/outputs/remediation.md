# Step 8 -- Remediation

## Case A: Affected -- Create Remediation Tasks

All 2.2.x stream versions ship criterion 0.5.1, which is within the affected range (< 0.5.2). Remediation tasks are required.

Since criterion is a **Cargo** (source dependency) ecosystem package, two tasks are created: an upstream backport task and a downstream propagation subtask.

**Dev-dependency handling applied**: Because criterion is a dev-only dependency (not shipped in production), the following modifications are applied per the dependency scope decision tree:
- Labels include `dev-dependency`
- Priority is set to **Normal** (overriding CVE severity of CVSS 5.3 Medium)
- Description includes a note that the dependency is dev/build-only

---

### Task 1: Upstream Backport Task

**Proposed** `jira.create_issue` (not executed -- eval mode):

- **Project**: TC
- **Issue Type**: Task
- **Summary**: Remediate CVE-2026-99001: bump criterion to 0.5.2 (rhtpa-2.2)
- **Labels**: `["ai-generated-jira", "Security", "CVE-2026-99001", "dev-dependency"]`
- **Priority**: Normal

**Description:**

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99001: path traversal in benchmark output in criterion.
The vulnerable dependency (criterion < 0.5.2) must be updated to the fixed version (0.5.2+).

This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only).

Affected versions: 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4
Source commit(s): v0.4.5, v0.4.8, v0.4.11, v0.4.12

CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (dev-dependency)
- **Dependency scope**: dev-only -- criterion is declared in [dev-dependencies] and is NOT shipped in production builds. Used for benchmarks only.

### Remediation approach (direct dependency)

- Update criterion dependency to >= 0.5.2 in backend/Cargo.toml [dev-dependencies]
- Run `cargo update -p criterion` to update Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8050 (parent tracking issue)

---

**Post-creation steps** (proposed, not executed):

1. Re-fetch task description via `jira.get_issue(<upstream-task-key>, fields=["description"])`
2. Compute SHA-256 digest using `python3 scripts/sha256-digest.py /tmp/task-desc.md`
3. Post digest comment: `[sdlc-workflow] Description digest: sha256-md:<hex-digest>` (or sha256-adf:<hex-digest>)
4. Create Depend link: `jira.create_link(inwardIssue: TC-8050, outwardIssue: <upstream-task-key>, type: "Depend")`

---

### Task 2: Downstream Propagation Subtask

**Proposed** `jira.create_issue` (not executed -- eval mode):

- **Project**: TC
- **Issue Type**: Task
- **Summary**: Propagate CVE-2026-99001 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
- **Labels**: `["ai-generated-jira", "Security", "CVE-2026-99001", "dev-dependency"]`
- **Priority**: Normal

**Description:**

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-99001 fix from the upstream backport task.

This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only).

The upstream backport bumps criterion to 0.5.2 on release/0.4.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct (dev-dependency) -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8050 (parent tracking issue)

---

**Post-creation steps** (proposed, not executed):

1. Re-fetch task description via `jira.get_issue(<downstream-task-key>, fields=["description"])`
2. Compute SHA-256 digest using `python3 scripts/sha256-digest.py /tmp/task-desc.md`
3. Post digest comment: `[sdlc-workflow] Description digest: sha256-md:<hex-digest>` (or sha256-adf:<hex-digest>)
4. Create Blocks link: `jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")`
5. Create Depend link: `jira.create_link(inwardIssue: TC-8050, outwardIssue: <downstream-task-key>, type: "Depend")`

---

## Post-Triage Summary

**Proposed actions** (not executed -- eval mode):

1. Add `ai-cve-triaged` label to TC-8050
2. Post summary comment to TC-8050 documenting:
   - Version impact table (all 2.2.x versions affected)
   - Affects Versions correction (if applicable)
   - Triage outcome: remediation tasks created with dev-dependency handling
   - Links to upstream and downstream remediation tasks
   - @mention of reporter (psirt-analyst, account ID from issue data) using ADF mention node
   - Comment Footnote: "This comment was AI-generated by sdlc-workflow/triage-security v0.12.3."
3. Transition TC-8050 to In Progress (if not already)
