# Status-Aware Handling Decisions

Per the triage-security skill, each issue's current Jira status determines how it should be handled when selected for triage.

---

## Untriaged Issues

### TC-9001 — CVE-2026-40112 h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2]

- **Current Status:** New
- **Handling:** Proceed with full triage (default path). No warnings required.
- **Stream Scope:** 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Action:** Execute Steps 1 through 7 in sequence — data extraction, external CVE enrichment, version impact analysis, Affects Versions correction, duplicate/sibling check, lifecycle check, already-fixed check, and remediation.

### TC-9002 — CVE-2026-40297 serde_json - Stack overflow on deeply nested input [rhtpa-2.1]

- **Current Status:** New
- **Handling:** Proceed with full triage (default path). No warnings required.
- **Stream Scope:** 2.1.x (from summary suffix `[rhtpa-2.1]`)
- **Action:** Execute Steps 1 through 7 in sequence.

### TC-9003 — CVE-2026-40455 tokio - Race condition in task cancellation [rhtpa-2.2]

- **Current Status:** In Progress
- **Handling:** Warn the user before proceeding.
  > "This issue is already in `In Progress`. It may be actively worked on."
- **Options presented to engineer:**
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue
- **Stream Scope:** 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Action:** Wait for engineer decision. If they choose to skip, return to the discovery list or end the session. If they choose to proceed, execute Steps 1 through 7 but with awareness that work may already be underway.

### TC-9004 — CVE-2026-40518 ring - Timing side-channel in RSA verification [rhtpa-2.2]

- **Current Status:** New
- **Handling:** Proceed with full triage (default path). No warnings required.
- **Stream Scope:** 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Action:** Execute Steps 1 through 7 in sequence.

---

## Triaged but still New (Stale Issues)

### TC-9010 — CVE-2026-39874 quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2]

- **Current Status:** New
- **Handling:** This issue has the `ai-cve-triaged` label but remains in New status. It was previously triaged but never actioned (no status transition occurred after triage).
- **Stream Scope:** 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Recommended Action:** This issue needs follow-up. The engineer should determine why it stalled after triage:
  - Were remediation tasks created but not started?
  - Was the triage outcome to close, but the close action was never confirmed?
  - Does it need re-triage due to changed conditions (new version stream, updated CVE data)?
- **If re-triage is selected:** Proceed with full triage (Steps 1 through 7). The `ai-cve-triaged` label is already present, so this is effectively a re-triage pass. The status is New, so no "already in progress" warning is needed.
- **If skip is selected:** Return to the discovery list or end the session.

---

## Summary Table

| Issue | Status | Handling | Warning Required |
|-------|--------|----------|------------------|
| TC-9001 | New | Full triage | No |
| TC-9002 | New | Full triage | No |
| TC-9003 | In Progress | Warn + ask engineer | Yes — may be actively worked on |
| TC-9004 | New | Full triage | No |
| TC-9010 | New (stale) | Follow-up or re-triage | No (but flagged as stale) |
