# Triage Outcome: TC-8010 (CVE-2026-44492, axios SSRF, [rhtpa-2.2])

## Decision

**No new remediation task. Recommend closing TC-8010 because the fix is covered by
existing remediation task TC-8009.**

TC-8009 is linked by Depend from related CVE TC-8008 (CVE-2026-42035). It is the same
upstream component (axios), the same PS Component (pscomponent:org/rhtpa-ui), and the
same stream (rhtpa-2.2). It bumps axios 1.7.4 -> **1.9.0**, which is at or above this
CVE's fix threshold of **1.8.2**. When TC-8009 lands, it also remediates CVE-2026-44492
in stream 2.2.x.

## Rationale by step

| Step | Result |
|---|---|
| 0 Config | Valid. Overlap field IDs come from the task context and are missing from the mock CLAUDE.md, so add them to Security Configuration. |
| 0.3 Staleness | Matrix is 151 days old (2026-06-28). Warned and proceeded. |
| 0.8 Assign | Propose assigning to the current user and transitioning New -> Assigned. |
| 1 Extraction | CVE-2026-44492, axios < 1.8.2, fixed in 1.8.2, CVSS 8.1, scoped to 2.2.x. |
| 1.5 Enrichment | External calls not allowed, so Jira description data was used (reduced confidence). |
| 1.7 Embargo | Skipped because no embargo URL is configured. |
| 2 Version impact | axios is npm. npm is not in the matrix Ecosystem Mappings and there is no axios lock data, so no lock-file versions were derived (none fabricated). The description and the TC-8009 description ("from 1.7.4") point to 2.2.x shipping a vulnerable axios, so the issue is treated as affected and pending coverage. |
| 3 Affects Versions | Not changed. Without npm lock-file evidence across 2.2.0–2.2.4, it is not possible to confirm which 2.2.x releases ship axios < 1.8.2. Flagged for manual verification and not corrected blindly. |
| 4.1/4.2 Siblings | None. |
| **4.3 Cross-CVE overlap** | **TC-8008 -> Depend -> TC-8009 bumps axios to 1.9.0, and 1.9.0 >= 1.8.2, so it is COVERED.** |
| 4.4 Preemptive | None found. |
| 5 Lifecycle | Not fetched (no external calls). No impact on the decision. |
| 6 Already fixed | No resolved siblings. |
| 7 Concurrent triage | TC-8008 is In Progress on the same component. This is the related CVE whose remediation covers this one, and it is already handled by 4.3. Creating tasks would duplicate TC-8009, so task creation is skipped. |
| 7.5 Release Jira | Optional: link TC-8010 -> RHTPA 2.2.x release Task as Related if one exists. 7.5.3 dedup gives the same result: TC-8009 already covers axios. |
| 8 Remediation | Dedup'd or covered, so **zero new tasks**. Case C (Not a Bug) does not apply because the product is affected. The close rests on coverage by TC-8009. |

## Proposed Jira mutations (each needs explicit engineer confirmation)

1. Assign TC-8010 to the current user and transition New -> Assigned (Step 0.8).
2. Create link **Related**: TC-8010 ↔ TC-8008, after an idempotency check (no existing link).
3. Create link **Depend**: TC-8010 -> TC-8009, after an idempotency check (no existing link).
4. Post the cross-CVE overlap comment on TC-8010, with Comment Footnote (see overlap-check.md).
5. Add label `ai-cve-triaged` to TC-8010.
6. Post the post-triage summary comment on TC-8010. It includes the version impact
   status (npm not analysable from the matrix), no Affects Versions correction, the
   outcome (covered by TC-8009, no new tasks), the dedup result, an @mention of the
   issue reporter (ADF mention node), and the Comment Footnote.
7. **Close recommendation:** do not close as "Not a Bug" and do not set VEX, because
   the product is affected. Keep TC-8010 open, tracked through the Depend link to
   TC-8009, so it follows TC-8009 to completion. If the engineer prefers to close now,
   close with a resolution reflecting "fixed by TC-8009", not "Not a Bug". Verify
   after TC-8009 merges that the 2.2.x lock file has axios >= 1.8.2.

## Caveats

- The npm ecosystem is not in the 2.2.x Ecosystem Mappings. Add an npm mapping for
  rhtpa-ui so future triages can confirm version impact from lock files.
- The due date 2026-08-01 has passed. TC-8009 is In Progress, so track its completion
  closely.
- The matrix is stale (151 days). Refresh it through setup Step 10.6.
