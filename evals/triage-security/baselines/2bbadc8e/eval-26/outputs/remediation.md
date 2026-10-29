# Step 8 -- Remediation: TC-8050

## Triage Outcome

**Case B: Affected -- create remediation tasks**

All versions in the 2.2.x stream ship criterion 0.5.1 (vulnerable, < 0.5.2 fix threshold). Remediation tasks are required.

**Dev-dependency override applies**: criterion is declared in `[dev-dependencies]` and is NOT present in production builds. Per the dependency scope decision tree:
- Label: `dev-dependency` added to all remediation tasks
- Priority: **Normal** (overrides CVE severity of Medium / CVSS 5.3)
- Rationale: Supply chain risk only -- the vulnerable code does not execute in production

## Remediation Tasks (PROPOSALS -- not executed)

### Task 1: Dependency Bump (upstream source repository)

**PROPOSED Jira Issue Creation:**

```
Project: TC
Issue Type: Task
Summary: Remediate CVE-2026-99001: update criterion to 0.5.2 (2.2.x)
Labels: ai-generated-jira, Security, CVE-2026-99001, dev-dependency
Priority: Normal
```

**Task Description:**

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99001: bump criterion to 0.5.2 via dependency update.
The vulnerable dependency (criterion < 0.5.2) is already fixed upstream --
a package manager update is sufficient.

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

Affected versions: 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4
Source commit(s): v0.4.5, v0.4.8, v0.4.11, v0.4.12

CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct dev-dependency
- **Dependency scope**: dev-only ([dev-dependencies] in backend/Cargo.toml) --
  NOT shipped in production builds. Used for benchmarks only.
- **Remediation action**: run `cargo update -p criterion` to pull in >= 0.5.2
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add criterion@0.5.2 --dev`
- Verify the lock file reflects criterion >= 0.5.2 after the update

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

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

**PROPOSED Jira link:**
```
Link Type: Depend
Inward Issue: TC-8050 (Vulnerability)
Outward Issue: <dependency-bump-task-key>
```

---

### Task 2: Downstream Propagation (Konflux release repository)

**PROPOSED Jira Issue Creation:**

```
Project: TC
Issue Type: Task
Summary: Propagate CVE-2026-99001 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)
Labels: ai-generated-jira, Security, CVE-2026-99001, dev-dependency
Priority: Normal
```

**Task Description:**

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99001 fix from <dependency-bump-task-key>.

The dependency bump task (<dependency-bump-task-key>) updates criterion to 0.5.2
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct dev-dependency -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <dependency-bump-task-key> (dependency bump must merge first)
- Depends on: TC-8050 (parent tracking issue)
```

**PROPOSED Jira links:**
```
Link Type: Depend
Inward Issue: TC-8050 (Vulnerability)
Outward Issue: <downstream-task-key>

Link Type: Blocks
Inward Issue: <dependency-bump-task-key> (upstream)
Outward Issue: <downstream-task-key> (downstream)
```

---

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks for 2.2.x stream (Cargo source dependency -- dependency bump + downstream propagation)
- [x] **Cross-stream coverage**: Issue is scoped to 2.2.x. Other streams (2.1.x) also ship criterion 0.5.1 but are outside this issue's scope. Case A cross-stream impact comment would note this in a real triage.
- [x] **Link types**: "Depend" for tasks linked to TC-8050, "Blocks" for upstream dependency bump to downstream propagation
- [x] **Dev-dependency label**: Both tasks carry the `dev-dependency` label
- [x] **Priority override**: Both tasks set to Normal priority (not inherited from CVE severity)
- [x] **Coordination guidance**: Included in both tasks with "upstream" deployment context guidance

## Post-Triage Summary (PROPOSAL)

**PROPOSED: Add `ai-cve-triaged` label to TC-8050**

**PROPOSED: Post summary comment to TC-8050:**

> Triage summary for CVE-2026-99001 (criterion path traversal in benchmark output):
>
> **Version Impact (2.2.x stream):**
>
> | Version | criterion | Affected? |
> |---------|-----------|-----------|
> | 2.2.0 | 0.5.1 | YES |
> | 2.2.1 | 0.5.1 | YES |
> | 2.2.2 | -- | YES (retag of 2.2.1) |
> | 2.2.3 | 0.5.1 | YES |
> | 2.2.4 | 0.5.1 | YES |
>
> **Dependency scope**: criterion is a dev-only dependency (`[dev-dependencies]`
> in backend/Cargo.toml). It is NOT shipped in production builds and is used
> for benchmarks only. Remediation priority overridden to Normal (supply chain
> risk only).
>
> **Affects Versions**: RHTPA 2.2.0 (as set by PSIRT -- to be corrected to
> include all affected 2.2.x versions based on lock file evidence)
>
> **Remediation tasks created:**
> - <dependency-bump-task-key>: Dependency bump -- update criterion to 0.5.2 (2.2.x)
> - <downstream-task-key>: Downstream propagation -- update backend ref in
>   rhtpa-release.0.4.z (2.2.x), blocked by <dependency-bump-task-key>
>
> Both tasks carry the `dev-dependency` label with Normal priority.
