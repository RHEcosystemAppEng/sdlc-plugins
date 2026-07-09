# Idempotency Check -- Pre-existing Triage Artifacts

This is a **re-run** of triage on TC-8001, which was already triaged in a prior run. Every triage artifact is checked for existence before any mutation is attempted.

## 1. Status Idempotency

- **Current status**: In Progress
- **Expected post-triage status**: In Progress
- **Action**: SKIP -- the issue is already in a post-triage state (In Progress). No status transition is attempted.
- **Note**: The triage detects that the issue is already In Progress and warns: "This issue is already in `In Progress`. It may be actively worked on." The re-run does not attempt to transition the status again.

## 2. Label Idempotency (`ai-cve-triaged`)

- **Current labels**: CVE-2026-31812, pscomponent:org/rhtpa-server, ai-cve-triaged
- **Label `ai-cve-triaged`**: Already present
- **Action**: SKIP -- the label is already on the issue. No duplicate label addition is attempted.

## 3. Assignee Idempotency

- **Current assignee**: engineer-a@example.com
- **Action**: SKIP -- the issue is already assigned. Step 0.7 detects the existing assignment. The assignment can be updated to the current user if different, but no new assignment action creates duplicate state.

## 4. Remediation Task Idempotency (Step 8)

- **Existing Depend links on TC-8001**:
  - TC-8100 (upstream backport task -- Status: In Progress, Labels: ai-generated-jira, Security, CVE-2026-31812)
  - TC-8101 (downstream propagation task -- Status: Open, Labels: ai-generated-jira, Security, CVE-2026-31812)
- **Action**: SKIP -- Step 8 detects that remediation tasks TC-8100 and TC-8101 already exist via the Depend links on the issue. These tasks match the CVE-2026-31812 label and cover the 2.2.x stream. No new remediation tasks are created. Creating duplicate tasks would be harmful -- the existing tasks are already in progress.

## 5. Description Digest Comment Idempotency

- **Existing digest comment**: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2` (created 2026-07-01T10:00:00Z)
- **Action**: SKIP -- a description digest comment with the marker `[sdlc-workflow] Description digest:` already exists on the issue. No duplicate digest comment is posted.

## 6. Post-Triage Summary Comment Idempotency

- **Existing summary comment**: Found at 2026-07-01T10:01:00Z. Content includes version impact table, Affects Versions correction, and links to remediation tasks TC-8100 and TC-8101.
- **Action**: SKIP -- a post-triage summary comment already exists. No duplicate summary comment is posted.

## 7. Affects Versions Idempotency

- **Current Affects Versions**: RHTPA 2.2.0, RHTPA 2.2.1
- **Expected Affects Versions** (from version impact analysis): RHTPA 2.2.0, RHTPA 2.2.1
- **Action**: SKIP -- Affects Versions are already correct (corrected during the prior triage run). No update is needed.

## Summary

All triage artifacts are already present. The second run produces **no new mutations**:

| Artifact | Status | Action |
|----------|--------|--------|
| ai-cve-triaged label | Already present | Skipped |
| Issue status (In Progress) | Already transitioned | Skipped |
| Remediation task TC-8100 | Already linked via Depend | Skipped |
| Remediation task TC-8101 | Already linked via Depend | Skipped |
| Description digest comment | Already posted | Skipped |
| Post-triage summary comment | Already posted | Skipped |
| Affects Versions | Already correct | Skipped |
