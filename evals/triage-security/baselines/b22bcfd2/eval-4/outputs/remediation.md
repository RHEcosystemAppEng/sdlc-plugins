# Step 8 -- Remediation

## Triage Decision

### Case A: Affected -- create remediation tasks

The version impact analysis shows **mixed results across streams**:
- **Stream 2.1.x**: ALL versions affected (h2 0.4.5, below fix threshold 0.4.8)
- **Stream 2.2.x**: ALL versions NOT affected (h2 >= 0.4.8, at or above fix threshold)

Since this issue is **unscoped** (no stream suffix), it covers all streams by definition. Remediation tasks are created only for the **affected stream (2.1.x)**. No remediation is needed for 2.2.x, which already ships the patched version.

**Cross-stream impact notice is NOT generated** because this issue is unscoped -- it covers all streams by definition. Case B (cross-stream impact) applies only to scoped issues where other streams outside the issue's scope are also affected.

### Step 4 -- Duplicate/Sibling Check

JQL search for sibling issues with label `CVE-2026-33501` returned no results (as stated in the eval). No duplicates or siblings exist. Proceeding to remediation.

### Step 4.3 -- Cross-CVE Overlap Detection

No Upstream Affected Component custom field is configured in the Security Configuration, so Step 4.3 is skipped.

### Step 7 -- Concurrent Triage Detection

No Upstream Affected Component custom field is configured in the Security Configuration, so Step 7 is skipped. Proceeding to Case A/B/C branching.

---

## Remediation Tasks for Stream 2.1.x

Since h2 is a **Cargo** (source dependency) ecosystem, two tasks are created per Important Rule 8: an upstream backport task and a downstream propagation subtask with a Blocks dependency.

### Task 1: Upstream Backport Task

**Proposed Jira Issue Creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (rhtpa-2.1)",
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

Affected versions: RHTPA 2.1.0 (v0.3.8, h2 0.4.5), RHTPA 2.1.1 (v0.3.12, h2 0.4.5)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- h2 is a transitive dependency via hyper -- the bump may require
  updating hyper or another intermediate crate
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)
```

**Post-creation steps (proposed):**

1. Re-fetch the created task's description from Jira: `jira.get_issue(<upstream-task-key>, fields=["description"])`
2. Compute SHA-256 digest of the re-fetched description using `python3 scripts/sha256-digest.py /tmp/task-desc.md`
3. Post digest comment **before** creating issue links: `jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`
4. Create Depend link to vulnerability issue: `jira.create_link(inwardIssue: "TC-8004", outwardIssue: <upstream-task-key>, type: "Depend")`

---

### Task 2: Downstream Propagation Subtask

**Proposed Jira Issue Creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
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
CVE-2026-33501 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps h2 to 0.4.8
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

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

**Post-creation steps (proposed):**

1. Re-fetch the created task's description from Jira: `jira.get_issue(<downstream-task-key>, fields=["description"])`
2. Compute SHA-256 digest of the re-fetched description using `python3 scripts/sha256-digest.py /tmp/task-desc.md`
3. Post digest comment **before** creating issue links: `jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`
4. Create Depend link to vulnerability issue: `jira.create_link(inwardIssue: "TC-8004", outwardIssue: <downstream-task-key>, type: "Depend")`
5. Create Blocks link from upstream to downstream: `jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")`

---

## No Remediation for Stream 2.2.x

Stream 2.2.x is **not affected** -- all versions (2.2.0 through 2.2.4) ship h2 >= 0.4.8, which is at or above the fix threshold. No remediation tasks are created for this stream.

---

## Post-Triage Summary (Proposed)

### 1. Add label

Propose adding the `ai-cve-triaged` label to TC-8004.

### 2. Post summary comment to TC-8004

```
Triage summary for CVE-2026-33501 (h2 < 0.4.8):

Version Impact Table:

| Version | Stream | h2 version | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.1.1 | 2.1.x | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.2.0 | 2.2.x | 0.4.8 | NO | >= 0.4.8 |
| 2.2.1 | 2.2.x | 0.4.8 | NO | >= 0.4.8 |
| 2.2.2 | 2.2.x | -- | NO | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.4.9 | NO | >= 0.4.8 |
| 2.2.4 | 2.2.x | 0.4.9 | NO | >= 0.4.8 |

Affects Versions corrected: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]

Triage outcome: Remediation required for stream 2.1.x only.
Stream 2.2.x already ships h2 >= 0.4.8 -- no fix needed.

Remediation tasks created:
- <upstream-task-key> (upstream backport: bump h2 in rhtpa-backend on release/0.3.z)
- <downstream-task-key> (downstream propagation: update rhtpa-backend ref in rhtpa-release.0.3.z, blocked by <upstream-task-key>)

@<reporter-name> (ADF mention node with reporter account ID from Jira issue)

---
_Comment posted by `sdlc-workflow:triage-security`_
```

### 3. Propose transitioning TC-8004 to In Progress

### 4. Propose assigning TC-8004 to current user
