# Idempotency Check: TC-8001 re-run

Each mutation the skill would perform on a first triage is checked against the
artifacts that already exist on TC-8001 from the prior run (2026-07-01, skill v0.11.1).
If a matching artifact exists, the step is skipped and nothing is duplicated.

| # | Step / mutation | Pre-existing artifact detected | Detection rule | Result |
|---|---|---|---|---|
| 1 | Step 0.8: transition to Assigned | Status = **In Progress** (later than Assigned) | "If already in Assigned or any later status, skip the transition silently" | SKIPPED |
| 2 | Step 0.8: assign to current user | Assignee = engineer-a@example.com | Assignment is a no-op when the current user is already the assignee | NO-OP (see note A) |
| 3 | Step 3: Affects Versions correction | `versions` = RHTPA 2.2.0, RHTPA 2.2.1 (prior correction applied) | "If Affects Versions are already correct: note and proceed without changes" | No duplicate correction or comment. **Discrepancy flagged** (note B) |
| 4 | Step 3: correction comment | Prior run's correction is recorded in the post-triage summary ("Affects Versions corrected to RHTPA 2.2.0, RHTPA 2.2.1") | Same correction already applied and documented | SKIPPED |
| 5 | Step 4.2: Related links to cross-stream siblings | No sibling data available (JQL not run). Existing links are Depend only | Check `issuelinks` for `Related` + sibling key before creating | No link created by this simulated run (note C) |
| 6 | Step 4.3: cross-CVE overlap | n/a | Upstream Affected Component field not configured in Security Configuration | SKIPPED (step not applicable) |
| 7 | Step 4.4: preemptive reconciliation | Remediation already linked via Depend (TC-8100, TC-8101). Neither carries `security-preemptive` | Remediation exists for stream 2.2.x | SKIPPED |
| 8 | Steps 5/6: lifecycle and already-fixed closure | Affected 2.2.x versions are not EOL per prior triage. No resolved siblings known | No closure recommendation | No action |
| 9 | Step 7 / 7.5.3: concurrent triage and dedup | n/a | Upstream Affected Component field not configured | SKIPPED |
| 10 | Step 8 Case B: upstream backport task | **TC-8100**: "Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2]", labels ai-generated-jira, Security, CVE-2026-31812, status In Progress | Existing Depend-linked task with the same CVE label, stream and role | SKIPPED (no new task) |
| 11 | Step 8 Case B: downstream propagation task | **TC-8101**: "Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2]", same labels, status Open | Existing Depend-linked task with the same CVE label, stream and role | SKIPPED (no new task) |
| 12 | Link CVE -> task (Depend) x2 | Depend -> TC-8100, Depend -> TC-8101 | "Check existing `issuelinks` first; if a matching link exists, skip" | SKIPPED |
| 13 | Link downstream -> upstream (Blocks) | TC-8101 Blocks TC-8100 | Existing Blocks link | SKIPPED |
| 14 | Description digest comment | `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4…a1b2` by sdlc-workflow/triage-security | Digest is posted exactly once per created task. No task is created, so there is no digest to post | SKIPPED |
| 15 | Post-triage: add `ai-cve-triaged` label | Label `ai-cve-triaged` present | Label already set | SKIPPED |
| 16 | Post-triage summary comment | "Post-triage summary" comment with Comment Footnote, by sdlc-workflow/triage-security | Summary already posted. Re-posting would duplicate the audit trail | SKIPPED |
| 17 | Step 7.5 release Jira | No release Epic/Task evidence in the issue data | Would require JQL/engineer confirmation | Not created in this run (note C) |

## Notes

**A. Assignment.** SKILL.md says the assignment "still proceeds regardless" on a re-triage.
If the person running it is engineer-a, the edit is a no-op. If someone else is running it,
reassignment is a real change and would need explicit confirmation. It is not executed here.

**B. Affects Versions discrepancy (2.2.2 retag).** The 2.2.x supportability matrix lists
RHTPA 2.2.2 as "backend retag of 2.2.1" with backend tag `v0.4.8`, which pins quinn-proto 0.11.12
(< 0.11.14). Under Important Rule 5, retags carry forward the original version's result, so
2.2.2 is **affected**. The stream-scoped impact set is therefore {2.2.0, 2.2.1, 2.2.2}. The prior
run applied {2.2.0, 2.2.1} and its summary says 2.2.2 is not affected. The idempotency check
does not hide this: the existing correction is not re-applied, but the skill
**presents** a proposed change (`Current: [RHTPA 2.2.0, RHTPA 2.2.1] -> Proposed: [RHTPA 2.2.0,
RHTPA 2.2.1, RHTPA 2.2.2]`) to the engineer. Every Jira mutation needs explicit confirmation,
so nothing is written without approval.

**C. Cross-stream (Case A).** Stream 2.1.x (2.1.0, 2.1.1 at quinn-proto 0.11.9) is also affected.
The issue is scoped to 2.2.x, so Case A applies: check for a sibling 2.1.x CVE Jira and, if there
is none, create preemptive tasks. The prior summary does not mention cross-stream handling, and
sibling/release data can only come from Jira JQL, which this eval does not allow. It is reported
as an open verification item. No mutation is performed or simulated.

## Summary

Every artifact a first run creates already exists: label, In Progress status, two
remediation Tasks, Depend and Blocks links, the digest comment and the summary comment. Each
matching step is skipped, so no duplicates are created.
