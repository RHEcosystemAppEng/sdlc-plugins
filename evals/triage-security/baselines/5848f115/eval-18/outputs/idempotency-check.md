# Idempotency Check: TC-8001 Re-Run Analysis

This document analyzes all pre-existing triage artifacts detected on TC-8001 during the second (re-run) invocation of triage-security, and explains which operations were skipped as a result.

## Pre-Existing Triage Artifacts Detected

### 1. Label: `ai-cve-triaged`

- **Detection**: The issue's Labels field contains `ai-cve-triaged`.
- **Significance**: This label is added in the Post-Triage Summary step (the final step of triage) to mark the issue as fully triaged. Its presence is the primary indicator that a complete triage has already been performed.
- **Action on re-run**: The label already exists. Adding it again would be a no-op (Jira labels are a set; duplicates are not created). No mutation needed.

### 2. Status: In Progress

- **Detection**: The issue's current Status is `In Progress`.
- **Significance**: Per the skill's status-aware handling (SKILL.md Inputs section), an issue in `In Progress` status triggers a warning: "This issue is already in In Progress. It may be actively worked on." The engineer would be asked whether to proceed with triage anyway or skip.
- **Action on re-run**: The status indicates prior triage has already transitioned the issue past New/Assigned. Step 0.7 (Assign and Transition to Assigned) would detect the issue is already past Assigned status and skip the transition. The assignment update (Step 0.7, step 2) could still proceed to record the current user, but no status transition mutation is needed.

### 3. Remediation Tasks: TC-8100 and TC-8101 (Depend links)

- **Detection**: The issue has two `Depend`-type issue links:
  - TC-8100: "Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2]" (In Progress)
  - TC-8101: "Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2]" (Open, Blocks TC-8100)
- **Significance**: These are the exact remediation tasks that Step 8 Case B would create for a Cargo (source dependency) ecosystem:
  - Task 1: upstream backport (TC-8100)
  - Task 2: downstream propagation (TC-8101), blocked by TC-8100
  - Both carry the labels `ai-generated-jira`, `Security`, and `CVE-2026-31812`
- **Action on re-run**: Step 8 Case B would detect that remediation tasks already exist for this stream and CVE. The existing Depend links from the Vulnerability issue to these tasks confirm that remediation was already created. No new tasks should be created. No new links should be created (the Depend links already exist).

### 4. Description Digest Comment

- **Detection**: Comment #1 is a description digest comment with the marker `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2`, posted by `sdlc-workflow/triage-security` on 2026-07-01T10:00:00Z.
- **Significance**: This comment records a hash of the issue description at the time of triage, per the description digest protocol. Its presence indicates Step 1 data extraction and digest posting were already completed.
- **Action on re-run**: The digest comment already exists. Posting a duplicate digest would create redundant comments. The re-run should detect the existing digest and skip posting a new one. If the description has not changed since the original triage (the digest hash would match a freshly computed hash), no update is needed.

### 5. Post-Triage Summary Comment

- **Detection**: Comment #2 is the post-triage summary documenting:
  - Version impact analysis results (RHTPA 2.2.0 and 2.2.1 affected; 2.2.2+ not affected)
  - Affects Versions correction applied
  - Label `ai-cve-triaged` added
  - Remediation tasks created: TC-8100 (upstream backport), TC-8101 (downstream propagation)
  - Status transitioned to In Progress
  - Comment includes the AI-generated footnote with skill name `triage-security` v0.11.1
- **Significance**: This is the final artifact of a complete triage run. Its presence, combined with the `ai-cve-triaged` label, confirms the full triage workflow executed successfully.
- **Action on re-run**: Posting a second summary comment would create misleading duplication. The re-run should detect the existing summary and skip posting a new one.

### 6. Affects Versions: Already Corrected

- **Detection**: The issue's Affects Versions field currently shows `RHTPA 2.2.0, RHTPA 2.2.1`.
- **Significance**: These match the version impact analysis (versions 2.2.0 and 2.2.1 ship quinn-proto < 0.11.14). The post-triage summary confirms Affects Versions were already corrected.
- **Action on re-run**: Step 3 (Affects Versions Correction) would compare the current Affects Versions against the version impact table and find they already match. No correction needed -- the skill notes "If Affects Versions are already correct: note this and proceed without changes."

### 7. Assignee: Already Set

- **Detection**: The issue's Assignee is `engineer-a@example.com`.
- **Significance**: Step 0.7 assigns the issue to the current user. The issue already has an assignee from the prior triage run.
- **Action on re-run**: Step 0.7 would still update the assignee to the current user (this is always applied regardless of prior state), but this is a benign overwrite, not a new artifact.

## Summary of Artifacts and Skip Decisions

| Artifact | Exists? | Re-Run Behavior |
|----------|---------|-----------------|
| `ai-cve-triaged` label | Yes | Skip -- already present |
| Status: In Progress | Yes | Skip transition -- already past Assigned |
| Remediation Task TC-8100 (upstream backport) | Yes, linked via Depend | Skip -- remediation already created |
| Remediation Task TC-8101 (downstream propagation) | Yes, linked via Depend | Skip -- remediation already created |
| Description digest comment | Yes | Skip -- digest already posted |
| Post-triage summary comment | Yes | Skip -- summary already posted |
| Affects Versions correction | Already correct (RHTPA 2.2.0, 2.2.1) | Skip -- values already match impact analysis |
| Assignee | Already set | Overwrite is benign (not a new mutation) |

All eight triage artifacts from the prior run are present and consistent. No new Jira mutations are warranted.
