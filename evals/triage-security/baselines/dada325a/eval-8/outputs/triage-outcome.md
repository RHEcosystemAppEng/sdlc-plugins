# Triage Outcome: TC-8010 (CVE-2026-44492, axios SSRF, [rhtpa-2.2])

## Decision

**Covered by existing cross-CVE remediation. No new remediation tasks will be created.**

Existing task **TC-8009** (linked from CVE-2026-42035 / **TC-8008**) bumps axios in rhtpa-ui on the 2.2.x stream from 1.7.4 to **1.9.0**. This CVE's fix threshold is **1.8.2**. Because 1.9.0 >= 1.8.2, TC-8009 already fixes CVE-2026-44492. Creating another bump task would duplicate work on the same component, stream, and lock file.

## Rationale

1. **Scope**: the `[rhtpa-2.2]` suffix scopes the issue to stream 2.2.x.
2. **No same-CVE siblings** (Step 4.1/4.2), so there is no duplicate closure.
3. **Cross-CVE overlap** (Step 4.3): TC-8008 shares Upstream Affected Component (axios), PS Component (`pscomponent:org/rhtpa-ui`), and Stream (rhtpa-2.2) with this issue. Its Depend-linked remediation task TC-8009 targets axios 1.9.0, which is at or above 1.8.2.
4. **Exposure confirmed**: TC-8009 says rhtpa-ui currently ships axios 1.7.4, which is inside this CVE's affected range (< 1.8.2). The issue is genuinely affected, so Case C (Not a Bug) does not apply.
5. **Step 7.5.3 dedup agrees**: an existing remediation task already covers the same Upstream Affected Component in the same stream. The stream is marked dedup'd, so Case B creates no tasks for 2.2.x and only links to the existing task.

## Proposed Jira Actions (each requires engineer confirmation; none were executed)

| # | Action | Detail |
|---|--------|--------|
| 1 | Assign + transition (Step 0.8) | Assign TC-8010 to the current user and move it from New to Assigned |
| 2 | Link | TC-8010 **Related** TC-8008 (same upstream component) |
| 3 | Link | TC-8010 **Depend** TC-8009 (covering remediation) |
| 4 | Comment | Cross-CVE overlap comment (text in `overlap-check.md`), with Comment Footnote |
| 5 | Affects Versions (Step 3) | Keep RHTPA 2.2.0 for now. It cannot be verified or expanded to 2.2.1–2.2.4 without npm lock-file evidence (see caveats) |
| 6 | Label | Add `ai-cve-triaged` |
| 7 | Summary comment | Post-triage summary covering scope, overlap finding, links, no new tasks (dedup result), @mention of the reporter, and Comment Footnote |
| 8 | Release Jira (Step 7.5) | Link TC-8010 **Related** to the RHTPA 2.2.x "CVE triage" release Task if one exists (TC-8009 should already Block it) |

## Closure Recommendation

Following Step 4.3, the recommendation is to **close TC-8010 because the fix is already covered by TC-8009**. TC-8009 is still **In Progress**, though, so the fix has not shipped. The safer choice, for the engineer to confirm, is:

- **Preferred**: keep TC-8010 open, tracked through the Depend link to TC-8009. When TC-8009 (and its downstream propagation) is Done, TC-8010 will appear in the "Ready for QA" discovery list and can move to ON_QA or Closed with the fix.
- **Alternative**: close now with a comment pointing to TC-8009. Do **not** use "Not a Bug" or a VEX justification. The product *is* affected; it is simply fixed by another CVE's remediation.

## Caveats / Items Needing Engineer Attention

1. **npm is not mapped in the 2.2.x security-matrix Ecosystem Mappings** (only Cargo and RPM), and `rhtpa-ui` is not in Source Repositories. Step 2 version impact for axios across 2.2.0–2.2.4 could not be computed from lock files, and no axios versions were invented. Exposure comes only from TC-8009's description (1.7.4). Add the npm/rhtpa-ui mapping and confirm per-version impact before finalizing Affects Versions.
2. **Matrix is stale**: last updated 2026-06-28, 131 days ago, past the 14-day limit. Refresh is recommended.
3. **Step 4.3 field configuration**: the Upstream Affected Component, PS Component, and Stream custom fields (customfield_10632 / 10669 / 10832) are not declared in the mock Security Configuration. They should be added so overlap detection runs automatically.
4. **External enrichment skipped** (no MITRE/OSV calls), so the 1.8.2 threshold comes from the Jira description only. 1.9.0 is comfortably above it, so the conclusion is robust to small threshold differences.
5. **Due date 2026-08-01 has passed**. Delivery depends on TC-8009 completing.
6. Cross-stream (Case A): the 2.1.x stream (rhtpa-release.0.3.z) also has no npm mapping, so its axios exposure is unknown and cannot be checked here.
