# Status-Aware Handling Decisions

This document lists the status-aware handling decision for each issue surfaced in discovery mode, following the rules from SKILL.md (Discovery mode -- Status-aware handling).

---

## Untriaged Issues

### TC-9001 -- CVE-2026-40112 h2 (New)

- **Status**: New
- **Handling**: Proceed with full triage (default path). No warnings required.

### TC-9002 -- CVE-2026-40297 serde_json (New)

- **Status**: New
- **Handling**: Proceed with full triage (default path). No warnings required.

### TC-9003 -- CVE-2026-40455 tokio (In Progress)

- **Status**: In Progress
- **Handling**: Warn the user -- "This issue is already in `In Progress`. It may be actively worked on." Ask the engineer whether to:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue
- **Note**: The In Progress status suggests another engineer may be actively working on this issue. Proceeding with triage could duplicate effort or conflict with ongoing work.

### TC-9004 -- CVE-2026-40518 ring (New)

- **Status**: New
- **Handling**: Proceed with full triage (default path). No warnings required.

---

## Triaged but still New

### TC-9010 -- CVE-2026-39874 quinn-proto (New, ai-cve-triaged)

- **Status**: New (with `ai-cve-triaged` label)
- **Handling**: This issue was previously triaged but never moved past New status. It is flagged so the engineer can spot that it was triaged but never moved forward. May need follow-up or re-triage.
- **If selected for triage**: Since the status is New, proceed with full triage (default path). No status warning is required, but the engineer should be aware that prior triage results may already exist.

---

## Ready for QA Candidates

### TC-9020 -- CVE-2026-38901 hyper (Modified)

- **Status**: Modified
- **Handling**: All linked remediation Tasks are completed (TC-9021 Done, TC-9022 Closed). This issue is ready for QA. Consider transitioning to ON_QA.
- **If selected for triage**: The Modified status falls under the "In Progress / Code Review / QA" category. Warn the user -- "This issue is already in `Modified`. It may be actively worked on." Ask the engineer whether to proceed or skip. However, the primary recommendation here is to transition to ON_QA since all remediation is complete.

### TC-9023 -- CVE-2026-39102 rustls (In Progress)

- **Status**: In Progress
- **Handling**: Not ready for QA -- TC-9025 is still In Progress. Remediation is ongoing.
- **If selected for triage**: Warn the user -- "This issue is already in `In Progress`. It may be actively worked on." Ask the engineer whether to:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue

### TC-9026 -- CVE-2026-39330 openssl (Modified)

- **Status**: Modified
- **Handling**: Not ready for QA -- no linked remediation Tasks with type "Depend" exist. There is no remediation to verify.
- **If selected for triage**: The Modified status falls under the "In Progress / Code Review / QA" category. Warn the user -- "This issue is already in `Modified`. It may be actively worked on." Ask the engineer whether to proceed or skip.

---

## Summary

| Issue | Status | Triage Decision | Action Required |
|-------|--------|----------------|-----------------|
| TC-9001 | New | Proceed with full triage | None -- default path |
| TC-9002 | New | Proceed with full triage | None -- default path |
| TC-9003 | In Progress | Warn before proceeding | Engineer must choose: proceed or skip |
| TC-9004 | New | Proceed with full triage | None -- default path |
| TC-9010 | New (triaged) | Follow-up or re-triage | Engineer review -- triaged but stalled |
| TC-9020 | Modified | Ready for QA | Consider transitioning to ON_QA |
| TC-9023 | In Progress | Not ready for QA | Remediation still in progress (TC-9025) |
| TC-9026 | Modified | Not ready for QA | No remediation tasks linked |
