# Status-Aware Handling Decisions

This document applies the status-aware handling rules from the triage-security skill
to each issue surfaced in discovery mode. The rules determine the triage path based
on the issue's current Jira status.

## Status-Aware Handling Rules Reference

| Current Status | Handling |
|----------------|----------|
| **New** | Proceed with full triage (default path). |
| **In Progress / Code Review / QA** | Warn: "This issue is already in `<status>`. It may be actively worked on." Offer: (1) Proceed with triage anyway, (2) Skip this issue. |
| **Closed / Done / Resolved** | Warn: "This issue is already closed." Offer: (1) Re-triage, (2) Skip this issue. |
| **Modified** | Not explicitly listed in the status rules -- treat as an active/in-progress status and apply the In Progress warning path. |

---

## Untriaged Issues (Query 1)

### TC-9001 -- CVE-2026-40112 (h2)
- **Current status**: New
- **Handling decision**: Proceed with full triage (default path). No warnings required. This issue is in the expected initial state for triage.

### TC-9002 -- CVE-2026-40297 (serde_json)
- **Current status**: New
- **Handling decision**: Proceed with full triage (default path). No warnings required. This issue is in the expected initial state for triage.

### TC-9003 -- CVE-2026-40455 (tokio)
- **Current status**: In Progress
- **Handling decision**: Warn the user: "This issue is already in `In Progress`. It may be actively worked on." Offer two options:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue
- **Rationale**: The In Progress status indicates someone may already be working on this issue. Triage can still add value (version impact verification, Affects Versions correction) but should not proceed without the engineer's acknowledgment.

### TC-9004 -- CVE-2026-40518 (ring)
- **Current status**: New
- **Handling decision**: Proceed with full triage (default path). No warnings required. This issue is in the expected initial state for triage.

---

## Triaged but still New (Query 2)

### TC-9010 -- CVE-2026-39874 (quinn-proto)
- **Current status**: New
- **Handling decision**: Proceed with full triage (default path). Although this issue carries the `ai-cve-triaged` label (indicating prior triage), it remains in New status, meaning it was never actioned after triage. The engineer should consider:
  - Re-triaging to verify whether the original triage conclusions are still valid
  - Investigating why the issue was not moved forward after triage (missing remediation tasks? declined recommendation?)
- **Note**: The New status means the standard triage path applies with no status warnings. However, the `ai-cve-triaged` label signals that prior triage output (comments, Affects Versions corrections) may already exist on the issue and should be reviewed before re-triaging.

---

## Ready for QA Candidates (Query 3)

### TC-9020 -- CVE-2026-38901 (hyper)
- **Current status**: Modified
- **Handling decision**: Warn the user: "This issue is already in `Modified`. It may be actively worked on." Offer two options:
  1. Proceed with triage anyway
  2. Skip this issue
- **Ready for QA assessment**: All linked remediation tasks are complete (TC-9021: Done, TC-9022: Closed). This issue is a candidate for transition to ON_QA. Recommended action: transition to ON_QA status rather than re-triaging.

### TC-9023 -- CVE-2026-39102 (rustls)
- **Current status**: In Progress
- **Handling decision**: Warn the user: "This issue is already in `In Progress`. It may be actively worked on." Offer two options:
  1. Proceed with triage anyway
  2. Skip this issue
- **Ready for QA assessment**: Not ready -- TC-9025 is still In Progress. Remediation is ongoing; no QA transition is appropriate until all linked tasks complete.

### TC-9026 -- CVE-2026-39330 (openssl)
- **Current status**: Modified
- **Handling decision**: Warn the user: "This issue is already in `Modified`. It may be actively worked on." Offer two options:
  1. Proceed with triage anyway
  2. Skip this issue
- **Ready for QA assessment**: Not ready -- no linked Tasks with type "Depend" exist. There is no remediation work to verify, so QA transition is not applicable. The engineer should investigate whether remediation tasks were never created or whether this issue was resolved through a different mechanism.

---

## Summary

| Issue | Status | Status Handling | Triage Path |
|-------|--------|-----------------|-------------|
| TC-9001 | New | No warning | Full triage |
| TC-9002 | New | No warning | Full triage |
| TC-9003 | In Progress | Warn: actively worked on | Engineer choice required |
| TC-9004 | New | No warning | Full triage |
| TC-9010 | New | No warning (but previously triaged) | Re-triage / follow-up |
| TC-9020 | Modified | Warn: actively worked on | Recommend ON_QA transition |
| TC-9023 | In Progress | Warn: actively worked on | Engineer choice required |
| TC-9026 | Modified | Warn: actively worked on | Engineer choice required |
