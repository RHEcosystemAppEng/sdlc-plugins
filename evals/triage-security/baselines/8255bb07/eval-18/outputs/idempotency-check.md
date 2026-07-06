# Idempotency Check: TC-8001 Re-Run Analysis

This document records every pre-existing triage artifact detected on TC-8001
during the second invocation of `triage-security`, and explains why each
corresponding mutation was skipped.

## 1. Label: `ai-cve-triaged`

- **Detection**: The issue's `labels` field already contains `ai-cve-triaged`.
- **Normal action**: Post-Triage Summary (Step 8 epilogue) adds this label to mark the issue as triaged.
- **Skip reason**: Label is already present. Adding a duplicate label is a no-op in Jira, but the skill recognizes the label's presence as evidence that triage has already completed. No label mutation required.

## 2. Status: In Progress

- **Detection**: The issue's `status` field is `In Progress`, which is a post-triage state (beyond New and Assigned).
- **Normal action**: Step 0.7 transitions the issue from New to Assigned; Step 8 transitions it further after remediation task creation (typically to In Progress).
- **Skip reason**: The issue is already past the Assigned state. Per the status-aware handling rules in the Inputs section, issues in In Progress trigger a warning: "This issue is already in In Progress. It may be actively worked on." The skill asks whether to proceed with re-triage or skip. Since there is nothing new to triage (all artifacts exist), no status transition is needed.

## 3. Depend Link: TC-8100 (upstream backport task)

- **Detection**: The issue's `issuelinks` field contains a Depend link to TC-8100 with summary "Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2]" (status: In Progress).
- **Normal action**: Step 8 Case A creates an upstream backport remediation task for the affected stream and links it via Depend.
- **Skip reason**: A remediation task for the upstream backport already exists and is linked. The task summary matches the expected template for a Cargo ecosystem upstream backport task targeting the 2.2.x stream. Creating a duplicate task would produce redundant work items. No task creation or link mutation required.

## 4. Depend Link: TC-8101 (downstream propagation task)

- **Detection**: The issue's `issuelinks` field contains a Depend link to TC-8101 with summary "Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2]" (status: Open, blocks TC-8100).
- **Normal action**: Step 8 Case A creates a downstream propagation subtask for Cargo ecosystem remediation and links it via Depend, with a Blocks link to the upstream task.
- **Skip reason**: A downstream propagation task already exists and is linked. The task summary matches the expected template for a Cargo ecosystem downstream propagation task. The Blocks relationship to TC-8100 is also already established. Creating a duplicate would produce redundant work items. No task creation or link mutation required.

## 5. Description Digest Comment

- **Detection**: Comment #1 on the issue is a description digest comment with marker `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2`, posted by `sdlc-workflow/triage-security` on 2026-07-01T10:00:00Z.
- **Normal action**: Per the description-digest-protocol, a digest comment is posted after the Vulnerability issue is processed to record the hash of the description at triage time.
- **Skip reason**: A digest comment already exists. The description digest protocol checks for an existing digest comment before posting a new one. Since one is present, no duplicate digest comment is posted. If the description had changed since the first triage, the digest would differ, but the presence of the comment itself signals that digest tracking is already in place. No comment mutation required.

## 6. Post-Triage Summary Comment

- **Detection**: Comment #2 on the issue is the post-triage summary, documenting: version impact (RHTPA 2.2.0 and 2.2.1 affected, 2.2.2+ not affected), Affects Versions correction, remediation tasks (TC-8100, TC-8101), and the transition to In Progress. Posted by `sdlc-workflow/triage-security` on 2026-07-01T10:01:00Z with the standard comment footnote.
- **Normal action**: Post-Triage Summary (Step 8 epilogue) posts a summary comment documenting the triage outcome, version impact, and created tasks.
- **Skip reason**: A post-triage summary comment already exists with complete triage documentation. Posting a second summary would create a confusing duplicate audit trail. No comment mutation required.

## 7. Affects Versions

- **Detection**: The issue's Affects Versions are already set to `RHTPA 2.2.0, RHTPA 2.2.1`, which matches the version impact analysis (versions 2.2.0 and 2.2.1 ship quinn-proto < 0.11.14; versions 2.2.2+ ship 0.11.14 and are not affected).
- **Normal action**: Step 3 corrects the Affects Versions based on lock file evidence.
- **Skip reason**: The current Affects Versions already match what the version impact analysis would produce. No correction needed. No field mutation required.

## Summary

| Artifact | Present? | Mutation Skipped? | Reason |
|----------|----------|-------------------|--------|
| `ai-cve-triaged` label | Yes | Yes | Already applied |
| Status (In Progress) | Yes | Yes | Already past triage transitions |
| Depend link to TC-8100 | Yes | Yes | Upstream backport task already exists and linked |
| Depend link to TC-8101 | Yes | Yes | Downstream propagation task already exists and linked |
| Description digest comment | Yes | Yes | Digest comment already posted |
| Post-triage summary comment | Yes | Yes | Summary already posted |
| Affects Versions correction | Yes (correct) | Yes | Already matches lock file evidence |

All seven triage artifacts are present and correct. Zero mutations are required on this re-run.
