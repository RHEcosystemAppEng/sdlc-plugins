# Step 7 -- Remediation: TC-8004

## Triage Outcome

**Case A: Affected -- create remediation tasks** for the 2.1.x stream only.

The version impact analysis shows:
- **2.1.x stream**: ALL versions affected (2.1.0 and 2.1.1 ship h2 0.4.5, below fix threshold 0.4.8)
- **2.2.x stream**: NO versions affected (all ship h2 >= 0.4.8)

Since the issue is **unscoped** (no stream suffix), there is no cross-stream impact notice to generate. The unscoped issue already covers all streams, so Case B (cross-stream impact) does not apply. Remediation tasks are created only for streams that are actually affected.

No sibling issues exist (JQL returns empty). No preemptive tasks to reconcile.

## Remediation Tasks -- 2.1.x Stream

The ecosystem is **Cargo** (source dependency), so two tasks are required:

### Task 1: Upstream Backport (source repo fix)

**Proposed Jira issue creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

**Task description:**

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed
version (0.4.8+).

Affected versions: RHTPA 2.1.0 (v0.3.8), RHTPA 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
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

**Post-creation:** Post description digest comment per `shared/description-digest-protocol.md`.

### Task 2: Downstream Propagation (Konflux release repo update)

**Proposed Jira issue creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

**Task description:**

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that
PR merges, update the source pinning in this Konflux release repo so
the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
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
```

**Post-creation:** Post description digest comment per `shared/description-digest-protocol.md`.

## Proposed Jira Linkage

After creating both tasks:

1. **Link upstream task to TC-8004:**
   ```
   jira.create_link(inwardIssue: "TC-8004", outwardIssue: <upstream-task-key>, type: "Depend")
   ```

2. **Link downstream task to TC-8004:**
   ```
   jira.create_link(inwardIssue: "TC-8004", outwardIssue: <downstream-task-key>, type: "Depend")
   ```

3. **Link downstream blocked by upstream:**
   ```
   jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
   ```

4. **Transition TC-8004 to In Progress**

5. **Assign TC-8004 to current user**

6. **Add `ai-cve-triaged` label to TC-8004**

## No Remediation for 2.2.x Stream

The 2.2.x stream does not require remediation. All versions in the 2.2.x stream ship h2 >= 0.4.8 (the fixed version):

| Version | h2 version | Status |
|---------|------------|--------|
| 2.2.0 | 0.4.8 | Not affected |
| 2.2.1 | 0.4.8 | Not affected |
| 2.2.2 | _(retag)_ | Not affected |
| 2.2.3 | 0.4.9 | Not affected |
| 2.2.4 | 0.4.9 | Not affected |

No tasks are created for this stream.

## Post-Triage Summary (Proposed Comment on TC-8004)

```
Triage complete for CVE-2026-33501 (h2 < 0.4.8).

Version Impact:

| Version | Stream | h2 | Affected? |
|---------|--------|----|-----------|
| 2.1.0 | 2.1.x | 0.4.5 | YES |
| 2.1.1 | 2.1.x | 0.4.5 | YES |
| 2.2.0 | 2.2.x | 0.4.8 | NO |
| 2.2.1 | 2.2.x | 0.4.8 | NO |
| 2.2.2 | 2.2.x | (retag) | NO |
| 2.2.3 | 2.2.x | 0.4.9 | NO |
| 2.2.4 | 2.2.x | 0.4.9 | NO |

Affects Versions corrected: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]
- Removed RHTPA 2.2.0 (ships h2 0.4.8, not affected)
- Added RHTPA 2.1.1 (ships h2 0.4.5, affected)

Remediation tasks created for 2.1.x stream:
- <upstream-task-key>: Upstream backport -- bump h2 to 0.4.8 on release/0.3.z
- <downstream-task-key>: Downstream propagation -- update backend ref in rhtpa-release.0.3.z
  (blocked by <upstream-task-key>)

No remediation needed for 2.2.x stream (all versions ship h2 >= 0.4.8).
```
