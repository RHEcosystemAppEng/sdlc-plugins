# Step 7.5 -- Release Jira Orchestration

Before creating remediation tasks, find or create the release Jira structure for each affected stream.

## 7.5.1 -- Resolve Stream-to-Version Mapping

### Stream 2.2.x

- Release family: 2.2.x
- Latest released version in the supportability matrix: **2.2.4**
- Default next patch: **2.2.5**

**Proposed action:** Search for an existing release Epic matching `"RHTPA 2.2.* Release Tasks"` via JQL:

```
jira.search_jql(
  "project = TC AND issuetype = Epic AND summary ~ 'RHTPA 2.2' AND summary ~ 'Release Tasks' ORDER BY created DESC",
  fields: ["summary", "status"],
  maxResults: 5
)
```

- If an existing Epic is found, reuse it.
- If no Epic exists, propose creation of `"RHTPA 2.2.5 Release Tasks"` with engineer confirmation (version decision is high-stakes and requires individual approval).

### Stream 2.1.x (Cross-stream -- preemptive tasks)

- Release family: 2.1.x
- Latest released version in the supportability matrix: **2.1.1**
- Default next patch: **2.1.2**

**Proposed action:** Search for an existing release Epic matching `"RHTPA 2.1.* Release Tasks"`.

- If an existing Epic is found, reuse it.
- If no Epic exists, propose creation of `"RHTPA 2.1.2 Release Tasks"` with engineer confirmation.

Note: preemptive tasks are linked to the release Task with "Related" (not "Blocks"), as they originate from a different stream's CVE.

## 7.5.2 -- Find or Create Release Task

For each release Epic resolved in 7.5.1, search for a child release Task matching `"RHTPA <version> CVE triage"`.

**Stream 2.2.x:**
```
jira.search_jql(
  "project = TC AND issuetype = Task AND parent = <release-epic-key> AND summary ~ 'RHTPA 2.2.5 CVE triage'",
  fields: ["summary", "status", "issuelinks"],
  maxResults: 5
)
```

- If found, reuse it.
- If not found, propose creation with engineer confirmation:
  - Summary: `"RHTPA 2.2.5 CVE triage"`
  - Parent: `<release-epic-key>`
  - Labels: `["ai-generated-jira"]`

**Stream 2.1.x:** Same pattern with `"RHTPA 2.1.2 CVE triage"`.

## 7.5.3 -- Cross-CVE Dedup Check

**Prerequisite:** The Upstream Affected Component custom field is NOT configured in the mock Security Configuration. Therefore, the dedup check based on component matching is skipped.

**Fallback:** Summary-based matching would check whether any existing remediation Task linked to the release Task contains "quinn-proto" in its summary. Since no existing release Task or remediation tasks are known from the mock data, no dedup match is found.

**Decision:** No dedup -- proceed to Step 8 remediation task creation for both streams.

---

# Step 8 -- Remediation

## Triage Decision Tree

1. **Any supported versions affected?** YES -- versions 2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2 are all affected.
2. **Issue scoped to a single stream?** YES -- scoped to 2.2.x via `[rhtpa-2.2]` suffix.
3. **Other streams also affected?** YES -- 2.1.x stream is also affected (2.1.0 and 2.1.1 both ship quinn-proto 0.11.9).
4. **Case A applies:** Post cross-stream impact comment, then create preemptive tasks for 2.1.x (no sibling CVE Jira for the 2.1.x stream was found).
5. **Case B applies:** Create remediation tasks for the 2.2.x stream (the issue's own scope).

## Case A -- Cross-Stream Impact

### Cross-stream impact comment (proposed, not executed)

A comment would be posted to TC-8001:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis.
- 2.1.0 (v0.3.8): quinn-proto 0.11.9 -- AFFECTED
- 2.1.1 (v0.3.12): quinn-proto 0.11.9 -- AFFECTED

These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.
```

### Check for existing sibling CVE Jiras for 2.1.x

A JQL search for sibling issues with the same CVE label and stream suffix `[rhtpa-2.1]` would be performed. In this mock scenario, no sibling CVE Jira exists for the 2.1.x stream, so preemptive tasks are created.

## Remediation Tasks -- Stream 2.2.x (Case B, Scoped Stream)

**Upstream fix status:** YES -- release/0.4.z already ships quinn-proto 0.11.14 (confirmed at build v0.4.11+).

**Remediation variant:** Dependency bump (fix available upstream per Step 2.5). Two tasks: dependency bump + downstream propagation.

### Task 1: Dependency Bump (2.2.x)

**Proposed Jira issue (not created):**

- **Type:** Task
- **Summary:** `Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)`
- **Labels:** `["ai-generated-jira", "Security", "CVE-2026-31812"]`
- **Link to TC-8001:** Depend

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

Affected versions: RHTPA 2.2.0 (v0.4.5), RHTPA 2.2.1 (v0.4.8), RHTPA 2.2.2 (v0.4.9, retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
- **Remediation action**: run `cargo update -p quinn-proto` to pull in the latest
  compatible version (>= 0.11.14)
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update
- Note: builds v0.4.11+ (versions 2.2.3+) already ship quinn-proto 0.11.14.
  This task ensures the fix is tracked and verified on the upstream branch.

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

### Task 2: Downstream Propagation (2.2.x)

**Proposed Jira issue (not created):**

- **Type:** Task
- **Summary:** `Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)`
- **Labels:** `["ai-generated-jira", "Security", "CVE-2026-31812"]`
- **Blocked by:** Task 1 (dependency bump)
- **Link to TC-8001:** Depend

**Task Description:**

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the dependency bump task.

The dependency bump task bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully
- Note: builds 0.4.11+ already reference a commit with quinn-proto 0.11.14.
  This task ensures traceability of the fix through the downstream pipeline.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <dependency-bump-task-key> (upstream dependency bump must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

## Remediation Tasks -- Stream 2.1.x (Case A, Preemptive)

**Upstream fix status:** NO -- release/0.3.z still ships quinn-proto 0.11.9 at the latest pinned version (v0.3.12). The fix is NOT available on this branch.

**Remediation variant:** Upstream backport (fix not available upstream). Two preemptive tasks: upstream backport + downstream propagation.

**Preemptive rationale:** No CVE Jira exists for the 2.1.x stream. These tasks are created proactively from cross-stream impact analysis of TC-8001 (stream 2.2.x). Labels include `security-preemptive` and link type to TC-8001 is "Related" (not "Depend").

### Task 3: Upstream Backport (2.1.x, Preemptive)

**Proposed Jira issue (not created):**

- **Type:** Task
- **Summary:** `Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)`
- **Labels:** `["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]`
- **Link to TC-8001:** Related (preemptive -- different stream's CVE Jira)

**Task Description:**

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (v0.3.8), RHTPA 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- The fix is NOT yet available on release/0.3.z -- the dependency must be
  bumped directly on this branch
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog and PR #2048)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (originating CVE tracking issue, via Related link)
```

### Task 4: Downstream Propagation (2.1.x, Preemptive)

**Proposed Jira issue (not created):**

- **Type:** Task
- **Summary:** `Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)`
- **Labels:** `["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]`
- **Blocked by:** Task 3 (upstream backport)
- **Link to TC-8001:** Related (preemptive)

**Task Description:**

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

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

- Depends on: <upstream-backport-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (originating CVE tracking issue, via Related link)
```

## Jira Linkage Summary (Proposed, Not Executed)

### Standard remediation links (2.2.x stream):

| Link Type | Inward Issue | Outward Issue | Purpose |
|-----------|-------------|---------------|---------|
| Depend | TC-8001 | Task 1 (dependency bump) | CVE -> remediation |
| Depend | TC-8001 | Task 2 (downstream propagation) | CVE -> remediation |
| Blocks | Task 1 (dependency bump) | Task 2 (downstream propagation) | upstream blocks downstream |
| Blocks | Task 1 (dependency bump) | Release Task (2.2.x) | remediation blocks release |
| Blocks | Task 2 (downstream propagation) | Release Task (2.2.x) | remediation blocks release |
| Related | Release Task (2.2.x) | TC-8001 | release traceability |

### Preemptive remediation links (2.1.x stream):

| Link Type | Inward Issue | Outward Issue | Purpose |
|-----------|-------------|---------------|---------|
| Related | TC-8001 | Task 3 (upstream backport) | preemptive -- different stream |
| Related | TC-8001 | Task 4 (downstream propagation) | preemptive -- different stream |
| Blocks | Task 3 (upstream backport) | Task 4 (downstream propagation) | upstream blocks downstream |
| Related | Release Task (2.1.x) | TC-8001 | release traceability |

## Pre-Creation Checklist

- [x] **Task count per stream**: 2.2.x = 2 tasks (dependency bump + downstream propagation); 2.1.x = 2 tasks (upstream backport + downstream propagation). Matches ecosystem classification (Cargo = source dependency = 2 tasks).
- [x] **Cross-stream coverage**: 2.1.x stream (outside issue scope) has no sibling CVE Jira, so preemptive tasks created with `security-preemptive` label.
- [x] **Link types**: "Depend" for tasks linked to their own CVE Jira (2.2.x tasks); "Related" for preemptive tasks linked to another stream's CVE Jira (2.1.x tasks); "Blocks" for upstream -> downstream within a stream.
- [x] **Preemptive labels**: 2.1.x tasks carry `security-preemptive` label.
- [x] **Coordination guidance**: Deployment Context column is absent from Source Repositories table; coordination guidance subsection omitted per backward-compatibility rule.
- [x] **Release Jira linking**: If Step 7.5 produced release Tasks, non-preemptive remediation Tasks would be linked (Blocks) and CVEs linked (Related).
- [x] **Dedup consistency**: No dedup matches found; all streams receive new remediation tasks.

## Post-Triage Actions (Proposed, Not Executed)

1. **Add label:** `ai-cve-triaged` to TC-8001
2. **Post summary comment** to TC-8001 with version impact table, Affects Versions correction, remediation task links, release Jira references, and @mention of the issue reporter
3. **Transition** TC-8001 to In Progress (if not already transitioned)
