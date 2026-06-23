# Triage Outcome — TC-8003

## Decision: Close as Duplicate

TC-8003 should be **closed as Duplicate** of TC-7999.

### Rationale

TC-8003 (CVE-2026-31812, quinn-proto panic on large stream counts, stream [rhtpa-2.2]) is a same-stream duplicate of TC-7999. Both issues track the same CVE for the same version stream (2.2.x), and TC-7999 is already In Progress with broader Affects Versions coverage.

### Evidence

| Criterion | TC-7999 (primary) | TC-8003 (duplicate) |
|-----------|--------------------|--------------------|
| CVE | CVE-2026-31812 | CVE-2026-31812 |
| Stream suffix | [rhtpa-2.2] | [rhtpa-2.2] |
| Component label | pscomponent:org/rhtpa-server | pscomponent:org/rhtpa-server |
| Status | In Progress | New |
| Affects Versions | RHTPA 2.2.0, RHTPA 2.2.1 | RHTPA 2.2.0 |

TC-7999 is the primary tracker because:
1. It was filed first (TC-7999 < TC-8003 by issue key sequence)
2. It is already In Progress (active remediation underway)
3. It has more complete Affects Versions (includes RHTPA 2.2.1 which TC-8003 is missing)

### Version Impact Summary

For the 2.2.x stream (both issues' scope):

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | — | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | fixed version |
| 2.2.4 | 0.11.14 | NO | fixed version |

The fix was introduced in version 2.2.3 (build tag v0.4.11), which bumped quinn-proto to 0.11.14. Versions 2.2.0 through 2.2.2 ship vulnerable versions (0.11.9 and 0.11.12).

### Cross-Stream Note

The 2.1.x stream is also affected (all versions ship quinn-proto 0.11.9), but this is outside TC-8003's scope. Cross-stream tracking is managed by PSIRT via separate Vulnerability issues per stream.

### Proposed Jira Actions

The following Jira mutations would be performed (with engineer confirmation):

1. **Add comment to TC-8003**:
   > Duplicate of TC-7999 — same CVE (CVE-2026-31812) tracked for the same stream [rhtpa-2.2]. TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1]. Version impact analysis confirms complete overlap.
   >
   > Version impact for the 2.2.x stream: 2.2.0 (quinn-proto 0.11.9, affected), 2.2.1 (0.11.12, affected), 2.2.2 (retag of 2.2.1, affected), 2.2.3 (0.11.14, not affected), 2.2.4 (0.11.14, not affected).

2. **Transition TC-8003** to Closed with resolution "Duplicate".

3. **Assign TC-8003** to current user.

4. **Add label** `ai-cve-triaged` to TC-8003.

### Steps Skipped

- **Step 3 (Affects Versions Correction)**: Not needed — the issue is being closed as duplicate. TC-7999 already has the correct Affects Versions.
- **Step 4.3 (Cross-CVE Overlap)**: Skipped — Upstream Affected Component, PS Component, and Stream custom fields are not configured in Security Configuration.
- **Step 5 (Version Lifecycle Check)**: Not needed — the issue is being closed as duplicate before reaching lifecycle evaluation.
- **Step 6 (Already Fixed Check)**: Not needed — duplicate closure takes precedence.
- **Step 7 (Remediation)**: Not needed — no remediation tasks are created for duplicates. TC-7999 owns remediation for this CVE in the 2.2.x stream.
