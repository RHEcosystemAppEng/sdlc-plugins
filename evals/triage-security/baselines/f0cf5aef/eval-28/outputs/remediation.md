# Step 8 -- Remediation: CVE-2026-99010

## Triage Outcome

**Case B: Affected -- create remediation tasks**

Versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream ship h2 0.4.4, which is
within the affected range (< 0.4.5). Versions 2.2.3 and 2.2.4 already ship
h2 0.4.5 and are not affected.

**Case A check (cross-stream impact)**: The 2.1.x stream is NOT affected (all
versions ship h2 0.4.5). No cross-stream impact comment or preemptive tasks needed.

**Ecosystem**: Cargo (source dependency) -- requires **2 tasks** for the 2.2.x stream:
1. Upstream backport task (fix in rhtpa-backend source repo)
2. Downstream propagation subtask (update reference in Konflux release repo, blocked by upstream task)

---

## Task 1: Upstream Backport Task

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-99010: bump h2 to 0.4.5 (2.2.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99010"]
)
```

### Task Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99010: h2 memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.5) must be updated to the fixed version (0.4.5+).

Affected versions: 2.2.0, 2.2.1, 2.2.2
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is a retag of v0.4.8)

Upstream fix: https://github.com/hyperium/h2/pull/800
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99010

## Implementation Notes

- Target branch: `release/0.4.z`
- **Dependency type**: transitive (chain: backend -> reqwest -> hyper -> h2, 3 levels deep)
- h2 is NOT a direct dependency of the backend workspace. It is pulled in transitively through the chain: `reqwest` (direct dep) -> `hyper` -> `h2`

### Remediation approach (transitive dependency)

The vulnerable package h2 is a **transitive** dependency pulled in through
intermediate packages (reqwest -> hyper -> h2). Use a two-tier approach:

**Preferred: bump the direct dependency (reqwest)**
- `reqwest` is the direct dependency that ultimately pulls in h2 via hyper
- Bump `reqwest` to a version whose transitive closure includes h2 >= 0.4.5
- Check reqwest's Cargo.lock or release notes to verify which version pulls in a fixed h2
- Verify the bump does not introduce breaking API changes to reqwest
- Current reqwest version: 0.12.5 (from Cargo.lock of affected versions)

**Fallback: pin the transitive dependency directly**
If bumping reqwest is not viable (breaking API changes, no release available with
the fix, or reqwest's dependency on hyper still resolves to h2 < 0.4.5):
- Run `cargo add h2@0.4.5` to add h2 as a direct dependency, overriding the
  transitive resolution
- This forces Cargo to resolve h2 to >= 0.4.5 regardless of what reqwest/hyper request
- Document why the direct dep bump was not viable in the PR description

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.5 (verify in Cargo.lock after build)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8060 (parent tracking issue)

---

## Task 2: Downstream Propagation Subtask

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-99010 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99010"]
)
```

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99010 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.5 on release/0.4.z by either bumping
reqwest (preferred) or pinning h2 directly (fallback). Once that PR merges,
update the source pinning in this Konflux release repo so the next build
ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: transitive -- carried forward from upstream task (chain: backend -> reqwest -> hyper -> h2)
- Update the rhtpa-backend reference to the merged commit or new release tag that includes h2 >= 0.4.5
- If the upstream fix pinned h2 directly (fallback approach via `cargo add h2@0.4.5`), verify the pinning is reflected in the downstream build's Cargo.lock after the source reference update
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix (h2 >= 0.4.5 in resolved Cargo.lock)
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8060 (parent tracking issue)

---

## Jira Linkage

After creating both tasks:

1. **Link upstream task to CVE Vulnerability issue:**
   ```
   jira.create_link(
     inwardIssue: "TC-8060",
     outwardIssue: <upstream-task-key>,
     type: "Depend"
   )
   ```

2. **Link downstream task to CVE Vulnerability issue:**
   ```
   jira.create_link(
     inwardIssue: "TC-8060",
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )
   ```

3. **Link downstream task as blocked by upstream task:**
   ```
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

4. **Transition** TC-8060 to In Progress.

5. **Add ai-cve-triaged label** to TC-8060.

6. **Post summary comment** to TC-8060 documenting the triage outcome,
   version impact table, and links to both remediation tasks, with
   @mention of the reporter (psirt-analyst, account ID: 557058:psirt-analyst-mock-id).

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks for 2.2.x stream (Cargo = source dependency ecosystem)
- [x] **Cross-stream coverage**: 2.1.x is not affected -- no preemptive tasks needed
- [x] **Link types**: "Depend" for tasks linked to TC-8060, "Blocks" for upstream -> downstream
- [x] **Preemptive labels**: N/A -- no preemptive tasks (no cross-stream impact)
- [x] **Coordination guidance**: included in both tasks (upstream deployment context)
- [x] **Dependency chain**: full chain (backend -> reqwest -> hyper -> h2) documented in upstream task Implementation Notes
- [x] **Two-tier remediation**: preferred (bump reqwest) and fallback (cargo add h2@0.4.5) both specified
