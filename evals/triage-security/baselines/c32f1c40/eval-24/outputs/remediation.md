# Remediation — TC-8001

## Step 3 — Affects Versions Correction

Current Affects Versions: `[RHTPA 2.0.0]`
Proposed (scoped to 2.2.x stream): `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Diff: `RHTPA 2.0.0` (invalid — no 2.0 stream exists) -> `RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2`

Proposed action: update Affects Versions via `jira.edit_issue(TC-8001, fields={"versions": [{"id": "<RHTPA-2.2.0-id>"}, {"id": "<RHTPA-2.2.1-id>"}, {"id": "<RHTPA-2.2.2-id>"}]})` using dynamically discovered Jira version IDs from Step 3.1.

A correction comment would be posted. No ProdSec Jira account ID is configured, so the @mention is omitted.

## Step 4 — Duplicate, Sibling, and Overlap Check

Proposed: search for sibling Vulnerability issues with JQL:
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8001
```

No sibling search results are assumed for this eval. Proceed to Step 5.

Step 4.3 (Cross-CVE overlap detection) is skipped because the Upstream Affected Component custom field is not configured.

Step 4.4 (Preemptive task reconciliation) — no preemptive tasks assumed.

## Step 5 — Version Lifecycle Check

Proposed: fetch product lifecycle from https://access.example.com/product-life-cycle/rhtpa. Not executed in eval mode.

## Step 6 — Already Fixed Check

No resolved sibling issues found. Proceed to Step 7.

## Step 7 — Concurrent Triage Detection

Skipped — the Upstream Affected Component custom field is not configured in Security Configuration.

## Step 7.5 — Release Jira Orchestration

Release orchestration requires interactive confirmation of the exact release Epic version and separate child Task creation. Since external tools cannot be invoked in this eval, release orchestration is reported as pending work:

- **Stream 2.2.x**: A release Epic matching `"RHTPA 2.2.* Release Tasks"` would be searched. If found, the existing Epic and its child release Task would be used. If not found, the engineer would be prompted to confirm the release version (default: next patch bump from 2.2.4, i.e., RHTPA 2.2.5) before creating the Epic and Task.
- Release Jira creation/linking is pending interactive confirmation and has not been performed.

### Step 7.5.3 — Cross-CVE Dedup

Dedup is skipped because the Upstream Affected Component custom field is not configured in Security Configuration.

## Step 8 — Remediation Decision

### Triage Outcome: Case A + Case B (Affected — create remediation tasks)

**Stream 2.2.x (scoped)**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 are not affected.

**Cross-stream impact (Case A)**: Stream 2.1.x is also affected (2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). A cross-stream impact comment would be posted on TC-8001:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x based on lock file analysis. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.

**Case B**: Create remediation tasks for the 2.2.x stream. Since the upstream branch `release/0.4.z` already ships the fix (Step 2.5), use the dependency bump variant.

Ecosystem: Cargo (source dependency) -> 2 tasks: dependency bump + downstream propagation.

### Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks for 2.2.x (source dependency ecosystem — dependency bump + downstream propagation)
- [x] **Cross-stream coverage**: 2.1.x is affected but outside issue scope. No sibling CVE Jira assumed. Preemptive tasks would be created for 2.1.x if no sibling exists (Case A).
- [x] **Link types**: "Depend" for tasks linked to TC-8001, "Blocks" for upstream -> downstream within stream
- [x] **Coordination guidance**: Omitted — no Deployment Context column in Source Repositories table (backward compatibility)
- [x] **Release Jira linking**: Pending interactive confirmation (Step 7.5)
- [x] **Dedup consistency**: Dedup skipped (no Upstream Affected Component field configured)

---

### Task 1: Dependency Bump Task (2.2.x stream)

**Proposed Jira creation** (not executed):

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

#### Task Description

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream —
a package manager update is sufficient.

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8, v0.4.9

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
- **Remediation action**: run the appropriate package manager update command:
  - **Cargo**: `cargo update -p quinn-proto` to pull in the latest compatible version
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

#### Description Digest Protocol

After creating the task, the following steps would be performed:

1. Re-fetch the task description from Jira: `jira.get_issue(<task-key>, fields=["description"])`
2. Write the re-fetched description to a temp file
3. Compute the digest: `python3 scripts/sha256-digest.py /tmp/task-desc.md` (produces `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`)
4. Post the digest comment: `jira.add_comment(<task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`
5. This digest comment is posted BEFORE creating any issue links (Depend, Blocks) or other comments on the task

#### Linkage

After digest comment:
- `jira.create_link(inwardIssue: TC-8001, outwardIssue: <task-key>, type: "Depend")`

---

### Task 2: Downstream Propagation Subtask (2.2.x stream)

**Proposed Jira creation** (not executed):

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

#### Task Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <upstream-task-key>.

The dependency bump (<upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct — carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (dependency bump must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Protocol

After creating the downstream task, the following steps would be performed:

1. Re-fetch the task description from Jira: `jira.get_issue(<downstream-task-key>, fields=["description"])`
2. Write the re-fetched description to a temp file
3. Compute the digest: `python3 scripts/sha256-digest.py /tmp/task-desc.md` (produces `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`)
4. Post the digest comment: `jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`
5. This digest comment is posted BEFORE creating any issue links (Depend, Blocks) or other comments on the task

#### Linkage

After digest comment:
- `jira.create_link(inwardIssue: TC-8001, outwardIssue: <downstream-task-key>, type: "Depend")`
- `jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")`

---

## Coordination Guidance — Omitted

The Source Repositories table in Security Configuration does not include a Deployment Context column. Per backward compatibility rules, all repositories default to `upstream` and the Coordination Guidance subsection is **omitted entirely** from remediation task descriptions. No `### Coordination Guidance` section appears in any task above. This preserves backward compatibility with existing configurations that predate the Deployment Context feature.

---

## Post-Triage Summary

After all remediation tasks are created and linked:

1. **Add label**: `ai-cve-triaged` to TC-8001
2. **Transition**: TC-8001 to In Progress
3. **Post summary comment** on TC-8001 documenting:
   - Version impact table (2.2.0-2.2.2 affected, 2.2.3-2.2.4 not affected)
   - Affects Versions correction (RHTPA 2.0.0 -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2)
   - Remediation tasks created (dependency bump + downstream propagation for 2.2.x)
   - Cross-stream impact notice (2.1.x also affected)
   - @mention of the vulnerability issue reporter using ADF mention node with the reporter's account ID from the Jira issue

   The summary comment MUST include the Comment Footnote (ADF rule + paragraph linking to sdlc-workflow/triage-security).

All actions above are presented as proposed — no Jira operations have been executed.
