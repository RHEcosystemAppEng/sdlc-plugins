# Triage Outcome: TC-8010 (CVE-2026-44492, axios SSRF, [rhtpa-2.2])

## Decision

**Covered by existing cross-CVE remediation. Do not create new remediation tasks. Recommend closing TC-8010 as covered by TC-8009.**

Remediation task TC-8009, which belongs to CVE-2026-42035 / TC-8008 (same upstream component `axios`, same PS Component `pscomponent:org/rhtpa-ui`, same stream `rhtpa-2.2`), bumps axios from 1.7.4 to **1.9.0**. That meets or exceeds this CVE's fix threshold of **1.8.2**, so the same change fixes both CVEs.

## Rationale by step

| Step | Result |
|---|---|
| 0 Config | Required sections are present. Upstream Affected Component, PS Component, and Stream fields are **not declared** in Security Configuration; the task supplied them (see deviation note). |
| 0.3 Staleness | Matrix is 148 days old (> 14). Recorded as "Proceed anyway". |
| 0.6 Mode | Interactive (`FULLSEND_OUTPUT_DIR` absent). |
| 0.8 Assign | Proposed: assign to current user and transition New to Assigned. |
| 1 Extraction | CVE-2026-44492, axios, < 1.8.2, fixed 1.8.2, CVSS 8.1, scoped to stream 2.2.x. |
| 1.5 Enrichment | External APIs not queried (eval constraint). Jira description threshold 1.8.2 used with reduced confidence. |
| 1.7 Embargo | Skipped because no embargo URL is configured. |
| 2 Version impact | **Not determinable from evidence.** npm and `rhtpa-ui` are absent from the 2.2.x Ecosystem Mappings, and the mock lock data has no axios entries. Versions were not invented. The TC-8009 description (bump *from* 1.7.4) indicates 2.2.x is likely affected. |
| 3 Affects Versions | No correction proposed: without lock-file evidence there is no basis to change PSIRT's `RHTPA 2.2.0`. |
| 4 / 4.1 / 4.2 | No same-CVE siblings. |
| **4.3 Cross-CVE overlap** | **TC-8008 matches. Its Depend task TC-8009 bumps to 1.9.0 >= 1.8.2, so this CVE is covered.** |
| 4.4 Preemptive | None found. |
| 5 Lifecycle | Not evaluated (no external fetch). Not needed for this decision. |
| 6 Already fixed | No resolved same-CVE siblings. |
| 7 Concurrent triage | TC-8008 (axios, In Progress) would match the concurrent-triage query. This is expected: it is the same covering CVE found in 4.3, so the overlap is already handled and no duplicate tasks will be created. |
| 7.5 Release Jira | Not needed for new tasks. The engineer may optionally link TC-8010 (Related) to the RHTPA 2.2.x release Task that TC-8009 already blocks. |
| 8 Remediation | **No new tasks.** The Step 4.3 covering remediation means Case A/B task creation is skipped. This is not Case C: the product is likely affected, but the fix is already in flight. |

## Proposed Jira mutations (each needs engineer confirmation; none executed)

1. Assign TC-8010 to the current user and transition New to Assigned (Step 0.8).
2. Link TC-8010 to TC-8008 with **Related**.
3. Link TC-8010 to TC-8009 with **Depend**.
4. Comment the cross-CVE overlap finding on TC-8010, with Comment Footnote and no ProdSec @mention (not configured).
5. Close TC-8010 as covered by TC-8009 (recommendation). Do **not** set VEX Justification, because the product is not "not affected"; the fix comes from another CVE's remediation.
6. Add label `ai-cve-triaged` to TC-8010.
7. Post the post-triage summary comment covering: version impact (undetermined, with reason), no Affects Versions change, outcome (covered by TC-8009), Related/Depend links, no new tasks, the dedup/overlap result, an @mention of the issue reporter (PSIRT analyst; the mock data has no account ID, so it is resolved from the live issue), and the Comment Footnote.

## Caveats for the engineer

- **TC-8009 is still In Progress.** CVE-2026-44492 is fixed only once TC-8009 merges and ships. An alternative to closing now is to keep TC-8010 open with the Depend link and let it move to ON_QA through discovery mode's "Ready for QA" check when TC-8009 is Done. Either way, no new remediation task is needed.
- When TC-8009 lands, check that the resolved axios version in rhtpa-ui's lock file (package-lock.json) is >= 1.8.2. A caret range can resolve differently than the stated 1.9.0.
- **Configuration gaps to fix:** add the Upstream Affected Component (`customfield_10632`), PS Component (`customfield_10669`), and Stream (`customfield_10832`) fields to Security Configuration. Add an npm / `rhtpa-ui` row to the 2.2.x Ecosystem Mappings and to Source Repositories so future axios CVEs get full lock-file impact analysis. Refresh the stale security matrix.
- The due date 2026-08-01 has already passed.
