# Step 8 -- Remediation

## Triage Outcome

criterion is a **dev-only dependency** (declared in `[dev-dependencies]`). It is NOT present in production builds. All 2.2.x versions ship criterion 0.5.1, which is within the affected range (< 0.5.2).

Per the dependency scope decision tree, remediation tasks are still created for supply chain risk mitigation, but with the `dev-dependency` label and **Normal** priority override.

## Case A: Cross-Stream Impact

The issue is scoped to the 2.2.x stream (`[rhtpa-2.2]`). Cross-stream analysis shows the 2.1.x stream is also affected (all versions ship criterion 0.5.1). A cross-stream impact comment would be posted to TC-8050:

> Cross-stream impact: criterion < 0.5.2 also affects stream 2.1.x based on lock file analysis. This stream is tracked by a companion issue (see Related links) or may require separate PSIRT triage.

## Case B: Remediation Tasks (2.2.x stream)

Ecosystem: Cargo (source dependency) -- 2 tasks created.

### Task 1: Upstream Backport

**Summary:** Remediate CVE-2026-99001: bump criterion to 0.5.2 (2.2.x)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority:** Normal (dev-dependency override)

#### Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99001: path traversal in benchmark output in criterion.
The vulnerable dependency (criterion < 0.5.2) must be updated to the fixed version (0.5.2+).

This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only).

Affected versions: 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4
Source commit(s): v0.4.5, v0.4.8, v0.4.11, v0.4.12

CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct dev-dependency
- **Dev-only**: criterion is in `[dev-dependencies]` and is used for benchmarks only. It is NOT shipped in production builds. Priority is Normal regardless of CVE severity.

### Remediation approach (direct dependency)

- Update criterion dependency to >= 0.5.2 in backend/Cargo.toml `[dev-dependencies]`
- Run `cargo update -p criterion` to update Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8050 (parent tracking issue)

---

### Task 2: Downstream Propagation

**Summary:** Propagate CVE-2026-99001 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority:** Normal (dev-dependency override)

**Blocked by:** Task 1 (upstream backport)

#### Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-99001 fix from the upstream backport task.

This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only).

The upstream backport bumps criterion to 0.5.2 on release/0.4.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct dev-dependency -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8050 (parent tracking issue)

---

## Linkage

1. Both tasks linked to TC-8050 with link type "Depend"
2. Downstream propagation task blocked by upstream backport task (link type "Blocks")
3. TC-8050 transitioned to In Progress
4. Label `ai-cve-triaged` added to TC-8050

## Preemptive Tasks for 2.1.x Stream

Since the 2.1.x stream is also affected but this issue is scoped to 2.2.x only, preemptive remediation tasks would be created for the 2.1.x stream with the `security-preemptive` label (in addition to `dev-dependency`), linked to TC-8050 with "Related" link type (not "Depend").
