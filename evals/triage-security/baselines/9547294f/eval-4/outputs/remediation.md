# Step 8 -- Remediation for TC-8004

## Triage Decision

**Case A: Affected -- create remediation tasks** for stream 2.1.x only.

The version impact analysis shows mixed results:
- **Stream 2.1.x**: AFFECTED (all versions ship h2 0.4.5, below fix threshold 0.4.8)
- **Stream 2.2.x**: NOT AFFECTED (all versions ship h2 >= 0.4.8)

Remediation tasks are created **only for the affected stream (2.1.x)**. No remediation is needed for 2.2.x, which already ships the patched version.

### Cross-stream impact notice

A cross-stream impact notice is **NOT generated** for this issue because it is **unscoped** -- an unscoped issue covers all streams by definition. Cross-stream impact notices (Step 8 Case B) apply only to scoped issues where the triage reveals impact outside the issue's declared stream scope. Since TC-8004 has no stream suffix, there is no "outside scope" to report.

## Ecosystem: Cargo (Source Dependency)

Since h2 is a Cargo (Rust) source dependency, remediation follows the two-task pattern: an upstream backport task and a downstream propagation subtask.

---

## Task 1: Upstream Backport Task (2.1.x stream)

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

```
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 - Memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (tag v0.3.8), RHTPA 2.1.1 (tag v0.3.12)
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

### Post-creation Linkage

```
jira.create_link(
  inwardIssue: "TC-8004",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)
```

---

## Task 2: Downstream Propagation Subtask (2.1.x stream)

### Proposed Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

### Task Description

```
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

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
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

### Post-creation Linkage

```
# Link downstream to vulnerability issue
jira.create_link(
  inwardIssue: "TC-8004",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)

# Link downstream as blocked by upstream
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)
```

---

## No Remediation for 2.2.x

Stream 2.2.x does **not** receive remediation tasks because the version impact table shows all 2.2.x versions ship h2 >= 0.4.8 (at or above the fix threshold). The patched dependency is already present in all 2.2.x releases.

## Post-Triage Actions

### 1. Add `ai-cve-triaged` label to TC-8004

```
jira.edit_issue("TC-8004", fields={
  "labels": ["CVE-2026-33501", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### 2. Proposed post-triage summary comment on TC-8004

The following summary comment would be posted to TC-8004 documenting the triage outcome:

```
## Triage Summary for CVE-2026-33501 (h2 < 0.4.8)

### Version Impact

| Version | Stream | h2 version | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.4.5 | YES | |
| 2.1.1 | 2.1.x | 0.4.5 | YES | |
| 2.2.0 | 2.2.x | 0.4.8 | NO | at fix threshold |
| 2.2.1 | 2.2.x | 0.4.8 | NO | at fix threshold |
| 2.2.2 | 2.2.x | -- | NO | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.4.9 | NO | |
| 2.2.4 | 2.2.x | 0.4.9 | NO | |

### Affects Versions Correction

[RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]

### Triage Outcome

Remediation tasks created for stream 2.1.x only (2.2.x ships the fix):
- <upstream-task-key> (upstream backport: bump h2 to 0.4.8 on release/0.3.z)
- <downstream-task-key> (downstream propagation: update rhtpa-backend ref in rhtpa-release.0.3.z, blocked by <upstream-task-key>)

---
_Comment generated by sdlc-workflow:triage-security_
```

### 3. Transition TC-8004 to In Progress
### 4. Assign TC-8004 to current user
