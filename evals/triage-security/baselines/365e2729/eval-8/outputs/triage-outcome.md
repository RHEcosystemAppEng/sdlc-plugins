# Triage Outcome: TC-8010 (CVE-2026-44492, axios SSRF, [rhtpa-2.2])

## Decision

**Covered by existing remediation. No new remediation tasks will be created.** This is the cross-CVE overlap path from Step 4.3.

Related CVE TC-8008 (CVE-2026-42035) affects the same upstream component (axios), PS component (pscomponent:org/rhtpa-ui) and stream (rhtpa-2.2). Its linked Depend remediation task **TC-8009** bumps axios to **1.9.0**. CVE-2026-44492's fix threshold is **1.8.2**. Since 1.9.0 >= 1.8.2, merging TC-8009 also fixes this CVE. Creating separate bump and downstream-propagation tasks for 2.2.x would duplicate TC-8009.

## Rationale by step

| Step | Result |
|---|---|
| 0 Config | Valid. The 10632/10669/10832 fields are not in the CLAUDE.md Security Configuration; they were taken from the task and issue data. |
| 0.3 Staleness | Matrix is 151 days old, so a warning was raised. Proceeded anyway. |
| 0.8 Assign | Proposed: assign TC-8010 to the current user and transition New -> Assigned. |
| 1 Extraction | CVE-2026-44492, axios (npm), affected < 1.8.2, fixed 1.8.2, CVSS 8.1, scoped to 2.2.x. |
| 1.5 Enrichment | Skipped (no external calls). Uses the Jira threshold 1.8.2, with reduced confidence. |
| 1.7 Embargo | Skipped (no policy URL configured). |
| 2 Version impact | No axios or npm lock data in the provided matrix or evidence. No impact table was fabricated. Manual verification is needed if per-version Affects Versions accuracy matters. TC-8009 says rhtpa-ui 2.2 ships axios 1.7.4, which is inside the affected range. |
| 3 Affects Versions | No correction proposed. There is no lock-file evidence to contradict RHTPA 2.2.0. |
| 4.1/4.2 Siblings | No same-CVE siblings. |
| **4.3 Cross-CVE overlap** | **TC-8008 / TC-8009 cover this CVE (1.9.0 >= 1.8.2).** |
| 4.4 Reconciliation | No preemptive tasks found. |
| 5 Lifecycle | Not checked (external). 2.2.x is the latest stream. |
| 6 Already fixed | Not already fixed. TC-8009 is still In Progress. |
| 7 Concurrent triage | TC-8008 is In Progress on the same component. No tasks will be created, so there is no duplicate risk. The overlap is resolved by linking. |
| 7.5 Release Jira | Not needed for new tasks. If a "RHTPA 2.2.x CVE triage" release Task exists that TC-8009 Blocks, 7.5.3 dedup gives the same answer: link TC-8010 to it as Related and add no new task. |
| 8 Remediation | No Case B task creation (dedup'd and covered). No Case A, because the impact on other streams (2.1.x) cannot be evaluated without npm data. |

## Proposed Jira mutations (each needs confirmation; none executed)

1. Assign TC-8010 to the current user and transition it to Assigned.
2. Create a **Related** link: TC-8010 <-> TC-8008.
3. Create a **Depend** link: TC-8010 -> TC-8009.
4. Post the cross-CVE overlap comment, with the Comment Footnote. Text is in overlap-check.md.
5. Add the label `ai-cve-triaged` to TC-8010.
6. Post the post-triage summary comment, with the Comment Footnote. It includes the overlap finding, the links, "no new remediation tasks", the dedup result (covered by TC-8009), and an @mention of the TC-8010 reporter.
7. **Close recommendation** (Step 4.3): close TC-8010 as covered by TC-8009. Caveat: TC-8009 is still In Progress, so the fix has not shipped yet. The engineer may prefer to keep TC-8010 open, tracked through its Depend link to TC-8009, and move it forward (Modified / ON_QA) once TC-8009 is Done. Either way, do **not** close it as "Not a Bug" or set VEX Justification, because the product is affected.

## Follow-ups

- Add Upstream Affected Component (customfield_10632), PS Component (customfield_10669) and Stream (customfield_10832) to CLAUDE.md Security Configuration.
- Add an npm ecosystem mapping and the rhtpa-ui repo to the security matrix and Source Repositories, so axios version impact can be checked from lock files. That would also show whether 2.1.x is affected (Case A).
- Refresh the stale security matrices.
- The due date (2026-08-01) has passed. Make sure TC-8009 is prioritized.
