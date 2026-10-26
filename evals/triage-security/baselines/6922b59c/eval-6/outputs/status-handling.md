# Status-Aware Handling Decisions

This document records the status-aware handling decision for each issue found during discovery, applying the rules from the triage-security skill:

- **New** -- proceed with full triage (default path)
- **In Progress / Code Review / QA** -- warn: issue may be actively worked on. Ask whether to (1) proceed with triage anyway, or (2) skip.
- **Closed / Done / Resolved** -- warn: issue is already closed. Ask whether to (1) re-triage, or (2) skip.
- **Modified** -- not a terminal status; issue may need further action depending on context.

---

## Untriaged Issues (Query 1)

### TC-9001 -- CVE-2026-40112 (h2 - HTTP/2 rapid reset vulnerability)

- **Status**: New
- **Handling**: Proceed with full triage (default path). No warnings required.
- **Stream scope**: rhtpa-2.2 (maps to stream 2.2.x)

### TC-9002 -- CVE-2026-40297 (serde_json - Stack overflow on deeply nested input)

- **Status**: New
- **Handling**: Proceed with full triage (default path). No warnings required.
- **Stream scope**: rhtpa-2.1 (maps to stream 2.1.x)

### TC-9003 -- CVE-2026-40455 (tokio - Race condition in task cancellation)

- **Status**: In Progress
- **Handling**: Warn the engineer before proceeding:

  > "This issue is already in **In Progress**. It may be actively worked on."
  >
  > Options:
  > 1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  > 2. Skip this issue

  The engineer must choose before triage can begin. If the engineer chooses to skip, return to the discovery list or end the session.

- **Stream scope**: rhtpa-2.2 (maps to stream 2.2.x)

### TC-9004 -- CVE-2026-40518 (ring - Timing side-channel in RSA verification)

- **Status**: New
- **Handling**: Proceed with full triage (default path). No warnings required.
- **Stream scope**: rhtpa-2.2 (maps to stream 2.2.x)

---

## Triaged but still New (Query 2)

### TC-9010 -- CVE-2026-39874 (quinn-proto - Panic on malformed QUIC frame)

- **Status**: New
- **Handling**: This issue carries the `ai-cve-triaged` label but remains in New status. It was previously triaged but never moved forward. Proceed with full triage if the engineer selects it (status is New, so no warning required), but flag that this is a potential re-triage scenario -- the engineer should review why the previous triage did not result in progression.
- **Stream scope**: rhtpa-2.2 (maps to stream 2.2.x)

---

## Ready for QA Candidates (Query 3)

### TC-9020 -- CVE-2026-38901 (hyper - HTTP request smuggling)

- **Status**: Modified
- **Handling**: All linked remediation Tasks are completed (TC-9021 Done, TC-9022 Closed). This issue is a candidate for ON_QA transition. If the engineer selects it for triage, proceed (Modified is not a terminal or warning status). The primary recommended action is to transition this issue to ON_QA rather than re-triage.
- **Stream scope**: rhtpa-2.2 (maps to stream 2.2.x)

### TC-9023 -- CVE-2026-39102 (rustls - Certificate validation bypass)

- **Status**: In Progress
- **Handling**: Warn the engineer before proceeding:

  > "This issue is already in **In Progress**. It may be actively worked on."
  >
  > Options:
  > 1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  > 2. Skip this issue

  Additionally, remediation is still in progress (TC-9025 is In Progress), so this issue is not ready for QA. The engineer should be informed that outstanding remediation work remains.

- **Stream scope**: rhtpa-2.1 (maps to stream 2.1.x)

### TC-9026 -- CVE-2026-39330 (openssl - Buffer overflow in X.509 parsing)

- **Status**: Modified
- **Handling**: No linked remediation Tasks with type "Depend" exist. This issue has no remediation to verify. If the engineer selects it, proceed with triage (Modified is not a warning status). The engineer should investigate why no remediation tasks were created -- it may indicate the issue was closed as not affected but later reopened, or remediation tasks were never created.
- **Stream scope**: rhtpa-2.2 (maps to stream 2.2.x)

---

## Summary Table

| Issue | Status | Handling Decision | Action Required |
|-------|--------|-------------------|-----------------|
| TC-9001 | New | Proceed with full triage | None |
| TC-9002 | New | Proceed with full triage | None |
| TC-9003 | In Progress | Warn -- may be actively worked on | Engineer must choose: proceed or skip |
| TC-9004 | New | Proceed with full triage | None |
| TC-9010 | New (triaged) | Proceed, but flag as stale triaged issue | Engineer should review prior triage |
| TC-9020 | Modified | Ready for QA -- suggest ON_QA transition | Consider transitioning to ON_QA |
| TC-9023 | In Progress | Warn -- may be actively worked on; remediation incomplete | Engineer must choose: proceed or skip |
| TC-9026 | Modified | No remediation tasks linked | Engineer should investigate missing remediation |
