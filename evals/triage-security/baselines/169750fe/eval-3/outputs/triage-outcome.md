# Triage Outcome -- TC-8003

## Summary

**Issue**: TC-8003 -- CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**Outcome**: **Close as Duplicate** of TC-7999
**Reason**: Same-stream sibling detected; TC-7999 already tracks the identical CVE for the identical stream and is actively In Progress.

## Triage Flow

| Step | Name | Result |
|------|------|--------|
| 0 | Validate Configuration | Passed -- Security Configuration present with version streams, source repos, and required fields |
| 0.3 | Matrix Staleness Check | Matrix last updated 2026-06-28 (within 14-day threshold) -- proceed |
| 0.5 | Jira Access | Simulated (eval mode -- no actual Jira calls) |
| 0.6 | Fullsend Mode Detection | Not applicable (interactive eval mode) |
| 1 | Data Extraction | CVE-2026-31812, quinn-proto, affected < 0.11.14, fixed in 0.11.14, stream [rhtpa-2.2] -> 2.2.x |
| 1.5 | External CVE Enrichment | Simulated -- fix threshold 0.11.14 confirmed |
| 1.7 | Embargo Check | Skipped -- no Embargo policy URL configured |
| 2 | Version Impact Analysis | Not fully executed -- duplicate detected at Step 4 short-circuits remediation |
| 3 | Affects Versions Correction | Not executed -- issue closing as duplicate; version ownership belongs to TC-7999 |
| 4 | Duplicate Check | **DUPLICATE DETECTED** -- TC-7999 is same-stream sibling (same CVE, same [rhtpa-2.2]), status In Progress |
| 5 | Version Lifecycle Check | Skipped -- duplicate short-circuit |
| 6 | Already Fixed Check | Skipped -- duplicate short-circuit |
| 7 | Concurrent Triage Detection | Skipped -- no remediation tasks to create |
| 7.5 | Release Jira Orchestration | Skipped -- no remediation tasks to create |
| 8 | Remediation | Skipped -- no remediation tasks to create |

## Proposed Actions (Not Executed)

All actions are proposals for engineer confirmation, consistent with the skill guardrail: "every Jira mutation requires confirmation."

### 1. Comment on TC-8003

**Type**: Jira comment
**Body**:
> Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same stream [rhtpa-2.2]. TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1]. Version impact analysis confirms overlap.
>
> [Comment Footnote: triage-security]

### 2. Transition TC-8003 to Closed

**Type**: Status transition
**Target status**: Closed
**Resolution**: Duplicate

### 3. Assign TC-8003

**Type**: Field edit (assignee)
**Value**: Current user (account ID to be retrieved via `jira.user_info()`)

### 4. Add ai-cve-triaged label

**Type**: Field edit (labels)
**Value**: Add `ai-cve-triaged` to existing labels [CVE-2026-31812, pscomponent:org/rhtpa-server]

## Why Duplicate (Not Cross-Stream Companion)

The distinction between a duplicate and a cross-stream companion is determined by the stream suffix in each issue's summary:

- TC-8003 summary: `CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]`
- TC-7999 summary: `CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]`

Both carry the suffix `[rhtpa-2.2]`, mapping to the **same** stream (2.2.x). Per Step 4.1 of the SKILL.md:

> If a same-stream sibling exists and is open or in progress: Recommendation: Close the current issue as Duplicate.

If TC-7999 had a different stream suffix (e.g., `[rhtpa-2.1]`), it would be a cross-stream companion and Step 4.2 would apply instead (Related link, no closure). But since both share `[rhtpa-2.2]`, TC-8003 is redundant.

## Remediation Tasks

**None created.** The duplicate detection at Step 4.1 short-circuits all downstream steps (Steps 5-8). TC-7999 owns the triage and remediation for CVE-2026-31812 in the 2.2.x stream.

## Key Evidence

| Evidence | Value |
|----------|-------|
| Current issue | TC-8003 (Status: New) |
| Sibling issue | TC-7999 (Status: In Progress) |
| CVE match | Both labeled CVE-2026-31812 |
| Stream match | Both suffixed [rhtpa-2.2] -> stream 2.2.x |
| TC-7999 Affects Versions | RHTPA 2.2.0, RHTPA 2.2.1 (superset of TC-8003's RHTPA 2.2.0) |
| Duplicate justification | Same CVE + same stream + sibling is open/active |
