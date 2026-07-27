# Idempotency Check: TC-8001 (Re-Run Detection)

This document records all pre-existing triage artifacts detected on TC-8001 and the corresponding skip decisions made during the second triage run.

## Summary

TC-8001 has **already been fully triaged** in a prior run. Every triage artifact that the workflow would produce already exists. The re-run detects each artifact and skips all mutations, producing a fully idempotent outcome.

## Pre-Existing Artifacts Detected

### 1. Label: `ai-cve-triaged`

- **Detection**: The issue's labels array includes `ai-cve-triaged`.
- **Workflow step**: Post-Triage Summary (label addition)
- **Action**: Skip -- label already present. Adding it again would be a no-op at the Jira API level, but the workflow recognizes this as evidence that triage has already completed and avoids redundant mutation.

### 2. Status: In Progress

- **Detection**: The issue status is `In Progress`, which is past the `Assigned` and `New` states.
- **Workflow step**: Step 0.7 (Assign and Transition to Assigned)
- **Action**: Skip transition -- the issue is already in a later status than `Assigned`. Per Step 0.7: "If the issue is already in Assigned or any later status, skip the transition silently." The assignment step (setting assignee to current user) would still proceed in a live run, but the transition is skipped.
- **Status-aware handling**: Per the Inputs section, an issue in `In Progress` status triggers a warning: "This issue is already in In Progress. It may be actively worked on." The engineer is asked whether to proceed with triage anyway or skip. For this analysis, we assume the engineer chose to proceed (to verify version impact and artifacts).

### 3. Remediation Task TC-8100 (Upstream Backport)

- **Detection**: Issue links include a `Depend` link to TC-8100 with summary "Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2]" and labels `ai-generated-jira, Security, CVE-2026-31812`.
- **Workflow step**: Step 8, Case B (Remediation task creation -- upstream backport)
- **Action**: Skip -- a remediation task for the upstream backport in the 2.2.x stream already exists and is linked via `Depend`. The task's labels include `ai-generated-jira` and match the CVE ID, confirming it was created by a prior triage run. Creating a duplicate task would violate the workflow's design.

### 4. Remediation Task TC-8101 (Downstream Propagation)

- **Detection**: Issue links include a `Depend` link to TC-8101 with summary "Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2]" and labels `ai-generated-jira, Security, CVE-2026-31812`. TC-8101 also blocks TC-8100.
- **Workflow step**: Step 8, Case B (Remediation task creation -- downstream propagation)
- **Action**: Skip -- a remediation task for the downstream propagation in the 2.2.x stream already exists and is linked via `Depend`. The blocking relationship (TC-8101 blocks TC-8100) matches the expected Cargo ecosystem pattern of two linked tasks per stream.

### 5. Description Digest Comment

- **Detection**: Comment 1 matches the pattern `[sdlc-workflow] Description digest: sha256-md:<hash>`, posted by `sdlc-workflow/triage-security` on 2026-07-01T10:00:00Z.
- **Workflow step**: Remediation Task Creation (description digest protocol)
- **Action**: Skip -- the description digest already exists. The digest `sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2` records the hash of the issue description at the time of original triage. A re-run would compute the same hash (assuming the description has not changed) and recognize the existing digest comment.

### 6. Post-Triage Summary Comment

- **Detection**: Comment 2 is a post-triage summary documenting: version impact (RHTPA 2.2.0 and 2.2.1 affected, 2.2.2+ not affected), actions taken (Affects Versions corrected, label added, tasks TC-8100 and TC-8101 created, transitioned to In Progress). Posted by `sdlc-workflow/triage-security` on 2026-07-01T10:01:00Z. Includes the comment footnote linking to sdlc-plugins v0.11.1.
- **Workflow step**: Post-Triage Summary (summary comment)
- **Action**: Skip -- posting a second summary comment would create a duplicate audit trail entry. The existing comment already documents all triage actions from the first run.

### 7. Affects Versions Already Correct

- **Detection**: The current Affects Versions on the issue are `RHTPA 2.2.0, RHTPA 2.2.1`. The version impact analysis confirms that within the 2.2.x stream scope, versions 2.2.0 (quinn-proto 0.11.9) and 2.2.1 (quinn-proto 0.11.12) are affected, while 2.2.2+ ship quinn-proto 0.11.14 (fixed). The Affects Versions already match the expected correction.
- **Workflow step**: Step 3 (Affects Versions Correction)
- **Action**: Skip -- per Step 3.2: "If Affects Versions are already correct: note this and proceed without changes." No Jira edit_issue call needed.

## Artifact Completeness Matrix

| Artifact | Expected by Workflow | Present on TC-8001 | Re-Run Action |
|----------|---------------------|--------------------|---------------|
| `ai-cve-triaged` label | Post-Triage Summary | Yes | Skip (already present) |
| Status >= Assigned | Step 0.7 | Yes (In Progress) | Skip transition |
| Upstream backport task | Step 8 Case B | Yes (TC-8100, Depend link) | Skip creation |
| Downstream propagation task | Step 8 Case B | Yes (TC-8101, Depend link) | Skip creation |
| Description digest comment | Remediation Task Creation | Yes (sha256-md:a1b2...) | Skip (already posted) |
| Post-triage summary comment | Post-Triage Summary | Yes (with full audit trail) | Skip (already posted) |
| Affects Versions correction | Step 3 | Yes (already correct) | Skip (no diff) |
| Task blocking relationship | Step 8 Case B | Yes (TC-8101 blocks TC-8100) | Skip (already linked) |
