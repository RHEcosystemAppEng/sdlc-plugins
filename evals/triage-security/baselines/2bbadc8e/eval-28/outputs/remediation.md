# Step 8 -- Remediation

## Triage Decision

**Case B: Affected -- create remediation tasks**

Versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream are affected (h2 0.4.4 < 0.4.5). Versions 2.2.3 and 2.2.4 already ship the fix (h2 0.4.5).

Since the upstream branch (release/0.4.z) already ships h2 0.4.5 (confirmed in Step 2.5), the **dependency bump** variant applies. This means 2 tasks per affected stream:
1. Dependency bump task (bump h2 to >= 0.4.5 in the source repo)
2. Downstream propagation task (update backend reference in Konflux release repo)

### Cross-stream assessment

- 2.1.x: NOT affected (h2 = 0.4.5 in all versions). Case A does not apply.
- No preemptive tasks needed for other streams.

### Dependency chain context

h2 is a **transitive** dependency (3 levels deep):
```
backend (workspace) -> reqwest -> hyper -> h2
```

Because h2 is transitive, the remediation uses a **two-tier approach**:
- **Preferred**: bump the direct dependency (reqwest) to a version whose transitive closure includes h2 >= 0.4.5
- **Fallback**: pin h2 directly via `cargo add h2@0.4.5` if the reqwest bump is not viable

---

## PROPOSED Remediation Task 1: Dependency Bump (upstream)

**PROPOSAL -- not executed. Requires engineer confirmation before Jira creation.**

### Jira creation parameters

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-99010: update h2 to 0.4.5 (2.2.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99010"]
)
```

### Task description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99010: bump h2 to 0.4.5 via dependency update.
The vulnerable dependency (h2 < 0.4.5) is already fixed upstream --
a package manager update is sufficient.

h2 is a **transitive** dependency pulled in through the following chain:
```
backend (workspace) -> reqwest -> hyper -> h2
```

Affected versions: 2.2.0, 2.2.1, 2.2.2
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is retag of v0.4.8)

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99010

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend -> reqwest -> hyper -> h2)
- **Remediation action**: use a two-tier approach for this transitive dependency:

### Remediation approach (transitive dependency -- two-tier)

**Preferred: bump the direct dependency (reqwest)**
- Identify whether a newer version of reqwest (currently 0.12.5) pulls in
  hyper with h2 >= 0.4.5 in its transitive closure
- Run `cargo update -p reqwest` to pull in the latest compatible version
- Verify via `cargo tree -p h2` that h2 is now >= 0.4.5
- If the reqwest update pulls h2 >= 0.4.5, this is sufficient

**Fallback: pin the transitive dependency directly**
If bumping reqwest does not resolve h2 to >= 0.4.5 (e.g., reqwest 0.12.x
pins hyper to a version that still depends on h2 < 0.4.5):
- Run `cargo add h2@0.4.5` to add h2 as a direct dependency, overriding
  the transitive resolution
- Document why the reqwest bump was not viable in the PR description
- Verify via `cargo tree -p h2` that only h2 >= 0.4.5 appears

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.5 (verified via `cargo tree -p h2`)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass
- [ ] If fallback pinning was used, PR description documents why reqwest bump was insufficient

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8060 (parent tracking issue)

---

## PROPOSED Remediation Task 2: Downstream Propagation

**PROPOSAL -- not executed. Requires engineer confirmation before Jira creation.**

### Jira creation parameters

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-99010 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99010"]
)
```

### Task description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99010 fix from the dependency bump task.

The dependency bump task updates h2 to 0.4.5 on release/0.4.z
(via reqwest/hyper transitive chain). Once that PR merges, update
the source pinning in this Konflux release repo so the next build
ships the fix.

h2 is a **transitive** dependency:
```
backend (workspace) -> reqwest -> hyper -> h2
```

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: transitive -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
  that includes h2 >= 0.4.5
- If the upstream fix pinned h2 directly (fallback approach), verify the
  pinning is reflected in the downstream build's Cargo.lock after the
  source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image
- [ ] Container image's Cargo.lock contains h2 >= 0.4.5

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: [dependency-bump-task-key] (dependency bump must merge first)
- Depends on: TC-8060 (parent tracking issue)

---

## PROPOSED Jira Linkage

After creating both tasks (pending engineer confirmation):

1. **Depend link**: TC-8060 (CVE) -> dependency bump task
   ```
   jira.create_link(inwardIssue: "TC-8060", outwardIssue: <bump-task-key>, type: "Depend")
   ```

2. **Depend link**: TC-8060 (CVE) -> downstream propagation task
   ```
   jira.create_link(inwardIssue: "TC-8060", outwardIssue: <downstream-task-key>, type: "Depend")
   ```

3. **Blocks link**: dependency bump task -> downstream propagation task
   ```
   jira.create_link(inwardIssue: <bump-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
   ```

4. **Description digest**: post digest comment on each task per description-digest-protocol.md (before any links or comments)

5. **Release Task linking** (if Step 7.5 produced a release Task):
   - Blocks: each remediation task -> release Task
   - Related: release Task -> TC-8060

## PROPOSED Post-Triage Actions

1. **Add label**: `ai-cve-triaged` to TC-8060
2. **Affects Versions correction**: PSIRT set `RHTPA 2.2.0`. Based on version impact analysis, affected versions are RHTPA 2.2.0, 2.2.1, and 2.2.2. Add RHTPA 2.2.1 and RHTPA 2.2.2 to Affects Versions (pending dynamic version discovery via Jira API).
3. **Post summary comment** on TC-8060 documenting:
   - Version impact table
   - Dependency chain: backend -> reqwest -> hyper -> h2 (transitive, 3 levels)
   - Remediation outcome: 2 tasks created (dependency bump + downstream propagation)
   - Two-tier remediation approach for transitive dependency
   - @mention reporter psirt-analyst (557058:psirt-analyst-mock-id)

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks for 2.2.x (Cargo source dependency -- dependency bump + downstream propagation). Matches ecosystem classification table.
- [x] **Cross-stream coverage**: 2.1.x is not affected. No preemptive tasks needed.
- [x] **Link types**: "Depend" for tasks linked to TC-8060 (their own CVE Jira). "Blocks" from dependency bump to downstream propagation.
- [x] **Preemptive labels**: Not applicable (no preemptive tasks created).
- [x] **Coordination guidance**: Included in dependency bump task -- "upstream" deployment context.
- [x] **Dependency chain documented**: Full transitive chain (backend -> reqwest -> hyper -> h2) included in both task descriptions with two-tier remediation approach.
- [x] **Two-tier remediation**: Preferred approach (bump reqwest) and fallback (pin h2 directly) both documented in dependency bump task.
