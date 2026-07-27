# Triage Outcome: TC-8003

## Decision: Close as Duplicate

TC-8003 should be **closed as a Duplicate** of **TC-7999**.

## Rationale

### Same CVE, Same Stream

TC-8003 and TC-7999 both track CVE-2026-31812 (quinn-proto panic on large stream counts) for the same product stream `[rhtpa-2.2]` (version stream 2.2.x). PSIRT created two Vulnerability issues for the same CVE and stream, which is a duplication. TC-7999 is already **In Progress**, meaning an engineer is actively working on triage or remediation for this vulnerability.

### Version Impact Summary

The version impact analysis confirms that the following versions in the 2.2.x stream are affected:

| Version | quinn-proto | Vulnerable? |
|---------|-------------|-------------|
| RHTPA 2.2.0 | 0.11.9 | YES |
| RHTPA 2.2.1 | 0.11.12 | YES |
| RHTPA 2.2.2 | 0.11.12 (retag of 2.2.1) | YES |
| RHTPA 2.2.3 | 0.11.14 | NO (fixed) |
| RHTPA 2.2.4 | 0.11.14 | NO (fixed) |

The fix threshold is quinn-proto >= 0.11.14. Versions 2.2.0 through 2.2.2 ship vulnerable versions; versions 2.2.3 and 2.2.4 ship the fixed version.

This impact applies equally to both TC-8003 and TC-7999 since they cover the same stream. TC-7999 (already In Progress) is the correct issue to carry this analysis forward.

### Workflow Steps Applied

| Step | Action | Result |
|------|--------|--------|
| 0 | Validate Configuration | Passed -- all required Security Configuration sections present |
| 0.3 | Matrix Staleness Check | Matrix last updated 2026-06-28 (29 days ago) -- stale but proceeding |
| 1 | Data Extraction | CVE-2026-31812, quinn-proto < 0.11.14, stream 2.2.x, Cargo ecosystem |
| 2 | Version Impact Analysis | RHTPA 2.2.0/2.2.1/2.2.2 affected; 2.2.3/2.2.4 not affected |
| 3 | Affects Versions Correction | Skipped -- issue is duplicate; correction belongs on TC-7999 |
| 4 | Duplicate Check | **TC-7999 is a same-stream duplicate (In Progress)** |
| 5-8 | Remaining steps | Skipped -- issue closed as duplicate before these steps |

### Proposed Jira Actions

1. **Add comment to TC-8003**: "Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same stream [rhtpa-2.2]. Version impact analysis confirms overlap. TC-7999 is already In Progress."
2. **Transition TC-8003** to Closed with resolution "Duplicate".
3. **Assign TC-8003** to the current user.
4. **Add `ai-cve-triaged` label** to TC-8003 to mark it as processed.

### Follow-Up Recommendation for TC-7999

TC-7999 currently has Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1]. The version impact analysis shows RHTPA 2.2.2 is also affected (it is a retag of 2.2.1 with the same vulnerable quinn-proto 0.11.12). Consider updating TC-7999's Affects Versions to include RHTPA 2.2.2 for completeness.
