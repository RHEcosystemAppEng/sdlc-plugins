# Step 7 -- Remediation: TC-8004

## Triage Outcome

**Case A: Affected -- create remediation tasks** (for stream 2.1.x only).

The version impact analysis shows:
- **Stream 2.1.x**: ALL versions affected (2.1.0, 2.1.1 ship h2 0.4.5, below fix threshold 0.4.8)
- **Stream 2.2.x**: NO versions affected (all ship h2 >= 0.4.8)

Since 2.2.x is not affected, there is no Case B cross-stream impact to report. The vulnerability only impacts the 2.1.x stream.

## Steps 4-6 Summary

### Step 4 -- Duplicate, Sibling, and Overlap Check

PROPOSED JQL query:
```
project = TC AND labels = 'CVE-2026-33501' AND issuetype = 10024 AND key != TC-8004
```

Result: **No sibling issues found.** No duplicates or companion trackers exist for this CVE.

Step 4.4 -- Preemptive task reconciliation:

PROPOSED JQL query:
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-33501' ORDER BY created DESC
```

Result: **No preemptive tasks found.** Proceeding with new remediation task creation.

### Step 5 -- Version Lifecycle Check

PROPOSED: Fetch product lifecycle page at `https://access.example.com/product-life-cycle/rhtpa` to verify support status.

Assumed status (pending lifecycle page verification):
- RHTPA 2.1.x: supported (active or maintenance)
- RHTPA 2.2.x: supported (active)

All affected versions are assumed to be within support lifecycle. Proceed to Step 6.

### Step 6 -- Already Fixed Check

No resolved sibling issues found in Step 4. Nothing to cross-reference. Proceed to Step 7.

## Remediation Task Creation

The ecosystem is **Cargo** (source dependency), so **two tasks** are required per the skill definition:
1. **Upstream backport task** -- bump h2 in the source repo on `release/0.3.z`
2. **Downstream propagation subtask** -- update the source reference in the Konflux release repo

Remediation is scoped to **stream 2.1.x only** (the only affected stream).

---

### Task 1: Upstream Backport (Source Repo Fix)

**PROPOSED Jira Issue Creation:**

```
PROPOSED: jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

**Task Description:**

```markdown
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 - Memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (tag v0.3.8, h2 0.4.5), RHTPA 2.1.1 (tag v0.3.12, h2 0.4.5)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock (and Cargo.toml if directly specified)
- Target branch: release/0.3.z
- h2 is a transitive dependency via hyper -- the bump may require updating hyper
  or adjusting version constraints in Cargo.toml
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)
- The fix adds a configurable maximum header list size defaulting to 16 KiB

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)
```

---

### Task 2: Downstream Propagation (Konflux Release Repo Update)

**PROPOSED Jira Issue Creation:**

```
PROPOSED: jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

**Task Description:**

```markdown
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from the upstream backport task.

The upstream backport bumps h2 to >= 0.4.8 on release/0.3.z. Once that PR merges,
update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

---

## PROPOSED Jira Linkage

After task creation, the following links would be created:

### 1. Link upstream task to Vulnerability issue

```
PROPOSED: jira.create_link(
  inwardIssue: "TC-8004",
  outwardIssue: "<upstream-task-key>",
  type: "Depend"
)
```

### 2. Link downstream subtask to Vulnerability issue

```
PROPOSED: jira.create_link(
  inwardIssue: "TC-8004",
  outwardIssue: "<downstream-task-key>",
  type: "Depend"
)
```

### 3. Link downstream subtask as blocked by upstream task

```
PROPOSED: jira.create_link(
  inwardIssue: "<upstream-task-key>",
  outwardIssue: "<downstream-task-key>",
  type: "Blocks"
)
```

### 4. Transition Vulnerability to In Progress

```
PROPOSED: jira.transition_issue("TC-8004", status="In Progress")
```

### 5. Assign Vulnerability to current user

```
PROPOSED: jira.edit_issue("TC-8004", fields={"assignee": {"accountId": "<current-user>"}})
```

## PROPOSED Post-Triage Actions

### Add ai-cve-triaged label

```
PROPOSED: jira.edit_issue("TC-8004", fields={
  "labels": ["CVE-2026-33501", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### Post summary comment

```
PROPOSED: jira.add_comment("TC-8004",
  "## Triage Summary for CVE-2026-33501

  ### Version Impact

  | Version | Stream | h2 version | Affected? | Notes |
  |---------|--------|------------|-----------|-------|
  | 2.1.0 | 2.1.x | 0.4.5 | YES | ships vulnerable h2 |
  | 2.1.1 | 2.1.x | 0.4.5 | YES | ships vulnerable h2 |
  | 2.2.0 | 2.2.x | 0.4.8 | NO | ships fixed version |
  | 2.2.1 | 2.2.x | 0.4.8 | NO | ships fixed version |
  | 2.2.2 | 2.2.x | -- | NO | retag of 2.2.1 |
  | 2.2.3 | 2.2.x | 0.4.9 | NO | above fix threshold |
  | 2.2.4 | 2.2.x | 0.4.9 | NO | above fix threshold |

  ### Affects Versions Correction

  [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]
  - Removed RHTPA 2.2.0: ships h2 0.4.8 (fix version)
  - Added RHTPA 2.1.1: ships h2 0.4.5 (vulnerable)

  ### Triage Outcome

  Affected -- remediation tasks created for stream 2.1.x:
  - <upstream-task-key>: upstream backport (bump h2 to >= 0.4.8 on release/0.3.z)
  - <downstream-task-key>: downstream propagation (update rhtpa-backend ref in rhtpa-release.0.3.z, blocked by upstream task)

  Stream 2.2.x is NOT affected -- all versions ship h2 >= 0.4.8.

  ---
  _Generated by triage-security skill | Claude Code SDLC Workflow_"
)
```

## Why No Remediation for 2.2.x

The 2.2.x stream requires **no remediation tasks** because:
- RHTPA 2.2.0 ships h2 0.4.8 (exactly the fix version)
- RHTPA 2.2.1 ships h2 0.4.8
- RHTPA 2.2.2 is a retag of 2.2.1 (same h2 0.4.8)
- RHTPA 2.2.3 and 2.2.4 ship h2 0.4.9 (above fix threshold)

All versions in the 2.2.x stream ship h2 at or above the fix threshold of 0.4.8. No Case B cross-stream impact notification is needed because the other stream (2.2.x) is not affected.
