# Triage Outcome: TC-8020 (CVE-2026-31812, quinn-proto)

## Decision

**Paused at Step 7 – Concurrent Triage Detection.** A concurrent triage on the same
upstream component was found: **TC-8019** (In Progress, assigned to
engineer-b@example.com, Upstream Affected Component `quinn-proto`). The skill must stop and
ask the engineer to choose **Wait / Skip / Proceed** before Step 7.5 (Release Jira) and
Step 8 (Remediation). No remediation tasks are created until that choice is made.

## Findings so far

1. **Scope**: issue is scoped to stream **2.2.x** (`[rhtpa-2.2]`).
2. **Version impact** (Cargo, quinn-proto < 0.11.14):
   - 2.2.x affected: **2.2.0** (0.11.9), **2.2.1** (0.11.12), **2.2.2** (retag of 2.2.1).
   - 2.2.x not affected: 2.2.3, 2.2.4 (0.11.14).
   - 2.1.x (outside scope) affected: 2.1.0, 2.1.1 (0.11.9) → cross-stream impact.
3. **Affects Versions correction (proposed)**: `[RHTPA 2.0.0] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`.
   PSIRT's RHTPA 2.0.0 is wrong (no 2.0.x stream). Requires engineer confirmation.
4. **Steps 4–6**: sibling / cross-CVE overlap / preemptive / lifecycle / already-fixed
   searches were not provided by the task and not executed (no external calls). They would
   run before Step 7 in a real triage.
5. **Matrix staleness**: matrix Last-Updated 2026-06-28 is ~152 days old (> 14-day
   threshold); flagged for refresh.

## Why the triage pauses

The current issue is affected (Case A/B path), so remediation tasks would be created.
Because TC-8019 is actively triaging another CVE in the same crate, creating tasks now
risks duplicate quinn-proto bump tasks for the same stream. Step 7 needs an explicit
engineer choice; none was given, so no choice is assumed.

## What happens after each choice

- **Wait**: stop now; re-run triage after TC-8019 completes. Step 4.3 will then check
  whether TC-8019's remediation bumps quinn-proto to >= 0.11.14 for 2.2.x. If it does,
  link TC-8020 to that task (Related + Depend) and recommend closing instead of creating
  tasks.
- **Skip**: no Step 8 task creation. Post an explanatory comment on TC-8020 (with Comment
  Footnote).
- **Proceed**: add `concurrent-triage-overlap` label to TC-8020, then:
  - Step 7.5: find/create the release Epic "RHTPA <version> Release Tasks" and Task
    "RHTPA <version> CVE triage" for 2.2.x (individual confirmation each), and run the
    cross-CVE dedup check (7.5.3) against existing quinn-proto remediation tasks.
  - **Case A** (scoped, 2.1.x also affected): post the cross-stream impact comment.
    Create preemptive tasks (`security-preemptive`, Related link) for 2.1.x only if no
    2.1.x sibling CVE Jira exists.
  - **Case B** for 2.2.x: 2 Cargo tasks: (1) upstream backport, or a dependency bump if
    Step 2.5 confirms `release/0.4.z` already ships 0.11.14, then (2) downstream Konflux
    propagation that the first task Blocks. Both link to TC-8020 with Depend and to the
    release Task with Blocks. TC-8020 links to the release Task with Related.
  - Post-triage: add `ai-cve-triaged` label and a summary comment @mentioning the reporter,
    with Comment Footnote.

## Mutations performed

None. Every proposed Jira change above (assignment, Affects Versions, labels, comments,
links, tasks) is pending engineer confirmation. Nothing was sent to Jira.
