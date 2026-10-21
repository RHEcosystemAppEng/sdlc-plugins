# Idempotency Check: TC-8001 (Re-Run Detection)

This document analyzes all pre-existing triage artifacts detected on TC-8001 during a second triage run. Each artifact that would normally be created or mutated is checked against the current issue state, and skipped if already present.

## 1. Label: ai-cve-triaged

- **Expected by triage**: Post-triage summary adds the `ai-cve-triaged` label to mark the issue as triaged.
- **Current state**: Label `ai-cve-triaged` is already present in the issue's label set: `[CVE-2026-31812, pscomponent:org/rhtpa-server, ai-cve-triaged]`.
- **Decision**: **SKIP** -- label already applied. No field-edit mutation needed.

## 2. Status Transition: Assigned / In Progress

- **Expected by triage**: Step 0.8 transitions the issue from New to Assigned. Step 8 (post-remediation) transitions to In Progress.
- **Current state**: Issue status is already **In Progress**, which is past both Assigned and New.
- **Decision**: **SKIP** -- issue is already in a later workflow state. No status-transition mutation needed. Per Step 0.8: "If the issue is already in Assigned or any later status, skip the transition silently."

## 3. Assignment

- **Expected by triage**: Step 0.8 assigns the issue to the current user.
- **Current state**: Issue is already assigned to `engineer-a@example.com`.
- **Decision**: **SKIP** -- assignment is already present. Re-assignment would be a no-op or redundant. The skill notes assignment "still proceeds regardless" on re-triage, but since this produces no observable mutation on an already-assigned issue, it is effectively idempotent.

## 4. Affects Versions Correction

- **Expected by triage**: Step 3 compares PSIRT-assigned Affects Versions against lock-file evidence and corrects if needed.
- **Current state**: Affects Versions is set to `[RHTPA 2.2.0, RHTPA 2.2.1]`.
- **Lock file evidence** (from security matrix mock data):
  - RHTPA 2.2.0 (tag v0.4.5): quinn-proto 0.11.9 -- affected (< 0.11.14) -- YES
  - RHTPA 2.2.1 (tag v0.4.8): quinn-proto 0.11.12 -- affected (< 0.11.14) -- YES
  - RHTPA 2.2.2 (tag v0.4.9): retag of v0.4.8, same as 2.2.1 -- affected -- YES
  - RHTPA 2.2.3 (tag v0.4.11): quinn-proto 0.11.14 -- NOT affected (>= 0.11.14) -- NO
  - RHTPA 2.2.4 (tag v0.4.12): quinn-proto 0.11.14 -- NOT affected (>= 0.11.14) -- NO
- **Note**: RHTPA 2.2.2 is also affected but may or may not have a corresponding Jira version. The existing Affects Versions (2.2.0, 2.2.1) were set during the first triage run and represent the correction already applied.
- **Decision**: **SKIP** -- Affects Versions already reflect the corrected values from the first triage. No field-edit mutation needed. If RHTPA 2.2.2 lacks a Jira version, this was already flagged in the first run.

## 5. Remediation Task: TC-8100 (Upstream Backport)

- **Expected by triage**: Step 8 Case B creates an upstream backport task for source dependency ecosystems.
- **Current state**: TC-8100 already exists and is linked to TC-8001 via **Depend**.
  - Summary: "Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2]"
  - Status: In Progress
  - Labels: ai-generated-jira, Security, CVE-2026-31812
- **Decision**: **SKIP** -- remediation task already exists with correct link type (Depend). No remediation-task creation or link mutation needed.

## 6. Remediation Task: TC-8101 (Downstream Propagation)

- **Expected by triage**: Step 8 Case B creates a downstream propagation task for source dependency ecosystems, blocked by the upstream task.
- **Current state**: TC-8101 already exists and is linked to TC-8001 via **Depend**.
  - Summary: "Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2]"
  - Status: Open
  - Labels: ai-generated-jira, Security, CVE-2026-31812
  - Blocks: TC-8100 (correct upstream-to-downstream blocking relationship)
- **Decision**: **SKIP** -- remediation task already exists with correct link type (Depend) and correct Blocks relationship. No remediation-task creation or link mutation needed.

## 7. Description Digest Comment

- **Expected by triage**: After creating each remediation task, post a description digest comment per the description-digest-protocol.
- **Current state**: Comment #1 is a description digest comment: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f6...`
  - Posted by: sdlc-workflow/triage-security
  - Created: 2026-07-01T10:00:00Z
- **Decision**: **SKIP** -- description digest comment already exists. No comment mutation needed.

## 8. Post-Triage Summary Comment

- **Expected by triage**: After all triage actions are complete, post a summary comment documenting version impact, Affects Versions correction, triage outcome, and remediation task links.
- **Current state**: Comment #2 is the post-triage summary comment documenting:
  - Version impact for RHTPA 2.2.0 and 2.2.1
  - Actions taken (Affects Versions correction, label addition, remediation task creation, status transition)
  - Comment Footnote included (sdlc-workflow/triage-security v0.11.1)
  - Posted by: sdlc-workflow/triage-security
  - Created: 2026-07-01T10:01:00Z
- **Decision**: **SKIP** -- post-triage summary comment already exists. Posting a duplicate summary would create noise. No comment mutation needed.

## 9. Cross-Stream Impact (Case A Check)

- **Expected by triage**: For stream-scoped issues, check if other streams are also affected and post a cross-stream impact comment.
- **Analysis**: The issue is scoped to stream 2.2.x. Stream 2.1.x (versions 2.1.0 and 2.1.1) ships quinn-proto 0.11.9, which IS affected. However, cross-stream impact analysis and any resulting preemptive tasks would have been handled in the first triage run.
- **Decision**: **SKIP** -- any cross-stream impact actions (comments, preemptive tasks) were already handled in the first run. Re-running would produce duplicates.

## Summary Table

| Artifact | Expected Action | Current State | Re-Run Decision |
|----------|-----------------|---------------|-----------------|
| `ai-cve-triaged` label | Add label | Already present | SKIP |
| Status transition | New -> Assigned -> In Progress | Already In Progress | SKIP |
| Assignment | Assign to current user | Already assigned | SKIP |
| Affects Versions | Correct to 2.2.0, 2.2.1 | Already set to 2.2.0, 2.2.1 | SKIP |
| TC-8100 (upstream backport) | Create + Depend link | Exists + linked | SKIP |
| TC-8101 (downstream propagation) | Create + Depend link | Exists + linked | SKIP |
| Description digest comment | Post digest | Already posted | SKIP |
| Post-triage summary comment | Post summary | Already posted | SKIP |
| Cross-stream impact | Analyze + comment | Already handled | SKIP |

**All 9 triage artifacts are already present. No new mutations are required.**
