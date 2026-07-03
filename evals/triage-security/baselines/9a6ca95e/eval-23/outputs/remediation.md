# Step 8 -- Remediation: TC-8001 (CVE-2026-31812)

## Triage Outcome

**Case A: Affected** -- supported versions in the scoped stream (2.2.x) are affected. Remediation tasks are required.

**Case B: Cross-stream impact** -- stream 2.1.x is also affected. Cross-stream notice and preemptive remediation tasks are required if no sibling CVE Jira exists for 2.1.x.

Affected versions within scope (2.2.x): RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Not affected within scope: RHTPA 2.2.3, RHTPA 2.2.4 (ship quinn-proto 0.11.14, the fixed version)

Ecosystem: **Cargo** (source dependency) -- two tasks required: upstream backport + downstream propagation.

---

## Remediation Task 1: Upstream Backport (2.2.x stream)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)

**Labels**: ai-generated-jira, Security, CVE-2026-31812

### Task Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (v0.4.5, quinn-proto 0.11.9), RHTPA 2.2.1 (v0.4.8, quinn-proto 0.11.12), RHTPA 2.2.2 (v0.4.9, retag of 2.2.1)
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

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

## Remediation Task 2: Downstream Propagation (2.2.x stream)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: ai-generated-jira, Security, CVE-2026-31812

### Task Description

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

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Cross-Stream Impact: 2.1.x Stream

Stream 2.1.x is also affected by CVE-2026-31812. All versions in the 2.1.x stream (RHTPA 2.1.0 and 2.1.1) ship quinn-proto 0.11.9, which is within the affected range (< 0.11.14).

### Cross-stream impact comment (to be posted on TC-8001):

> Cross-stream impact: quinn-proto versions before 0.11.14 also affects stream 2.1.x based on lock file analysis. This stream is tracked by a companion issue (see Related links) or may require separate PSIRT triage.

### Preemptive Remediation Tasks (if no sibling CVE Jira exists for 2.1.x)

If no sibling Vulnerability issue with label CVE-2026-31812 and suffix `[rhtpa-2.1]` exists, the following preemptive tasks should be created:

#### Preemptive Task 1: Upstream Backport (2.1.x stream)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

**Link type**: Related (to TC-8001, not Depend, because the originating CVE belongs to a different stream)

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (v0.3.8, quinn-proto 0.11.9), RHTPA 2.1.1 (v0.3.12, quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

#### Preemptive Task 2: Downstream Propagation (2.1.x stream)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

**Link type**: Related (to TC-8001)

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: preemptive upstream backport task for 2.1.x (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Jira Linkage Summary

### Standard remediation (2.2.x stream):
1. Link upstream backport task to TC-8001 with type "Depend"
2. Link downstream propagation task to TC-8001 with type "Depend"
3. Link downstream propagation task as blocked by upstream backport task with type "Blocks"

### Preemptive remediation (2.1.x stream, if no sibling CVE exists):
1. Link preemptive upstream task to TC-8001 with type "Related" (not Depend)
2. Link preemptive downstream task to TC-8001 with type "Related"
3. Link preemptive downstream task as blocked by preemptive upstream task with type "Blocks"

### Post-triage actions:
1. Add label `ai-cve-triaged` to TC-8001
2. Post summary comment on TC-8001 with version impact table, Affects Versions correction, triage outcome, and links to all created tasks
3. Transition TC-8001 to In Progress
