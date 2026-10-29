# Remediation -- TC-8004

## Step 4: Duplicate / Sibling Check

JQL search for sibling Vulnerability issues with label `CVE-2026-33501`:

```
project = TC AND labels = 'CVE-2026-33501' AND issuetype = 10024 AND key != TC-8004
```

**Result: No siblings found.** No duplicate or companion issues exist. Proceeding
to remediation.

## Step 5: Version Lifecycle Check

_Skipped in this eval (no external service calls). In a live triage, the product
lifecycle page at `https://access.example.com/product-life-cycle/rhtpa` would be
checked to confirm that 2.1.x versions are still within their support lifecycle._

## Step 6: Already Fixed Check

No resolved sibling issues exist (Step 4 returned empty). No already-fixed scenario
applies.

## Step 7: Concurrent Triage Detection

_Skipped -- the Upstream Affected Component custom field is not configured in the
Security Configuration._

## Step 7.5: Release Jira Orchestration

_Skipped in this eval (no Jira access). In a live triage, the skill would search
for or create a release Epic and Task for the 2.1.x stream before creating
remediation tasks._

## Step 8: Remediation Decision

### Decision Tree Evaluation

- **Any supported versions affected?** YES -- 2.1.x stream (2.1.0, 2.1.1)
- **Issue scoped to a single stream?** NO -- unscoped (no stream suffix)
- **Path:** Case B -- create remediation tasks for affected streams only

Since the issue is unscoped, Case A (cross-stream impact) does not apply. Case B
creates remediation tasks for all actually affected streams. Only the 2.1.x stream
is affected; the 2.2.x stream ships the fixed version and requires no remediation.

### Ecosystem Classification

- **Library:** h2 (Rust crate)
- **Ecosystem:** Cargo (source dependency)
- **Fix available upstream:** YES (h2 0.4.8 is a published crate version)
- **Task count per stream:** 2 (dependency bump + downstream propagation)

### Remediation Tasks for 2.1.x Stream

Since h2 0.4.8 is already published upstream and the 2.2.x stream confirms it is
a compatible version, the remediation uses the **dependency bump** variant (not the
upstream backport variant).

---

#### PROPOSAL: Task 1 -- Dependency Bump (2.1.x)

**Summary:** Remediate CVE-2026-33501: update h2 to 0.4.8 (2.1.x)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-33501`

**Description:**

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: bump h2 to 0.4.8 via dependency update.
The vulnerable dependency (h2 < 0.4.8) is already fixed upstream --
a package manager update is sufficient.

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
Source commit(s): v0.3.8 (2.1.0), v0.3.12 (2.1.1)

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (h2 is a direct Cargo dependency)
- **Remediation action**: run `cargo update -p h2` to pull in h2 >= 0.4.8
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add h2@0.4.8`
- Verify Cargo.lock reflects h2 >= 0.4.8 after the update

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

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

**Jira creation (PROPOSAL):**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: update h2 to 0.4.8 (2.1.x)",
  description: <dependency-bump-task-description above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

---

#### PROPOSAL: Task 2 -- Downstream Propagation (2.1.x)

**Summary:** Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-33501`

**Description:**

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from the dependency bump task.

The dependency bump task updates h2 to 0.4.8 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux
release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
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
- Depends on: TC-8004 (parent tracking issue)
```

**Jira creation (PROPOSAL):**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <downstream-propagation-task-description above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

---

### PROPOSAL: Jira Linkage

After creating both remediation tasks:

1. **Link dependency bump task to CVE:**
   ```
   jira.create_link(
     inwardIssue: "TC-8004",
     outwardIssue: <dependency-bump-task-key>,
     type: "Depend"
   )
   ```

2. **Link downstream propagation task to CVE:**
   ```
   jira.create_link(
     inwardIssue: "TC-8004",
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )
   ```

3. **Link downstream as blocked by upstream (dependency bump):**
   ```
   jira.create_link(
     inwardIssue: <dependency-bump-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

4. **Link both remediation tasks to release Task (if created in Step 7.5):**
   ```
   jira.create_link(
     inwardIssue: <remediation-task-key>,
     outwardIssue: <release-task-key>,
     type: "Blocks"
   )
   ```

5. **Link CVE to release Task (traceability):**
   ```
   jira.create_link(
     inwardIssue: <release-task-key>,
     outwardIssue: "TC-8004",
     type: "Related"
   )
   ```

### PROPOSAL: Post-Triage Summary

Add `ai-cve-triaged` label to TC-8004 and post summary comment:

```
jira.edit_issue("TC-8004", fields={
  "labels": ["CVE-2026-33501", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

**Summary comment:**

```
CVE-2026-33501 triage complete for TC-8004.

Version impact (h2 < 0.4.8):

| Stream | Version | h2 version | Affected? |
|--------|---------|------------|-----------|
| 2.1.x  | 2.1.0   | 0.4.5      | YES       |
| 2.1.x  | 2.1.1   | 0.4.5      | YES       |
| 2.2.x  | 2.2.0   | 0.4.8      | NO        |
| 2.2.x  | 2.2.1   | 0.4.8      | NO        |
| 2.2.x  | 2.2.2   | --         | NO (retag of 2.2.1) |
| 2.2.x  | 2.2.3   | 0.4.9      | NO        |
| 2.2.x  | 2.2.4   | 0.4.9      | NO        |

Affects Versions corrected: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].
RHTPA 2.2.0 removed (ships fixed h2 0.4.8); RHTPA 2.1.1 added (ships vulnerable h2 0.4.5).

Outcome: Remediation required for 2.1.x stream only.
2.2.x stream ships h2 >= 0.4.8 and is not affected.

Remediation tasks created:
- <dependency-bump-task-key> (dependency bump: update h2 to 0.4.8 on release/0.3.z)
- <downstream-task-key> (downstream propagation: update backend ref in
  rhtpa-release.0.3.z, blocked by <dependency-bump-task-key>)
```

### 2.2.x Stream: No Remediation Needed

The 2.2.x stream requires **no remediation tasks**. All versions in this stream
(2.2.0 through 2.2.4) ship h2 >= 0.4.8, which is at or above the fix threshold.
The PSIRT-assigned Affects Version "RHTPA 2.2.0" was incorrect and has been proposed
for removal in the Affects Versions correction (see outputs/affects-versions.md).

### Pre-Creation Checklist

- [x] **Task count per stream**: 2.1.x gets 2 tasks (source dependency / Cargo
  ecosystem: dependency bump + downstream propagation). 2.2.x gets 0 tasks (not affected).
- [x] **Cross-stream coverage**: Not applicable -- issue is unscoped, so Case A
  does not apply. Only affected stream (2.1.x) gets remediation.
- [x] **Link types**: "Depend" for tasks linked to TC-8004 (their CVE Jira).
  "Blocks" from dependency bump task to downstream propagation task.
- [x] **Preemptive labels**: Not applicable -- no preemptive tasks needed (issue
  is unscoped, so all streams are analyzed directly).
- [x] **Coordination guidance**: Included in both task descriptions with "upstream"
  deployment context guidance.
- [x] **Dedup consistency**: No dedup detected (no sibling issues, no existing
  remediation tasks for this component).
