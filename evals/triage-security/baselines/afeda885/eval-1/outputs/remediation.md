# Step 7 - Remediation: TC-8001

## Triage Outcome

This is **Case A** (Affected) with **Case B** (Cross-stream impact).

- **Issue stream scope**: 2.2.x
- **Affected versions in scope**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Not affected in scope**: RHTPA 2.2.3, RHTPA 2.2.4 (ship quinn-proto 0.11.14)
- **Cross-stream impact**: 2.1.x stream is also affected (versions 2.1.0, 2.1.1 ship quinn-proto 0.11.9)
- **Ecosystem**: Cargo (source dependency) — requires 2 tasks per stream (upstream backport + downstream propagation)

## Case A: Remediation Tasks for 2.2.x Stream

Since the upstream fix is already available on the release/0.4.z branch (v0.4.11+ ships quinn-proto 0.11.14), the upstream backport task confirms the fix exists and the downstream propagation task updates affected version references.

### Task 1: Upstream Backport Task (2.2.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)

**Labels**: ai-generated-jira, Security, CVE-2026-31812

**Description**:

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (v0.4.5, quinn-proto 0.11.9), RHTPA 2.2.1 (v0.4.8, quinn-proto 0.11.12), RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

Note: The fix is already present on release/0.4.z as of tag v0.4.11 (quinn-proto 0.11.14). This task confirms the fix is available and ensures it is tracked for downstream propagation to affected versions.

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

### Task 2: Downstream Propagation Task (2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: ai-generated-jira, Security, CVE-2026-31812

**Description**:

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

## Case B: Cross-Stream Impact (2.1.x)

The version impact analysis reveals that the **2.1.x stream** is also affected:

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.1.0 | 0.11.9 | YES |
| 2.1.1 | 0.11.9 | YES |

The 2.1.x stream is outside this issue's scope (issue is scoped to 2.2.x via `[rhtpa-2.2]`). A cross-stream impact comment would be posted to TC-8001.

**Cross-stream impact comment** (would be posted to TC-8001):

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. Versions 2.1.0 and 2.1.1 ship quinn-proto 0.11.9. This stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.

Since the upstream fix is NOT available on the release/0.3.z branch for the 2.1.x stream (still ships quinn-proto 0.11.9), preemptive remediation tasks would be created if no sibling CVE Jira exists for the 2.1.x stream.

### Preemptive Task 3: Upstream Backport Task (2.1.x, preemptive)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)

**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

**Description**:

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (v0.3.8, quinn-proto 0.11.9), RHTPA 2.1.1 (v0.3.12, quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

Note: The fix is NOT yet present on release/0.3.z. This task requires an upstream PR to bump quinn-proto to >= 0.11.14 on the release/0.3.z branch.

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue — Related link, not Depend)
```

### Preemptive Task 4: Downstream Propagation Task (2.1.x, preemptive)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

**Description**:

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
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

- Depends on: preemptive upstream backport task for 2.1.x (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue — Related link, not Depend)
```

## Jira Linkage (would execute after engineer confirmation)

### Standard remediation (2.2.x stream):
```
# Link upstream task to vulnerability
jira.create_link(inwardIssue: "TC-8001", outwardIssue: "<upstream-task-key>", type: "Depend")

# Link downstream task to vulnerability
jira.create_link(inwardIssue: "TC-8001", outwardIssue: "<downstream-task-key>", type: "Depend")

# Link downstream blocked by upstream
jira.create_link(inwardIssue: "<upstream-task-key>", outwardIssue: "<downstream-task-key>", type: "Blocks")
```

### Preemptive remediation (2.1.x stream):
```
# Link preemptive upstream task to originating CVE with "Related" (not "Depend")
jira.create_link(inwardIssue: "TC-8001", outwardIssue: "<preemptive-upstream-task-key>", type: "Related")

# Link preemptive downstream task to originating CVE with "Related"
jira.create_link(inwardIssue: "TC-8001", outwardIssue: "<preemptive-downstream-task-key>", type: "Related")

# Link preemptive downstream blocked by preemptive upstream
jira.create_link(inwardIssue: "<preemptive-upstream-task-key>", outwardIssue: "<preemptive-downstream-task-key>", type: "Blocks")
```

## Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8001
2. Transition TC-8001 to In Progress
3. Assign TC-8001 to current user
4. Post summary comment to TC-8001 with version impact table, Affects Versions correction, remediation task links, cross-stream impact notice, and preemptive task references
