# Triage Outcome: TC-8020 (CVE-2026-31812, quinn-proto)

## Decision
**AFFECTED: remediation needed in stream 2.2.x. Task creation is paused at the Step 7 concurrent-triage gate until the engineer chooses an option.**

## Summary of findings

| Step | Result |
|------|--------|
| 0 Config | Valid. Upstream Affected Component = customfield_10632 (assumed configured). |
| 0.3 Staleness | Matrices are 145 days old (Last-Updated 2026-06-28). Warning issued; proceeded under eval assumption. |
| 1 Extraction | CVE-2026-31812, quinn-proto < 0.11.14 (fixed 0.11.14), CVSS 7.5. Scoped `[rhtpa-2.2]` to 2.2.x. Ecosystem Cargo (source dependency). |
| 1.5 / 1.7 | External enrichment simulated (Jira data only). Embargo check skipped (no URL configured). |
| 2 Version impact | 2.2.0 (0.11.9) YES · 2.2.1 (0.11.12) YES · 2.2.2 (retag of 2.2.1) YES · 2.2.3 / 2.2.4 (0.11.14) NO. Out of scope: 2.1.0 and 2.1.1 (0.11.9) YES. |
| 3 Affects Versions | Propose `[RHTPA 2.0.0]` -> `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`. PSIRT's 2.0.0 does not exist as a stream. |
| 4 Duplicates / siblings | None supplied. 4.3 skipped (PS Component and Stream fields not configured). No preemptive tasks. |
| 5 Lifecycle | Not fetched. 2.2.x assumed supported. |
| 6 Already fixed | No resolved siblings. Newer 2.2.x releases (2.2.3 and later) already ship the fix, but the affected 2.2.0–2.2.2 releases remain. |
| **7 Concurrent triage** | **Detected: TC-8019 (In Progress, engineer-b@example.com) on the same component, quinn-proto.** Wait / Skip / Proceed options presented. **Waiting for engineer choice.** |
| 7.5 / 8 | **Not run.** Blocked by the Step 7 gate. |

## Why execution stopped at Step 7
The concurrent-triage protocol requires the engineer to choose Wait, Skip or Proceed before Step 7.5 (release Jira orchestration) or Case A/B/C. TC-8019 is a different CVE on the same upstream crate and is being triaged right now. If both triages create quinn-proto bump tasks for 2.2.x, the tasks would be duplicates. Release-Task dedup (7.5.3) cannot catch this, because neither triage has linked its remediation yet. No choice was provided in this eval, so no tasks were created and no Jira mutations were made.

**Recommendation: Option 1 (Wait).** Re-run triage after TC-8019 completes. Step 4.3 and Step 7.5.3 will then check whether TC-8019's remediation bumps quinn-proto to >= 0.11.14. If it does, TC-8020 should be linked to that task (Depend plus release Task Related, and the CVE label added to the task) rather than getting new tasks. Because the due date has already passed (2026-07-15), the engineer may prefer **Option 3 (Proceed)** with the `concurrent-triage-overlap` label.

## Planned actions once the gate clears (Option 3, or after Wait with no covering task)
All of these need engineer confirmation and none have been executed.

1. Step 0.8: assign TC-8020 to the current user and transition New -> Assigned.
2. Step 3: update Affects Versions to RHTPA 2.2.0, 2.2.1, 2.2.2, plus a correction comment with the footnote.
3. Option 3 only: add the label `concurrent-triage-overlap` to TC-8020.
4. Step 7.5: find or create the release Epic for 2.2.x (default proposal "RHTPA 2.2.5 Release Tasks", the next patch after 2.2.4 in the matrix) and the release Task "RHTPA 2.2.5 CVE triage". Then run the 7.5.3 dedup on quinn-proto.
5. **Case A** (the issue is scoped and stream 2.1.x is also affected): post a cross-stream impact comment saying quinn-proto < 0.11.14 also affects 2.1.x (2.1.0 and 2.1.1 ship 0.11.9). If no CVE-2026-31812 Jira exists for 2.1.x, create preemptive tasks for 2.1.x with label `security-preemptive` and a Related link (upstream backport to `release/0.3.z` + downstream propagation in rhtpa-release.0.3.z).
6. **Case B** for 2.2.x (Cargo, so 2 tasks): `release/0.4.z` already ships 0.11.14 (v0.4.11 and later), so use the **fix-available** variant.
   - Task 1: quinn-proto dependency bump / verification on rhtpa-backend `release/0.4.z` (`cargo update -p quinn-proto` to >= 0.11.14). This may be a no-op confirmation if HEAD is already at 0.11.14.
   - Task 2: downstream propagation in rhtpa-release.0.4.z, so the next 2.2.x release pins a backend tag with quinn-proto >= 0.11.14. Blocked by Task 1.
   - Links: Depend (TC-8020 to each task), Blocks (Task 1 to Task 2), Blocks (tasks to the release Task), Related (release Task to TC-8020). A description digest comment is posted on each task.
7. Post-triage: add the `ai-cve-triaged` label and a summary comment (impact table, AV correction, outcome, task and release links, @mention of the reporter, footnote).

## Caveats
- The mock issue file shows key TC-8001, but the prompt says TC-8020. TC-8020 was used.
- The matrices are stale (145 days), so releases after 2.2.4 may be missing.
- The development-stream HEAD was not read directly. It is expected to be fixed, based on v0.4.11 and later.
- No external services were contacted. All Jira and git results are simulated from the provided files and the task instructions.
