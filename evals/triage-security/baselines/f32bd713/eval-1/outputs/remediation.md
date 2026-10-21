# Step 7.5 -- Release Jira Orchestration

## Release Orchestration Confirmations

Before creating remediation tasks, Step 7.5 finds or creates the release Jira
structure for each affected stream. This applies only to non-preemptive
remediation types.

### Stream 2.2.x (in-scope, non-preemptive)

**Step 7.5.1 -- Resolve stream-to-version mapping:**

- Stream `2.2.x` belongs to the `2.2` release family.
- Search for existing release Epic matching `"RHTPA 2.2.* Release Tasks"` in
  project TC.
- If no existing Epic is found, propose the next patch version. The latest
  released version in the 2.2.x supportability matrix is `2.2.4`, so the
  default next patch is `2.2.5`.
- Engineer confirmation required:

  > No release Epic found for stream 2.2.x.
  >
  > Proposed version: RHTPA 2.2.5 Release Tasks
  > (based on latest released version 2.2.4 in supportability matrix)
  >
  > Options:
  > 1. Accept -- create Epic with version 2.2.5
  > 2. Specify different version
  > 3. Skip -- do not create release Jira for this stream

- If accepted, create:
  ```
  release_epic = jira.create_issue(
    projectKey: "TC",
    issueTypeName: "Epic",
    summary: "RHTPA 2.2.5 Release Tasks",
    description: "Release tracking Epic for RHTPA 2.2.5. Contains CVE triage
      and remediation tasks for this release.",
    labels: ["ai-generated-jira"]
  )
  ```
  Post description digest comment per description-digest-protocol.md.

**Step 7.5.2 -- Find or create the release Task:**

- Search for existing release Task under the release Epic with summary matching
  `"RHTPA 2.2.5 CVE triage"`.
- If not found, engineer confirmation required:

  > No release Task found under <release-epic-key>.
  >
  > Proposed: Create "RHTPA 2.2.5 CVE triage" as child of <release-epic-key>
  >
  > Proceed? (Yes / No)

- If confirmed, create:
  ```
  release_task = jira.create_issue(
    projectKey: "TC",
    issueTypeName: "Task",
    summary: "RHTPA 2.2.5 CVE triage",
    description: "CVE triage tracking task for RHTPA 2.2.5. Linked to CVE
      Vulnerability issues (Related) and blocked by remediation Tasks (Blocks).",
    labels: ["ai-generated-jira"],
    parent: <release-epic-key>
  )
  ```
  Post description digest comment per description-digest-protocol.md.

### Stream 2.1.x (out-of-scope, preemptive)

Per the skill specification, release Jira orchestration applies only to
**non-preemptive** remediation types. The 2.1.x stream's remediation tasks are
preemptive (created via Case A for a stream without its own CVE Jira). Therefore,
**no release Jira is created or linked for 2.1.x** preemptive tasks.

## Cross-CVE Dedup Decision (Step 7.5.3)

Step 7.5.3 requires the **Upstream Affected Component** custom field to be
configured in Security Configuration. This field is **not configured** in the
project's CLAUDE.md.

**Decision: Dedup check is skipped entirely.**

No existing remediation Task is checked for overlap. Proceed to Step 8 for
standard remediation task creation.

---

# Steps 4-7 Summary

The following intermediate steps were evaluated before remediation:

- **Step 4 (Duplicate/Sibling Check)**: Would search for sibling Vulnerability
  issues with label `CVE-2026-31812`. No mock sibling data provided -- in a real
  triage, any siblings would be linked and classified as same-stream duplicates
  or cross-stream companions.

- **Step 4.3 (Cross-CVE Overlap)**: **Skipped** -- Upstream Affected Component
  custom field not configured.

- **Step 4.4 (Preemptive Task Reconciliation)**: Would search for existing
  preemptive tasks with labels `security-preemptive` and `CVE-2026-31812`.
  No existing preemptive tasks assumed for this analysis.

- **Step 5 (Version Lifecycle Check)**: Would fetch product lifecycle data from
  `https://access.example.com/product-life-cycle/rhtpa`. For this analysis, all
  affected versions (2.1.x and 2.2.x) are assumed to be within support lifecycle.

- **Step 6 (Already Fixed Check)**: No resolved sibling issues found. Proceeding
  to remediation.

- **Step 7 (Concurrent Triage Detection)**: **Skipped** -- Upstream Affected
  Component custom field not configured.

---

# Step 8 -- Remediation

## Triage Decision

The issue TC-8001 is scoped to the **2.2.x** stream. The version impact analysis
shows:

- **2.2.x (in-scope)**: Versions 2.2.0, 2.2.1, 2.2.2 are affected. Versions
  2.2.3 and 2.2.4 already ship the fix (quinn-proto 0.11.14).
- **2.1.x (out-of-scope)**: All versions (2.1.0, 2.1.1) are affected.

This triggers:
- **Case A** (cross-stream impact): 2.1.x is affected but outside the issue's
  scope. A cross-stream impact comment is posted, and preemptive remediation
  tasks are created for 2.1.x since no sibling CVE Jira exists for that stream.
- **Case B** (affected -- create remediation tasks): 2.2.x versions are affected
  within the issue's scope.

## Case A: Cross-Stream Impact Comment

The following comment would be posted to TC-8001:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based
> on lock file analysis. This stream is tracked by companion issues (see Related
> links) or may require separate PSIRT triage.
>
> ---
> This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10.

## Case B: Remediation Tasks for 2.2.x (In-Scope)

Ecosystem: **Cargo** (source dependency)
Upstream fix status: **Fixed** on release/0.4.z (quinn-proto 0.11.14 at v0.4.11+)
Remediation type: **Dependency bump + downstream propagation** (2 tasks)

### Task 1: Dependency Bump (2.2.x)

**Summary**: Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description**:

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream --
a package manager update is sufficient.

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 retag of v0.4.8)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
- **Remediation action**: run `cargo update -p quinn-proto` to pull in the
  latest compatible version (>= 0.11.14)
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

After creation, a description digest comment would be posted per
description-digest-protocol.md, and the task would be linked to TC-8001
with link type "Depend".

### Task 2: Downstream Propagation (2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description**:

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <dependency-bump-task-key>.

The dependency bump (<dependency-bump-task-key>) updates quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <dependency-bump-task-key> (dependency bump must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

After creation, a description digest comment would be posted per
description-digest-protocol.md. The task would be linked to TC-8001 with
"Depend" and to the dependency bump task with "Blocks" (upstream blocks
downstream).

### Post-Creation Release Linking (2.2.x)

After creating the two remediation tasks for 2.2.x:

1. **Link each remediation task to the release Task** (Blocks):
   ```
   jira.create_link(inwardIssue: <bump-task-key>, outwardIssue: <release-task-key>, type: "Blocks")
   jira.create_link(inwardIssue: <downstream-task-key>, outwardIssue: <release-task-key>, type: "Blocks")
   ```

2. **Link the CVE to the release Task** (Related):
   ```
   jira.create_link(inwardIssue: <release-task-key>, outwardIssue: TC-8001, type: "Related")
   ```

---

## Case A: Preemptive Remediation Tasks for 2.1.x (Out-of-Scope)

The 2.1.x stream has no sibling CVE Jira for CVE-2026-31812. Preemptive
remediation tasks are created with the `security-preemptive` label and linked
to the originating CVE (TC-8001) with "Related" (not "Depend").

Ecosystem: **Cargo** (source dependency)
Upstream fix status: **Not fixed** on release/0.3.z (quinn-proto 0.11.9 at v0.3.12)
Remediation type: **Upstream backport + downstream propagation** (2 tasks)

### Preemptive Task 1: Upstream Backport (2.1.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Description**:

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2). No stream-specific CVE Jira
> exists yet for this stream. When PSIRT creates one, this task will be linked
> and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto denial of service via excessive stream
counts. The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

After creation, a description digest comment would be posted. The task would
be linked to TC-8001 with "Related" (preemptive link type, not "Depend").

### Preemptive Task 2: Downstream Propagation (2.1.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Description**:

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2). No stream-specific CVE Jira
> exists yet for this stream. When PSIRT creates one, this task will be linked
> and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from <upstream-backport-task-key>.

The upstream backport (<upstream-backport-task-key>) bumps quinn-proto to
0.11.14 on release/0.3.z. Once that PR merges, update the source pinning in
this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-backport-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

After creation, a description digest comment would be posted. The task would
be linked to TC-8001 with "Related" (preemptive link type) and to the upstream
backport task with "Blocks" (upstream blocks downstream).

---

## Case A: Preemptive Tasks Comment on TC-8001

After creating the preemptive tasks, the following comment would be posted to
TC-8001:

> Preemptive remediation tasks created for streams without CVE Jiras:
> - 2.1.x: <upstream-backport-task-key> (upstream backport, security-preemptive),
>   <downstream-propagation-task-key> (downstream propagation, security-preemptive)
>
> These tasks use the "Related" link type and carry the security-preemptive
> label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
> reconciliation will link them and remove the label.
>
> ---
> This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10.

---

## Post-Triage Summary

After all triage actions, the following post-triage operations would be performed:

1. **Add `ai-cve-triaged` label** to TC-8001.

2. **Post summary comment** to TC-8001 documenting:
   - Version impact table
   - Affects Versions correction: RHTPA 2.0.0 -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
   - Triage outcome: remediation tasks created
   - Remediation tasks for 2.2.x: <bump-task-key> (dependency bump),
     <downstream-task-key> (downstream propagation)
   - Preemptive tasks for 2.1.x: <upstream-backport-task-key>,
     <downstream-propagation-task-key>
   - Release Jira: <release-epic-key> (RHTPA 2.2.5 Release Tasks),
     <release-task-key> (RHTPA 2.2.5 CVE triage)
   - @mention of TC-8001 reporter (mandatory, using reporter's account ID)

No Jira operations were actually performed -- all actions described above are
proposed and pending engineer confirmation.

## Pre-Creation Checklist

- [x] **Task count per stream**: 2.2.x has 2 tasks (dependency bump +
  downstream propagation) per Cargo ecosystem classification. 2.1.x has 2
  preemptive tasks (upstream backport + downstream propagation).
- [x] **Cross-stream coverage**: 2.1.x (affected, outside scope) has preemptive
  tasks created. No sibling CVE Jira exists for 2.1.x.
- [x] **Link types**: "Depend" for 2.2.x tasks linked to TC-8001. "Related" for
  2.1.x preemptive tasks linked to TC-8001. "Blocks" for upstream-to-downstream
  within each stream.
- [x] **Preemptive labels**: 2.1.x tasks carry `security-preemptive` label.
- [x] **Coordination guidance**: Omitted -- Source Repositories table does not
  include a Deployment Context column (backward compatibility).
- [x] **Release Jira linking**: 2.2.x remediation tasks linked to release Task
  (Blocks). TC-8001 linked to release Task (Related). Preemptive 2.1.x tasks
  are not linked to release Jira (preemptive scope).
- [x] **Dedup consistency**: Dedup check was skipped (Upstream Affected Component
  field not configured). No streams marked as dedup'd.
