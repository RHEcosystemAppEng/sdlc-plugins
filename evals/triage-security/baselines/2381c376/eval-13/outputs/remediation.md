# Step 8 -- Remediation for TC-8001

## Triage Decision Tree

1. **Any supported versions affected?** YES -- 2.2.0, 2.2.1, 2.2.2 (in-scope), 2.1.0, 2.1.1 (cross-stream)
2. **Issue scoped to a single stream?** YES -- scoped to 2.2.x via `[rhtpa-2.2]`
3. **Other streams also affected?** YES -- 2.1.x is also affected
4. **Upstream Affected Component field configured?** NO -- Steps 4.3 (cross-CVE overlap), 7 (concurrent triage), and 7.5.3 (cross-CVE dedup) are skipped

Therefore:
- **Case A** applies: post cross-stream impact comment, then create preemptive tasks for the 2.1.x stream (if no sibling CVE Jira exists)
- **Case B** applies: create in-scope remediation tasks for the 2.2.x stream

## Step 3 -- Affects Versions Correction (Proposed)

**Current Affects Versions**: RHTPA 2.0.0
**Proposed Affects Versions** (scoped to 2.2.x): RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

The PSIRT-assigned "RHTPA 2.0.0" is incorrect -- there is no 2.0.x stream in the configured Version Streams. Based on lock file analysis at pinned commits, the affected versions within the 2.2.x stream are 2.2.0, 2.2.1, and 2.2.2. Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fixed version) and are not affected.

**Proposed Jira mutation:**
```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-jira-id>"},
    {"id": "<RHTPA-2.2.1-jira-id>"},
    {"id": "<RHTPA-2.2.2-jira-id>"}
  ]
})
```

**Proposed comment on TC-8001:**
```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

[Comment Footnote]
```

(No ProdSec @mention -- ProdSec Jira account ID is not configured.)

## Step 4 -- Duplicate, Sibling, and Overlap Check (Proposed)

**Proposed JQL search:**
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8001
```

Assuming no sibling Vulnerability issues found for CVE-2026-31812, proceed to Step 5.

Step 4.3 (Cross-CVE overlap) is skipped -- Upstream Affected Component custom field is not configured.

Step 4.4 (Preemptive task reconciliation) -- would search:
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812'
```
Assuming no preemptive tasks found, proceed to Step 5.

## Step 5 -- Version Lifecycle Check (Proposed)

**Proposed action:** Fetch the product lifecycle page at https://access.example.com/product-life-cycle/rhtpa and verify that 2.1.x and 2.2.x are within support lifecycle.

Assuming all affected versions are within support lifecycle, proceed to Step 6.

## Step 6 -- Already Fixed Check

No resolved sibling issues found in Step 4. Proceed to Step 7.

## Step 7 -- Concurrent Triage Detection

Skipped -- Upstream Affected Component custom field is not configured.

## Step 7.5 -- Release Jira Orchestration (Proposed)

For the 2.2.x stream, the proposed release Jira orchestration would:

1. Search for existing release Epic: `project = TC AND issuetype = Epic AND summary ~ 'RHTPA 2.2' AND summary ~ 'Release Tasks'`
2. If not found, propose creating "RHTPA 2.2.5 Release Tasks" (next patch bump from latest released 2.2.4)
3. Find or create release Task: "RHTPA 2.2.5 CVE triage" as child of the release Epic
4. Step 7.5.3 (dedup) is skipped -- Upstream Affected Component field not configured

For the 2.1.x stream (preemptive tasks), the same orchestration would apply:
1. Search for existing release Epic matching "RHTPA 2.1" pattern
2. If not found, propose creating "RHTPA 2.1.2 Release Tasks" (next patch bump from latest released 2.1.1)
3. Find or create release Task: "RHTPA 2.1.2 CVE triage"

---

## Case A -- Cross-Stream Impact Comment (Proposed)

Since the issue is scoped to 2.2.x and the 2.1.x stream is also affected, post a cross-stream impact comment on TC-8001:

**Proposed comment on TC-8001:**
```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. Versions 2.1.0 and 2.1.1 ship quinn-proto
0.11.9 which is within the affected range.

These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

[Comment Footnote]
```

Assuming no sibling CVE Jira exists for the 2.1.x stream, create **preemptive remediation tasks** for stream 2.1.x.

---

## Case B -- Remediation Tasks

### In-Scope: Stream 2.2.x (Dependency Bump Variant)

The upstream fix is available on `release/0.4.z` (Step 2.5 confirmed quinn-proto 0.11.14 at branch HEAD). Use the dependency bump variant.

#### Task 1: Dependency Bump Task (2.2.x)

**Proposed Jira creation:**
```
bump_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task description:**

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
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: [to be determined by inspecting Cargo.toml at pinned commits]
- **Remediation action**: run `cargo update -p quinn-proto` to pull in the latest
  compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

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

**Description digest comment (proposed steps after creation):**

1. Re-fetch the task description from Jira after creation:
   ```
   bump_desc = jira.get_issue(<bump-task-key>, fields=["description"])
   ```
2. Write the description content to a temporary file.
3. Compute the digest using the script:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   Output: `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>` (format-tagged)
4. Post the digest as a standalone comment on the newly created task (before any links or other comments):
   ```
   jira.add_comment(<bump-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

**Proposed links after digest:**
- `jira.create_link(inwardIssue: "TC-8001", outwardIssue: <bump-task-key>, type: "Depend")`
- If release Task exists: `jira.create_link(inwardIssue: <bump-task-key>, outwardIssue: <release-task-key>, type: "Blocks")`

---

#### Task 2: Downstream Propagation Task (2.2.x)

**Proposed Jira creation:**
```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task description:**

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
- **Dependency type**: carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <bump-task-key> (dependency bump must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Description digest comment (proposed steps after creation):**

1. Re-fetch the task description from Jira after creation:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```
2. Write the description content to a temporary file.
3. Compute the digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
4. Post the digest as a standalone comment on the newly created task (before any links or other comments):
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

**Proposed links after digest:**
- `jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-key>, type: "Depend")`
- `jira.create_link(inwardIssue: <bump-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")`
- If release Task exists: `jira.create_link(inwardIssue: <downstream-task-key>, outwardIssue: <release-task-key>, type: "Blocks")`

---

### Cross-Stream Preemptive: Stream 2.1.x (Upstream Backport Variant)

The upstream fix is NOT available on `release/0.3.z` (Step 2.5 confirmed quinn-proto 0.11.9 at branch HEAD). Use the upstream backport variant with the `security-preemptive` label.

#### Task 3: Preemptive Upstream Backport Task (2.1.x)

**Proposed Jira creation:**
```
upstream_task_21 = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task description:**

```
## Repository

backend

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
- **Dependency type**: [to be determined by inspecting Cargo.toml at pinned commits]
- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- The fix is NOT yet available on release/0.3.z -- this requires an upstream
  backport (cherry-pick or dependency bump PR to release/0.3.z)

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

When the vulnerable package is a **transitive** dependency (pulled in
through intermediate packages), use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (see dependency
  chain above)
- Bump the direct dependency to a version whose transitive closure
  includes quinn-proto >= 0.11.14

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable:
- Cargo: `cargo add quinn-proto@0.11.14` to add as a direct
  dependency, overriding the transitive resolution

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (originating tracking issue -- Related link)
```

**Description digest comment (proposed steps after creation):**

1. Re-fetch the task description from Jira after creation:
   ```
   upstream_desc_21 = jira.get_issue(<upstream-task-21-key>, fields=["description"])
   ```
2. Write the description content to a temporary file.
3. Compute the digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
4. Post the digest as a standalone comment on the newly created task (before any links or other comments):
   ```
   jira.add_comment(<upstream-task-21-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

**Proposed links after digest:**
- `jira.create_link(inwardIssue: "TC-8001", outwardIssue: <upstream-task-21-key>, type: "Related")` (preemptive -- uses Related, not Depend)
- If release Task exists for 2.1.x: `jira.create_link(inwardIssue: <upstream-task-21-key>, outwardIssue: <release-task-21-key>, type: "Blocks")`

---

#### Task 4: Preemptive Downstream Propagation Task (2.1.x)

**Proposed Jira creation:**
```
downstream_task_21 = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task description:**

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from <upstream-task-21-key>.

The upstream backport (<upstream-task-21-key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-21-key> (upstream backport must merge first)
- Depends on: TC-8001 (originating tracking issue -- Related link)
```

**Description digest comment (proposed steps after creation):**

1. Re-fetch the task description from Jira after creation:
   ```
   downstream_desc_21 = jira.get_issue(<downstream-task-21-key>, fields=["description"])
   ```
2. Write the description content to a temporary file.
3. Compute the digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
4. Post the digest as a standalone comment on the newly created task (before any links or other comments):
   ```
   jira.add_comment(<downstream-task-21-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

**Proposed links after digest:**
- `jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-21-key>, type: "Related")` (preemptive -- uses Related, not Depend)
- `jira.create_link(inwardIssue: <upstream-task-21-key>, outwardIssue: <downstream-task-21-key>, type: "Blocks")`
- If release Task exists for 2.1.x: `jira.create_link(inwardIssue: <downstream-task-21-key>, outwardIssue: <release-task-21-key>, type: "Blocks")`

---

## Case A -- Preemptive Tasks Comment (Proposed)

After creating preemptive tasks for the 2.1.x stream, post a comment on TC-8001:

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <upstream-task-21-key> (upstream backport, security-preemptive),
         <downstream-task-21-key> (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.

[Comment Footnote]
```

---

## Post-Triage Summary (Proposed)

### 1. Add `ai-cve-triaged` label

**Proposed mutation:**
```
jira.edit_issue("TC-8001", fields={
  "labels": ["CVE-2026-31812", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### 2. Post summary comment on TC-8001

**Proposed comment:**
```
## CVE-2026-31812 Triage Summary

### Version Impact

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0   | 2.1.x  | 0.11.9      | YES       |       |
| 2.1.1   | 2.1.x  | 0.11.9      | YES       |       |
| 2.2.0   | 2.2.x  | 0.11.9      | YES       |       |
| 2.2.1   | 2.2.x  | 0.11.12     | YES       |       |
| 2.2.2   | 2.2.x  | --          | YES       | retag of 2.2.1 |
| 2.2.3   | 2.2.x  | 0.11.14     | NO        | ships fixed version |
| 2.2.4   | 2.2.x  | 0.11.14     | NO        | ships fixed version |

### Affects Versions Correction

[RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
(Scoped to stream 2.2.x per issue suffix [rhtpa-2.2])

### Triage Outcome

Remediation tasks created.

### Remediation Tasks (in-scope, stream 2.2.x)

- <bump-task-key>: Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2) [dependency bump]
- <downstream-task-key>: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2) [downstream propagation, blocked by <bump-task-key>]

### Preemptive Remediation Tasks (cross-stream, stream 2.1.x)

- <upstream-task-21-key>: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1) [upstream backport, security-preemptive]
- <downstream-task-21-key>: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1) [downstream propagation, blocked by <upstream-task-21-key>, security-preemptive]

### Release Jira

- 2.2.x: <release-epic-key> / <release-task-key> (if created in Step 7.5)
- 2.1.x: <release-epic-21-key> / <release-task-21-key> (if created in Step 7.5)

@<reporter-account-id> (reporter mention)

[Comment Footnote]
```

### 3. Link CVE to release Tasks (if active)

- `jira.create_link(inwardIssue: <release-task-key>, outwardIssue: "TC-8001", type: "Related")` (2.2.x)
- `jira.create_link(inwardIssue: <release-task-21-key>, outwardIssue: "TC-8001", type: "Related")` (2.1.x)

---

## Pre-Creation Checklist

- [x] **Task count per stream**: 2.2.x gets 2 tasks (dependency bump + downstream propagation); 2.1.x gets 2 tasks (upstream backport + downstream propagation). Matches Cargo source dependency classification.
- [x] **Cross-stream coverage**: 2.1.x (outside issue scope) has preemptive tasks created (no sibling CVE Jira found).
- [x] **Link types**: "Depend" for 2.2.x tasks linked to TC-8001; "Related" for 2.1.x preemptive tasks linked to TC-8001; "Blocks" for upstream/bump -> downstream within each stream.
- [x] **Preemptive labels**: 2.1.x tasks carry `security-preemptive` label.
- [x] **Coordination guidance**: Each task includes "upstream" deployment context guidance.
- [x] **Release Jira linking**: Proposed for both streams (pending Step 7.5 execution).
- [x] **Dedup consistency**: Step 7.5.3 skipped (Upstream Affected Component field not configured); no dedup constraints.
