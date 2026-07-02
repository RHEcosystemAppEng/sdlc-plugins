# Step 8 -- Remediation: TC-8004

## Triage Outcome

**Case A: Affected -- create remediation tasks for stream 2.1.x only.**

The version impact analysis shows:
- **2.1.x**: ALL versions affected (h2 0.4.5, below fix threshold 0.4.8) --> needs remediation
- **2.2.x**: NO versions affected (h2 >= 0.4.8, at or above fix threshold) --> no remediation needed

Since only stream 2.1.x is affected and stream 2.2.x is not affected, there is no
cross-stream impact (Case B does not apply). Remediation tasks are created for the
2.1.x stream only.

The ecosystem is **Cargo** (source dependency), so **two tasks** are required:
1. Upstream backport task (fix in the source repo)
2. Downstream propagation subtask (update the reference in the Konflux release repo)

---

## PROPOSAL: Remediation Task 1 -- Upstream Backport (2.1.x)

### Jira Issue Creation

```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

### Task Description

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: memory exhaustion via CONTINUATION frames in h2.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version
(0.4.8+).

Affected versions: RHTPA 2.1.0 (v0.3.8), RHTPA 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- h2 is a transitive dependency via hyper -- a direct bump of h2
  may require updating hyper or adjusting dependency constraints
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)
```

### Post-Creation Actions

```
# Post description digest comment
upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
python3 scripts/sha256-digest.py /tmp/task-desc.md
jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")

# Link to vulnerability issue
jira.create_link(
  inwardIssue: "TC-8004",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)
```

---

## PROPOSAL: Remediation Task 2 -- Downstream Propagation (2.1.x)

### Jira Issue Creation

```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)",
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

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps h2 to 0.4.8
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
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

### Post-Creation Actions

```
# Post description digest comment
downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
python3 scripts/sha256-digest.py /tmp/task-desc.md
jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")

# Link to vulnerability issue
jira.create_link(
  inwardIssue: "TC-8004",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)

# Link downstream blocked by upstream
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)
```

---

## PROPOSAL: Post-Triage Actions

### 1. Add ai-cve-triaged label

```
jira.edit_issue("TC-8004", fields={
  "labels": ["CVE-2026-33501", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### 2. Post summary comment

```
jira.add_comment("TC-8004",
  "## Triage Summary for CVE-2026-33501

  **Vulnerability**: h2 < 0.4.8 -- memory exhaustion via CONTINUATION frames
  **CVSS**: 7.5 (High)
  **Fix threshold**: h2 >= 0.4.8

  ### Version Impact

  | Version | Stream | h2 version | Affected? |
  |---------|--------|------------|-----------|
  | 2.1.0   | 2.1.x  | 0.4.5      | YES       |
  | 2.1.1   | 2.1.x  | 0.4.5      | YES       |
  | 2.2.0   | 2.2.x  | 0.4.8      | NO        |
  | 2.2.1   | 2.2.x  | 0.4.8      | NO        |
  | 2.2.2   | 2.2.x  | --         | NO (retag of 2.2.1) |
  | 2.2.3   | 2.2.x  | 0.4.9      | NO        |
  | 2.2.4   | 2.2.x  | 0.4.9      | NO        |

  ### Affects Versions Correction

  [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]
  - Added RHTPA 2.1.1 (affected, was missing)
  - Removed RHTPA 2.2.0 (not affected -- ships h2 0.4.8)

  ### Triage Outcome

  **Case A**: Stream 2.1.x affected. Stream 2.2.x not affected.

  Remediation tasks created:
  - <upstream-task-key>: upstream backport -- bump h2 to >= 0.4.8 on release/0.3.z
  - <downstream-task-key>: downstream propagation -- update backend ref in rhtpa-release.0.3.z (blocked by <upstream-task-key>)

  No remediation needed for stream 2.2.x (all versions ship h2 >= 0.4.8).

  @<reporter-mention>

  ---
  _This comment was generated by the triage-security skill in the sdlc-workflow plugin._")
```

### 3. Transition to In Progress

```
jira.get_transitions("TC-8004")
# Select transition whose target status is "In Progress"
jira.transition_issue("TC-8004", <in-progress-transition-id>)
```
