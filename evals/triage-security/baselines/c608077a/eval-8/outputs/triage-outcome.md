# Triage Outcome: TC-8010 (CVE-2026-44492, axios SSRF, [rhtpa-2.2])

## Decision

**Covered by existing remediation. Create no new remediation tasks.**

The fix for CVE-2026-44492 (axios < 1.8.2, fixed in 1.8.2) is already covered by **TC-8009**, "Bump axios to 1.9.0 in rhtpa-ui [rhtpa-2.2]". TC-8009 is the Depend-linked remediation task of **TC-8008** (CVE-2026-42035). That issue has the same upstream component (axios), the same PS component (pscomponent:org/rhtpa-ui) and the same stream (rhtpa-2.2). The bump target 1.9.0 is at or above the 1.8.2 fix threshold.

## Reasoning

1. **Scope.** The issue is scoped to stream 2.2.x via `[rhtpa-2.2]`.
2. **Affected status.** TC-8009 says rhtpa-ui 2.2.x currently ships axios 1.7.4, which is inside the affected range (< 1.8.2). That points to a real vulnerability in 2.2.x, so this is **not** a "Not a Bug" or Case C close. The vulnerability is real, and its fix is already in flight in another ticket.
3. **Cross-CVE overlap (Step 4.3).** 1.9.0 >= 1.8.2, so TC-8009 covers this CVE. See overlap-check.md.
4. **Dedup (Step 7.5.3 / Case B).** An existing remediation task for upstream component axios in this stream already covers the threshold. The stream is marked dedup'd and no upstream or downstream remediation tasks are created. The CVE is linked to the existing task instead.

## Jira actions (proposed, each needs confirmation, none executed)

| # | Action | Detail |
|---|---|---|
| 1 | Assign + transition | Assign TC-8010 to the current user and move New -> Assigned (Step 0.8) |
| 2 | Link | TC-8010 **Related** TC-8008 (same upstream component) |
| 3 | Link | TC-8010 **Depend** TC-8009 (covering remediation) |
| 4 | Comment | Cross-CVE overlap comment with Comment Footnote (text in overlap-check.md) |
| 5 | Release Jira (7.5) | If a release Task "RHTPA 2.2.x CVE triage" exists, or is created with confirmation, link TC-8010 to it (Related). TC-8009 should already block it. No new remediation task to link. |
| 6 | Label | Add `ai-cve-triaged` to TC-8010 |
| 7 | Summary comment | Post-triage summary covering: the overlap finding; dedup result (linked to TC-8009, no new tasks); Affects Versions (RHTPA 2.2.0 kept as-is because axios lock-file evidence was unavailable); @mention of the issue reporter; Comment Footnote |
| 8 | Status / closure | Step 4.3 recommends closing TC-8010 because the fix is covered by TC-8009. Because 2.2.x really ships a vulnerable axios (1.7.4), close it as covered by, or a duplicate fix of, TC-8009, **not** as "Not a Bug", and do not set a VEX "not affected" justification. Alternatively, the engineer can keep TC-8010 open, tracking TC-8009 through the Depend link, and move it to ON_QA once TC-8009 is Done. Engineer's choice. |

## Not done

- **No new remediation tasks.** No dependency bump, upstream backport or downstream propagation tasks, because TC-8009 already covers the fix.
- **No Case A cross-stream proactive tasks.** The 2.1.x stream could not be assessed for axios. The mock matrix has no npm/rhtpa-ui mapping and no axios lock data, so no preemptive tasks are justified by evidence.

## Caveats for the engineer

- The Upstream Affected Component, PS Component and Stream custom fields (customfield_10632/10669/10832) are **not** declared in the CLAUDE.md Security Configuration. Add them so Step 4.3 runs without being prompted.
- The npm ecosystem and rhtpa-ui repo are missing from the security matrices and Source Repositories. The Step 2 version-impact table (per-release axios versions) could not be built from evidence and needs manual confirmation. 2.1.x exposure is still unknown.
- The security matrices are 145 days stale (Last-Updated 2026-06-28). A refresh is recommended.
- TC-8009 is still **In Progress**. Coverage depends on it merging with axios >= 1.9.0. If its target version drops below 1.8.2, re-triage TC-8010.
- The due date (2026-08-01) has already passed.
