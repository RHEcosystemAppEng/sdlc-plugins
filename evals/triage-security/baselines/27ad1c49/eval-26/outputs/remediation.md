# Step 8 -- Remediation: CVE-2026-99001 (criterion)

## Triage Outcome

**Case B: Affected -- create remediation tasks** for stream 2.2.x.

All versions in the 2.2.x stream (2.2.0 through 2.2.4) ship criterion 0.5.1,
which is within the affected range (< 0.5.2). Remediation is required.

**Dev-dependency handling**: criterion is declared in `[dev-dependencies]` and
is NOT present in production builds. Per the dependency scope decision tree:
- Add `dev-dependency` label to all remediation tasks
- Override priority to **Normal** regardless of CVE severity (Medium/5.3)
- Include dev-dependency note in task descriptions

## Cross-stream impact (Case A)

The 2.1.x stream is also affected but is outside this issue's scope. A
cross-stream impact comment would be posted to TC-8050:

> Cross-stream impact: criterion < 0.5.2 also affects stream 2.1.x based on
> lock file analysis. These streams are tracked by companion issues (see
> Related links) or may require separate PSIRT triage.

If no sibling CVE Jira exists for 2.1.x, preemptive remediation tasks would be
created with the `security-preemptive` label for that stream.

## Remediation Tasks for Stream 2.2.x

Ecosystem: Cargo (source dependency) -- 2 tasks required:
1. Upstream dependency bump task
2. Downstream propagation subtask (blocked by task 1)

---

### Task 1: Upstream Dependency Bump (rhtpa-2.2)

**Summary**: Remediate CVE-2026-99001: update criterion to 0.5.2 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority**: Normal (override -- dev-dependency, not shipped in production)

**Description**:

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99001: bump criterion to 0.5.2 via dependency update.
The vulnerable dependency (criterion < 0.5.2) allows an attacker to write
benchmark output files to arbitrary paths via crafted benchmark names
containing path separators.

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

Affected versions: RHTPA 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4
Source commit(s): v0.4.5, v0.4.8, v0.4.11, v0.4.12

CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct dev-dependency
- **Dependency scope**: dev-only ([dev-dependencies] in backend/Cargo.toml) --
  used for benchmarks only, NOT shipped in production builds
- **Remediation action**: run `cargo update -p criterion` to pull in the latest
  compatible version (>= 0.5.2)
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add criterion@0.5.2 --dev`
- Verify the lock file reflects >= 0.5.2 after the update

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8050 (parent tracking issue)
```

---

### Task 2: Downstream Propagation (rhtpa-2.2)

**Summary**: Propagate CVE-2026-99001 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority**: Normal (override -- dev-dependency, not shipped in production)

**Description**:

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99001 fix from the upstream dependency bump task.

The upstream task bumps criterion to 0.5.2 on release/0.4.z.
Once that PR merges, update the source pinning in this Konflux release
repo so the next build ships the fix.

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

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

- Depends on: [upstream-task-key] (upstream dependency bump must merge first)
- Depends on: TC-8050 (parent tracking issue)
```

## Jira Linkage Plan

1. **Task 1 -> TC-8050**: Link type "Depend" (remediation task depends on CVE)
2. **Task 2 -> TC-8050**: Link type "Depend" (remediation task depends on CVE)
3. **Task 1 -> Task 2**: Link type "Blocks" (upstream blocks downstream)
4. **Release Task linking**: If release Jira is active (Step 7.5), link both
   remediation tasks to the release Task (Blocks) and TC-8050 to the release
   Task (Related).

## Priority Override Rationale

Per the dependency scope decision tree in version-impact-analysis.md:

- criterion is declared in `[dev-dependencies]` in backend/Cargo.toml
- It is used for benchmarks only and is NOT present in production builds
- Even though dev-only dependencies are not shipped, they still represent a
  supply chain risk (compromised dev deps can inject malicious code during builds)
- Remediation tasks are still created, but with these modifications:
  - **Label**: `dev-dependency` added to both tasks
  - **Priority**: Normal (overrides the CVE severity of Medium/5.3)
  - **Description note**: Includes "This dependency is dev/build-only and is not
    shipped in production. Remediation priority is Normal (supply chain risk only)."

## Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8050
2. Post summary comment to TC-8050 documenting:
   - Version impact table (all 2.2.x versions affected)
   - Affects Versions correction (if any)
   - Remediation tasks created (upstream bump + downstream propagation)
   - Dev-dependency classification and Normal priority override
   - Cross-stream impact on 2.1.x
