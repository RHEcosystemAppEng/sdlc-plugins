# Idempotency Check: TC-8001 Re-Run Analysis

This document records every pre-existing triage artifact detected on TC-8001
during the second invocation of `/sdlc-workflow:triage-security`, and explains
why each mutation was skipped.

## Summary

All triage artifacts from the prior run are present and intact. The re-run
detects each one and skips the corresponding mutation. **No new Jira writes
are produced.**

---

## 1. Status -- Already In Progress

- **Expected by triage**: Step 0.7 assigns the issue and transitions to Assigned;
  Step 8 / Remediation Templates transitions to In Progress after creating tasks.
- **Current state**: Status is `In Progress`.
- **Action**: Skip. The issue is already past Assigned and in a later status.
  Step 0.7 specifies: "If the issue is already in Assigned or any later status,
  skip the transition silently." The status-aware handling in the Inputs section
  also fires a warning because In Progress indicates the issue may be actively
  worked on. Since this is a known re-run, we acknowledge and proceed with the
  read-only analysis.

## 2. Label `ai-cve-triaged` -- Already Present

- **Expected by triage**: Post-Triage Summary (after Step 8) adds the
  `ai-cve-triaged` label to mark the issue as triaged.
- **Current state**: Labels include `ai-cve-triaged`.
- **Action**: Skip. Adding the label again would be a no-op (Jira labels are
  a set), but the presence of the label is the primary idempotency signal --
  it indicates a prior triage run completed successfully. No label mutation
  needed.

## 3. Affects Versions -- Already Correct

- **Expected by triage**: Step 3 corrects Affects Versions based on lock file
  evidence scoped to the issue's stream (2.2.x).
- **Current state**: Affects Versions are `RHTPA 2.2.0, RHTPA 2.2.1`.
- **Lock file evidence**: quinn-proto versions for 2.2.x stream:
  - 2.2.0 (v0.4.5): 0.11.9 -- affected
  - 2.2.1 (v0.4.8): 0.11.12 -- affected
  - 2.2.2 (v0.4.9): retag of 2.2.1 -- affected
  - 2.2.3 (v0.4.11): 0.11.14 -- NOT affected (fixed)
  - 2.2.4 (v0.4.12): 0.11.14 -- NOT affected (fixed)
- **Analysis**: RHTPA 2.2.0 and 2.2.1 are the correct Affects Versions for
  the scoped stream. Version 2.2.2 is a retag of 2.2.1 (same source) and
  would typically share an Affects Version entry. Versions 2.2.3+ ship the
  fix. The current Affects Versions match the expected correction.
- **Action**: Skip. Step 3.2 states: "If Affects Versions are already correct:
  note this and proceed without changes." No edit_issue call needed.

## 4. Remediation Tasks -- Already Exist (TC-8100, TC-8101)

- **Expected by triage**: Step 8 Case B creates remediation tasks. For a Cargo
  (source dependency) ecosystem, two tasks per stream: upstream backport +
  downstream propagation.
- **Current state**: Two tasks are linked via `Depend`:
  - **TC-8100**: "Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2]"
    -- Status: In Progress, Labels: ai-generated-jira, Security, CVE-2026-31812
  - **TC-8101**: "Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2]"
    -- Status: Open, Labels: ai-generated-jira, Security, CVE-2026-31812, Blocks: TC-8100
- **Analysis**: Both tasks match the expected remediation structure:
  - TC-8100 is the upstream backport task (Cargo source dependency, upstream branch)
  - TC-8101 is the downstream propagation subtask (Konflux release repo update),
    blocked by TC-8100
  - Both carry the expected labels (ai-generated-jira, Security, CVE-2026-31812)
  - Link type is Depend (standard remediation linkage to the Vulnerability issue)
  - Blocks link exists between TC-8101 and TC-8100 (downstream blocked by upstream)
- **Action**: Skip. Creating duplicate remediation tasks would be incorrect.
  The existing tasks cover the 2.2.x stream completely. No create_issue or
  create_link calls needed.

## 5. Description Digest Comment -- Already Exists

- **Expected by triage**: Step 1 / Post-Triage processing posts a description
  digest comment per `shared/description-digest-protocol.md`.
- **Current state**: Comment #1 is: `[sdlc-workflow] Description digest:
  sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2`
  -- posted by sdlc-workflow/triage-security on 2026-07-01T10:00:00Z.
- **Action**: Skip. The digest comment exists. Re-posting would create a
  duplicate comment. The description has not changed (the digest would be
  the same), so no update is needed.

## 6. Post-Triage Summary Comment -- Already Exists

- **Expected by triage**: The Post-Triage Summary section adds a summary
  comment documenting version impact, Affects Versions correction, triage
  outcome, and remediation task links.
- **Current state**: Comment #2 is the post-triage summary, documenting:
  - Version impact: RHTPA 2.2.0 and 2.2.1 affected, 2.2.2+ not affected
  - Actions: Affects Versions corrected, ai-cve-triaged label added,
    remediation tasks TC-8100 and TC-8101 created, transitioned to In Progress
  - Comment Footnote present (sdlc-workflow/triage-security v0.11.1)
- **Action**: Skip. The summary comment is already present and documents the
  complete triage outcome. Re-posting would create a duplicate. No add_comment
  call needed.

## 7. Issue Assignment -- Already Assigned

- **Expected by triage**: Step 0.7 assigns the issue to the current user.
- **Current state**: Assignee is engineer-a@example.com.
- **Action**: Step 0.7 specifies: "The assignment in step 2 still proceeds
  regardless -- it ensures the current user is recorded even when re-triaging
  an issue that was previously assigned." In a live run, the assignment API
  call would fire but produce no meaningful change if the same user is
  re-triaging. Since we are writing to files rather than calling Jira, this
  is noted but not executed.

---

## Artifact Detection Summary

| Artifact | Expected By | Pre-Existing? | Mutation Skipped? |
|---|---|---|---|
| Status = In Progress | Step 0.7 + Step 8 | YES | YES -- already past Assigned |
| Label `ai-cve-triaged` | Post-Triage Summary | YES | YES -- label already present |
| Affects Versions = RHTPA 2.2.0, 2.2.1 | Step 3 | YES -- correct | YES -- no correction needed |
| Remediation task TC-8100 (upstream) | Step 8 Case B | YES -- linked via Depend | YES -- task exists |
| Remediation task TC-8101 (downstream) | Step 8 Case B | YES -- linked via Depend | YES -- task exists |
| Blocks link TC-8101 -> TC-8100 | Remediation Templates | YES | YES -- link exists |
| Description digest comment | Post-Triage | YES | YES -- digest present |
| Post-triage summary comment | Post-Triage Summary | YES | YES -- summary present |
| Issue assignment | Step 0.7 | YES | YES (or no-op reassignment) |

**Total Jira mutations that would be executed on re-run: 0**
(excluding the idempotent reassignment in Step 0.7, which is a no-op for the same user)
