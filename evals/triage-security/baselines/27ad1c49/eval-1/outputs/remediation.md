# Remediation — TC-8001 (CVE-2026-31812)

## Preliminary Steps (Steps 4-7)

### Step 4 — Duplicate, Sibling, and Overlap Check

**Step 4.1-4.2 (Sibling search):** In interactive mode, a JQL search would be
executed for sibling Vulnerability issues with the CVE-2026-31812 label:

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8001
```

For this analysis, no sibling issues are assumed to exist. No companion CVE
Jiras exist for the 2.1.x stream.

**Step 4.3 (Cross-CVE overlap):** SKIPPED. The Upstream Affected Component
custom field is not configured in Security Configuration.

**Step 4.4 (Preemptive task reconciliation):** In interactive mode, a search
would check for existing preemptive tasks matching CVE-2026-31812. For this
analysis, no existing preemptive tasks are assumed.

### Step 5 — Version Lifecycle Check

In interactive mode, the Product pages URL
(`https://access.example.com/product-life-cycle/rhtpa`) would be queried to
verify that affected versions are within their support lifecycle. For this
analysis, all versions (2.1.x and 2.2.x) are assumed to be actively supported.

### Step 6 — Already Fixed Check

No resolved sibling Vulnerability issues exist for CVE-2026-31812. The
already-fixed check does not apply. Proceeding to Step 7.

### Step 7 — Concurrent Triage Detection

**SKIPPED.** The Upstream Affected Component custom field is not configured in
Security Configuration. Concurrent triage detection requires this field.

---

## Step 7.5 — Release Jira Orchestration

### 7.5.1 — Stream-to-Version Mapping

**Stream 2.2.x** (the issue's scoped stream):
- Release family: 2.2
- Latest released version in the supportability matrix: RHTPA 2.2.4 (shipped 2026-05-04)
- Default next version: **RHTPA 2.2.5**
- Proposed action: Search for an existing release Epic matching
  `"RHTPA 2.2.* Release Tasks"` via JQL:

  ```
  project = TC AND issuetype = Epic AND summary ~ 'RHTPA 2.2' AND summary ~ 'Release Tasks' ORDER BY created DESC
  ```

- **If an existing Epic is found**: Reuse it and proceed to Step 7.5.2.
- **If no Epic is found**: Propose creating a new Epic with engineer confirmation:

  ```
  Proposed: Create "RHTPA 2.2.5 Release Tasks" Epic
  (based on latest released version 2.2.4 in supportability matrix)

  Options:
  1. Accept -- create Epic with version 2.2.5
  2. Specify different version
  3. Skip -- do not create release Jira for this stream
  ```

  The engineer must confirm before creation proceeds. This is a high-stakes
  version decision requiring individual confirmation.

### 7.5.2 — Find or Create Release Task

After resolving the release Epic (assumed key: `<release-epic-key>`), search for
an existing release Task:

```
project = TC AND issuetype = Task AND parent = <release-epic-key> AND summary ~ 'RHTPA 2.2.5 CVE triage' ORDER BY created DESC
```

- **If a release Task exists**: Reuse it and proceed to Step 7.5.3.
- **If no release Task exists**: Propose creating:

  ```
  Proposed: Create "RHTPA 2.2.5 CVE triage" as child of <release-epic-key>
  Proceed? (Yes / No)
  ```

  The engineer must confirm before creation. After creation, a description
  digest comment would be posted per the description digest protocol.

### 7.5.3 — Cross-CVE Dedup Check

**SKIPPED.** The Upstream Affected Component custom field is not configured in
Security Configuration. Cross-CVE dedup requires this field to match remediation
tasks against the current CVE's upstream component.

Without dedup, all affected streams proceed to Step 8 for standard remediation
task creation.

---

## Step 8 — Remediation Decision

### Triage Decision Tree

```
Version impact table shows:
- 2.2.x stream (scoped): 3 versions affected (2.2.0, 2.2.1, 2.2.2), 2 NOT affected (2.2.3, 2.2.4)
- 2.1.x stream (out of scope): 2 versions affected (2.1.0, 2.1.1)

Case A check: Issue is scoped to 2.2.x. Other streams (2.1.x) ARE affected.
  --> Case A applies: cross-stream impact detected.

Case B check: Stream-scoped versions (2.2.x) include affected versions.
  --> Case B applies: remediation tasks for the scoped stream.

Upstream fix check (Step 2.5):
  - 2.2.x: Fix ALREADY available on release/0.4.z (quinn-proto 0.11.14)
  - 2.1.x: Fix NOT available on release/0.3.z (quinn-proto 0.11.9)
```

### 2.2.x Stream — No New Remediation Tasks Needed

For the 2.2.x stream, versions 2.2.3 (shipped 2026-03-23) and 2.2.4 (shipped
2026-05-04) already ship quinn-proto 0.11.14, which is at or above the fix
threshold. The upstream branch `release/0.4.z` already contains the fix. The
vulnerability was resolved through the normal release pipeline without requiring
a dedicated remediation task.

Since the fix is already incorporated in the latest releases of the 2.2.x stream,
creating remediation tasks (dependency bump + downstream propagation) would
produce tasks for work that has already been completed. No new remediation tasks
are proposed for the 2.2.x stream.

The corrected Affects Versions (RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2) document
which historical releases shipped the vulnerable dependency. Customers on those
versions should upgrade to RHTPA 2.2.3 or later.

### Case A — Cross-Stream Impact: 2.1.x Stream

TC-8001 is scoped to 2.2.x, but the version impact analysis reveals that the
2.1.x stream is also affected:

- RHTPA 2.1.0 (tag `v0.3.8`): quinn-proto 0.11.9 -- **affected**
- RHTPA 2.1.1 (tag `v0.3.12`): quinn-proto 0.11.9 -- **affected**

The upstream branch `release/0.3.z` does NOT have the fix (latest version at
tag `v0.3.12` still ships quinn-proto 0.11.9).

#### Cross-Stream Impact Comment (proposed)

The following comment would be posted to TC-8001:

```
Cross-stream impact: quinn-proto (versions before 0.11.14) also affects
stream 2.1.x based on lock file analysis.

Stream 2.1.x versions affected:
- RHTPA 2.1.0 (quinn-proto 0.11.9)
- RHTPA 2.1.1 (quinn-proto 0.11.9)

These streams are tracked by companion issues (see Related links) or may
require separate PSIRT triage.

---
This comment was AI-generated by sdlc-workflow/triage-security v0.13.10.
```

#### Sibling Check for 2.1.x

In interactive mode, a JQL search would check for an existing CVE Jira for
the 2.1.x stream:

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND summary ~ 'rhtpa-2.1'
```

For this analysis, no sibling CVE Jira exists for 2.1.x. Therefore, preemptive
remediation tasks are proposed for the 2.1.x stream.

#### Preemptive Remediation Tasks for 2.1.x

Since the upstream fix is NOT available on `release/0.3.z`, the remediation uses
the **upstream backport** variant (2 tasks per stream). These are preemptive
tasks because no stream-specific CVE Jira exists for 2.1.x yet.

---

### Preemptive Task 1: Upstream Backport (2.1.x)

**Proposed Jira Issue Creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Description:**

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for this stream. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: to be confirmed via Cargo.toml inspection (direct or transitive)

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
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
- Verify the bump does not introduce breaking API changes to the
  direct dependency

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable (breaking API changes,
no release available with the fix):
- Cargo: `cargo add quinn-proto@0.11.14` to add as a direct dependency,
  overriding the transitive resolution
- Document why the direct dep bump was not viable in the PR description

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

**Post-creation actions:**
1. Post description digest comment per description-digest-protocol.md
2. Link to TC-8001 with "Related" (preemptive link type, not "Depend"):
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <upstream-task-key>, type: "Related")
   ```

---

### Preemptive Task 2: Downstream Propagation (2.1.x)

**Proposed Jira Issue Creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Description:**

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for this stream. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-31812
fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps quinn-proto to 0.11.14 on
release/0.3.z. Once that PR merges, update the source pinning in this Konflux
release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Post-creation actions:**
1. Post description digest comment per description-digest-protocol.md
2. Link to TC-8001 with "Related" (preemptive link type):
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-key>, type: "Related")
   ```
3. Link downstream as blocked by upstream task:
   ```
   jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
   ```

---

### Preemptive Tasks Comment (proposed for TC-8001)

After creating the preemptive tasks, the following comment would be posted to
TC-8001:

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <upstream-task-key> (upstream backport, security-preemptive)
- 2.1.x: <downstream-task-key> (downstream propagation, security-preemptive, blocked by <upstream-task-key>)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.

---
This comment was AI-generated by sdlc-workflow/triage-security v0.13.10.
```

---

## Post-Triage Summary (proposed)

### Label Addition

Proposed action: Add the `ai-cve-triaged` label to TC-8001.

```
jira.edit_issue("TC-8001", fields={
  "labels": ["CVE-2026-31812", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### Release Jira Linking

If Step 7.5 produced a release Task for 2.2.x (e.g., `<release-task-key>`):
- Link TC-8001 to the release Task (Related):
  ```
  jira.create_link(inwardIssue: <release-task-key>, outwardIssue: "TC-8001", type: "Related")
  ```
- Note: No remediation tasks are linked to the release Task for 2.2.x since
  no new tasks were created for that stream.

### Summary Comment (proposed for TC-8001)

```
CVE-2026-31812 triage complete for TC-8001 (quinn-proto < 0.11.14).

Version impact:

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | >= fix threshold |
| 2.2.4 | 2.2.x | 0.11.14 | NO | >= fix threshold |

Affects Versions corrected: [RHTPA 2.0.0] --> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

Triage outcome:
- 2.2.x stream: Fix already incorporated in RHTPA 2.2.3+ (quinn-proto 0.11.14).
  No new remediation tasks needed for this stream.
- 2.1.x stream (cross-stream impact): Preemptive remediation tasks created:
  - <upstream-task-key>: upstream backport (bump quinn-proto to 0.11.14 on release/0.3.z)
  - <downstream-task-key>: downstream propagation (update backend ref in rhtpa-release.0.3.z)
  Both tasks carry the security-preemptive label and are linked via "Related".

Release Jira: <release-epic-key> / <release-task-key> (RHTPA 2.2.5, if created in Step 7.5)

@<reporter-account-id> (PSIRT reporter)

---
This comment was AI-generated by sdlc-workflow/triage-security v0.13.10.
```

---

## Pre-Creation Checklist

- [x] **Task count per stream**: 2.1.x gets 2 preemptive tasks (upstream backport +
  downstream propagation) -- matches the Cargo source dependency classification.
  2.2.x gets 0 tasks (fix already shipped in 2.2.3+).
- [x] **Cross-stream coverage**: 2.1.x (the only other stream) has preemptive tasks
  created. No sibling CVE Jira exists for 2.1.x.
- [x] **Link types**: "Related" for preemptive tasks linked to TC-8001 (originating
  CVE from a different stream). "Blocks" for upstream-to-downstream within 2.1.x.
- [x] **Preemptive labels**: Both 2.1.x tasks carry the `security-preemptive` label.
- [x] **Coordination guidance**: Omitted. The Source Repositories table has no
  Deployment Context column (backward compatibility -- coordination guidance is
  not added).
- [x] **Release Jira linking**: If Step 7.5 produced a release Task, TC-8001 would
  be linked to it (Related). No non-preemptive remediation tasks exist for 2.2.x,
  so no Blocks links to the release Task from remediation tasks.
- [x] **Dedup consistency**: Dedup was skipped (Upstream Affected Component not
  configured). No dedup exclusions to enforce.

---

*All proposed actions above are recommendations. No Jira operations were performed.*
