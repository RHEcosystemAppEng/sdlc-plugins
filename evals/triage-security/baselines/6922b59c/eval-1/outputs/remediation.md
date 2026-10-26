# Step 7.5 -- Release Jira Orchestration

## Release Orchestration Confirmations

Before creating remediation tasks, the release Jira structure must be resolved for
each affected stream.

### Stream 2.2.x (in-scope)

**7.5.1 -- Resolve stream-to-version mapping:**

Search for an existing release Epic matching
`"RHTPA 2.2.* Release Tasks"` in project TC.

- If an existing release Epic is found (e.g., "RHTPA 2.2.5 Release Tasks"), use it.
- If no release Epic exists, the default version would be **RHTPA 2.2.5** (next patch
  bump from the latest released version 2.2.4 in the supportability matrix).
- Engineer confirmation is required before creating the Epic. Options:
  1. Accept RHTPA 2.2.5
  2. Specify a different version
  3. Skip release Jira for this stream

**7.5.2 -- Find or create the release Task:**

Search for an existing release Task under the release Epic matching
`"RHTPA <version> CVE triage"`.

- If a release Task exists, use it.
- If no release Task exists, prompt the engineer to confirm creation of
  "RHTPA <version> CVE triage" as a child of the release Epic.

**7.5.3 -- Cross-CVE dedup check:**

The Upstream Affected Component custom field is **not configured** in the Security
Configuration for this project. Therefore, the cross-CVE dedup check is **skipped
entirely**. No existing remediation Task can be matched by component, so standard
remediation task creation proceeds for all affected versions in this stream.

### Stream 2.1.x (cross-stream, preemptive)

Since stream 2.1.x is outside the issue's scope (TC-8001 is scoped to 2.2.x),
preemptive remediation tasks for 2.1.x would use "Related" link type instead of
"Depend". Release Jira orchestration for 2.1.x follows the same 7.5.1/7.5.2 pattern:

- Default version: **RHTPA 2.1.2** (next patch bump from latest released 2.1.1)
- Same confirmation gates apply for Epic and Task creation.
- Cross-CVE dedup is skipped (no Upstream Affected Component field configured).

## Dedup Decision

**Decision: No dedup applies.** The Upstream Affected Component custom field is not
configured in Security Configuration, so Step 7.5.3 cross-CVE dedup is skipped entirely.
All affected streams proceed to standard remediation task creation without dedup filtering.

---

# Step 8 -- Remediation

## Triage Outcome

The version impact analysis shows that supported versions **are** affected:
- Stream 2.2.x: versions 2.2.0, 2.2.1, 2.2.2 are affected
- Stream 2.1.x: versions 2.1.0, 2.1.1 are affected

This is **Case A + Case B**: the issue is scoped to 2.2.x, but cross-stream analysis
reveals that 2.1.x is also affected. Case A applies for the cross-stream notice, and
Case B applies for remediation task creation.

### Case A -- Cross-Stream Impact

A cross-stream impact comment would be posted to TC-8001:

> Cross-stream impact: quinn-proto versions before 0.11.14 also affects stream 2.1.x
> based on lock file analysis. Stream 2.1.x versions (2.1.0, 2.1.1) ship quinn-proto
> 0.11.9 which is within the affected range.
> These streams are tracked by companion issues (see Related links) or may require
> separate PSIRT triage.

Since there is no existing CVE Jira for stream 2.1.x (no sibling with `[rhtpa-2.1]`
suffix found), preemptive remediation tasks are created for 2.1.x.

---

## Remediation Tasks -- Stream 2.2.x (In-Scope)

Ecosystem: Cargo (source dependency). Upstream fix status: **YES** (release/0.4.z
branch already ships quinn-proto 0.11.14 at tags v0.4.11 and v0.4.12).
Remediation variant: **dependency bump + downstream propagation** (2 tasks).

### Task 1: Dependency Bump (2.2.x)

**Summary**: Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description**:

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto versions before 0.11.14) is already fixed
upstream -- a package manager update is sufficient.

Affected versions: 2.2.0, 2.2.1, 2.2.2
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is retag of v0.4.8)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (quinn-proto is a direct Cargo dependency)
- **Remediation action**: run `cargo update -p quinn-proto` to pull in the latest
  compatible version (>= 0.11.14)
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

### Task 2: Downstream Propagation (2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description**:

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-31812 fix
from the dependency bump task.

The dependency bump task bumps quinn-proto to 0.11.14 on release/0.4.z. Once that
PR merges, update the source pinning in this Konflux release repo so the next build
ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <dependency-bump-task-key> (dependency bump must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Jira Linkage for 2.2.x tasks

1. Dependency bump task -> TC-8001: **Depend** link
2. Downstream propagation task -> dependency bump task: **Blocks** link
   (downstream is blocked by upstream)
3. Downstream propagation task -> TC-8001: **Depend** link
4. Both remediation tasks -> release Task: **Blocks** link
5. TC-8001 -> release Task: **Related** link

---

## Remediation Tasks -- Stream 2.1.x (Preemptive / Cross-Stream)

Ecosystem: Cargo (source dependency). Upstream fix status: **NO** (release/0.3.z
branch still ships quinn-proto 0.11.9 at latest tag v0.3.12).
Remediation variant: **upstream backport + downstream propagation** (2 tasks).

These tasks are **preemptive** because stream 2.1.x does not have its own CVE Jira.
They carry the `security-preemptive` label and use "Related" link type to TC-8001.

### Task 3: Upstream Backport (2.1.x, preemptive)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Description**:

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2). No stream-specific CVE Jira exists
> yet for this stream. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0, 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (quinn-proto is a direct Cargo dependency)
- The upstream branch release/0.3.z does NOT yet ship the fix (latest v0.3.12
  has quinn-proto 0.11.9). An upstream backport PR is required to bump
  quinn-proto to >= 0.11.14.
- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a code-level
  workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

### Task 4: Downstream Propagation (2.1.x, preemptive)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Description**:

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2). No stream-specific CVE Jira exists
> yet for this stream. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-31812 fix
from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14 on release/0.3.z. Once that
PR merges, update the source pinning in this Konflux release repo so the next build
ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-backport-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Jira Linkage for 2.1.x preemptive tasks

1. Upstream backport task -> TC-8001: **Related** link (preemptive -- not "Depend")
2. Downstream propagation task -> upstream backport task: **Blocks** link
   (downstream is blocked by upstream)
3. Downstream propagation task -> TC-8001: **Related** link (preemptive)
4. Both preemptive tasks -> 2.1.x release Task: **Blocks** link (if release Jira active)
5. TC-8001 -> 2.1.x release Task: **Related** link (if release Jira active)

### Post-creation comment on TC-8001

A comment would be posted to TC-8001 listing all preemptive tasks:

> Preemptive remediation tasks created for streams without CVE Jiras:
> - rhtpa-2.1: <upstream-backport-task-key> (security-preemptive), <downstream-propagation-task-key> (security-preemptive)
>
> These tasks use the "Related" link type and carry the security-preemptive
> label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
> reconciliation will link them and remove the label.

---

## Summary

| Stream | Remediation Type | Tasks | Fix Available Upstream? |
|--------|-----------------|-------|------------------------|
| 2.2.x (in-scope) | Dependency bump + downstream propagation | 2 | Yes |
| 2.1.x (preemptive) | Upstream backport + downstream propagation | 2 | No |
| **Total** | | **4** | |

No Jira operations were actually performed -- all task descriptions and linkage
plans are documented here for reference only.
