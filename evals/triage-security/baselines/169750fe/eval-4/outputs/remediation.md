# Step 8 -- Remediation: TC-8004

## Triage Decision

**Case B: Affected -- create remediation tasks**

The version impact analysis shows that 2.1.x versions are affected (ship h2 0.4.5 < 0.4.8) while 2.2.x versions are not affected (ship h2 >= 0.4.8). Since this is an **unscoped issue**, Case A (cross-stream impact notice) does **not** apply -- unscoped issues cover all streams by definition, so there are no "other streams outside this issue's scope."

Remediation tasks are created only for the **2.1.x stream**, which is the only affected stream.

No remediation is needed for the 2.2.x stream, as all versions already ship the fixed h2 version.

## Ecosystem and Task Count

- **Ecosystem**: Cargo (source dependency)
- **Tasks per affected stream**: 2 (upstream dependency bump + downstream propagation)
- **Total tasks**: 2 (for the 2.1.x stream only)

## Sibling and Duplicate Check

No sibling issues exist (JQL returns empty). No duplicates or overlapping remediation found.

## Remediation Task 1: Upstream Dependency Bump (2.1.x)

**Summary**: Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-33501`

### Task Description

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: bump h2 to 0.4.8 via dependency update.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

h2 versions before 0.4.8 are vulnerable to memory exhaustion caused by a peer
sending an excessive number of CONTINUATION frames following a HEADERS frame.

Affected versions: RHTPA 2.1.0 (build v0.3.8), RHTPA 2.1.1 (build v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: source dependency (Cargo crate)
- **Remediation action**: run `cargo update -p h2` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add h2@0.4.8`
- Verify the lock file reflects >= 0.4.8 after the update

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)
```

### Jira Creation

```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)",
  description: <upstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

### Linkage

```
jira.create_link(
  inwardIssue: "TC-8004",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)
```

---

## Remediation Task 2: Downstream Propagation (2.1.x)

**Summary**: Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-33501`

### Task Description

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from the upstream dependency bump task.

The upstream task bumps h2 to 0.4.8 on release/0.3.z. Once that PR merges,
update the source pinning in this Konflux release repo so the next build
ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag)
- **Dependency type**: source dependency -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream dependency bump must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

### Jira Creation

```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <downstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

### Linkage

```
# Link downstream to CVE
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

## Post-Triage Actions

### 1. Add `ai-cve-triaged` label

```
jira.edit_issue("TC-8004", { "labels": { "add": ["ai-cve-triaged"] } })
```

### 2. Post-triage summary comment on TC-8004

> **Triage Summary for CVE-2026-33501 (h2 < 0.4.8)**
>
> **Version Impact:**
>
> | Version | Stream | h2 version | Affected? |
> |---------|--------|------------|-----------|
> | 2.1.0 | 2.1.x | 0.4.5 | YES |
> | 2.1.1 | 2.1.x | 0.4.5 | YES |
> | 2.2.0 | 2.2.x | 0.4.8 | NO |
> | 2.2.1 | 2.2.x | 0.4.8 | NO |
> | 2.2.2 | 2.2.x | -- | NO (retag of 2.2.1) |
> | 2.2.3 | 2.2.x | 0.4.9 | NO |
> | 2.2.4 | 2.2.x | 0.4.9 | NO |
>
> **Affects Versions correction**: Removed RHTPA 2.2.0, added RHTPA 2.1.1.
> Corrected to: RHTPA 2.1.0, RHTPA 2.1.1.
>
> **Outcome**: Remediation tasks created for 2.1.x stream only.
> No remediation needed for 2.2.x stream (all versions ship h2 >= 0.4.8).
>
> **Remediation tasks**:
> - <upstream-task-key>: Upstream dependency bump -- bump h2 to 0.4.8 on release/0.3.z
> - <downstream-task-key>: Downstream propagation -- update backend ref in rhtpa-release.0.3.z (blocked by upstream task)
>
> Cross-stream impact notice: Not applicable (issue is unscoped -- covers all streams).

## What Was NOT Created

- **No remediation tasks for 2.2.x** -- all 2.2.x versions (2.2.0 through 2.2.4) ship h2 >= 0.4.8 and are not affected by this CVE.
- **No cross-stream impact notice** -- this is an unscoped issue covering all streams. Case A does not apply to unscoped issues.
- **No sibling issue links** -- JQL returned no sibling issues.
