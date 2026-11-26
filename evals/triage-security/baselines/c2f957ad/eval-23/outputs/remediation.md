# Remediation Plan: TC-8001 (CVE-2026-31812, quinn-proto < 0.11.14)

## Decision

- Issue scope: **2.2.x** (scoped by the `[rhtpa-2.2]` suffix).
- 2.2.x is affected (2.2.0, 2.2.1, 2.2.2), so **Case B** applies.
- 2.1.x, outside this issue's scope, is also affected (2.1.0, 2.1.1), so **Case A** applies: post a cross-stream impact comment and create preemptive tasks, assuming no `[rhtpa-2.1]` sibling CVE Jira exists.
- Ecosystem: Cargo, a source dependency, so each stream gets **2 tasks**.
  - 2.2.x: the fix is already on `release/0.4.z` (tags v0.4.11 and v0.4.12 ship 0.11.14), so it uses the **dependency bump + downstream propagation** variant.
  - 2.1.x: there is no evidence of the fix on `release/0.3.z`, so it uses the **upstream backport + downstream propagation** variant, marked preemptive.
- Affected repository: **rhtpa-backend**. Its Deployment Context is **customer-shipped**, so every task includes the customer-shipped Coordination Guidance.

> Engineer note: released 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14. Before creating the 2.2.x tasks, check whether the open work is only to confirm that `release/0.4.z` HEAD and the Konflux reference stay at 0.11.14 or higher, and whether customer guidance should be "upgrade to 2.2.3+".

Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`. Preemptive tasks also get `security-preemptive`. Each task carries the parent Vulnerability's security level. A description digest comment is posted after each task is created and before any links.

## Coordination Guidance

Deployment context lookup: `rhtpa-backend` maps to **customer-shipped**, taken from the Source Repositories table in CLAUDE.md.

Every remediation task below adds this subsection to its Implementation Notes:

```
### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE
assignment, advisory preparation, and formal disclosure. Fix must be released via a
security advisory with explicit CVE-to-component mapping.
```

Neither the `internal` guidance (merge in repo, no advisory) nor the `upstream` guidance (coordinate with upstream maintainers or embargo) applies here.

---

## Task 1 (2.2.x): Dependency bump

**Summary:** Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x)
**Labels:** ai-generated-jira, Security, CVE-2026-31812
**Links:** TC-8001 Depend -> Task 1; Task 1 Blocks Task 2; Task 1 Blocks the release Task (RHTPA 2.2.x CVE triage, if Step 7.5 is active)

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream —
a package manager update is sufficient.

Affected versions: RHTPA 2.2.0 (v0.4.5, quinn-proto 0.11.9), RHTPA 2.2.1 (v0.4.8, quinn-proto 0.11.12), RHTPA 2.2.2 (same as 2.2.1, retag of v0.4.8)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: not determined from available evidence (direct vs transitive via quinn; verify with `cargo tree -i quinn-proto`)
- **Remediation action**: run `cargo update -p quinn-proto` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify Cargo.lock reflects >= 0.11.14 after the update (released tags v0.4.11/v0.4.12 already ship 0.11.14; confirm branch HEAD)
- If the vulnerable dependency is dev-only or build-only, the remediation priority is Normal regardless of CVE severity. Add `dev-dependency` label to the task.

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE
assignment, advisory preparation, and formal disclosure. Fix must be released via a
security advisory with explicit CVE-to-component mapping.

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

## Task 2 (2.2.x): Downstream propagation

**Summary:** Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)
**Labels:** ai-generated-jira, Security, CVE-2026-31812
**Links:** TC-8001 Depend -> Task 2; blocked by Task 1; Task 2 Blocks the release Task (if active)

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <Task 1 key>.

The dependency bump (<Task 1 key>) bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: not determined — carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback
  approach), verify the pinning is reflected in the downstream build's
  lock file after the source reference update
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE
assignment, advisory preparation, and formal disclosure. Fix must be released via a
security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <Task 1 key> (upstream change must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

## Task 3 (2.1.x, preemptive): Upstream backport

**Summary:** Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)
**Labels:** ai-generated-jira, Security, CVE-2026-31812, security-preemptive
**Links:** TC-8001 Related -> Task 3; Task 3 Blocks Task 4. Preemptive tasks are not linked to release Jira.

```
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (remote DoS).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (v0.3.8, quinn-proto 0.11.9), RHTPA 2.1.1 (v0.3.12, quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: not determined from available evidence (verify with `cargo tree -i quinn-proto`)
- If the vulnerable dependency is dev-only or build-only, the remediation priority is Normal regardless of CVE severity. Add `dev-dependency` label to the task.

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (likely quinn)
- Bump it to a version whose transitive closure includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes

**Fallback: pin the transitive dependency directly**
- `cargo add quinn-proto@0.11.14` to override the transitive resolution
- Document why the direct dep bump was not viable in the PR description

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE
assignment, advisory preparation, and formal disclosure. Fix must be released via a
security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

## Task 4 (2.1.x, preemptive): Downstream propagation

**Summary:** Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)
**Labels:** ai-generated-jira, Security, CVE-2026-31812, security-preemptive
**Links:** TC-8001 Related -> Task 4; blocked by Task 3

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

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from <Task 3 key>.

The upstream backport (<Task 3 key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: not determined — carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback
  approach), verify the pinning is reflected in the downstream build's
  lock file after the source reference update
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE
assignment, advisory preparation, and formal disclosure. Fix must be released via a
security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <Task 3 key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

## Proposed Jira comments (each comment ends with the triage-security Comment Footnote)

1. **Cross-stream impact (Case A):** "Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x based on lock file analysis. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage."
2. **Preemptive task list:** "Preemptive remediation tasks created for streams without CVE Jiras: 2.1.x: <Task 3 key>, <Task 4 key> (security-preemptive)."
3. **Post-triage summary:** the version impact table; the Affects Versions correction (RHTPA 2.0.0 -> RHTPA 2.2.0, 2.2.1, 2.2.2); the outcome (remediation created); the task links; release Jira references; and an @mention of the reporter. Add the `ai-cve-triaged` label at the same time.

## Pre-creation checklist

- [x] Task count per stream: 2 for each of 2.2.x and 2.1.x, as required for a Cargo source dependency
- [x] Cross-stream coverage: 2.1.x has preemptive tasks
- [x] Link types: Depend for 2.2.x tasks to TC-8001, Related for the 2.1.x preemptive tasks, Blocks from upstream to downstream
- [x] Preemptive labels: `security-preemptive` on Tasks 3 and 4
- [x] Coordination guidance: the customer-shipped guidance is in every task's Implementation Notes
- [ ] Release Jira linking: depends on the Step 7.5 outcome, which needs Jira and was not run
- [x] Dedup consistency: no dedup'd streams (Step 7.5.3 not evaluated, because the Upstream Affected Component field is not configured)
