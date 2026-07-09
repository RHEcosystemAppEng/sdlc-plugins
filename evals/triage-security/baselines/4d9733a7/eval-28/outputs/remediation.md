# Step 8 -- Remediation

## Case A: Affected -- Create Remediation Tasks

Versions 2.2.0, 2.2.1, and 2.2.2 ship h2 0.4.4, which is within the affected range (< 0.4.5). Remediation tasks are required for the 2.2.x stream.

Since h2 is a **Cargo** (source dependency) ecosystem package, two tasks are created: an upstream backport task and a downstream propagation subtask.

---

### Task 1: Upstream Backport Task

**Proposed** `jira.create_issue` (not executed -- eval mode):

- **Project**: TC
- **Issue Type**: Task
- **Summary**: Remediate CVE-2026-99010: bump h2 to 0.4.5 (rhtpa-2.2)
- **Labels**: `["ai-generated-jira", "Security", "CVE-2026-99010"]`

**Description:**

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99010: memory exhaustion via CONTINUATION frames in h2.
The vulnerable dependency (h2 < 0.4.5) must be updated to the fixed version (0.4.5+).

Affected versions: 2.2.0, 2.2.1, 2.2.2
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is retag of v0.4.8)

Upstream fix: hyperium/h2#800
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99010

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend -> reqwest -> hyper -> h2, 3 levels deep)

### Remediation approach (transitive dependency)

h2 is a **transitive** dependency pulled in through reqwest -> hyper -> h2. Use the two-tier remediation approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in h2: `reqwest` (declared in backend/Cargo.toml as `reqwest = { version = "0.12", features = ["json"] }`)
- Bump reqwest to a version whose transitive closure includes h2 >= 0.4.5
- Check if a newer reqwest release (e.g., 0.12.6+) ships with hyper that depends on h2 >= 0.4.5
- Verify the bump does not introduce breaking API changes to reqwest

**Fallback: pin the transitive dependency directly**
If bumping reqwest is not viable (breaking API changes, no release available with the fix):
- Run `cargo add h2@0.4.5` to add h2 as a direct dependency, overriding the transitive resolution
- This forces h2 to 0.4.5 regardless of what reqwest/hyper request
- Document why the direct dep bump was not viable in the PR description

Full dependency chain for reference:
```
backend (workspace) -> reqwest -> hyper -> h2
```

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.5
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8060 (parent tracking issue)

---

**Post-creation steps** (proposed, not executed):

1. Re-fetch task description via `jira.get_issue(<upstream-task-key>, fields=["description"])`
2. Compute SHA-256 digest using `python3 scripts/sha256-digest.py /tmp/task-desc.md`
3. Post digest comment: `[sdlc-workflow] Description digest: sha256-md:<hex-digest>` (or sha256-adf:<hex-digest>)
4. Create Depend link: `jira.create_link(inwardIssue: TC-8060, outwardIssue: <upstream-task-key>, type: "Depend")`

---

### Task 2: Downstream Propagation Subtask

**Proposed** `jira.create_issue` (not executed -- eval mode):

- **Project**: TC
- **Issue Type**: Task
- **Summary**: Propagate CVE-2026-99010 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
- **Labels**: `["ai-generated-jira", "Security", "CVE-2026-99010"]`

**Description:**

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-99010 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.5 (via reqwest bump or direct pinning) on release/0.4.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: transitive (chain: backend -> reqwest -> hyper -> h2) -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned h2 directly (fallback approach via `cargo add h2@0.4.5`), verify the pinning is reflected in the downstream build's lock file after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8060 (parent tracking issue)

---

**Post-creation steps** (proposed, not executed):

1. Re-fetch task description via `jira.get_issue(<downstream-task-key>, fields=["description"])`
2. Compute SHA-256 digest using `python3 scripts/sha256-digest.py /tmp/task-desc.md`
3. Post digest comment: `[sdlc-workflow] Description digest: sha256-md:<hex-digest>` (or sha256-adf:<hex-digest>)
4. Create Blocks link: `jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")`
5. Create Depend link: `jira.create_link(inwardIssue: TC-8060, outwardIssue: <downstream-task-key>, type: "Depend")`

---

## Post-Triage Summary

**Proposed actions** (not executed -- eval mode):

1. Add `ai-cve-triaged` label to TC-8060
2. Post summary comment to TC-8060 documenting:
   - Version impact table (2.2.0, 2.2.1, 2.2.2 affected; 2.2.3, 2.2.4 not affected)
   - Affects Versions correction (if applicable)
   - Triage outcome: remediation tasks created
   - Dependency chain: h2 is transitive via reqwest -> hyper -> h2 (3 levels deep)
   - Links to upstream and downstream remediation tasks
   - @mention of reporter (psirt-analyst, account ID: 557058:psirt-analyst-mock-id) using ADF mention node:
     ```json
     { "type": "mention", "attrs": { "id": "557058:psirt-analyst-mock-id", "text": "@psirt-analyst" } }
     ```
   - Comment Footnote:
     ---
     This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.12.3.
3. Transition TC-8060 to In Progress (if not already)
