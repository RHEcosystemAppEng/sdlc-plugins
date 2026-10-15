# Step 8 -- Remediation Analysis

## Decision Tree Evaluation

1. **Any supported versions affected?** YES -- 2.1.x versions (2.1.0, 2.1.1) are affected.
2. **Issue scoped to a single stream?** YES -- scoped to 2.2.x via suffix `[rhtpa-2.2]`.
3. **Scoped stream (2.2.x) affected?** NO -- all 2.2.x versions ship h2 >= 0.4.8.
4. **Other streams affected?** YES -- 2.1.x ships h2 0.4.5 (< 0.4.8).

## Outcome for Scoped Stream (2.2.x): Close as Not a Bug

**Recommendation**: Close TC-8030 as "Not a Bug" (not affected).

No supported versions in the 2.2.x stream ship a vulnerable version of h2.
All versions ship h2 >= 0.4.8 which is at or above the fix threshold.

### Proposed Jira Actions (Not Executed)

1. **Add comment** to TC-8030:
   > No supported versions in stream 2.2.x ship a vulnerable version of h2.
   > Version impact analysis shows all 2.2.x versions ship h2 >= 0.4.8,
   > which is at or above the fix threshold (< 0.4.8).
   >
   > | Version | h2 version | Affected? |
   > |---------|------------|-----------|
   > | 2.2.0 | 0.4.8 | NO |
   > | 2.2.1 | 0.4.8 | NO |
   > | 2.2.2 | -- | NO (retag of 2.2.1) |
   > | 2.2.3 | 0.4.9 | NO |
   > | 2.2.4 | 0.4.9 | NO |

2. **Set VEX Justification** (customfield_12345): "Component not Present"
   - Rationale: The vulnerable version of h2 (< 0.4.8) is not shipped in any 2.2.x release.

3. **Transition** TC-8030 to Closed with resolution "Not a Bug".

## Case A: Cross-Stream Impact Notice

Stream 2.1.x is affected but outside this issue's scope. The following cross-stream
impact comment would be posted to TC-8030:

### Proposed Cross-Stream Impact Comment

> Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file
> analysis. Versions 2.1.0 and 2.1.1 both ship h2 0.4.5.
> These streams are tracked by companion issues (see Related links)
> or may require separate PSIRT triage.

### Preemptive Remediation Tasks for Stream 2.1.x

Since 2.1.x is affected and (assuming) no sibling CVE Jira exists for the 2.1.x
stream, preemptive remediation tasks would be created. The ecosystem is Cargo
(source dependency), so two tasks are required per stream.

The upstream fix is NOT available on the 2.1.x upstream branch (release/0.3.z
ships h2 0.4.5), so the upstream backport variant applies.

---

### Task 1: Upstream Backport (Preemptive, 2.1.x)

**Proposed Jira Issue** (not executed):
- Type: Task
- Summary: `Remediate CVE-2026-48901: bump h2 to 0.4.8 (rhtpa-2.1)`
- Labels: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`
- Link: Related to TC-8030 (originating CVE from different stream)

**Description:**

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated
to the fixed version (0.4.8+).

Affected versions: 2.1.0 (h2 0.4.5), 2.1.1 (h2 0.4.5)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: to be determined via Cargo.lock inspection at implementation time

### Remediation approach

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- If h2 is a direct dependency, bump it directly in Cargo.toml
- If h2 is a transitive dependency, bump the direct dependency that pulls it in;
  fall back to pinning h2 directly via `cargo add h2@0.4.8`

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8030 (originating CVE from stream rhtpa-2.2)
```

---

### Task 2: Downstream Propagation (Preemptive, 2.1.x)

**Proposed Jira Issue** (not executed):
- Type: Task
- Summary: `Propagate CVE-2026-48901 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)`
- Labels: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`
- Blocked by: Task 1 (upstream backport must merge first)
- Link: Related to TC-8030 (originating CVE from different stream)

**Description:**

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-48901 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

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

- Blocked by: upstream backport task (must merge first)
- Related to: TC-8030 (originating CVE from stream rhtpa-2.2)
```

---

## Proposed Jira Link Topology

| Link Type | Inward Issue | Outward Issue | Purpose |
|-----------|-------------|---------------|---------|
| Related | TC-8030 | Task 1 (upstream backport) | Preemptive task linked to originating CVE |
| Related | TC-8030 | Task 2 (downstream propagation) | Preemptive task linked to originating CVE |
| Blocks | Task 1 (upstream backport) | Task 2 (downstream propagation) | Downstream blocked by upstream |

## Post-Triage Summary

### Proposed Label Addition

Add `ai-cve-triaged` label to TC-8030.

### Proposed Summary Comment on TC-8030

> **Triage summary for CVE-2026-48901 (h2 < 0.4.8)**
>
> **Version impact (enriched via MITRE + OSV.dev -- fix threshold 0.4.8):**
>
> | Stream | Version | h2 | Affected? |
> |--------|---------|-----|-----------|
> | 2.1.x | 2.1.0 | 0.4.5 | YES |
> | 2.1.x | 2.1.1 | 0.4.5 | YES |
> | 2.2.x | 2.2.0 | 0.4.8 | NO |
> | 2.2.x | 2.2.1 | 0.4.8 | NO |
> | 2.2.x | 2.2.2 | -- | NO (retag) |
> | 2.2.x | 2.2.3 | 0.4.9 | NO |
> | 2.2.x | 2.2.4 | 0.4.9 | NO |
>
> **Scoped stream (2.2.x)**: Not affected. All versions ship h2 >= 0.4.8.
> Closed as Not a Bug. VEX Justification: Component not Present.
>
> **Cross-stream impact (2.1.x)**: Affected. Preemptive remediation tasks created:
> - Upstream backport: bump h2 to 0.4.8 on release/0.3.z (security-preemptive)
> - Downstream propagation: update backend ref in rhtpa-release.0.3.z (security-preemptive)
>
> Note: The Jira description provided only an imprecise affected range
> ("versions prior to the fix"). The fix threshold (0.4.8) was determined
> via external CVE data enrichment from MITRE CVE API and OSV.dev, both
> of which agreed on the threshold.
