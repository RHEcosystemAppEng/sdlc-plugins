# Step 8 -- Remediation

## Triage Outcome

**Case A + Case B**: The issue is scoped to stream 2.2.x, and stream 2.1.x is also affected. This triggers Case A (cross-stream impact notice) followed by Case B (remediation task creation).

Ecosystem classification: **Cargo** (source dependency) -- 2 tasks per stream (upstream backport + downstream propagation).

---

## Case A: Cross-Stream Impact Notice

The version impact analysis reveals that stream **2.1.x** (outside this issue's scope) is also affected. A cross-stream impact comment would be posted to TC-8001:

```
Cross-stream impact: quinn-proto (versions before 0.11.14) also affects
stream 2.1.x based on lock file analysis. Versions 2.1.0 and 2.1.1 both
ship quinn-proto 0.11.9, which is within the affected range.

These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

Since no sibling CVE Jira exists for stream 2.1.x (no companion issue with suffix `[rhtpa-2.1]` found in Step 4), **preemptive remediation tasks** are created for stream 2.1.x (see below).

---

## Case B: Remediation Tasks for Stream 2.2.x (In-Scope)

### Task 1: Upstream Backport (Stream 2.2.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)

**Labels**: ai-generated-jira, Security, CVE-2026-31812

**Link**: Depend -> TC-8001

```markdown
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0, 2.2.1, 2.2.2
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is retag of v0.4.8)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
- Note: quinn-proto 0.11.14 is already present at tags v0.4.11 and v0.4.12
  on this branch, so the fix is already available in newer commits. Verify
  the upstream branch HEAD already includes the fix before creating a new PR.

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

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

- Depends on: TC-8001 (parent tracking issue)
```

### Task 2: Downstream Propagation (Stream 2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: ai-generated-jira, Security, CVE-2026-31812

**Links**:
- Depend -> TC-8001
- Blocked by -> upstream backport task (Task 1 above)

```markdown
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14 on release/0.4.z.
Once that PR merges, update the source pinning in this Konflux release
repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

## Case A Preemptive Tasks: Stream 2.1.x (Out-of-Scope, No Sibling CVE Jira)

Since no sibling CVE Jira with suffix `[rhtpa-2.1]` exists for stream 2.1.x, preemptive remediation tasks are created with the `security-preemptive` label and "Related" link type to TC-8001.

### Task 3: Preemptive Upstream Backport (Stream 2.1.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)

**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

**Link**: Related -> TC-8001 (originating CVE Jira from stream 2.2.x)

```markdown
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for stream 2.1.x. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0, 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- Note: The upstream branch release/0.3.z still ships quinn-proto 0.11.9 at
  the latest tag (v0.3.12). An upstream backport PR is needed to bump
  quinn-proto to >= 0.11.14 on this branch.

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

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

- Depends on: TC-8001 (originating tracking issue, stream 2.2.x)
```

### Task 4: Preemptive Downstream Propagation (Stream 2.1.x)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

**Links**:
- Related -> TC-8001 (originating CVE Jira from stream 2.2.x)
- Blocked by -> preemptive upstream backport task (Task 3 above)

```markdown
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for stream 2.1.x. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the preemptive upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release
repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: preemptive upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (originating tracking issue, stream 2.2.x)
```

---

## Post-Triage Summary

### Comment to TC-8001

```
Triage complete for CVE-2026-31812 (quinn-proto < 0.11.14).

Version Impact:
| Stream | Version | quinn-proto | Affected? | Notes |
|--------|---------|-------------|-----------|-------|
| 2.1.x  | 2.1.0   | 0.11.9      | YES       |       |
| 2.1.x  | 2.1.1   | 0.11.9      | YES       |       |
| 2.2.x  | 2.2.0   | 0.11.9      | YES       |       |
| 2.2.x  | 2.2.1   | 0.11.12     | YES       |       |
| 2.2.x  | 2.2.2   | --          | YES       | retag of 2.2.1 |
| 2.2.x  | 2.2.3   | 0.11.14     | NO        |       |
| 2.2.x  | 2.2.4   | 0.11.14     | NO        |       |

Affects Versions corrected: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
(scoped to stream 2.2.x per issue suffix)

Remediation tasks created (stream 2.2.x):
- Upstream backport: bump quinn-proto to 0.11.14 (release/0.4.z)
- Downstream propagation: update rhtpa-backend ref in rhtpa-release.0.4.z (blocked by upstream)

Preemptive remediation tasks created for streams without CVE Jiras:
- Stream 2.1.x: upstream backport (security-preemptive) - bump quinn-proto on release/0.3.z
- Stream 2.1.x: downstream propagation (security-preemptive) - update ref in rhtpa-release.0.3.z

Label added: ai-cve-triaged
```

### Task Summary Table

| # | Task | Stream | Type | Labels | Link to TC-8001 |
|---|------|--------|------|--------|-----------------|
| 1 | Upstream backport (2.2.x) | 2.2.x | Standard | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 2 | Downstream propagation (2.2.x) | 2.2.x | Standard | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 3 | Upstream backport (2.1.x) | 2.1.x | Preemptive | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |
| 4 | Downstream propagation (2.1.x) | 2.1.x | Preemptive | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |

### Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks per stream (Cargo = source dependency ecosystem)
- [x] **Cross-stream coverage**: stream 2.1.x has preemptive tasks (no sibling CVE Jira exists)
- [x] **Link types**: "Depend" for standard tasks (2.2.x), "Related" for preemptive tasks (2.1.x), "Blocks" for upstream -> downstream within each stream
- [x] **Preemptive labels**: 2.1.x tasks carry `security-preemptive` label
- [x] **Coordination guidance**: each task includes upstream deployment context guidance
