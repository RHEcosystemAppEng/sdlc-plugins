# Step 8 -- Remediation

## Triage Outcome

**Case A + Case B**: The in-scope stream (2.2.x) has affected versions (2.2.0, 2.2.1, 2.2.2), but the fix is already present in later versions (2.2.3+). Additionally, the cross-stream analysis shows that stream 2.1.x is also affected (Case B).

## Stream 2.2.x (In-Scope) -- Already Fixed in Latest Releases

The upstream fix for quinn-proto is already integrated into the 2.2.x stream starting from version 2.2.3 (build tag v0.4.11). Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14, which is the fixed version. No new remediation task is required for the 2.2.x stream -- the Affects Versions correction (Step 3) documents which shipped versions were affected, but the fix has already been released.

The Affects Versions for TC-8001 should be set to `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]` to accurately reflect which versions shipped the vulnerable dependency.

## Stream 2.1.x (Cross-Stream Impact -- Case B)

Stream 2.1.x is also affected: both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9, which is within the vulnerable range (< 0.11.14). The upstream branch `release/0.3.z` does NOT have the fix. Since this issue is scoped to 2.2.x, the 2.1.x impact is handled via Case B (cross-stream proactive remediation).

### Cross-stream impact comment (posted to TC-8001)

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based
on lock file analysis. Stream 2.1.x versions 2.1.0 and 2.1.1 both ship
quinn-proto 0.11.9. This stream is tracked by companion issues (see Related
links) or may require separate PSIRT triage.
```

### Preemptive Remediation Tasks for Stream 2.1.x

Since stream 2.1.x has no companion CVE Jira for CVE-2026-31812, proactive remediation tasks are created with the `security-preemptive` label and "Related" link type to the originating CVE Jira (TC-8001).

#### Task 1: Upstream Backport (2.1.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link**: Related to TC-8001

**Description**:

```
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for stream 2.1.x. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (DoS).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8), 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: to be determined via manifest inspection
- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

When the vulnerable package is a **transitive** dependency (pulled in
through intermediate packages), use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (see dependency
  chain)
- Bump the direct dependency to a version whose transitive closure
  includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes to the
  direct dependency

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable:
- Cargo: `cargo add quinn-proto@0.11.14` to add as a direct
  dependency, overriding the transitive resolution
- Document why the direct dep bump was not viable in the PR description

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

#### Task 2: Downstream Propagation (2.1.x)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link**: Related to TC-8001; Blocked by upstream backport task (Task 1)

**Description**:

```
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for stream 2.1.x. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Preemptive task comment (posted to TC-8001)

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <upstream-task-key> (security-preemptive, upstream backport)
- 2.1.x: <downstream-task-key> (security-preemptive, downstream propagation)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

## Post-Triage Summary

After all triage actions are complete:

1. **Label**: Add `ai-cve-triaged` label to TC-8001.
2. **Summary comment** on TC-8001:
   - Version impact table showing all streams
   - Affects Versions correction: `[RHTPA 2.0.0]` corrected to `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
   - Triage outcome: 2.2.x stream already fixed in 2.2.3+; preemptive remediation tasks created for 2.1.x
   - Links to all remediation tasks created
   - @mention of the vulnerability issue reporter
