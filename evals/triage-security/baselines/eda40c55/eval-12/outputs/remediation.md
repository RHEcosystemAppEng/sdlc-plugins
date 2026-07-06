# Step 8 -- Remediation

## Triage Decision

**Case A + Case B**: The scoped stream (2.2.x) has one affected version (2.2.0). The cross-stream analysis shows 2.1.x is also affected (all versions). Create remediation tasks for the scoped 2.2.x stream (Case A) and post a cross-stream impact notice for 2.1.x (Case B).

Ecosystem: Cargo (source dependency) -- requires two tasks per affected stream: upstream backport + downstream propagation.

---

## Case A: Remediation Tasks for Stream 2.2.x

### Task 1: Upstream Backport Task

**Summary:** Remediate CVE-2026-48901: bump h2 to 0.4.8 (2.2.x)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-48901`

**Description:**

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: 2.2.0 (build 0.4.5, ships h2 0.4.5)
Source commit(s): v0.4.5

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Target branch: release/0.4.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

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

- Depends on: TC-8030 (parent tracking issue)

---

### Task 2: Downstream Propagation Subtask

**Summary:** Propagate CVE-2026-48901 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-48901`

**Description:**

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-48901 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8 on release/0.4.z. Once that PR merges,
update the source pinning in this Konflux release repo so the next build ships the fix.

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

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8030 (parent tracking issue)

---

## Case B: Cross-Stream Impact Notice

### Cross-stream impact comment (to be posted on TC-8030):

> Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file analysis.
> All versions in stream 2.1.x (2.1.0, 2.1.1) ship h2 0.4.5 which is within the affected range.
> This stream is tracked by a companion issue (see Related links) or may require separate PSIRT triage.

### Proactive Remediation Tasks for Stream 2.1.x (if no companion CVE Jira exists)

If no stream-specific CVE Jira exists for 2.1.x, create preemptive remediation tasks:

#### Preemptive Task 1: Upstream Backport (2.1.x)

**Summary:** Remediate CVE-2026-48901: bump h2 to 0.4.8 (2.1.x)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Link type:** Related (to TC-8030)

**Description:**

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

Affected versions: 2.1.0 (build 0.3.8, ships h2 0.4.5), 2.1.1 (build 0.3.12, ships h2 0.4.5)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

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

- Depends on: TC-8030 (parent tracking issue)

#### Preemptive Task 2: Downstream Propagation (2.1.x)

**Summary:** Propagate CVE-2026-48901 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Link type:** Related (to TC-8030)

**Description:**

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-48901 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that PR merges,
update the source pinning in this Konflux release repo so the next build ships the fix.

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

- Depends on: preemptive upstream backport task (upstream backport must merge first)
- Depends on: TC-8030 (parent tracking issue)

---

## Jira Linkage Summary

### Case A (2.2.x scoped tasks):
1. Upstream backport task linked to TC-8030 with link type **Depend**
2. Downstream propagation subtask linked to upstream task with link type **Blocks**
3. Downstream propagation subtask linked to TC-8030 with link type **Depend**

### Case B (2.1.x preemptive tasks):
1. Preemptive upstream task linked to TC-8030 with link type **Related**
2. Preemptive downstream task linked to TC-8030 with link type **Related**
3. Preemptive downstream task blocked by preemptive upstream task with link type **Blocks**

## Post-Triage Actions

1. Add label `ai-cve-triaged` to TC-8030
2. Post summary comment to TC-8030 with:
   - Version impact table
   - Affects Versions correction (if needed): RHTPA 2.2.0 is correctly set as Affects Version
   - Triage outcome: remediation tasks created for 2.2.x, preemptive tasks for 2.1.x
   - Links to all remediation tasks
   - @mention of the issue reporter
   - Comment footnote: "This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/mrizzi/sdlc-plugins) v0.12.2."
