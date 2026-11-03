# Triage Outcome: TC-8010 (CVE-2026-44492, axios, [rhtpa-2.2])

## Decision

**Covered by existing cross-CVE remediation. Do NOT create new remediation tasks.**

Remediation task **TC-8009** belongs to CVE-2026-42035 / TC-8008. It is in the same upstream component (axios), the same PS Component (`pscomponent:org/rhtpa-ui`) and the same stream (rhtpa-2.2). It bumps axios **1.7.4 to 1.9.0**. This CVE's fix threshold is **1.8.2**. Because 1.9.0 >= 1.8.2, TC-8009 fully remediates CVE-2026-44492 for the 2.2.x stream.

## Rationale

1. **Step 1:** CVE-2026-44492 affects axios < 1.8.2, with a fix in 1.8.2. The issue is scoped to stream 2.2.x.
2. **Step 4.1/4.2:** there are no same-CVE siblings, so this is neither a duplicate nor a cross-stream companion.
3. **Step 4.3:** the JQL `cf[10632] ~ 'axios'` returns TC-8008. Its PS Component and Stream match. Its Depend-linked task TC-8009 bumps to 1.9.0, which **meets or exceeds** 1.8.2, so a **covering remediation exists**.
4. **Step 4.4:** there are no preemptive tasks for this CVE.
5. **Step 7 (Concurrent triage):** TC-8008 is In Progress on the same component and would normally raise the concurrent-triage warning. Since no new task will be created, there is no duplicate-task risk. The overlap is now tracked explicitly through the links below.
6. **Step 7.5.3 / Step 8 Case B:** existing coverage counts as dedup, so task creation is skipped for 2.2.x. Creating a second axios bump task would duplicate TC-8009 and conflict with it.

## Proposed Jira Actions (each needs engineer confirmation; none were executed)

| # | Action | Detail |
|---|---|---|
| 1 | Assign + transition (Step 0.8) | Assign TC-8010 to the current user. Transition New to Assigned. |
| 2 | Create link | TC-8010 **Related** TC-8008 (same upstream component). No existing link was found. |
| 3 | Create link | TC-8010 **Depend** TC-8009 (covering remediation). No existing link was found. |
| 4 | Comment | Cross-CVE overlap comment with Comment Footnote (text in overlap-check.md). |
| 5 | Skip task creation | No new upstream or downstream remediation tasks for 2.2.x. |
| 6 | Release Jira (Step 7.5) | If a "RHTPA 2.2.x CVE triage" release Task exists, link TC-8010 to it with Related. TC-8009 should already block it through TC-8008's triage. |
| 7 | Label | Add `ai-cve-triaged` to TC-8010. |
| 8 | Summary comment | Post-triage summary: outcome = covered by TC-8009, dedup result, links, @mention of the reporter, and the Comment Footnote. |
| 9 | Closure | Skill recommendation: "Close this issue — the fix is already covered by TC-8009." Practical note: TC-8009 is still **In Progress**, so axios 1.9.0 has not shipped. The safer approach is to keep TC-8010 open, tracked by the Depend link to TC-8009, and move it forward (e.g., to ON_QA) when TC-8009 is Done. Close only if the team's process allows closing on planned coverage. Do **not** close as "Not a Bug" with VEX: the product is affected today (current axios 1.7.4 < 1.8.2), so VEX "not affected" justifications do not apply. |

## Affects Versions (Step 3)

The current value is RHTPA 2.2.0. Lock-file verification of axios across 2.2.0 to 2.2.4 was **not possible**: the 2.2.x security matrix has no npm/rhtpa-ui ecosystem mapping, and rhtpa-ui is not a configured Source Repository. No correction is proposed, because there is no evidence and versions are not invented. Recommendation: add an npm/rhtpa-ui mapping to the matrix and Source Repositories through `/setup` so that future axios CVEs can be checked per version.

## Caveats

- The security matrix is 128 days old (Last-Updated 2026-06-28), past the 14-day threshold.
- The Step 4.3 custom fields (10632/10669/10832) are not declared in the mock CLAUDE.md Security Configuration. They were used because the task and the issue data supply them.
- There was no MITRE/OSV cross-validation, since external calls are disallowed. The 1.8.2 threshold comes from the Jira description only.
- Embargo check skipped: CVSS 8.1, but no embargo policy URL is configured.
- The due date of 2026-08-01 has passed. Tracking TC-8009 to completion is the path to resolution.
