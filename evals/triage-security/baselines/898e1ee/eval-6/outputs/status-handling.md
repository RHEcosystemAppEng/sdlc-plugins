# Status-Aware Handling Decisions

This document describes the triage handling decision for each discovered Vulnerability issue based on its current Jira status.

---

## Untriaged Issues

### TC-9001 — CVE-2026-40112 (h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2])

- **Status**: New
- **Handling**: Proceed with full triage (default path). This issue is in New status and has not been triaged. All seven triage steps (Data Extraction, External CVE Enrichment, Version Impact Analysis, Affects Versions Correction, Duplicate/Sibling Check, Version Lifecycle Check, Already Fixed Check, and Remediation) apply.

### TC-9002 — CVE-2026-40297 (serde_json - Stack overflow on deeply nested input [rhtpa-2.1])

- **Status**: New
- **Handling**: Proceed with full triage (default path). This issue is in New status and has not been triaged. All seven triage steps apply.

### TC-9003 — CVE-2026-40455 (tokio - Race condition in task cancellation [rhtpa-2.2])

- **Status**: In Progress
- **Handling**: **Warning — this issue is already in `In Progress` status. It may be actively worked on.** Before proceeding, the engineer must choose:
  1. **Proceed with triage anyway** — useful to verify version impact or update Affects Versions even though work is underway.
  2. **Skip this issue** — return to the discovery list.

  This warning is required because triaging an issue that is already being worked on could conflict with or duplicate ongoing remediation efforts.

### TC-9004 — CVE-2026-40518 (ring - Timing side-channel in RSA verification [rhtpa-2.2])

- **Status**: New
- **Handling**: Proceed with full triage (default path). This issue is in New status and has not been triaged. All seven triage steps apply.

---

## Triaged but still New

### TC-9010 — CVE-2026-39874 (quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2])

- **Status**: New (with `ai-cve-triaged` label)
- **Handling**: This issue was previously triaged but remains in New status. It has not transitioned to In Progress or any subsequent status, which suggests remediation tasks may not have been actioned, or the triage outcome may need revisiting. The engineer should review the prior triage results and decide whether to:
  1. **Re-triage** — run a fresh triage pass to verify findings or update the assessment.
  2. **Follow up on existing remediation tasks** — check whether tasks created during the prior triage are blocked or unassigned.
  3. **Skip** — no action needed at this time.

---

## Summary of Status-Based Routing

| Issue Key | Status | Decision |
|-----------|--------|----------|
| TC-9001 | New | Full triage |
| TC-9002 | New | Full triage |
| TC-9003 | In Progress | Warning: active work detected; engineer must confirm before proceeding |
| TC-9004 | New | Full triage |
| TC-9010 | New (triaged) | Stale: previously triaged but not actioned; needs follow-up decision |
