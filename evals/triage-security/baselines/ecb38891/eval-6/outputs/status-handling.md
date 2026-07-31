# Status-Aware Handling Decisions

Each issue from the discovery listing is evaluated for status-aware handling per
the triage-security skill's discovery mode protocol.

---

## Query 1: Untriaged Issues

### TC-9001 — CVE-2026-40112 (h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2])

- **Status**: New
- **Handling**: Proceed with full triage (default path).
  New issues follow the standard triage flow: Steps 0 through 8.

### TC-9002 — CVE-2026-40297 (serde_json - Stack overflow on deeply nested input [rhtpa-2.1])

- **Status**: New
- **Handling**: Proceed with full triage (default path).
  New issues follow the standard triage flow: Steps 0 through 8.

### TC-9003 — CVE-2026-40455 (tokio - Race condition in task cancellation [rhtpa-2.2])

- **Status**: In Progress
- **Handling**: WARNING — This issue is already in `In Progress`. It may be
  actively worked on.

  This issue requires a status-aware warning before proceeding. The engineer
  should be asked:

  > "This issue is already in `In Progress`. It may be actively worked on."
  >
  > Options:
  > 1. Proceed with triage anyway (e.g., to verify version impact or update
  >    Affects Versions)
  > 2. Skip this issue

  If the engineer chooses to skip, return to the discovery list or end the
  session. If they proceed, continue with full triage while being aware that
  prior triage work may already exist.

### TC-9004 — CVE-2026-40518 (ring - Timing side-channel in RSA verification [rhtpa-2.2])

- **Status**: New
- **Handling**: Proceed with full triage (default path).
  New issues follow the standard triage flow: Steps 0 through 8.

---

## Query 2: Triaged but still New

### TC-9010 — CVE-2026-39874 (quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2])

- **Status**: New
- **Labels**: ai-cve-triaged (present)
- **Handling**: This issue was triaged (ai-cve-triaged label is present) but
  remains in New status. It was never moved forward after triage, which suggests
  the triage may have been incomplete, or the remediation was never started.

  This issue is flagged for the engineer's attention. It may need:
  - Follow-up to determine why it was not actioned after triage
  - Re-triage if the original analysis is stale or incomplete

---

## Query 3: Ready for QA

### TC-9020 — CVE-2026-38901 (hyper - HTTP request smuggling [rhtpa-2.2])

- **Status**: Modified
- **Linked Remediation Tasks**: TC-9021 (Done), TC-9022 (Closed)
- **Handling**: All linked remediation Tasks are completed (Done or Closed).
  This issue is **Ready for QA**.

  Proposed action: Consider transitioning TC-9020 to ON_QA.

### TC-9023 — CVE-2026-39102 (rustls - Certificate validation bypass [rhtpa-2.1])

- **Status**: In Progress
- **Linked Remediation Tasks**: TC-9024 (Done), TC-9025 (In Progress)
- **Handling**: Excluded from Ready for QA. Remediation task TC-9025 is still
  In Progress. Not all remediation work is complete.

### TC-9026 — CVE-2026-39330 (openssl - Buffer overflow in X.509 parsing [rhtpa-2.2])

- **Status**: Modified
- **Linked Remediation Tasks**: (no Depend links)
- **Handling**: Excluded from Ready for QA. No linked remediation Tasks with
  link type "Depend" exist. There is no remediation to verify.

---

## Summary

| Issue | Status | Decision |
|-------|--------|----------|
| TC-9001 | New | Full triage |
| TC-9002 | New | Full triage |
| TC-9003 | In Progress | Warning: active work — ask engineer to proceed or skip |
| TC-9004 | New | Full triage |
| TC-9010 | New (triaged) | Flagged: triaged but never actioned — may need follow-up |
| TC-9020 | Modified | Ready for QA — propose transition to ON_QA |
| TC-9023 | In Progress | Not Ready for QA — TC-9025 still In Progress |
| TC-9026 | Modified | Not Ready for QA — no Depend links |
