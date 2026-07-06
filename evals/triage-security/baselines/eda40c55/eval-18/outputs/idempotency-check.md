# Idempotency Check: TC-8001 (Re-Run)

This document records all pre-existing triage artifacts detected on TC-8001 during the second triage run and explains why each mutation was skipped.

## Summary

All five triage artifacts from the initial run are already present on the issue. The re-run detects each one and skips the corresponding mutation, producing zero new Jira writes.

## Artifact-by-Artifact Analysis

### 1. Label: `ai-cve-triaged`

- **Detection**: The issue's `labels` field contains `ai-cve-triaged` (present alongside `CVE-2026-31812` and `pscomponent:org/rhtpa-server`).
- **Skill behavior**: The Post-Triage Summary (SKILL.md) adds `ai-cve-triaged` to mark the issue as triaged. On re-run, the label is already present in the labels array.
- **Action**: SKIP -- label already exists. No `jira.edit_issue` call to add labels is needed. Adding it again would be a no-op at the Jira API level, but the skill avoids the redundant call entirely.

### 2. Status: `In Progress`

- **Detection**: The issue's `status` field is `In Progress`.
- **Skill behavior**: Step 0.7 transitions the issue from `New` to `Assigned`, and the Post-Triage Summary transitions to `In Progress`. The status-aware handling in the Inputs section detects that the issue is already in `In Progress` (a later state than `New` or `Assigned`).
- **Action**: SKIP -- issue is already past the `Assigned` and `In Progress` transition targets. Per Step 0.7: "If the issue is already in Assigned or any later status, skip the transition silently." No `jira.transition_issue` call is issued.
- **Note**: The status-aware handling warns: "This issue is already in In Progress. It may be actively worked on." In a re-run context, this is expected since the prior triage moved it to this status.

### 3. Issue Links: Depend -> TC-8100, Depend -> TC-8101

- **Detection**: The issue's `issuelinks` array contains two `Depend` links:
  - TC-8100 (remediation Task -- upstream backport): "Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2]"
  - TC-8101 (remediation Task -- downstream propagation): "Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2]"
- **Skill behavior**: Step 8 (Case A) creates remediation tasks and links them to the Vulnerability issue with `Depend` link type. On re-run, Step 4.4 (Preemptive task reconciliation) and the remediation task creation logic in Step 8 check for existing linked tasks. The existing `Depend` links to TC-8100 and TC-8101 indicate that remediation tasks have already been created and linked.
- **Action**: SKIP -- remediation tasks TC-8100 and TC-8101 already exist and are linked via `Depend`. No new `jira.create_issue` or `jira.create_link` calls are issued. Creating duplicate tasks would violate the "one remediation Task per affected stream" rule (Important Rule 8).

### 4. Description Digest Comment

- **Detection**: Comment #1 on the issue matches the description digest pattern: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2`. It was posted by `sdlc-workflow/triage-security` on 2026-07-01T10:00:00Z.
- **Skill behavior**: Per `shared/description-digest-protocol.md`, the skill posts a description digest comment after creating remediation tasks. On re-run, the existing comments are inspected (fetched in Step 1 as part of `jira.get_issue`). The digest comment is already present.
- **Action**: SKIP -- description digest comment already exists. No duplicate `jira.add_comment` call is issued. Posting a second digest comment would create confusing duplication in the comment history.

### 5. Post-Triage Summary Comment

- **Detection**: Comment #2 on the issue is the post-triage summary. It contains the complete triage audit trail: version impact analysis, Affects Versions correction, remediation task references (TC-8100, TC-8101), and the sdlc-workflow/triage-security footnote. Posted 2026-07-01T10:01:00Z.
- **Skill behavior**: The Post-Triage Summary section of SKILL.md posts a summary comment after all triage actions are complete. On re-run, the existing comments are inspected. The post-triage summary comment is already present, identifiable by its content structure (version impact table, actions taken list) and the sdlc-workflow/triage-security footnote.
- **Action**: SKIP -- post-triage summary comment already exists. No duplicate `jira.add_comment` call is issued. A second summary would add noise and could confuse downstream consumers reading the comment history.

## Idempotency Mechanism

The triage-security skill achieves idempotency through detection-before-mutation at each step:

1. **Labels**: Check the existing `labels` array before adding
2. **Status transitions**: Check current `status` before calling `transition_issue`
3. **Issue links**: Check existing `issuelinks` array before calling `create_link`
4. **Task creation**: Check existing linked tasks before calling `create_issue`
5. **Comments**: Check existing `comments` for matching patterns (digest prefix, summary structure) before calling `add_comment`

This pattern ensures that re-running triage on an already-triaged issue is safe and produces no side effects.
