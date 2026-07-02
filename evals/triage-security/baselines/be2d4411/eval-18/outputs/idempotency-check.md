# Idempotency Check -- Re-Run Analysis for TC-8001

This document records every pre-existing triage artifact detected during the
second run of triage-security on TC-8001, and explains why each was skipped.

## Summary

All triage artifacts from the first run are present and intact. The second run
detects each artifact and skips the corresponding mutation. Zero new Jira
mutations are produced.

---

## 1. Label: ai-cve-triaged

- **Check**: Issue labels include `ai-cve-triaged`.
- **Status**: ALREADY PRESENT
- **Action**: SKIP -- do not add the label again. The Post-Triage Summary
  (SKILL.md) adds `ai-cve-triaged` after triage completes. Since the label
  is already on the issue, re-adding it would be a no-op at best and could
  trigger unnecessary Jira webhooks. Skipped.

## 2. Status: In Progress

- **Check**: Current issue status is `In Progress`.
- **Status**: ALREADY TRANSITIONED
- **Action**: SKIP -- do not transition again. Step 0.7 transitions the issue
  from New to Assigned, and the Post-Triage Summary transitions to In Progress.
  Since the issue is already past both of those states, no status transition
  is needed. The status-aware handling (Inputs section) notes that issues in
  In Progress may be actively worked on and asks whether to proceed or skip.
  In an idempotent re-run, proceeding with analysis is valid, but no status
  mutation is emitted.

## 3. Remediation Task TC-8100 (upstream backport)

- **Check**: Issue links of type `Depend` include TC-8100.
- **Linked issue**: TC-8100 -- "Backport quinn-proto fix to >= 0.11.14 on
  release/0.4.z [rhtpa-2.2]"
- **Status**: In Progress
- **Labels**: ai-generated-jira, Security, CVE-2026-31812
- **Action**: SKIP -- do not create a duplicate upstream backport task. Step 8
  (Remediation Task Creation) checks for existing Depend-linked tasks before
  creating new ones. TC-8100 matches the expected upstream backport task for
  this CVE and stream. No new task is created.

## 4. Remediation Task TC-8101 (downstream propagation)

- **Check**: Issue links of type `Depend` include TC-8101.
- **Linked issue**: TC-8101 -- "Propagate quinn-proto bump to rhtpa-server
  release branch [rhtpa-2.2]"
- **Status**: Open
- **Labels**: ai-generated-jira, Security, CVE-2026-31812
- **Blocks**: TC-8100
- **Action**: SKIP -- do not create a duplicate downstream propagation task.
  TC-8101 matches the expected downstream propagation subtask for this CVE
  and stream (Cargo ecosystem produces two tasks: upstream + downstream).
  The Blocks relationship to TC-8100 is also already in place. No new task
  is created.

## 5. Description Digest Comment

- **Check**: Comments on TC-8001 include one matching the marker string
  `[sdlc-workflow] Description digest:`.
- **Found**: Comment #1 -- `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2`
  (posted 2026-07-01T10:00:00Z by sdlc-workflow/triage-security)
- **Action**: SKIP -- do not post a duplicate description digest comment.
  The Description Digest Protocol (shared/description-digest-protocol.md)
  states that consumers locate the most recent digest comment by the marker
  string. A second identical comment would be harmless but unnecessary and
  would clutter the comment history. The existing digest is valid and
  sufficient.

## 6. Post-Triage Summary Comment

- **Check**: Comments on TC-8001 include a post-triage summary documenting
  version impact, Affects Versions correction, remediation tasks, and status
  transition.
- **Found**: Comment #2 -- Post-triage summary with:
  - Version impact: RHTPA 2.2.0 and 2.2.1 affected, 2.2.2+ not affected
  - Actions taken: Affects Versions corrected, ai-cve-triaged label added,
    remediation tasks TC-8100 and TC-8101 created, transitioned to In Progress
  - Comment Footnote: sdlc-workflow/triage-security v0.11.1
  - Posted 2026-07-01T10:01:00Z by sdlc-workflow/triage-security
- **Action**: SKIP -- do not post a duplicate post-triage summary comment.
  The existing summary is complete and accurate. Posting a second summary
  would create confusion about which is authoritative and clutter the audit
  trail.

## 7. Affects Versions

- **Check**: Current Affects Versions on TC-8001 are RHTPA 2.2.0, RHTPA 2.2.1.
- **Expected**: Based on version impact analysis (2.2.0 and 2.2.1 ship
  quinn-proto < 0.11.14; 2.2.2+ ship 0.11.14), the correct Affects Versions
  for the 2.2.x stream scope are RHTPA 2.2.0 and RHTPA 2.2.1.
- **Action**: SKIP -- Affects Versions are already correct. Step 3 (Affects
  Versions Correction) compares the current values against the version impact
  table and finds no diff. No correction needed.

---

## Artifact Inventory

| # | Artifact | Expected | Found | Action |
|---|----------|----------|-------|--------|
| 1 | ai-cve-triaged label | Present | Present | SKIP |
| 2 | Status In Progress | In Progress or later | In Progress | SKIP |
| 3 | Remediation task (upstream) | Depend link to upstream backport task | TC-8100 via Depend | SKIP |
| 4 | Remediation task (downstream) | Depend link to downstream propagation task | TC-8101 via Depend | SKIP |
| 5 | Description digest comment | Marker comment with sha256 digest | sha256-md:a1b2...a1b2 | SKIP |
| 6 | Post-triage summary comment | Summary with version impact + actions | Present with full audit trail | SKIP |
| 7 | Affects Versions | RHTPA 2.2.0, RHTPA 2.2.1 | RHTPA 2.2.0, RHTPA 2.2.1 | SKIP |

**Total mutations in second run: 0**
