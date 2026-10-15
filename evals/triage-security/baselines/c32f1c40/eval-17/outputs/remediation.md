# Step 3 -- Affects Versions Correction

**Proposed correction** (not executed -- eval prohibits Jira calls):

The issue is scoped to stream 2.2.x (suffix [rhtpa-2.2]). Only 2.2.x versions are included in the Affects Versions correction for this issue.

- Current (PSIRT-assigned): [RHTPA 2.0.0]
- Proposed (lock-file-verified): [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

The PSIRT-assigned version RHTPA 2.0.0 does not exist in the supportability matrix and is incorrect. The proposed correction is based on lock file analysis at pinned commits from security-matrix.md, scoped to stream 2.2.x per issue suffix.

Version names are referenced from the supportability matrix rather than hardcoded Jira version IDs (Important Rule 6). The actual Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` at runtime.

No ProdSec Jira account ID is configured, so no @mention is included in the correction comment.

---

# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

Step 4.3 (Cross-CVE overlap detection) is skipped because the Upstream Affected Component custom field is not configured in the Security Configuration.

Step 4.4 (Preemptive task reconciliation) would search for preemptive tasks with labels `security-preemptive` and `CVE-2026-31812`. No preemptive tasks assumed for this eval scenario.

---

# Step 7 -- Concurrent Triage Detection

Step 7 is skipped because the Upstream Affected Component custom field is not configured in the Security Configuration.

---

# Step 7.5 -- Release Jira Orchestration

**Release orchestration confirmations** (not executed -- eval prohibits Jira calls):

Since Jira calls cannot be made in this eval, the release Epic version cannot be confirmed interactively. Release orchestration requires:

1. Searching for an existing release Epic matching "RHTPA 2.2.* Release Tasks"
2. If no Epic exists, proposing the next patch version (e.g., RHTPA 2.2.5 based on latest released 2.2.4) and requiring individual engineer confirmation
3. Finding or creating a release Task "RHTPA <version> CVE triage" as a child of the Epic, requiring individual confirmation for creation

Since release evidence and interactive confirmation are unavailable in this eval, release Jira orchestration is reported as **pending work**. Remediation tasks would be created but release linking would be deferred until the release Epic and Task are confirmed.

**Dedup decision**: Step 7.5.3 cross-CVE dedup check requires the Upstream Affected Component custom field to be configured. Since it is not configured in this project's Security Configuration, dedup is skipped entirely.

---

# Step 8 -- Remediation

## Triage Decision

The version impact table shows affected versions in the scoped 2.2.x stream (2.2.0, 2.2.1, 2.2.2) and in the cross-stream 2.1.x stream (2.1.0, 2.1.1). This is **Case A** (cross-stream impact) followed by **Case B** (create remediation tasks).

## Case A: Cross-Stream Impact (scoped issue)

The issue is scoped to stream 2.2.x via suffix [rhtpa-2.2]. The version impact analysis reveals that 2.1.x stream is also affected (versions 2.1.0 and 2.1.1 ship quinn-proto 0.11.9, which is within the affected range < 0.11.14).

**Proposed cross-stream impact comment** on TC-8001:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x based on lock file analysis. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.

A JQL search for sibling issues with label CVE-2026-31812 would determine whether a CVE Jira already exists for the 2.1.x stream. If no sibling exists, proactive preemptive remediation tasks would be created for 2.1.x (see Case B preemptive variant below).

## Case B: Remediation Task Creation (2.2.x stream)

Ecosystem: Cargo (source dependency) -- creates **2 tasks**: upstream backport + downstream propagation (Important Rule 8).

### Task 1: Upstream Backport Task

**Proposed Jira creation** (not executed):

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task Description:**

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (v0.4.5), RHTPA 2.2.1 (v0.4.8), RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z (from Ecosystem Mappings Upstream Branch column)
- **Dependency type**: direct (quinn-proto is a direct workspace dependency)
- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

### Task 2: Downstream Propagation Subtask

**Proposed Jira creation** (not executed):

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task Description:**

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14 on release/0.4.z.
Once that PR merges, update the source pinning in this Konflux release
repo so the next build ships the fix.

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

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Jira Linkage (proposed, not executed)

After creating each remediation task, the following links would be established:

1. **Depend**: TC-8001 (CVE) --> upstream backport task (remediation)
2. **Depend**: TC-8001 (CVE) --> downstream propagation task (remediation)
3. **Blocks**: upstream backport task --> downstream propagation task (upstream must complete first)
4. **Transition**: TC-8001 to In Progress
5. **Assign**: TC-8001 to current user

## Description Digest Protocol

After creating each remediation task, the description digest protocol would be executed:

**For the upstream backport task:**
1. Re-fetch the task description from Jira after create_issue: `jira.get_issue(<upstream-task-key>, fields=["description"])`
2. Write the re-fetched description to a temp file
3. Compute SHA-256 digest using `python3 scripts/sha256-digest.py /tmp/task-desc.md` (outputs format-tagged digest, e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`)
4. Post digest comment: `jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`
5. The digest comment is posted BEFORE creating issue links (Depend, Blocks) or other comments

**For the downstream propagation subtask:**
1. Re-fetch the task description from Jira after create_issue: `jira.get_issue(<downstream-task-key>, fields=["description"])`
2. Write the re-fetched description to a temp file
3. Compute SHA-256 digest using `python3 scripts/sha256-digest.py /tmp/task-desc.md` (outputs format-tagged digest)
4. Post digest comment: `jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`
5. The digest comment is posted BEFORE creating issue links (Depend, Blocks) or other comments

The digest is computed from the re-fetched description (via Jira API after create_issue), not from the description string passed to create_issue, because Jira normalizes content during storage.

## Post-Triage Summary

After all remediation tasks are created and linked:

1. **Add label**: `ai-cve-triaged` to TC-8001
2. **Post summary comment** on TC-8001 documenting:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 --> RHTPA 2.2.0, 2.2.1, 2.2.2)
   - Triage outcome: remediation tasks created
   - Links to all remediation tasks
   - Cross-stream impact notice for 2.1.x
   - @mention of the vulnerability issue reporter (from Jira issue reporter field)
   - Comment Footnote (from shared/comment-footnote.md using skill name `triage-security`)

All proposed actions are presented as recommendations -- no Jira operations have been executed in this eval. Affects Versions changes, label additions, status transitions, task creation, and link creation are all proposals to be confirmed by the engineer before execution.
