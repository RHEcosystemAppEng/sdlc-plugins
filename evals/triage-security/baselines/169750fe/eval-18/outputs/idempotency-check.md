# Idempotency Check -- Re-Run Triage of TC-8001

This document analyzes all pre-existing triage artifacts detected on issue TC-8001
and explains why each mutation is skipped on a second triage run.

## Summary

All triage artifacts from the prior run are intact. The re-run detects every
artifact and skips all corresponding mutations. Zero new Jira writes are produced.

---

## 1. Label: ai-cve-triaged

- **Status**: ALREADY PRESENT
- **Evidence**: The issue's labels array contains `ai-cve-triaged` (visible in the issue metadata alongside `CVE-2026-31812` and `pscomponent:org/rhtpa-server`).
- **Action**: SKIP -- do not add the label again. The `edit_issue` call to append `ai-cve-triaged` is suppressed because the label is already in the labels list.
- **Skill reference**: Post-Triage Summary, step 1 ("Add the `ai-cve-triaged` label ... prevents re-triaging the same issue").

## 2. Status: In Progress

- **Status**: ALREADY IN TARGET STATE
- **Evidence**: The issue's current status is "In Progress". The triage workflow would transition from New to Assigned (Step 0.8) and later to In Progress. Since the status is already at or beyond the target state, no transition is needed.
- **Action**: SKIP -- do not call `transition_issue`. The issue has already passed through the Assigned and In Progress transitions in the prior run.
- **Skill reference**: Step 0.8 ("If the issue is already in Assigned or any later status ... skip the transition silently").

## 3. Remediation Task TC-8100 (upstream backport)

- **Status**: ALREADY EXISTS via Depend link
- **Evidence**: The issue's `issuelinks` array contains a Depend link to TC-8100 with summary "Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2]". TC-8100 has status In Progress and labels `ai-generated-jira, Security, CVE-2026-31812`.
- **Action**: SKIP -- do not create a new upstream backport task. The existing Depend link proves TC-8100 was created by the prior triage run and is already linked to this Vulnerability issue.
- **Skill reference**: Step 8, Case B ("Check dedup status ... skip task creation for that stream") and the general idempotency principle of checking existing issuelinks before creating remediation tasks.

## 4. Remediation Task TC-8101 (downstream propagation)

- **Status**: ALREADY EXISTS via Depend link
- **Evidence**: The issue's `issuelinks` array contains a Depend link to TC-8101 with summary "Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2]". TC-8101 has status Open, labels `ai-generated-jira, Security, CVE-2026-31812`, and a Blocks relationship to TC-8100.
- **Action**: SKIP -- do not create a new downstream propagation task. The existing Depend link proves TC-8101 was created by the prior triage run and is already linked to this Vulnerability issue. The Blocks relationship between TC-8101 and TC-8100 is also intact.
- **Skill reference**: Same as above -- existing Depend links indicate remediation tasks are already in place.

## 5. Description Digest Comment

- **Status**: ALREADY EXISTS
- **Evidence**: Comment #1 on the issue is a description digest comment with marker `sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2`, posted by `sdlc-workflow/triage-security` at 2026-07-01T10:00:00Z.
- **Action**: SKIP -- do not post a duplicate digest comment. The description digest protocol requires checking for an existing digest comment before posting; one already exists.
- **Skill reference**: `shared/description-digest-protocol.md` -- digest comments are idempotent; only one should exist per issue.

## 6. Post-Triage Summary Comment

- **Status**: ALREADY EXISTS
- **Evidence**: Comment #2 on the issue is a post-triage summary comment posted by `sdlc-workflow/triage-security` at 2026-07-01T10:01:00Z. It documents: version impact (RHTPA 2.2.0 and 2.2.1 affected, 2.2.2+ not affected), Affects Versions correction, ai-cve-triaged label addition, remediation task creation (TC-8100 upstream backport, TC-8101 downstream propagation), and transition to In Progress.
- **Action**: SKIP -- do not post a duplicate summary comment. The existing summary comment provides a complete audit trail from the first triage run.
- **Skill reference**: Post-Triage Summary, step 2 -- the summary comment is posted once after all triage actions are complete; a re-run that performs no new actions should not post a second summary.

## 7. Affects Versions

- **Status**: ALREADY CORRECT
- **Evidence**: The issue's Affects Versions field contains `RHTPA 2.2.0, RHTPA 2.2.1`. The version impact analysis confirms these are the correct affected versions within the 2.2.x stream scope (versions 2.2.0 and 2.2.1 ship quinn-proto < 0.11.14; versions 2.2.2+ ship quinn-proto >= 0.11.14). The prior run already corrected Affects Versions to this value.
- **Action**: SKIP -- no correction needed. Current Affects Versions match the lock-file-derived version impact table.
- **Skill reference**: Step 3.2 ("If Affects Versions are already correct: note this and proceed without changes").

## 8. Assignee

- **Status**: ALREADY ASSIGNED
- **Evidence**: The issue's Assignee is `engineer-a@example.com`. The issue is already assigned from the prior triage run.
- **Action**: SKIP -- assignment is already in place. In a real re-run, Step 0.8 might re-assign to the current user, but since the issue is already assigned and in a post-Assigned status, no functional change is needed.

---

## Artifact Detection Summary Table

| # | Artifact | Detection Method | Found? | Action |
|---|----------|-----------------|--------|--------|
| 1 | ai-cve-triaged label | Check issue labels array | Yes | Skip label add |
| 2 | In Progress status | Check issue status field | Yes | Skip transition |
| 3 | TC-8100 (upstream backport) | Check issuelinks for Depend to remediation Task | Yes | Skip task creation |
| 4 | TC-8101 (downstream propagation) | Check issuelinks for Depend to remediation Task | Yes | Skip task creation |
| 5 | Description digest comment | Check comments for digest marker pattern | Yes | Skip comment post |
| 6 | Post-triage summary comment | Check comments for summary by sdlc-workflow/triage-security | Yes | Skip comment post |
| 7 | Affects Versions | Compare current versions to version impact table | Correct | Skip correction |
| 8 | Assignee | Check assignee field | Present | Skip assignment |
