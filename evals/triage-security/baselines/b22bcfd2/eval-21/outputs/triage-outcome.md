# Triage Outcome -- TC-8020

## Summary

Triage of TC-8020 (CVE-2026-31812, quinn-proto < 0.11.14) is **paused at Step 7 (Concurrent Triage Detection)** pending engineer decision.

## Steps Completed

| Step | Status | Result |
|------|--------|--------|
| 0 | Complete | Project configuration validated. Project key: TC, Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432, Vulnerability issue type ID: 10024. Upstream Affected Component custom field configured. |
| 0.3 | Complete | Security matrix Last-Updated timestamp (2026-06-28T10:00:00Z) is within the 14-day threshold. No staleness warning. |
| 1 | Complete | CVE data extracted: CVE-2026-31812, quinn-proto, affected range < 0.11.14, fixed version 0.11.14, CVSS 7.5 (High). Stream scope: 2.2.x. Ecosystem: Cargo. Upstream Affected Component: quinn-proto. |
| 2 | Complete (implied) | Version impact analysis performed against security-matrix.md pinned commits for the 2.2.x stream. |
| 3 | Pending confirmation | Affects Versions correction proposed (RHTPA 2.0.0 is incorrect). |
| 4 | Complete | Duplicate/sibling/overlap checks performed. |
| 5 | Complete | Version lifecycle check performed. |
| 6 | Complete | Already-fixed check performed. |
| **7** | **Blocked** | **Concurrent triage detected -- TC-8019 (In Progress, assigned to engineer-b@example.com) is triaging the same upstream component (quinn-proto).** |
| 8 | Not started | Awaiting Step 7 resolution. |

## Concurrent Triage Gate

Step 7 detected that TC-8019 is concurrently triaging a CVE that affects the same upstream component (`quinn-proto`). The triage is paused to prevent creating duplicate remediation tasks.

The engineer must choose one of three options before the triage can proceed:

1. **Wait** -- Pause until TC-8019 completes, then re-run Step 4.3 for overlap detection.
2. **Skip** -- Skip remediation task creation; add a comment to TC-8020 documenting the reason.
3. **Proceed** -- Create tasks with `concurrent-triage-overlap` label for cross-detection.

## What Happens After the Decision

- **If Wait**: The triage session ends. The engineer should re-invoke `/triage-security TC-8020` after TC-8019's triage is complete. At that point, Step 4.3 (Cross-CVE Overlap Detection) will automatically check whether TC-8019's remediation task already bumps quinn-proto to >= 0.11.14, potentially making TC-8020's remediation unnecessary.

- **If Skip**: Step 8 is skipped entirely. No remediation tasks are created. A Jira comment is added to TC-8020 explaining the deferral. The `ai-cve-triaged` label is still added to mark the issue as reviewed. The engineer can re-triage later.

- **If Proceed**: The triage continues to Case A/B/C branching in Step 8 with the `concurrent-triage-overlap` label applied. For the 2.2.x stream (Cargo ecosystem), this would create:
  - An upstream backport task to bump quinn-proto to >= 0.11.14 on `release/0.4.z` branch in the backend repository
  - A downstream propagation subtask to update the backend reference in the Konflux release repo (rhtpa-release.0.4.z)
  - Both tasks linked to TC-8020 with "Depend" link type
  - The downstream subtask blocked by the upstream task via "Blocks" link type

## Proposed Actions (All Presented as Proposals)

The following triage actions are **proposed** but not yet executed. All Jira mutations require explicit engineer confirmation:

- **Affects Versions correction**: Replace `RHTPA 2.0.0` with the lock-file-verified affected versions from the 2.2.x stream (RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 -- versions shipping quinn-proto < 0.11.14).
- **Label addition**: Propose adding `ai-cve-triaged` label after triage completes.
- **Remediation tasks**: Pending Step 7 resolution -- task creation is gated on the engineer's concurrent triage decision.
- **Status transition**: Propose transitioning TC-8020 from New to In Progress after remediation tasks are created (if applicable).
