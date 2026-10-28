# Step 7.5 -- Release Jira Orchestration

## Release Orchestration for 2.2.x Stream

### 7.5.1 -- Resolve stream-to-version mapping

The issue is scoped to the **2.2.x** stream (release family `2.2`). The latest released version in the 2.2.x supportability matrix is **2.2.4** (build 0.4.12, released 2026-05-04).

**Search for existing release Epic:**
```
jira.search_jql(
  "project = TC AND issuetype = Epic AND summary ~ 'RHTPA 2.2' AND summary ~ 'Release Tasks' ORDER BY created DESC",
  fields: ["summary", "status"],
  maxResults: 5
)
```

If no existing release Epic is found, the default next version would be **RHTPA 2.2.5** (next patch bump from 2.2.4).

**Confirmation required:**
```
No release Epic found for stream 2.2.x.

Proposed version: RHTPA 2.2.5 Release Tasks
(based on latest released version 2.2.4 in supportability matrix)

Options:
1. Accept -- create Epic with version 2.2.5
2. Specify different version
3. Skip -- do not create release Jira for this stream
```

If accepted, would create:
```
release_epic = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Epic",
  summary: "RHTPA 2.2.5 Release Tasks",
  description: "Release tracking Epic for RHTPA 2.2.5. Contains CVE triage and remediation tasks for this release.",
  labels: ["ai-generated-jira"]
)
```

### 7.5.2 -- Find or create the release Task

Search for an existing release Task under the release Epic:
```
jira.search_jql(
  "project = TC AND issuetype = Task AND parent = <release-epic-key> AND summary ~ 'RHTPA 2.2.5 CVE triage' ORDER BY created DESC",
  fields: ["summary", "status", "issuelinks"],
  maxResults: 5
)
```

If no release Task exists, would create:
```
release_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "RHTPA 2.2.5 CVE triage",
  description: "CVE triage tracking task for RHTPA 2.2.5. Linked to CVE Vulnerability issues (Related) and blocked by remediation Tasks (Blocks).",
  labels: ["ai-generated-jira"],
  parent: <release-epic-key>
)
```

### 7.5.3 -- Cross-CVE Dedup Check

**Result: SKIPPED.** The Upstream Affected Component custom field is not configured in the project's Security Configuration. Without this field, cross-CVE dedup cannot be performed. Proceeding to Step 8 without dedup filtering.

---

# Step 7 -- Concurrent Triage Detection

**Result: SKIPPED.** The Upstream Affected Component custom field is not configured in the project's Security Configuration. Step 7 requires this field to search for concurrent triages on the same component.

---

# Step 8 -- Remediation

## Triage Decision

### Case A: Cross-Stream Impact (scoped issue)

TC-8001 is scoped to the **2.2.x** stream, but the version impact analysis (Step 2) reveals that the **2.1.x** stream is also affected:

- 2.1.0: quinn-proto 0.11.9 -- **AFFECTED**
- 2.1.1: quinn-proto 0.11.9 -- **AFFECTED**

**Cross-stream impact comment** (would be posted to TC-8001):
```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

**Sibling check for 2.1.x:** No sibling Vulnerability issue with label CVE-2026-31812 and suffix `[rhtpa-2.1]` was found. Therefore, **preemptive remediation tasks** are required for the 2.1.x stream.

### Case B: Remediation for Scoped Stream (2.2.x)

Within the 2.2.x stream, versions 2.2.0, 2.2.1, and 2.2.2 are affected. However, versions 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14 (the fix). The upstream branch `release/0.4.z` also already ships the fixed version (confirmed in Step 2.5).

Since the upstream fix is available, the **dependency bump + downstream propagation** variant applies (2 tasks).

---

## Remediation Task Descriptions

### Task 1: Dependency Bump for 2.2.x Stream

**Summary:** `Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)`
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`
**Link:** Depend (TC-8001 inward, this task outward)

#### Task Description

```markdown
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream --
a package manager update is sufficient.

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8, v0.4.9

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (quinn-proto is a direct workspace dependency)
- **Remediation action**: run the appropriate package manager update command:
  - **Cargo**: `cargo update -p quinn-proto` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

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

---

### Task 2: Downstream Propagation for 2.2.x Stream

**Summary:** `Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)`
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`
**Link:** Depend (TC-8001 inward, this task outward); Blocks (Task 1 inward, this task outward)

#### Task Description

```markdown
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the dependency bump task.

The dependency bump task bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: dependency bump task (upstream fix must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

### Task 3 (Preemptive): Upstream Backport for 2.1.x Stream

**Summary:** `Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)`
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
**Link:** Related (TC-8001 inward, this task outward) -- "Related" not "Depend" because this is a preemptive task linked to a different stream's CVE Jira

#### Task Description

```markdown
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (quinn-proto is a direct workspace dependency)
- The upstream branch release/0.3.z currently ships quinn-proto 0.11.9.
  The fix is NOT yet available on this branch. A backport or dependency
  bump PR is required.

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock / Cargo.toml
- Run `cargo update -p quinn-proto` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (originating CVE tracking issue, different stream)
```

---

### Task 4 (Preemptive): Downstream Propagation for 2.1.x Stream

**Summary:** `Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)`
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
**Link:** Related (TC-8001 inward, this task outward)

#### Task Description

```markdown
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task for 2.1.x (must merge first)
- Depends on: TC-8001 (originating CVE tracking issue, different stream)
```

---

## Jira Linkage Summary

### For 2.2.x remediation tasks (non-preemptive):

| Link Type | Inward | Outward |
|-----------|--------|---------|
| Depend | TC-8001 | Task 1 (dependency bump) |
| Depend | TC-8001 | Task 2 (downstream propagation) |
| Blocks | Task 1 (dependency bump) | Task 2 (downstream propagation) |
| Blocks | Task 1 (dependency bump) | release Task (RHTPA 2.2.5 CVE triage) |
| Blocks | Task 2 (downstream propagation) | release Task (RHTPA 2.2.5 CVE triage) |
| Related | release Task | TC-8001 |

### For 2.1.x preemptive tasks:

| Link Type | Inward | Outward |
|-----------|--------|---------|
| Related | TC-8001 | Task 3 (upstream backport, preemptive) |
| Related | TC-8001 | Task 4 (downstream propagation, preemptive) |
| Blocks | Task 3 (upstream backport) | Task 4 (downstream propagation) |

Preemptive tasks use "Related" (not "Depend") because they are linked to a different stream's CVE Jira. They are NOT linked to the release Task (only non-preemptive remediation types are linked to release Jira).

## Preemptive Task Comment

Would be posted to TC-8001:
```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: Task 3 (upstream backport, security-preemptive)
- 2.1.x: Task 4 (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

## Post-Triage Summary

Would add the `ai-cve-triaged` label to TC-8001 and post a summary comment documenting:
1. Version impact table (all streams)
2. Affects Versions correction: RHTPA 2.0.0 -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
3. Cross-stream impact: 2.1.x also affected (preemptive tasks created)
4. Remediation tasks created: 2 standard (2.2.x) + 2 preemptive (2.1.x)
5. Release Jira: RHTPA 2.2.5 Release Tasks Epic and CVE triage Task

No Jira operations were performed (eval-only mode).
