# Step 7.5 -- Release Jira Orchestration

## Release Orchestration Analysis

### Stream 2.2.x (in-scope stream)

The 2.2.x stream has affected versions (2.2.0, 2.2.1, 2.2.2) but the fix is
already present in versions 2.2.3 and 2.2.4 (which ship quinn-proto 0.11.14).
The upstream branch `release/0.4.z` already has the fix. No remediation tasks
are needed for the 2.2.x stream, so no release Jira structure is required.

### Stream 2.1.x (cross-stream, Case A)

All versions in the 2.1.x stream are affected (2.1.0, 2.1.1). The upstream
branch `release/0.3.z` does NOT have the fix. Remediation is needed.

However, remediation tasks for the 2.1.x stream are **preemptive** (created
via Case A cross-stream impact, since no sibling CVE Jira exists for 2.1.x).
Per Step 7.5: "This step applies to all non-preemptive remediation types."
Preemptive tasks are excluded from release Jira linking. Therefore, release
Jira orchestration does not apply to the preemptive 2.1.x remediation tasks.

### Confirmation decisions (proposed, not executed)

If release Jira orchestration were applicable:

- **2.1.x stream**: latest released version is 2.1.1. Next patch would be
  RHTPA 2.1.2. Would propose creating:
  - Release Epic: "RHTPA 2.1.2 Release Tasks"
  - Release Task: "RHTPA 2.1.2 CVE triage" (child of release Epic)
  - Engineer confirmation required for both Epic and Task creation

- **2.2.x stream**: latest released version is 2.2.4. Next patch would be
  RHTPA 2.2.5. However, since no remediation tasks are needed (fix already
  shipped), no release Epic or Task would be created.

### Step 7.5.3 -- Cross-CVE Dedup Decision

The Upstream Affected Component custom field is **not configured** in Security
Configuration. Per Step 7.5.3 prerequisite: "Requires the Upstream Affected
Component custom field to be configured. If not configured, skip dedup and
proceed to Step 8."

**Decision**: Dedup check is skipped entirely. Proceeding directly to Step 8
remediation task creation.

---

# Step 8 -- Remediation

## Triage Decision Tree

1. **Any supported versions affected?** YES -- versions 2.1.0, 2.1.1, 2.2.0,
   2.2.1, 2.2.2 are all affected.
2. **Issue scoped to a single stream?** YES -- scoped to 2.2.x via `[rhtpa-2.2]`.
3. **Other streams also affected?** YES -- 2.1.x stream is also affected
   (all versions).
4. **Case A applies**: Cross-stream impact detected. Post cross-stream impact
   comment and create preemptive remediation tasks for the 2.1.x stream.

## 2.2.x Stream (In-Scope) -- No Remediation Needed

Within the scoped 2.2.x stream, the fix was already shipped starting from
version 2.2.3 (quinn-proto 0.11.14). The upstream branch `release/0.4.z`
already contains the fix (confirmed by Step 2.5). No new remediation tasks
are needed for the 2.2.x stream.

The Affects Versions have been corrected (Step 3) to document that versions
2.2.0, 2.2.1, and 2.2.2 were affected. Customers on those versions should
upgrade to 2.2.3 or later.

## 2.1.x Stream (Cross-Stream, Case A) -- Preemptive Remediation

The 2.1.x stream does not have its own CVE Jira for CVE-2026-31812. All
versions in this stream (2.1.0, 2.1.1) ship quinn-proto 0.11.9, which is
within the affected range (< 0.11.14). The upstream branch `release/0.3.z`
does NOT have the fix.

### Cross-Stream Impact Comment (proposed, not executed)

The following comment would be posted to TC-8001:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis.

2.1.x versions affected:
- 2.1.0: quinn-proto 0.11.9 (via backend tag v0.3.8)
- 2.1.1: quinn-proto 0.11.9 (via backend tag v0.3.12)

This stream is not tracked by a companion CVE Jira issue.
Preemptive remediation tasks will be created.
```

### Preemptive Remediation Task 1: Upstream Backport (2.1.x)

**Type**: Upstream backport task (source dependency ecosystem, fix NOT
available on upstream branch release/0.3.z)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link type**: Related (to TC-8001, the originating CVE Jira from 2.2.x stream)

**Proposed summary**:
```
Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)
```

**Proposed description**:

```markdown
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (DoS).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated to the
fixed version (0.11.14+).

Affected versions: 2.1.0 (backend v0.3.8), 2.1.1 (backend v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: transitive (chain: backend -> quinn -> quinn-proto)
- The fix is NOT yet available on the release/0.3.z branch. An upstream
  backport is required to bump quinn-proto to >= 0.11.14.

### Remediation approach (transitive dependency)

The vulnerable package quinn-proto is a transitive dependency pulled in
through the quinn crate.

**Preferred: bump the direct dependency**
- Identify the version of quinn whose transitive closure includes
  quinn-proto >= 0.11.14
- Bump quinn to that version in Cargo.toml on the release/0.3.z branch
- Verify the bump does not introduce breaking API changes

**Fallback: pin the transitive dependency directly**
If bumping quinn is not viable (breaking API changes, no compatible release):
- Run `cargo add quinn-proto@0.11.14` to add as a direct dependency,
  overriding the transitive resolution
- Document why the direct dep bump was not viable in the PR description

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8001 (originating CVE Jira, stream 2.2.x)
```

### Preemptive Remediation Task 2: Downstream Propagation (2.1.x)

**Type**: Downstream propagation subtask (blocked by upstream backport task)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link type**: Related (to TC-8001, the originating CVE Jira)

**Proposed summary**:
```
Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)
```

**Proposed description**:

```markdown
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-31812
fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14 on release/0.3.z. Once
that PR merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag,
  e.g., `v0.3.12`)
- **Dependency type**: transitive -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully
- Since the upstream fix pinned a transitive dependency (quinn-proto via quinn),
  verify the pinning is reflected in the downstream build's Cargo.lock after
  the source reference update

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Blocked by: upstream backport task (upstream backport must merge first)
- Related to: TC-8001 (originating CVE Jira, stream 2.2.x)
```

## Proposed Jira Operations (not executed)

### Task Creation

```
# 1. Create upstream backport task (preemptive, 2.1.x)
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)",
  description: <upstream-task-description-above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)

# 1a. Post description digest comment (before links)
# python3 scripts/sha256-digest.py /tmp/task-desc.md -> sha256-md:<hex> or sha256-adf:<hex>
# jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")

# 2. Create downstream propagation task (preemptive, 2.1.x)
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <downstream-task-description-above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)

# 2a. Post description digest comment (before links)
# python3 scripts/sha256-digest.py /tmp/task-desc.md -> sha256-md:<hex> or sha256-adf:<hex>
# jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
```

### Jira Linkage

```
# Link upstream backport task to TC-8001 (Related, preemptive)
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <upstream-task-key>,
  type: "Related"
)

# Link downstream propagation task to TC-8001 (Related, preemptive)
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <downstream-task-key>,
  type: "Related"
)

# Link downstream task as blocked by upstream task
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)
```

### Preemptive Task Comment on TC-8001

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <upstream-task-key> (upstream backport, security-preemptive)
- 2.1.x: <downstream-task-key> (downstream propagation, security-preemptive,
  blocked by <upstream-task-key>)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates a stream-specific CVE Jira for 2.1.x, Step 4.4
reconciliation will link them and remove the label.
```

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks for the 2.1.x stream (source
  dependency ecosystem: upstream backport + downstream propagation). Matches
  the ecosystem classification table.
- [x] **Cross-stream coverage**: the 2.1.x stream (outside the issue's 2.2.x
  scope) is covered by preemptive remediation tasks. No sibling CVE Jira
  exists for 2.1.x.
- [x] **Link types**: "Related" for preemptive tasks linked to TC-8001
  (another stream's CVE Jira). "Blocks" from upstream to downstream within
  the 2.1.x stream.
- [x] **Preemptive labels**: both tasks carry the `security-preemptive` label
  since no CVE Jira exists for the 2.1.x stream.
- [x] **Coordination guidance**: each task includes upstream coordination
  guidance (deployment context: upstream).
- [x] **Release Jira linking**: not applicable -- preemptive tasks are
  excluded from release Jira linking per Step 7.5 scope.
- [x] **Dedup consistency**: dedup check was skipped (no Upstream Affected
  Component field configured). No dedup conflicts.

## Post-Triage Summary (proposed, not executed)

After all triage actions, the following would be posted to TC-8001:

1. **Add label**: `ai-cve-triaged` to TC-8001
2. **Post summary comment** to TC-8001:

```
CVE-2026-31812 Triage Summary -- quinn-proto < 0.11.14 (DoS)

Version Impact:

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | |
| 2.1.1 | 0.11.9 | YES | |
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | fixed |
| 2.2.4 | 0.11.14 | NO | fixed |

Affects Versions Correction:
[RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
(scoped to 2.2.x per issue suffix)

Triage Outcome:
- 2.2.x stream: fix already shipped in 2.2.3+ (quinn-proto 0.11.14).
  No remediation tasks needed.
- 2.1.x stream (cross-stream impact): preemptive remediation tasks created:
  - <upstream-task-key> (upstream backport: bump quinn-proto on release/0.3.z)
  - <downstream-task-key> (downstream propagation: update backend ref in
    rhtpa-release.0.3.z, blocked by upstream task)
```
