# Remediation — TC-8004

## Triage Outcome

**Case B: Affected -- create remediation tasks** for the 2.1.x stream only.

The 2.2.x stream is NOT affected (all versions ship h2 >= 0.4.8) and requires no remediation.

Since this is an **unscoped issue**, Case A (cross-stream impact) does not apply. Unscoped issues cover all streams by definition, so there are no "other streams outside this issue's scope." Remediation tasks are created only for actually affected streams.

## Affected Stream Summary

| Stream | Status | Action |
|--------|--------|--------|
| 2.1.x | **AFFECTED** (h2 0.4.5 in all versions) | Create remediation tasks |
| 2.2.x | NOT AFFECTED (h2 >= 0.4.8 in all versions) | No action needed |

## Ecosystem Classification

- **Ecosystem**: Cargo (source dependency)
- **Task count per stream**: 2 (upstream backport or dependency bump + downstream propagation)
- **Total tasks**: 2 (for 2.1.x stream only)

Since h2 0.4.8 is a published crate and the fix is available upstream, the remediation is a **dependency bump** (not an upstream backport requiring source code changes). The `release/0.3.z` branch needs `cargo update -p h2` to pull in h2 >= 0.4.8.

## Remediation Task 1: Dependency Bump (2.1.x stream)

### Jira Issue Creation

```
Project: TC
Issue Type: Task
Summary: Remediate CVE-2026-33501: update h2 to 0.4.8 (2.1.x)
Labels: ai-generated-jira, Security, CVE-2026-33501
Link: Depend -> TC-8004
```

### Task Description

```markdown
## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: bump h2 to 0.4.8 via dependency update.
The vulnerable dependency (h2 versions before 0.4.8) is already fixed upstream --
a package manager update is sufficient.

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: likely transitive (chain: backend -> hyper/reqwest -> h2)
- **Remediation action**: run the appropriate package manager update command:
  - **Cargo**: `cargo update -p h2` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add h2@0.4.8`
- Verify the lock file reflects >= 0.4.8 after the update

### Remediation approach (transitive dependency)

When the vulnerable package is a **transitive** dependency (pulled in
through intermediate packages), use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in h2 (likely hyper or reqwest)
- Bump the direct dependency to a version whose transitive closure
  includes h2 >= 0.4.8
- Verify the bump does not introduce breaking API changes to the
  direct dependency

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable (breaking API changes,
no release available with the fix):
- Cargo: `cargo add h2@0.4.8` to add as a direct dependency,
  overriding the transitive resolution
- Document why the direct dep bump was not viable in the PR description

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)
```

## Remediation Task 2: Downstream Propagation (2.1.x stream)

### Jira Issue Creation

```
Project: TC
Issue Type: Task
Summary: Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)
Labels: ai-generated-jira, Security, CVE-2026-33501
Link: Depend -> TC-8004
Link: Blocked by -> [Task 1 key]
```

### Task Description

```markdown
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from [Task 1 key].

The dependency bump ([Task 1 key]) updates h2 to 0.4.8
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: transitive -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: [Task 1 key] (dependency bump must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

## Link Topology

```
TC-8004 (CVE Vulnerability)
  |
  +-- Depend --> [Task 1] (Remediate CVE-2026-33501: update h2 to 0.4.8 (2.1.x))
  |                |
  |                +-- Blocks --> [Task 2] (Propagate fix: update backend ref in rhtpa-release.0.3.z)
  |
  +-- Depend --> [Task 2]
```

## Post-Triage Actions

1. **Add label** `ai-cve-triaged` to TC-8004
2. **Post summary comment** to TC-8004 documenting:
   - Version impact table (2.1.x affected, 2.2.x not affected)
   - Affects Versions correction (removed RHTPA 2.2.0, added RHTPA 2.1.1)
   - Remediation tasks created (2 tasks for 2.1.x stream)
   - @mention of TC-8004 reporter
3. **Transition** TC-8004 to In Progress

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks for 2.1.x (Cargo source dependency: dependency bump + downstream propagation). 0 tasks for 2.2.x (not affected).
- [x] **Cross-stream coverage**: Not applicable (unscoped issue -- Case A skipped). 2.2.x requires no remediation as it is not affected.
- [x] **Link types**: "Depend" for tasks linked to TC-8004. "Blocks" for upstream dependency bump blocking downstream propagation.
- [x] **Preemptive labels**: Not applicable (no preemptive tasks needed -- unscoped issue with no affected streams lacking CVE coverage).
- [x] **Coordination guidance**: Omitted (Source Repositories table has no Deployment Context column).
- [x] **Dedup consistency**: No dedup applies (no existing remediation tasks found, JQL returned empty).

## Version Lifecycle Check (Step 5)

Both affected versions (RHTPA 2.1.0, RHTPA 2.1.1) should be verified against the product lifecycle page at https://access.example.com/product-life-cycle/rhtpa to confirm they are still within support. If any version is EOL, remediation tasks for that version would be skipped.

## Already Fixed Check (Step 6)

No resolved sibling issues exist (JQL returned empty). No already-fixed scenario detected.
