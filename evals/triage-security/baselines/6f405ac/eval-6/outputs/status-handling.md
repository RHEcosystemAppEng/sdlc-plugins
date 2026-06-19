# Status-Aware Handling Decisions

Per SKILL.md discovery mode, each issue's current Jira status determines the
handling path when selected for triage.

---

## Untriaged Issues (Query 1)

### TC-9001 — CVE-2026-40112 h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2]

- **Current status**: New
- **Handling**: Proceed with full triage (Steps 1-7). This is the default path for New issues.
- **Stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Action required**: None — standard triage workflow applies.

### TC-9002 — CVE-2026-40297 serde_json - Stack overflow on deeply nested input [rhtpa-2.1]

- **Current status**: New
- **Handling**: Proceed with full triage (Steps 1-7). This is the default path for New issues.
- **Stream scope**: 2.1.x (from summary suffix `[rhtpa-2.1]`)
- **Action required**: None — standard triage workflow applies.

### TC-9003 — CVE-2026-40455 tokio - Race condition in task cancellation [rhtpa-2.2]

- **Current status**: In Progress
- **Handling**: **Warning required.** This issue is already in `In Progress`. It may be actively worked on.
- **Stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Action required**: Prompt the engineer with two options:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue
- If the engineer chooses to skip, return to the discovery list or end the session.

### TC-9004 — CVE-2026-40518 ring - Timing side-channel in RSA verification [rhtpa-2.2]

- **Current status**: New
- **Handling**: Proceed with full triage (Steps 1-7). This is the default path for New issues.
- **Stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Action required**: None — standard triage workflow applies.

---

## Triaged but Still New Issues (Query 2)

### TC-9010 — CVE-2026-39874 quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2]

- **Current status**: New
- **Labels**: ai-cve-triaged (already triaged)
- **Handling**: This issue was previously triaged but never moved beyond New status. It appears in the "Triaged but still New" list as a stale issue.
- **Stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Action required**: The engineer should review why this issue was not actioned after triage. Options:
  1. Re-triage to verify the original assessment (e.g., version impact may have changed since the original triage on 2026-05-28)
  2. Follow up on any remediation tasks that may have been created but not started
  3. Skip this issue if the original triage decision is still valid and work is planned

---

## Status Handling Summary

| Key | Status | Handling Decision | Confirmation Needed? |
|-----|--------|-------------------|----------------------|
| TC-9001 | New | Full triage (default path) | No |
| TC-9002 | New | Full triage (default path) | No |
| TC-9003 | In Progress | Warn: already in progress, ask to proceed or skip | Yes |
| TC-9004 | New | Full triage (default path) | No |
| TC-9010 | New (stale) | Previously triaged, may need re-triage or follow-up | Yes |

### Status Categories Reference

| Status | Handling Rule |
|--------|---------------|
| **New** | Proceed with full triage (Steps 1-7) |
| **In Progress / Code Review / QA** | Warn the user, ask whether to proceed or skip |
| **Closed / Done / Resolved** | Warn the user, ask whether to re-triage or skip |
