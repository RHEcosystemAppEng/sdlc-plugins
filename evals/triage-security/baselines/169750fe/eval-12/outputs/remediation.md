# Step 8 -- Remediation

## Triage Decision

### Scoped Stream (2.2.x): Case C -- Close as Not a Bug

No supported versions in the 2.2.x stream ship a vulnerable version of h2. All versions ship h2 >= 0.4.8, which is at or above the fix threshold.

**Recommendation**: Close TC-8030 as "Not a Bug" (not affected).

**Actions**:
1. Add comment documenting the version impact analysis and close rationale
2. Transition TC-8030 to Closed with resolution "Not a Bug"
3. Set VEX Justification (customfield_12345) to "Component not Present" -- the vulnerable version of h2 (< 0.4.8) is not shipped in any 2.2.x version
4. Add `ai-cve-triaged` label

**Close comment**:

> No supported versions in the 2.2.x stream ship a vulnerable version of h2.
> Version impact analysis shows all 2.2.x versions ship h2 >= 0.4.8, which is
> at or above the fix threshold established by MITRE CVE API and OSV.dev.
>
> | Version | h2 version | Affected? |
> |---------|------------|-----------|
> | 2.2.0 | 0.4.8 | NO |
> | 2.2.1 | 0.4.8 | NO |
> | 2.2.2 | 0.4.8 | NO (retag of 2.2.1) |
> | 2.2.3 | 0.4.9 | NO |
> | 2.2.4 | 0.4.9 | NO |
>
> Closing as Not a Bug. VEX Justification: Component not Present.

### Cross-Stream Impact (2.1.x): Case A -- Proactive Remediation

The 2.1.x stream IS affected. Both versions (2.1.0 and 2.1.1) ship h2 0.4.5, which is below the fix threshold of 0.4.8.

**Cross-stream impact comment** (posted to TC-8030):

> Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file
> analysis. Stream 2.1.x versions 2.1.0 and 2.1.1 both ship h2 0.4.5.
> These streams are tracked by companion issues (see Related links)
> or may require separate PSIRT triage.

If no existing CVE Jira exists for the 2.1.x stream, create preemptive remediation tasks:

---

## Preemptive Remediation Tasks for Stream 2.1.x

Since the ecosystem is **Cargo** (source dependency), two tasks are required per stream.

### Task 1: Upstream Backport -- Bump h2 in backend (2.1.x)

**Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Link type**: Related (to TC-8030, since this is a preemptive task for a different stream)

#### Task Description

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: 2.1.0 (h2 0.4.5), 2.1.1 (h2 0.4.5)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct or transitive (verify in Cargo.toml)
- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Run `cargo update -p h2` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add h2@0.4.8`

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

- Related to: TC-8030 (originating CVE -- stream 2.2.x)
```

### Task 2: Downstream Propagation -- Update backend ref in rhtpa-release.0.3.z (2.1.x)

**Summary**: Propagate CVE-2026-48901 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Link type**: Related (to TC-8030), Blocks (blocked by upstream backport task)

#### Task Description

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

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-48901
fix from the upstream backport task.

The upstream backport bumps h2 to >= 0.4.8 on release/0.3.z. Once that PR merges,
update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Blocked by: upstream backport task (upstream fix must merge first)
- Related to: TC-8030 (originating CVE -- stream 2.2.x)
```

---

## Summary of Remediation Actions

| Action | Stream | Detail |
|--------|--------|--------|
| Close as Not a Bug | 2.2.x (scoped) | No versions affected; VEX: Component not Present |
| Cross-stream impact comment | 2.2.x (posted to TC-8030) | Notes 2.1.x is affected |
| Preemptive upstream backport task | 2.1.x | Bump h2 to >= 0.4.8 on release/0.3.z |
| Preemptive downstream propagation task | 2.1.x | Update backend ref in rhtpa-release.0.3.z |
| Add ai-cve-triaged label | TC-8030 | Mark as triaged |
