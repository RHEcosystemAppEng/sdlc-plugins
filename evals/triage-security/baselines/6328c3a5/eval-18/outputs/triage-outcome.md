# Triage Outcome -- Why the Second Run Produces No New Mutations

## Context

TC-8001 (CVE-2026-31812, quinn-proto panic on large stream counts) was fully triaged
in a prior run. All triage artifacts -- label, status transition, Affects Versions
correction, remediation task creation, issue links, description digest, and post-triage
summary -- were applied during the first run. This document explains why a re-run of
`/sdlc-workflow:triage-security TC-8001` produces zero new Jira mutations.

## Idempotency Principle

The triage-security skill is designed to be idempotent: re-running triage on the same
issue should detect all previously applied artifacts and skip their corresponding
mutations. Each step checks for the existence of its expected output before acting:

1. **Label check**: Step "Post-Triage Summary" checks whether `ai-cve-triaged` is
   already in the issue's labels before adding it.
2. **Status check**: Step 0.8 checks the current status. If the issue is already in
   Assigned or any later status (In Progress, Code Review, QA, etc.), the transition
   is skipped silently.
3. **Link check**: Steps 4.2, 4.3, and the Jira Linkage procedure check the issue's
   existing `issuelinks` array before creating any new links. If a link of the same
   type to the same target already exists, creation is skipped.
4. **Remediation task check**: The skill inspects existing Depend-linked Tasks on the
   CVE issue. When remediation tasks matching the expected pattern (same CVE, same
   stream, same library) are already linked, Step 8 skips task creation.
5. **Comment check**: The description-digest-protocol requires checking for an existing
   digest comment before posting. The post-triage summary is similarly checked to
   avoid duplicate audit trail entries.
6. **Affects Versions check**: Step 3.2 compares the current Affects Versions against
   the expected values from the version impact table. When they already match, no
   correction is issued.

## Step-by-Step Analysis of the Re-run

| Step | Action | First Run Result | Re-run Result |
|------|--------|-----------------|---------------|
| 0 | Validate Configuration | Configuration validated | Configuration validated (read-only, same result) |
| 0.3 | Matrix Staleness Check | Matrix is current | Matrix is current (read-only, same result) |
| 0.5 | Jira Access | Connected | Connected (read-only, same result) |
| 0.8 | Assign and Transition | Assigned and transitioned to Assigned | SKIPPED -- already In Progress (past Assigned) |
| 1 | Data Extraction | Extracted CVE data | Same extraction (read-only, same result) |
| 1.5 | External CVE Enrichment | Enriched fix threshold | Same enrichment (read-only, same result) |
| 1.7 | Embargo Check | Passed (or skipped if no policy URL) | Same result (read-only) |
| 2 | Version Impact Analysis | Built impact table | Same table (read-only, same result) |
| 3 | Affects Versions Correction | Corrected to RHTPA 2.2.0, 2.2.1 | SKIPPED -- already correct |
| 4 | Duplicate/Sibling Check | Checked, no duplicates | Same result (read-only) |
| 5 | Lifecycle Check | Versions within support | Same result (read-only) |
| 6 | Already Fixed Check | No resolved siblings | Same result (read-only) |
| 7 | Concurrent Triage Detection | No concurrent triages (or already past) | Same result (read-only) |
| 7.5 | Release Jira Orchestration | Handled (if applicable) | Same result |
| 8 | Remediation | Created TC-8100, TC-8101 | SKIPPED -- both tasks already exist and are linked |
| Post | Add `ai-cve-triaged` label | Added | SKIPPED -- label already present |
| Post | Post summary comment | Posted | SKIPPED -- summary comment already exists |
| Post | Transition to In Progress | Transitioned | SKIPPED -- already In Progress |

## Why Zero Mutations

Every mutation the skill would perform on a fresh issue has an idempotency guard:

1. **Remediation tasks TC-8100 and TC-8101 already exist** and are linked to TC-8001
   via Depend links. The skill detects these existing tasks by inspecting the issue's
   `issuelinks` array and matching them against the expected remediation pattern for
   CVE-2026-31812 on stream rhtpa-2.2 (Cargo ecosystem, source dependency). Since both
   the upstream backport task and downstream propagation task exist, Step 8 Case B
   creates nothing new.

2. **The `ai-cve-triaged` label is already present**, so the post-triage label addition
   is a no-op.

3. **The status is already In Progress**, which is past both Assigned (Step 0.8) and
   the post-triage In Progress transition. Both transitions are skipped.

4. **Affects Versions are already correct** (RHTPA 2.2.0 and RHTPA 2.2.1), matching
   the version impact analysis for the 2.2.x stream scope. No field edit is needed.

5. **The description digest comment already exists** with a valid digest hash. The
   description-digest-protocol's existence check prevents a duplicate.

6. **The post-triage summary comment already exists** with full audit trail. No
   duplicate summary is posted.

7. **All issue links already exist** (Depend to TC-8100, Depend to TC-8101, Blocks
   from TC-8100 to TC-8101). The link creation guards in Steps 4.2, 8, and the Jira
   Linkage procedure detect existing links and skip.

## Conclusion

The second run of triage-security on TC-8001 completes all read-only analysis steps
(data extraction, version impact analysis, duplicate checks, lifecycle checks) but
produces **zero new Jira mutations**. Every write operation is guarded by an
idempotency check that detects the corresponding artifact from the first run. This
behavior is by design: the skill is safe to re-run on already-triaged issues without
creating duplicate tasks, comments, links, or field changes.
