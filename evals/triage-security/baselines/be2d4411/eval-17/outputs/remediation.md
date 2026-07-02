# Step 8 -- Remediation

## Triage Outcome

**Case A: Affected** -- the issue's stream-scoped versions (2.2.0, 2.2.1, 2.2.2) are affected.

**Case B: Cross-stream impact** -- stream 2.1.x (versions 2.1.0, 2.1.1) is also affected but outside this issue's scope. A cross-stream impact comment would be posted.

Since quinn-proto is a **Cargo** (source dependency) ecosystem, two remediation tasks are created for the in-scope stream (2.2.x): an upstream backport task and a downstream propagation subtask.

---

## Task 1: Upstream Backport Task (2.2.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

### Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0 (quinn-proto 0.11.9), 2.2.1 (quinn-proto 0.11.12), 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
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

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

## Task 2: Downstream Propagation Subtask (2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

### Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
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

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Jira Linkage

After task creation:

1. **Link** upstream backport task to TC-8001 with link type "Depend"
2. **Link** downstream propagation subtask to TC-8001 with link type "Depend"
3. **Link** downstream propagation subtask as blocked by upstream backport task with link type "Blocks"
4. **Transition** TC-8001 to In Progress
5. **Add `ai-cve-triaged` label** to TC-8001

## Cross-Stream Impact (Case B)

Stream 2.1.x (versions 2.1.0, 2.1.1) is also affected by CVE-2026-31812 but outside this issue's scope (issue is scoped to 2.2.x).

Cross-stream impact comment to be posted on TC-8001:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x
based on lock file analysis. These streams are tracked by companion issues
(see Related links) or may require separate PSIRT triage.
```

If no companion CVE Jira exists for stream 2.1.x, preemptive remediation tasks would be created with `security-preemptive` label and "Related" link type to TC-8001.

For stream 2.1.x, the upstream branch `release/0.3.z` does NOT have the fix (latest v0.3.12 ships quinn-proto 0.11.9). Preemptive remediation for 2.1.x would require:
- Task 1 (upstream): bump quinn-proto to >= 0.11.14 on branch `release/0.3.z` in the backend repo
- Task 2 (downstream): update backend ref in rhtpa-release.0.3.z

## Post-Triage Summary Comment

A summary comment would be posted to TC-8001 documenting:
1. The version impact table
2. Affects Versions correction: `[RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
3. Triage outcome: remediation tasks created for stream 2.2.x
4. Links to all remediation tasks (upstream backport + downstream propagation)
5. @mention of the vulnerability issue's reporter

The comment includes the Comment Footnote:

---
This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/mrizzi/sdlc-plugins) v0.11.1.
