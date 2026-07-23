# Status-Aware Handling Decisions

This document lists the handling decision for each discovered Vulnerability issue based on its current Jira status, per the triage-security skill's status-aware handling rules.

---

## Untriaged Issues

### TC-9001 — CVE-2026-40112 (h2 - HTTP/2 rapid reset vulnerability)
- **Status**: New
- **Handling**: Proceed with full triage (default path). This issue is in New status and has not been triaged. All triage steps apply: Data Extraction (Step 1), External CVE Enrichment (Step 1.5), Version Impact Analysis (Step 2), Affects Versions Correction (Step 3), Duplicate/Sibling Check (Step 4), Lifecycle Check (Step 5), Already Fixed Check (Step 6), Concurrent Triage Detection (Step 7), and Remediation (Step 8).

### TC-9002 — CVE-2026-40297 (serde_json - Stack overflow on deeply nested input)
- **Status**: New
- **Handling**: Proceed with full triage (default path). This issue is in New status and has not been triaged. All triage steps apply.

### TC-9003 — CVE-2026-40455 (tokio - Race condition in task cancellation)
- **Status**: In Progress
- **Handling**: **WARNING** — This issue is already in `In Progress`. It may be actively worked on. Before proceeding, the engineer must choose:
  1. **Proceed with triage anyway** — e.g., to verify version impact or update Affects Versions even though work is underway.
  2. **Skip this issue** — return to the discovery list.
  
  The skill will not proceed with triage on this issue until the engineer explicitly confirms which option to take.

### TC-9004 — CVE-2026-40518 (ring - Timing side-channel in RSA verification)
- **Status**: New
- **Handling**: Proceed with full triage (default path). This issue is in New status and has not been triaged. All triage steps apply.

---

## Triaged but still New Issues

### TC-9010 — CVE-2026-39874 (quinn-proto - Panic on malformed QUIC frame)
- **Status**: New (with `ai-cve-triaged` label)
- **Handling**: This issue was previously triaged but remains in New status, meaning no remediation work was started after triage. It should be reviewed for follow-up. The engineer may choose to:
  1. **Re-triage** — run full triage again to verify whether the previous assessment is still current (e.g., dependency versions may have changed since the original triage on 2026-05-28).
  2. **Review previous triage** — check the existing triage comment on the issue to determine why no action was taken, and decide whether remediation tasks need to be created.
  3. **Skip** — no action needed at this time.

---

## Ready for QA Issues

### TC-9020 — CVE-2026-38901 (hyper - HTTP request smuggling)
- **Status**: Modified
- **Handling**: All linked remediation Tasks are complete (TC-9021 Done, TC-9022 Closed). This issue is a candidate for transition to ON_QA status. The engineer should verify that remediation is satisfactory and then transition to ON_QA.

### TC-9023 — CVE-2026-39102 (rustls - Certificate validation bypass)
- **Status**: In Progress
- **Handling**: Excluded from Ready for QA. Linked remediation Task TC-9025 is still In Progress. This issue cannot move to ON_QA until all remediation work is complete.

### TC-9026 — CVE-2026-39330 (openssl - Buffer overflow in X.509 parsing)
- **Status**: Modified
- **Handling**: Excluded from Ready for QA. No linked Tasks with link type "Depend" exist on this issue. There is no remediation work to verify, so it does not qualify for the Ready for QA workflow. This may indicate that remediation tasks were never created or were linked differently.

---

## Summary Table

| Key | CVE ID | Status | Query Group | Handling Decision |
|-----|--------|--------|-------------|-------------------|
| TC-9001 | CVE-2026-40112 | New | Untriaged | Full triage |
| TC-9002 | CVE-2026-40297 | New | Untriaged | Full triage |
| TC-9003 | CVE-2026-40455 | In Progress | Untriaged | **Warning**: active work — engineer must confirm before proceeding |
| TC-9004 | CVE-2026-40518 | New | Untriaged | Full triage |
| TC-9010 | CVE-2026-39874 | New (triaged) | Triaged but still New | Follow-up review or re-triage recommended |
| TC-9020 | CVE-2026-38901 | Modified | Ready for QA | Ready for ON_QA transition (all remediation Tasks complete) |
| TC-9023 | CVE-2026-39102 | In Progress | Ready for QA | Excluded — remediation Task TC-9025 still In Progress |
| TC-9026 | CVE-2026-39330 | Modified | Ready for QA | Excluded — no Depend-type linked Tasks |
