# Step 8 -- Remediation

## Triage Outcome

### Issue-scoped stream (2.2.x): NOT AFFECTED

No 2.2.x versions ship a vulnerable version of h2. All versions in the 2.2.x stream ship h2 >= 0.4.8, which is at or above the fix threshold. No remediation tasks are needed for this stream.

**Recommendation for TC-8030 (scoped to 2.2.x):** Close as Not a Bug -- the h2 vulnerability does not affect any 2.2.x versions. VEX Justification: **Component not Present** (the vulnerable version of h2 is not included in any 2.2.x build).

### Cross-stream impact (2.1.x): AFFECTED -- Case A

The version impact analysis reveals that the **2.1.x** stream (outside this issue's scope) is affected. Both 2.1.0 and 2.1.1 ship h2 0.4.5, which is below the fix threshold of 0.4.8.

**Cross-stream impact comment (for TC-8030):**

> Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file analysis.
> The 2.1.x stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.

### Preemptive Remediation Tasks for 2.1.x

Since the 2.1.x stream is affected and (assumed) does not have its own CVE Jira for CVE-2026-48901, preemptive remediation tasks are created. h2 is a Cargo (source dependency) ecosystem, so two tasks are created:

---

## Task 1: Upstream Backport (2.1.x -- preemptive)

**Summary:** Remediate CVE-2026-48901: bump h2 to 0.4.8 (2.1.x)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Link type:** Related (to TC-8030, since this is a preemptive task for a different stream)

### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: 2.1.0 (tag v0.3.8, h2 0.4.5), 2.1.1 (tag v0.3.12, h2 0.4.5)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: to be determined by inspecting Cargo.toml at the pinned commits (direct if h2 is listed in [dependencies], transitive if pulled in through another crate)
- Update h2 dependency to >= 0.4.8 in Cargo.lock (and Cargo.toml if direct)
- If the vulnerable dependency is transitive, prefer bumping the direct dependency that pulls in h2; fall back to pinning h2 directly via `cargo add h2@0.4.8`

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8030 (cross-stream CVE tracking issue)

---

## Task 2: Downstream Propagation (2.1.x -- preemptive)

**Summary:** Propagate CVE-2026-48901 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Link type:** Related (to TC-8030); Blocked by upstream backport task above

### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-48901 fix from the upstream backport task.

The upstream backport task bumps h2 to 0.4.8 on release/0.3.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Blocked by: upstream backport task (upstream backport must merge first)
- Related to: TC-8030 (cross-stream CVE tracking issue)
