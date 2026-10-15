# Step 8 -- Remediation

## Triage Outcome: Case B (Affected -- create remediation tasks)

All supported versions in the 2.2.x stream ship criterion 0.5.1 (vulnerable).
Remediation tasks are required.

**Dev-dependency override applies:** criterion is a dev-only dependency
(`[dev-dependencies]` in backend/Cargo.toml). Per the dependency scope decision
tree, remediation tasks receive the `dev-dependency` label and priority is
overridden to **Normal** regardless of CVE severity (CVSS 5.3 Medium).

## Case A: Cross-Stream Impact

The issue is scoped to 2.2.x (`[rhtpa-2.2]`), but the 2.1.x stream is also
affected (criterion 0.5.1 at all 2.1.x versions). A cross-stream impact comment
would be posted on TC-8050:

> Cross-stream impact: criterion < 0.5.2 also affects stream 2.1.x based on lock
> file analysis. This stream is tracked by a companion issue (see Related links) or
> may require separate PSIRT triage.

Preemptive remediation tasks for the 2.1.x stream would be created if no sibling
CVE Jira exists for that stream (with `security-preemptive` label and "Related"
link type).

## Remediation Tasks for 2.2.x Stream

Ecosystem: Cargo (source dependency). Upstream fix not yet available on
`release/0.4.z`. Two tasks required per the ecosystem classification table.

---

### Task 1: Upstream Dependency Bump

**Proposed Jira action: create_issue (Task)**

- **Summary:** Remediate CVE-2026-99001: bump criterion to 0.5.2 (rhtpa-2.2)
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`
- **Priority:** Normal (dev-dependency override -- not inherited from CVE severity)

#### Task Description

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99001: bump criterion to 0.5.2 via dependency update.
The vulnerable dependency (criterion < 0.5.2) allows path traversal in
benchmark output files via crafted benchmark names.

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

Affected versions: RHTPA 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4
Source commit(s): v0.4.5, v0.4.8, v0.4.11, v0.4.12

CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct dev-dependency
- **Dependency scope**: dev-only ([dev-dependencies] in backend/Cargo.toml)
  -- NOT present in production builds, used for benchmarks only
- **Remediation action**: update criterion version in backend/Cargo.toml
  from "0.5.1" to ">= 0.5.2" and run `cargo update -p criterion` to
  update Cargo.lock
- Verify Cargo.lock reflects criterion >= 0.5.2 after the update

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2 in backend/Cargo.toml
- [ ] Cargo.lock updated via cargo update (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency
- [ ] Benchmarks still compile and run correctly

## Dependencies

- Depends on: TC-8050 (parent tracking issue)
```

**Proposed Jira actions after task creation:**
- Post description digest comment on the new task
- Create link: Depend (inward: TC-8050, outward: new task key)

---

### Task 2: Downstream Propagation

**Proposed Jira action: create_issue (Task)**

- **Summary:** Propagate CVE-2026-99001 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`
- **Priority:** Normal (dev-dependency override -- not inherited from CVE severity)

#### Task Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99001 fix from the upstream dependency bump task.

The upstream task bumps criterion to 0.5.2 on release/0.4.z. Once that
PR merges, update the source pinning in this Konflux release repo so
the next build ships the fix.

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct dev-dependency -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the criterion bump
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream dependency bump task (must merge first)
- Depends on: TC-8050 (parent tracking issue)
```

**Proposed Jira actions after task creation:**
- Post description digest comment on the new task
- Create link: Depend (inward: TC-8050, outward: new downstream task key)
- Create link: Blocks (inward: upstream task key, outward: downstream task key)

---

## Post-Triage Summary (proposed actions)

The following Jira mutations are proposed (not executed):

1. **Add label** `ai-cve-triaged` to TC-8050
2. **Affects Versions correction:** Current `[RHTPA 2.2.0]` should be corrected
   to `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2, RHTPA 2.2.3, RHTPA 2.2.4]`
   (all 2.2.x versions are affected, scoped to this stream only)
3. **Post summary comment** on TC-8050 documenting:
   - Version impact table (all 2.2.x versions affected)
   - Affects Versions correction (RHTPA 2.2.0 -> all 2.2.x versions)
   - Remediation outcome: 2 tasks created (upstream bump + downstream propagation)
   - Dev-dependency status: criterion is dev-only, priority set to Normal
   - Cross-stream impact: 2.1.x also affected
4. **Cross-stream impact comment** on TC-8050 noting 2.1.x is also affected

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks for 2.2.x (Cargo source dependency: upstream bump + downstream propagation)
- [x] **Cross-stream coverage**: 2.1.x stream identified as also affected; preemptive tasks would be created if no sibling CVE Jira exists for 2.1.x
- [x] **Link types**: "Depend" for tasks linked to TC-8050; "Blocks" for upstream -> downstream within stream
- [x] **Dev-dependency label**: both tasks carry the `dev-dependency` label
- [x] **Priority override**: both tasks set to Normal (dev-dependency override)
- [x] **Coordination guidance**: upstream deployment context -- included in task descriptions
