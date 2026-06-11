# Step 4 -- Duplicate and Sibling Check

## JQL Search

Simulated JQL query:
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8003
```

### Search Results

One sibling issue found:

| Field | Value |
|-------|-------|
| Issue key | TC-7999 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Status | In Progress |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server |
| Affects Versions | RHTPA 2.2.0, RHTPA 2.2.1 |
| Stream suffix | [rhtpa-2.2] |

## Sibling Classification

### Current issue: TC-8003
- Stream suffix: `[rhtpa-2.2]` -> stream 2.2.x
- Status: New
- Affects Versions: RHTPA 2.2.0

### Sibling issue: TC-7999
- Stream suffix: `[rhtpa-2.2]` -> stream 2.2.x
- Status: In Progress
- Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1

### Classification: SAME-STREAM DUPLICATE

Both TC-8003 and TC-7999 share:
- Same CVE: CVE-2026-31812
- Same stream suffix: [rhtpa-2.2] (both map to stream 2.2.x)
- Same component: pscomponent:org/rhtpa-server
- Same vulnerability: quinn-proto panic on large stream counts

TC-7999 is already **In Progress**, meaning it has been triaged and work has begun. TC-7999 also has more complete Affects Versions (RHTPA 2.2.0 and RHTPA 2.2.1) compared to TC-8003 which only has RHTPA 2.2.0.

## Step 4.1 -- Same-Stream Duplicate Resolution

Per the triage-security methodology (Section 4.1 of jira-triage-operations.md):

> If a same-stream sibling exists and is open or in progress:
> - **Recommendation**: Close the current issue as Duplicate.

TC-7999 is the existing tracker for CVE-2026-31812 on the 2.2.x stream and is already In Progress. TC-8003 is a duplicate that should be closed.

### Recommendation: Close TC-8003 as Duplicate of TC-7999

**Rationale:**
1. TC-7999 and TC-8003 track the identical CVE (CVE-2026-31812) for the identical stream ([rhtpa-2.2] / 2.2.x).
2. TC-7999 is already In Progress -- work is actively underway.
3. TC-7999 has more complete Affects Versions (includes both RHTPA 2.2.0 and RHTPA 2.2.1), whereas TC-8003 only lists RHTPA 2.2.0.
4. Keeping both issues open would create confusion and duplicate work tracking.

### Proposed Jira Actions (require engineer confirmation)

1. **Add comment to TC-8003:**
   > Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same stream [rhtpa-2.2]. TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1]. Version impact analysis confirms overlap: quinn-proto versions 0.11.9 (2.2.0) and 0.11.12 (2.2.1) are both vulnerable (< 0.11.14). The fix is already shipped in versions 2.2.3+ (quinn-proto 0.11.14).

2. **Transition TC-8003** to Closed with resolution "Duplicate".

3. **Assign TC-8003** to current user.

4. **Add `ai-cve-triaged` label** to TC-8003.

Note: Steps 5 (Version Lifecycle Check), 6 (Already Fixed Check), and 7 (Remediation) are **skipped** because the issue is being closed as a duplicate. The active tracker TC-7999 is responsible for those steps.
