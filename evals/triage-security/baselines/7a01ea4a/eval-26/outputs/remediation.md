# Step 8 -- Remediation: CVE-2026-99001

## Triage Outcome

**Case A**: Affected -- create remediation tasks for the 2.2.x stream (issue scope).

**Case B**: Cross-stream impact -- the 2.1.x stream is also affected. A cross-stream impact comment would be posted, and preemptive remediation tasks created for the 2.1.x stream if no companion CVE Jira exists.

**Dev-dependency override**: criterion is a dev-only dependency (not shipped in production). Per the dependency scope decision tree, all remediation tasks receive:
- Label: `dev-dependency`
- Priority: **Normal** (overrides CVE severity of Medium/5.3)
- Note in description: "This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only)."

---

## Remediation Tasks -- 2.2.x Stream (Case A, in scope)

### Task 1: Upstream Backport (2.2.x)

**Summary**: Remediate CVE-2026-99001: bump criterion to 0.5.2 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority**: Normal

#### Repository

rhtpa-backend

#### Target Branch

release/0.4.z

#### Description

Remediate CVE-2026-99001: path traversal in benchmark output in criterion.
The vulnerable dependency (criterion < 0.5.2) must be updated to the fixed version (0.5.2+).

This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only).

Affected versions: 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4
Source commit(s): v0.4.5, v0.4.8, v0.4.9 (retag), v0.4.11, v0.4.12

CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99001

#### Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct dev-dependency
- **Dependency scope**: dev-only ([dev-dependencies] in backend/Cargo.toml) -- NOT shipped in production builds, used for benchmarks only

##### Remediation approach (direct dependency)

- Update criterion dependency to >= 0.5.2 in backend/Cargo.toml `[dev-dependencies]`
- Run `cargo update -p criterion` to update Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

#### Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2 in backend/Cargo.toml
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

#### Test Requirements

- [ ] Existing test suite passes with the updated dependency

#### Dependencies

- Depends on: TC-8050 (parent tracking issue)

---

### Task 2: Downstream Propagation (2.2.x)

**Summary**: Propagate CVE-2026-99001 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority**: Normal

#### Repository

rhtpa-release.0.4.z

#### Target Branch

main

#### Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-99001 fix from the upstream backport task.

The upstream backport bumps criterion to 0.5.2 on release/0.4.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only).

#### Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct dev-dependency -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

#### Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

#### Test Requirements

- [ ] Container image builds successfully with the updated reference

#### Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8050 (parent tracking issue)

---

## Preemptive Remediation Tasks -- 2.1.x Stream (Case B, cross-stream)

The 2.1.x stream is also affected (criterion 0.5.1 in versions 2.1.0 and 2.1.1). Since this issue is scoped to the 2.2.x stream, preemptive remediation tasks are created for the 2.1.x stream with the `security-preemptive` label.

### Task 3: Preemptive Upstream Backport (2.1.x)

**Summary**: Remediate CVE-2026-99001: bump criterion to 0.5.2 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`, `security-preemptive`

**Priority**: Normal

**Link type**: Related (to TC-8050, not Depend, because this is a preemptive task from a different stream)

#### Repository

rhtpa-backend

#### Target Branch

release/0.3.z

#### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8050 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-99001: path traversal in benchmark output in criterion.
The vulnerable dependency (criterion < 0.5.2) must be updated to the fixed version (0.5.2+).

This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only).

Affected versions: 2.1.0, 2.1.1
Source commit(s): v0.3.8, v0.3.12

CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99001

#### Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct dev-dependency
- **Dependency scope**: dev-only ([dev-dependencies] in backend/Cargo.toml) -- NOT shipped in production builds, used for benchmarks only

##### Remediation approach (direct dependency)

- Update criterion dependency to >= 0.5.2 in backend/Cargo.toml `[dev-dependencies]`
- Run `cargo update -p criterion` to update Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

#### Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2 in backend/Cargo.toml
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

#### Test Requirements

- [ ] Existing test suite passes with the updated dependency

#### Dependencies

- Depends on: TC-8050 (related -- originating CVE from 2.2.x stream)

---

### Task 4: Preemptive Downstream Propagation (2.1.x)

**Summary**: Propagate CVE-2026-99001 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`, `security-preemptive`

**Priority**: Normal

**Link type**: Related (to TC-8050)

#### Repository

rhtpa-release.0.3.z

#### Target Branch

main

#### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8050 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-99001 fix from the preemptive upstream backport task.

The upstream backport bumps criterion to 0.5.2 on release/0.3.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only).

#### Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct dev-dependency -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

#### Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

#### Test Requirements

- [ ] Container image builds successfully with the updated reference

#### Dependencies

- Depends on: preemptive upstream backport task (upstream backport must merge first)
- Depends on: TC-8050 (related -- originating CVE from 2.2.x stream)

---

## Cross-Stream Impact Comment

The following comment would be posted to TC-8050:

```
Cross-stream impact: criterion < 0.5.2 also affects stream 2.1.x based on lock file analysis.
These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: upstream backport task + downstream propagation task (security-preemptive, dev-dependency)

These tasks use the "Related" link type and carry the security-preemptive label.
When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link them and remove the label.
```

## Summary of Dev-Dependency Handling

| Aspect | Standard Handling | Dev-Dependency Override |
|--------|-------------------|------------------------|
| Priority | Inherits CVE severity (Medium) | **Normal** |
| Labels | ai-generated-jira, Security, CVE-ID | ai-generated-jira, Security, CVE-ID, **dev-dependency** |
| Description note | (none) | "This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only)." |
| Rationale | Production risk | Supply chain risk only -- criterion is in [dev-dependencies] and is NOT present in production builds |
