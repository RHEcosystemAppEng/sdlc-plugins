# Step 8 -- Remediation

## Triage Decision

**Case B** -- Affected versions exist within the scoped 2.2.x stream (versions 2.2.0, 2.2.1, 2.2.2 ship quinn-proto < 0.11.14).

**Case A** -- Cross-stream impact detected. Stream 2.1.x (versions 2.1.0, 2.1.1) is also affected but outside this issue's scope. Preemptive remediation tasks are created for 2.1.x.

## Deployment Context and Coordination Guidance

The Source Repositories table in the project CLAUDE.md does **not** include a Deployment Context column. Per backward compatibility rules (remediation-templates.md), all repositories default to `upstream` internally, but the Coordination Guidance subsection is **omitted entirely** from all remediation task descriptions. No `### Coordination Guidance` subsection is appended to any task's Implementation Notes.

---

## Case A: Cross-Stream Impact Comment

Since the issue is scoped to 2.2.x but stream 2.1.x is also affected, a cross-stream impact comment would be posted to TC-8001:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. Versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9. This stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.

Since no sibling CVE Jira exists for 2.1.x (no issue found with label CVE-2026-31812 and suffix [rhtpa-2.1]), preemptive remediation tasks are created for 2.1.x with the `security-preemptive` label and "Related" link type to TC-8001.

---

## Remediation Tasks for Stream 2.2.x (Scoped -- Case B)

**Ecosystem**: Cargo (source dependency)
**Upstream fix status**: YES -- release/0.4.z already ships quinn-proto 0.11.14
**Remediation type**: Dependency bump + downstream propagation (2 tasks)

### Task 1: Dependency Bump Task (2.2.x)

**Proposed Jira Issue:**
- **Type**: Task
- **Summary**: Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Task Description:**

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
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is a retag of v0.4.8)

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

**Post-creation steps (proposed):**

1. Re-fetch the task description and compute SHA-256 digest
2. Post description digest comment (BEFORE creating issue links)
3. Create Depend link: `jira.create_link(inwardIssue: "TC-8001", outwardIssue: <bump-task-key>, type: "Depend")`
4. Link to release Task (if active from Step 7.5): `jira.create_link(inwardIssue: <bump-task-key>, outwardIssue: <release-task-key>, type: "Blocks")`

---

### Task 2: Downstream Propagation Subtask (2.2.x)

**Proposed Jira Issue:**
- **Type**: Task
- **Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Task Description:**

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <bump-task-key>.

The dependency bump (<bump-task-key>) updates quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <bump-task-key> (dependency bump must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Post-creation steps (proposed):**

1. Re-fetch the task description and compute SHA-256 digest
2. Post description digest comment (BEFORE creating issue links)
3. Create Depend link: `jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-key>, type: "Depend")`
4. Create Blocks link: `jira.create_link(inwardIssue: <bump-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")`
5. Link to release Task (if active from Step 7.5): `jira.create_link(inwardIssue: <downstream-task-key>, outwardIssue: <release-task-key>, type: "Blocks")`

---

## Preemptive Remediation Tasks for Stream 2.1.x (Case A -- Cross-Stream)

**Ecosystem**: Cargo (source dependency)
**Upstream fix status**: NO -- release/0.3.z still has quinn-proto 0.11.9
**Remediation type**: Upstream backport + downstream propagation (2 preemptive tasks)
**Link type**: Related (to TC-8001, not Depend, because this is a different stream)
**Labels**: include `security-preemptive`

### Task 3 (Preemptive): Upstream Backport Task (2.1.x)

**Proposed Jira Issue:**
- **Type**: Task
- **Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Task Description:**

```
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

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

**Post-creation steps (proposed):**

1. Re-fetch the task description and compute SHA-256 digest
2. Post description digest comment (BEFORE creating issue links)
3. Create Related link (preemptive, not Depend): `jira.create_link(inwardIssue: "TC-8001", outwardIssue: <preemptive-upstream-task-key>, type: "Related")`

---

### Task 4 (Preemptive): Downstream Propagation Subtask (2.1.x)

**Proposed Jira Issue:**
- **Type**: Task
- **Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Task Description:**

```
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from <preemptive-upstream-task-key>.

The upstream backport (<preemptive-upstream-task-key>) bumps quinn-proto to
0.11.14 on release/0.3.z. Once that PR merges, update the source pinning
in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <preemptive-upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Post-creation steps (proposed):**

1. Re-fetch the task description and compute SHA-256 digest
2. Post description digest comment (BEFORE creating issue links)
3. Create Related link (preemptive): `jira.create_link(inwardIssue: "TC-8001", outwardIssue: <preemptive-downstream-task-key>, type: "Related")`
4. Create Blocks link: `jira.create_link(inwardIssue: <preemptive-upstream-task-key>, outwardIssue: <preemptive-downstream-task-key>, type: "Blocks")`

---

## Preemptive Task Comment on TC-8001

After creating preemptive tasks for 2.1.x, a comment would be posted to TC-8001:

> Preemptive remediation tasks created for streams without CVE Jiras:
> - 2.1.x: <preemptive-upstream-task-key> (upstream backport, security-preemptive), <preemptive-downstream-task-key> (downstream propagation, security-preemptive)
>
> These tasks use the "Related" link type and carry the security-preemptive label. When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link them and remove the label.

---

## Task Summary

| # | Stream | Type | Summary | Labels | Link to TC-8001 |
|---|--------|------|---------|--------|-----------------|
| 1 | 2.2.x | Dependency bump | Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2) | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 2 | 2.2.x | Downstream propagation | Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2) | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 3 | 2.1.x | Upstream backport (preemptive) | Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |
| 4 | 2.1.x | Downstream propagation (preemptive) | Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |

### Pre-creation checklist

- [x] **Task count per stream**: 2 tasks per stream (source dependency ecosystem: Cargo)
  - 2.2.x: dependency bump + downstream propagation (fix available upstream)
  - 2.1.x: upstream backport + downstream propagation (fix NOT available upstream)
- [x] **Cross-stream coverage**: 2.1.x (outside issue scope) has preemptive tasks created
- [x] **Link types**: "Depend" for tasks linked to TC-8001 (scoped stream 2.2.x), "Related" for preemptive tasks linked to TC-8001 (cross-stream 2.1.x), "Blocks" for upstream/bump -> downstream within each stream
- [x] **Preemptive labels**: 2.1.x tasks carry the `security-preemptive` label
- [x] **Coordination guidance**: omitted -- Source Repositories table has no Deployment Context column
- [x] **Dedup consistency**: no prior dedup detected

---

## Affects Versions Correction (Step 3)

- **Current**: RHTPA 2.0.0
- **Proposed**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

The correction is scoped to stream 2.2.x per the issue suffix. RHTPA 2.0.0 is incorrect (no 2.0.x stream exists). Versions 2.2.3 and 2.2.4 are NOT affected (ship quinn-proto 0.11.14).

---

## Post-Triage Summary

After all triage actions are complete:

1. **Add the `ai-cve-triaged` label** to TC-8001 to mark it as triaged.

2. **Post a summary comment** to TC-8001 documenting:
   - The version impact table (all versions from both streams)
   - The Affects Versions correction (RHTPA 2.0.0 -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2)
   - The triage outcome: remediation tasks created for 2.2.x stream (dependency bump + downstream propagation)
   - Cross-stream impact on 2.1.x: preemptive tasks created
   - Links to all 4 created remediation tasks
   - Release Jira references (if created in Step 7.5)
   - An @mention of the vulnerability reporter using an ADF mention node

3. **Transition** TC-8001 to In Progress.

All proposed actions require explicit engineer confirmation before execution.
