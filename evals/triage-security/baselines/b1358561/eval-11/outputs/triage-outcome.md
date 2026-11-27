# TC-8021 — Triage Outcome

## Summary

TC-8021 (CVE-2026-55123, tokio < 1.42.0 use-after-free, stream `[rhtpa-2.1]`) is the PSIRT CVE Jira for the 2.1.x stream. Its remediation was already planned: the earlier triage of TC-8020 (`[rhtpa-2.2]`) found 2.1.x affected and created preemptive task **TC-8022** under Step 8 Case A. Step 4.4 reconciles that task with this issue, so **no new remediation tasks are created**.

## How the preemptive task was reconciled

1. **Found.** The Step 4.4 JQL `labels = 'security-preemptive' AND labels = 'CVE-2026-55123'` returned TC-8022.
2. **Matched to this stream.** TC-8022's summary ends in `(rhtpa-2.1)`, which matches TC-8021's `[rhtpa-2.1]` suffix. It bumps tokio to 1.42.0, which equals the fix threshold. Its status is Open.
3. **Linked.** `TC-8021 → TC-8022` with **Depend**, the standard link between a CVE Jira and its own remediation task. This replaces the "orphaned preemptive" state, where the task was tied only by a Related link to the other stream's CVE (TC-8020).
4. **Label removed.** `security-preemptive` comes off TC-8022, leaving `ai-generated-jira, Security, CVE-2026-55123`. The task is no longer preemptive because it now has its own CVE Jira.
5. **Provenance kept.** The Related link TC-8022 to TC-8020 stays, so the origin of the task remains traceable.
6. **Step 8 skip recorded.** Stream 2.1.x is marked as already remediated by TC-8022.

## Step-by-step disposition

| Step | Outcome |
|---|---|
| 0 / 0.6 | Config valid. Interactive mode. |
| 0.3 | **Matrix stale** (152 days since 2026-06-28). Continued under "Proceed anyway". A refresh is recommended. |
| 0.8 | Planned: assign TC-8021 to the current user and move New to Assigned. |
| 1 | Extracted. CVE-2026-55123, tokio, < 1.42.0, fixed 1.42.0, Cargo, scoped to 2.1.x. |
| 1.5 | External DBs not queried (no external calls allowed). Used Jira description data, with reduced confidence. |
| 1.7 | Skipped. No embargo policy URL configured. |
| 2 | **Blocked on evidence.** The mock lock data has no tokio versions for `v0.3.8` and `v0.3.12`. Impact is not fabricated, and the engineer must run `git show v0.3.8:Cargo.lock` and `git show v0.3.12:Cargo.lock`. TC-8022's existence (from the TC-8020 analysis) indirectly suggests 2.1.x is affected. |
| 3 | Affects Versions (RHTPA 2.1.0, 2.1.1) left **unchanged pending** Step 2 evidence. They match the in-scope 2.1.x versions in the matrix. |
| 4.1 | No same-stream duplicate. |
| 4.2 | TC-8020 is a cross-stream companion. Planned: Related link TC-8021 ↔ TC-8020. |
| 4.3 | Skipped. Component, PS Component, and Stream custom fields are not configured. |
| **4.4** | **Reconciled TC-8022.** Depend link added and `security-preemptive` removed. |
| 5 | Lifecycle check is pending. The Product pages URL was not fetched (no external calls). |
| 6 | No resolved siblings known, so not already fixed. |
| 7 | Skipped. Upstream Affected Component field is not configured. |
| 7.5 | Find or create the RHTPA 2.1.x release Epic and Task. If active, link TC-8022 → release Task (Blocks) and TC-8021 → release Task (Related). |
| 8 | **Case B, with task creation skipped for 2.1.x** because TC-8022 reconciles it. Case A does not apply: 2.2.x, the only other stream, already has its own CVE Jira (TC-8020). No Case C. |

## Planned Jira mutations (each needs engineer confirmation; none executed)

1. TC-8021: assign to the current user, then transition to Assigned.
2. Link TC-8021 ↔ TC-8020 (Related).
3. Link TC-8021 → TC-8022 (Depend).
4. TC-8022: labels become `[ai-generated-jira, Security, CVE-2026-55123]` (`security-preemptive` removed).
5. (Step 7.5, if a release Task exists or is created) TC-8022 Blocks the release Task, and TC-8021 is Related to the release Task.
6. TC-8021: add the label `ai-cve-triaged`.
7. TC-8021: post a summary comment. Draft:

```
Triage summary for CVE-2026-55123 (tokio < 1.42.0) — stream rhtpa-2.1

Version impact (2.1.x): 2.1.0 (backend v0.3.8), 2.1.1 (backend v0.3.12) —
tokio version pending lock file confirmation; Affects Versions RHTPA 2.1.0,
RHTPA 2.1.1 retained.

Outcome: remediation already exists. Preemptive task TC-8022
("Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)"), created
from cross-stream triage of TC-8020 [rhtpa-2.2], was reconciled:
- Linked TC-8021 → TC-8022 (Depend)
- Removed security-preemptive label from TC-8022
No new remediation tasks were created.

Companion issue: TC-8020 (rhtpa-2.2) — Related.
Release Jira: <release Epic / Task keys from Step 7.5, if any>

@<reporter>

---
<Comment Footnote per shared/comment-footnote.md, skill: triage-security>
```

## Follow-ups for the engineer

- Confirm the tokio versions at `v0.3.8` and `v0.3.12` so the version impact and Affects Versions can be finalized.
- Refresh the stale security matrix (setup Step 10.6).
- Check whether a downstream-propagation companion task to TC-8022 exists. Cargo is a 2-task ecosystem. If it exists, reconcile it the same way.
- The due date (2026-08-15) has passed, so TC-8022 should be prioritized.
