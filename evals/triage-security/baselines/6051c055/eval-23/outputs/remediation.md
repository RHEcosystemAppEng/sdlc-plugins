# Step 8 -- Remediation: TC-8001 (CVE-2026-31812)

## Triage Outcome

The issue TC-8001 is **scoped to stream 2.2.x** (from the `[rhtpa-2.2]` summary suffix).

- **Case A** applies for stream 2.2.x: versions 2.2.0, 2.2.1, and 2.2.2 are affected.
- **Case B** applies: stream 2.1.x is also affected (all versions ship quinn-proto 0.11.9) but has no stream-specific CVE Jira. Preemptive remediation tasks are created for 2.1.x.

Ecosystem: **Cargo** (source dependency) -- two tasks per affected stream (upstream backport + downstream propagation).

---

## Case A: Remediation Tasks for Stream 2.2.x

### Task 1: Upstream Backport Task (Stream 2.2.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)
**Labels**: ai-generated-jira, Security, CVE-2026-31812

#### Repository

rhtpa-backend

#### Target Branch

release/0.4.z

#### Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0 (v0.4.5, quinn-proto 0.11.9), 2.2.1 (v0.4.8, quinn-proto 0.11.12), 2.2.2 (v0.4.9, retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

#### Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (quinn-proto is a direct Cargo dependency)

##### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

##### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

#### Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

#### Test Requirements

- [ ] Existing test suite passes with the updated dependency

#### Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

### Task 2: Downstream Propagation Subtask (Stream 2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)
**Labels**: ai-generated-jira, Security, CVE-2026-31812

#### Repository

rhtpa-release.0.4.z

#### Target Branch

main

#### Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

#### Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

##### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

#### Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

#### Test Requirements

- [ ] Container image builds successfully with the updated reference

#### Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Case B: Preemptive Remediation Tasks for Stream 2.1.x

Stream 2.1.x is affected (all versions ship quinn-proto 0.11.9) but has no
stream-specific CVE Jira for CVE-2026-31812. Preemptive tasks are created with
the `security-preemptive` label and linked to TC-8001 via "Related" (not "Depend").

### Task 3: Upstream Backport Task (Stream 2.1.x, Preemptive)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)
**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

#### Repository

rhtpa-backend

#### Target Branch

release/0.3.z

#### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8, quinn-proto 0.11.9), 2.1.1 (v0.3.12, quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

#### Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (quinn-proto is a direct Cargo dependency)

##### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

##### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

#### Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

#### Test Requirements

- [ ] Existing test suite passes with the updated dependency

#### Dependencies

- Related to: TC-8001 (originating CVE Jira, stream 2.2.x)

---

### Task 4: Downstream Propagation Subtask (Stream 2.1.x, Preemptive)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)
**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

#### Repository

rhtpa-release.0.3.z

#### Target Branch

main

#### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task for stream 2.1.x.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

#### Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

##### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

#### Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

#### Test Requirements

- [ ] Container image builds successfully with the updated reference

#### Dependencies

- Depends on: upstream backport task for 2.1.x (upstream backport must merge first)
- Related to: TC-8001 (originating CVE Jira, stream 2.2.x)

---

## Cross-Stream Impact Comment (for TC-8001)

```
Cross-stream impact: quinn-proto (versions before 0.11.14) also affects stream(s)
2.1.x based on lock file analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: upstream backport task (security-preemptive) + downstream propagation task (security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

## Jira Linkage Summary

### Standard remediation (stream 2.2.x)
- Upstream backport task --[Depend]--> TC-8001
- Downstream propagation task --[Blocks by]--> upstream backport task
- Downstream propagation task --[Depend]--> TC-8001

### Preemptive remediation (stream 2.1.x)
- Upstream backport task --[Related]--> TC-8001
- Downstream propagation task --[Blocks by]--> upstream backport task (2.1.x)
- Downstream propagation task --[Related]--> TC-8001
