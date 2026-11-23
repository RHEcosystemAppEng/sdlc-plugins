# Triage Outcome: TC-8020 (CVE-2026-31812, quinn-proto)

## Decision

**Triage paused at Step 7 (Concurrent Triage Detection). Waiting for the engineer to choose.**
No remediation tasks were created, no release Jira orchestration (Step 7.5) was run, and no
Case A/B/C action was taken.

The Step 7 JQL found **TC-8019** (In Progress, assigned to engineer-b@example.com). It is
another Vulnerability triage on the same Upstream Affected Component, **quinn-proto**. The
engineer must pick Wait, Skip, or Proceed before triage continues.
Recommended: **Wait** (see concurrent-triage.md).

## Findings so far (Steps 0–6)

- Issue is scoped to stream **2.2.x** (`[rhtpa-2.2]`). Ecosystem: Cargo (source dependency).
- quinn-proto < 0.11.14 is vulnerable (CVSS 7.5, DoS). Fixed in 0.11.14.
- Version impact (lock files at pinned tags):
  - 2.1.0, 2.1.1: 0.11.9 → **affected** (outside issue scope)
  - 2.2.0: 0.11.9 → **affected**
  - 2.2.1: 0.11.12 → **affected**
  - 2.2.2: retag of 2.2.1 → **affected**
  - 2.2.3, 2.2.4: 0.11.14 → not affected
- PSIRT Affects Versions `RHTPA 2.0.0` is wrong. Proposed correction: RHTPA 2.2.0,
  2.2.1, 2.2.2 (needs confirmation).
- Matrix is stale (last updated 2026-06-28, about 148 days old). Proceeded with it for this eval.
- External CVE enrichment (MITRE/OSV) and lifecycle check were not run because external
  calls are not allowed. The fix threshold comes from the Jira description only, so
  confidence is lower.

## Path that will apply once the engineer decides

Supported versions are affected, so this would be **Case B** for 2.2.x. Because the issue is
scoped and 2.1.x is also affected, **Case A** applies too: post a cross-stream impact
comment, and create preemptive tasks for 2.1.x if no 2.1.x CVE Jira exists.

- **Wait**: stop now. Re-run after TC-8019 finishes. Step 4.3 / 7.5.3 will then likely
  find TC-8019's quinn-proto remediation tasks, so this CVE gets linked to them instead of
  getting new tasks.
- **Skip**: create no remediation tasks. Post a comment on TC-8020 (with the
  `triage-security` Comment Footnote) explaining the skip because of TC-8019.
- **Proceed**: add the `concurrent-triage-overlap` label to TC-8020, then run Step 7.5
  (release Epic/Task for the 2.2.x release family) and Step 8:
  - 2.2.x: 2 tasks. The fix is already in the release/0.4.z lineage (v0.4.11+ ships 0.11.14),
    so these are a dependency bump / Konflux source-ref bump plus downstream propagation
    (Blocks). Link with Depend to TC-8020 and Blocks to the release Task.
  - 2.1.x: cross-stream comment, plus 2 preemptive tasks (`security-preemptive`, Related
    link) if no sibling 2.1.x CVE Jira exists.

## Jira mutations proposed (none executed)

1. Assign TC-8020 to the current user and transition it to Assigned (Step 0.8).
2. Change Affects Versions from RHTPA 2.0.0 to RHTPA 2.2.0, 2.2.1, 2.2.2 (Step 3).
3. Depends on the Step 7 choice: a skip comment, or the `concurrent-triage-overlap` label
   followed by Steps 7.5/8.
4. Post-triage: add the `ai-cve-triaged` label and a summary comment with a reporter
   @mention and the Comment Footnote. This happens only after triage completes, not
   while it is paused at Step 7.
