# Step 8 — Remediation: TC-8001 (CVE-2026-31812)

## Triage Outcome

- **Case B** applies for stream 2.2.x: affected versions exist (2.2.0, 2.2.1, 2.2.2)
- **Case A** applies: cross-stream impact detected (2.1.x is also affected but outside this issue's scope)
- **Ecosystem**: Cargo (source dependency, fix available upstream)
- **Task count**: 2 tasks for 2.2.x stream (dependency bump + downstream propagation)
- **Deployment context**: customer-shipped

---

## Remediation Task 1: Dependency Bump (2.2.x stream)

### Jira Issue Creation

```
summary: "Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)"
issueType: Task
labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
```

### Task Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream --
a package manager update is sufficient.

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8, v0.4.8 (2.2.2 is retag of 2.2.1)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct dependency (quinn-proto is a direct Cargo dependency)
- **Remediation action**: run the appropriate package manager update command:
  - **Cargo**: `cargo update -p quinn-proto` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

## Remediation Task 2: Downstream Propagation (2.2.x stream)

### Jira Issue Creation

```
summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)"
issueType: Task
labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
```

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the dependency bump task.

The dependency bump task bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
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

- Depends on: dependency bump task (upstream dependency bump must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Jira Linkage Plan

1. **Depend**: TC-8001 (CVE Vulnerability) --> dependency bump task
2. **Depend**: TC-8001 (CVE Vulnerability) --> downstream propagation task
3. **Blocks**: dependency bump task --> downstream propagation task (upstream must merge first)
4. **Blocks**: dependency bump task --> release Task (if release Jira active from Step 7.5)
5. **Blocks**: downstream propagation task --> release Task (if release Jira active from Step 7.5)
6. **Related**: release Task --> TC-8001 (traceability)

---

## Cross-Stream Impact (Case A)

Stream **2.1.x** is also affected by CVE-2026-31812 but is outside this issue's scope (issue is scoped to `[rhtpa-2.2]`).

### Cross-stream impact comment (to post on TC-8001):

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis.
> Versions affected: 2.1.0 (quinn-proto 0.11.9), 2.1.1 (quinn-proto 0.11.9).
> This stream is tracked by a companion issue (see Related links) or may require separate PSIRT triage.

If no sibling CVE Jira exists for 2.1.x, preemptive remediation tasks would be created with:
- Labels: `["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]`
- Link type: "Related" (not "Depend") to TC-8001
- Description prefix noting the originating CVE and stream

Note: The 2.1.x upstream branch (`release/0.3.z`) does NOT have the fix (quinn-proto 0.11.9), so 2.1.x preemptive tasks would use the **upstream backport** template (not the dependency bump template).

---

## Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions is incorrect:

- **Current**: `[RHTPA 2.0.0]` (RHTPA 2.0.0 does not exist as a configured version)
- **Proposed** (scoped to 2.2.x stream): `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are NOT affected (they ship quinn-proto 0.11.14).

---

## Post-Triage Summary

1. **Version impact**: quinn-proto < 0.11.14 affects RHTPA 2.2.0, 2.2.1, 2.2.2 (and 2.1.0, 2.1.1 cross-stream)
2. **Affects Versions correction**: RHTPA 2.0.0 --> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
3. **Triage outcome**: Remediation tasks created for 2.2.x stream
4. **Remediation tasks**:
   - Dependency bump: update quinn-proto to 0.11.14 on release/0.4.z
   - Downstream propagation: update backend ref in rhtpa-release.0.4.z
5. **Cross-stream impact**: 2.1.x also affected -- preemptive tasks or separate PSIRT triage needed
6. **Label**: `ai-cve-triaged` added to TC-8001
