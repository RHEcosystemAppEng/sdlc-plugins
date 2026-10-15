# Step 3 -- Affects Versions Correction

**Current Affects Versions**: RHTPA 2.2.0
**Proposed Affects Versions**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2, RHTPA 2.2.3, RHTPA 2.2.4

All 2.2.x versions are affected (all ship criterion 0.5.1, which is within the affected range < 0.5.2). The PSIRT-assigned Affects Versions is incomplete -- it only lists RHTPA 2.2.0 but should include all affected versions in the 2.2.x stream.

**Proposed correction** (not executed -- eval mode):
```
Current: [RHTPA 2.2.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2, RHTPA 2.2.3, RHTPA 2.2.4]
```

Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (not hardcoded).

---

# Step 4 -- Duplicate, Sibling, and Overlap Check

Step 4.3 (Cross-CVE overlap detection): **Skipped** -- Upstream Affected Component custom field is not configured in Security Configuration.

Step 4.4 (Preemptive task reconciliation): No preemptive tasks found (no search executed -- eval mode).

---

# Step 7 -- Concurrent Triage Detection

**Skipped** -- Upstream Affected Component custom field is not configured in Security Configuration.

---

# Step 7.5 -- Release Jira Orchestration

Release orchestration confirmations would be required before creating remediation tasks. In eval mode, release Jira creation is not executed. The engineer would be prompted to confirm the release Epic version and release Task creation for the 2.2.x stream.

Since release evidence and confirmation are unavailable in eval mode, this is reported as pending work rather than claiming creation.

---

# Step 8 -- Remediation

## Triage Decision

**Case B: Affected -- create remediation tasks**

All versions in the 2.2.x stream are affected. Remediation tasks are required.

**Ecosystem**: Cargo (source dependency) -- 2 tasks per stream: upstream backport + downstream propagation.

**Dev-dependency handling**: criterion is a dev-only dependency (identified in Step 2.3.5). Per the dependency scope decision tree:
- Add `dev-dependency` label to all remediation tasks
- Set priority to **Normal** (overriding CVE severity CVSS 5.3 Medium)
- Include dev/build-only note in task descriptions

---

## Remediation Task 1: Upstream Backport Task

**Summary**: Remediate CVE-2026-99001: bump criterion to 0.5.2 (rhtpa-2.2)

**Issue Type**: Task
**Labels**: `["ai-generated-jira", "Security", "CVE-2026-99001", "dev-dependency"]`
**Priority**: Normal (dev-dependency override -- CVE severity is Medium/CVSS 5.3 but criterion is dev-only and not shipped in production)

### Task Description

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99001: criterion path traversal in benchmark output.
The vulnerable dependency (criterion < 0.5.2) must be updated to the fixed
version (0.5.2+).

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

Affected versions: RHTPA 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4
Source commit(s): v0.4.5, v0.4.8, v0.4.11, v0.4.12

Upstream fix: (none available in remote links)
Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (dev-only)
- **Dependency scope**: [dev-dependencies] in backend/Cargo.toml -- NOT shipped in production builds (benchmarks only)
- This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only).

### Remediation approach (direct dependency)

criterion is a direct dependency (declared in [dev-dependencies]). Update the
version constraint:

- Update criterion dependency to >= 0.5.2 in backend/Cargo.toml [dev-dependencies]
- Run `cargo update -p criterion` to update Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass (criterion benchmarks compile and run)

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8050 (parent tracking issue)
```

### Post-creation procedure (not executed -- eval mode)

1. **Create the task** via `jira.create_issue(...)` with the labels and priority above
2. **Post description digest comment** (before any links or other comments):
   - Re-fetch the task description from Jira after `create_issue`
   - Compute SHA-256 digest using `python3 scripts/sha256-digest.py`
   - Post comment: `[sdlc-workflow] Description digest: <tagged-digest>`
3. **Create Depend link**: `jira.create_link(inwardIssue: TC-8050, outwardIssue: <upstream-task-key>, type: "Depend")`

---

## Remediation Task 2: Downstream Propagation Subtask

**Summary**: Propagate CVE-2026-99001 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Issue Type**: Task
**Labels**: `["ai-generated-jira", "Security", "CVE-2026-99001", "dev-dependency"]`
**Priority**: Normal (dev-dependency override -- inherited from upstream task)

### Task Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99001 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps criterion to 0.5.2
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct (dev-only) -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8050 (parent tracking issue)
```

### Post-creation procedure (not executed -- eval mode)

1. **Create the task** via `jira.create_issue(...)` with the labels and priority above
2. **Post description digest comment** (before any links or other comments):
   - Re-fetch the task description from Jira after `create_issue`
   - Compute SHA-256 digest using `python3 scripts/sha256-digest.py`
   - Post comment: `[sdlc-workflow] Description digest: <tagged-digest>`
3. **Create Depend link**: `jira.create_link(inwardIssue: TC-8050, outwardIssue: <downstream-task-key>, type: "Depend")`
4. **Create Blocks link**: `jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")`

---

## Post-Triage Summary

After remediation task creation, the following post-triage actions would be performed (not executed -- eval mode):

1. **Add `ai-cve-triaged` label** to TC-8050
2. **Transition TC-8050 to In Progress** (if not already)
3. **Post summary comment** on TC-8050 documenting:
   - Version impact table (all 2.2.x versions affected -- criterion 0.5.1 < 0.5.2)
   - Affects Versions correction (RHTPA 2.2.0 -> RHTPA 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4)
   - Triage outcome: remediation tasks created (Case B)
   - Dev-dependency classification: criterion is in [dev-dependencies], not shipped in production; priority overridden to Normal
   - Links to upstream backport task and downstream propagation subtask
   - @mention of the vulnerability issue's reporter using ADF mention node
   - Comment Footnote: "This comment was AI-generated by sdlc-workflow/triage-security v0.13.10."

### Comment Footnote

All Jira comments posted by this skill include the following footnote (ADF format):

```json
{
  "type": "rule"
},
{
  "type": "paragraph",
  "content": [
    {
      "type": "text",
      "text": "This comment was AI-generated by "
    },
    {
      "type": "text",
      "text": "sdlc-workflow/triage-security",
      "marks": [
        {
          "type": "link",
          "attrs": {
            "href": "https://github.com/RHEcosystemAppEng/sdlc-plugins"
          }
        }
      ]
    },
    {
      "type": "text",
      "text": " v0.13.10."
    }
  ]
}
```
