# Step 8 -- Remediation

## Triage Outcome

**Case B + Case A**: The issue is scoped to the 2.2.x stream, and cross-stream analysis shows the 2.1.x stream is also affected. Remediation tasks are needed for the scoped stream (2.2.x), and a cross-stream impact notice plus preemptive remediation tasks are needed for the 2.1.x stream.

Within the 2.2.x scoped stream, only version 2.2.0 is affected. Versions 2.2.1+ already ship h2 >= 0.4.8 (the fix). However, version 2.2.0 shipped with h2 0.4.5 which is vulnerable, so remediation tasks document the fix for completeness and traceability.

## Cross-Stream Impact Comment

```
Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file analysis.
Both versions in the 2.1.x stream (2.1.0 and 2.1.1) ship h2 0.4.5.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

## Remediation Tasks -- 2.2.x Stream (Scoped)

Since h2 is a source dependency (Cargo ecosystem), two tasks are created: an upstream backport task and a downstream propagation subtask.

### Task 1: Upstream Backport (2.2.x)

**Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (2.2.x)

**Labels**: ai-generated-jira, Security, CVE-2026-48901

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed
version (0.4.8+).

Affected versions: 2.2.0 (ships h2 0.4.5)
Source commit(s): v0.4.5

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
- Update h2 dependency to >= 0.4.8 in Cargo.toml / Cargo.lock

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update h2 dependency to >= 0.4.8 in Cargo.toml
- Run `cargo update -p h2` to update Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

Note: versions 2.2.1+ already ship h2 0.4.8+. The fix is already present
on the release/0.4.z branch at commits v0.4.8 and later.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8030 (parent tracking issue)
```

### Task 2: Downstream Propagation (2.2.x)

**Summary**: Propagate CVE-2026-48901 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: ai-generated-jira, Security, CVE-2026-48901

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-48901 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8 on release/0.4.z. Once that PR
merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8030 (parent tracking issue)
```

## Preemptive Remediation Tasks -- 2.1.x Stream (Cross-Stream)

Since no CVE Jira exists for the 2.1.x stream, preemptive remediation tasks are created with the `security-preemptive` label and "Related" link type to the originating CVE TC-8030.

### Task 3: Upstream Backport -- Preemptive (2.1.x)

**Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-48901, security-preemptive

```
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed
version (0.4.8+).

Affected versions: 2.1.0 (h2 0.4.5), 2.1.1 (h2 0.4.5)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- Update h2 dependency to >= 0.4.8 in Cargo.toml / Cargo.lock
- This is a backport to the 2.1.x stream (release/0.3.z branch)

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update h2 dependency to >= 0.4.8 in Cargo.toml
- Run `cargo update -p h2` to update Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8030 (originating CVE -- different stream)
```

### Task 4: Downstream Propagation -- Preemptive (2.1.x)

**Summary**: Propagate CVE-2026-48901 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-48901, security-preemptive

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-48901 fix from the upstream backport task for the 2.1.x stream.

The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that PR
merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: preemptive upstream backport task for 2.1.x (upstream backport must merge first)
- Related to: TC-8030 (originating CVE -- different stream)
```

## Jira Linkage Summary

### Scoped stream (2.2.x) tasks:
- Upstream backport task -> TC-8030: link type "Depend"
- Downstream propagation task -> upstream backport task: link type "Blocks"
- Downstream propagation task -> TC-8030: link type "Depend"

### Preemptive (2.1.x) tasks:
- Upstream backport task (preemptive) -> TC-8030: link type "Related"
- Downstream propagation task (preemptive) -> upstream backport task (preemptive): link type "Blocks"
- Downstream propagation task (preemptive) -> TC-8030: link type "Related"

## Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8030
2. Post summary comment to TC-8030 with:
   - Version impact table
   - Affects Versions assessment (PSIRT assignment correct for 2.2.x)
   - Cross-stream impact notice for 2.1.x
   - Links to all 4 remediation tasks
   - @mention of the reporter (PSIRT analyst)
3. Post preemptive task comment listing tasks created for the 2.1.x stream
