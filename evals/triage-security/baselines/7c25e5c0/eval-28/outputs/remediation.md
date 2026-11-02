# Step 8 — Remediation (Case B: Affected versions exist)

## Triage Outcome

Versions 2.2.0 through 2.2.2 are affected (h2 0.4.4 < 0.4.5 fix threshold).
Versions 2.2.3 and 2.2.4 are not affected.

**Decision**: Create remediation tasks for the 2.2.x stream (Case B).

Since the upstream branch `release/0.4.z` already ships h2 >= 0.4.5 (Step 2.5 confirms fix is available), use the **dependency bump** variant rather than the upstream backport variant.

Cargo is a source dependency ecosystem → **2 tasks**: dependency bump + downstream propagation.

---

## Task 1: Dependency Bump Task (upstream)

**Proposed Jira creation (not executed — eval mode):**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-99010: update h2 to 0.4.5 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99010"]
)
```

### Task Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99010: bump h2 to 0.4.5 via dependency update.
The vulnerable dependency (h2 < 0.4.5) is already fixed upstream —
a package manager update is sufficient.

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5 (2.2.0), v0.4.8 (2.2.1), v0.4.8 (2.2.2, retag of 2.2.1)

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99010

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend → reqwest → hyper → h2, 3 levels deep)

### Remediation approach (transitive dependency)

The vulnerable package h2 is a **transitive** dependency pulled in through
intermediate packages. Use a two-tier approach:

**Preferred: bump the direct dependency (reqwest)**
- Identify that reqwest (direct dependency) pulls in h2 through hyper
- Bump reqwest to a version whose transitive closure includes h2 >= 0.4.5
- Run `cargo update -p reqwest` to pull in the latest compatible version
- Verify the lock file reflects h2 >= 0.4.5 after the update
- Verify the bump does not introduce breaking API changes to reqwest

**Fallback: pin h2 directly**
If bumping reqwest is not viable (breaking API changes, no release available
with the fix):
- Cargo: `cargo add h2@0.4.5` to add as a direct dependency, overriding
  the transitive resolution
- Document why the direct dep bump was not viable in the PR description

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.5
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8060 (parent tracking issue)

---

### Post-creation procedures for Task 1

**Description digest protocol (proposed — not executed):**
1. After `create_issue`, re-fetch the task description from Jira: `jira.get_issue(<task-key>, fields=["description"])`
2. Write the re-fetched description to a temp file
3. Compute SHA-256 digest: `python3 scripts/sha256-digest.py /tmp/task-desc.md`
4. Post digest comment: `jira.add_comment(<task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`
5. The digest comment is posted BEFORE creating issue links or other comments

**Jira linkage:**
- `jira.create_link(inwardIssue: TC-8060, outwardIssue: <task-key>, type: "Depend")`

---

## Task 2: Downstream Propagation Subtask

**Proposed Jira creation (not executed — eval mode):**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-99010 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99010"]
)
```

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99010 fix from the upstream dependency bump task.

The upstream task bumps h2 to 0.4.5
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag)
- **Dependency type**: transitive — carried forward from upstream task
- Dependency chain: backend → reqwest → hyper → h2
- Update the backend reference to the merged commit or new release tag
- If the upstream fix pinned h2 directly (fallback approach), verify the
  pinning is reflected in the downstream build's lock file after the source
  reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-bump-task-key> (upstream dependency bump must merge first)
- Depends on: TC-8060 (parent tracking issue)

---

### Post-creation procedures for Task 2

**Description digest protocol (proposed — not executed):**
1. After `create_issue`, re-fetch the task description from Jira: `jira.get_issue(<task-key>, fields=["description"])`
2. Write the re-fetched description to a temp file
3. Compute SHA-256 digest: `python3 scripts/sha256-digest.py /tmp/task-desc.md`
4. Post digest comment: `jira.add_comment(<task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`
5. The digest comment is posted BEFORE creating issue links or other comments

**Jira linkage:**
- `jira.create_link(inwardIssue: TC-8060, outwardIssue: <downstream-task-key>, type: "Depend")`
- `jira.create_link(inwardIssue: <upstream-bump-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")`

---

## Post-Triage Summary

**Proposed actions (not executed — eval mode):**

1. Add `ai-cve-triaged` label to TC-8060
2. Post summary comment to TC-8060 with:
   - Version impact table
   - Affects Versions correction: Current [RHTPA 2.2.0] → Proposed [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
   - Triage outcome: remediation tasks created (dependency bump + downstream propagation)
   - Links to created tasks
   - @mention of reporter psirt-analyst (ADF mention node with account ID 557058:psirt-analyst-mock-id)
   - Comment Footnote
3. Transition TC-8060 to In Progress
