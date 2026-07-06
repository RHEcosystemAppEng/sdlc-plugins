# Status-Aware Handling Decisions

Per the triage-security skill's status-aware handling rules, each discovered issue
requires a handling decision based on its current Jira status before triage can proceed.

---

## Untriaged Issues

### TC-9001 -- CVE-2026-40112 (h2 - HTTP/2 rapid reset vulnerability)
- **Current status**: New
- **Handling**: Proceed with full triage (default path). No warnings required.

### TC-9002 -- CVE-2026-40297 (serde_json - Stack overflow on deeply nested input)
- **Current status**: New
- **Handling**: Proceed with full triage (default path). No warnings required.

### TC-9003 -- CVE-2026-40455 (tokio - Race condition in task cancellation)
- **Current status**: In Progress
- **Handling**: Warn the user: "This issue is already in In Progress. It may be actively worked on." Present options:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue

### TC-9004 -- CVE-2026-40518 (ring - Timing side-channel in RSA verification)
- **Current status**: New
- **Handling**: Proceed with full triage (default path). No warnings required.

---

## Triaged but still New

### TC-9010 -- CVE-2026-39874 (quinn-proto - Panic on malformed QUIC frame)
- **Current status**: New
- **Handling**: This issue was previously triaged (has `ai-cve-triaged` label) but never moved past New status. Proceed with full triage if the user selects it -- the New status means the default path applies, but the stale state should be flagged. The issue may need follow-up or re-triage to determine why it stalled after initial triage.

---

## Ready for QA Candidates

### TC-9020 -- CVE-2026-38901 (hyper - HTTP request smuggling)
- **Current status**: Modified
- **Handling**: All linked remediation Tasks are completed (TC-9021 Done, TC-9022 Closed). This issue qualifies for Ready for QA. Suggest: "Consider transitioning to ON_QA." If the user selects this issue for triage, warn: "This issue is already in Modified status. It may be actively worked on." Present options:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue

### TC-9023 -- CVE-2026-39102 (rustls - Certificate validation bypass)
- **Current status**: In Progress
- **Handling**: Not ready for QA -- TC-9025 is still In Progress. If the user selects this issue for triage, warn: "This issue is already in In Progress. It may be actively worked on." Present options:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue

### TC-9026 -- CVE-2026-39330 (openssl - Buffer overflow in X.509 parsing)
- **Current status**: Modified
- **Handling**: Not ready for QA -- no linked Tasks with type "Depend" exist, so there is no remediation to verify. If the user selects this issue for triage, warn: "This issue is already in Modified status. It may be actively worked on." Present options:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue

---

## Decision Summary

| Issue | Status | Decision |
|-------|--------|----------|
| TC-9001 | New | Full triage (default path) |
| TC-9002 | New | Full triage (default path) |
| TC-9003 | In Progress | Warn -- may be actively worked on; ask user to proceed or skip |
| TC-9004 | New | Full triage (default path) |
| TC-9010 | New | Full triage (default path); flag as stale -- triaged but never actioned |
| TC-9020 | Modified | Warn -- may be actively worked on; suggest ON_QA transition (all Tasks done) |
| TC-9023 | In Progress | Warn -- may be actively worked on; not ready for QA (TC-9025 In Progress) |
| TC-9026 | Modified | Warn -- may be actively worked on; not ready for QA (no Depend links) |
