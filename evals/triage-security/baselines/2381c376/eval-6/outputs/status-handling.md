# Status-Aware Handling Decisions

This document describes the status-aware handling decision for each issue surfaced in the discovery listing, following the triage-security skill's status-handling rules.

## Status-Handling Rules Reference

Per the triage-security skill (SKILL.md, Discovery Mode, Status-aware handling):

| Current Status | Handling |
|---------------|----------|
| **New** | Proceed with full triage (default path) |
| **In Progress / Code Review / QA** | Warn: "This issue is already in `<status>`. It may be actively worked on." Offer: (1) Proceed with triage anyway, (2) Skip this issue |
| **Modified** | Same as In Progress -- warn and offer proceed/skip |
| **Closed / Done / Resolved** | Warn: "This issue is already closed." Offer: (1) Re-triage, (2) Skip this issue |

---

## Query 1: Untriaged Issues

### TC-9001 -- CVE-2026-40112 h2 [rhtpa-2.2]

- **Status:** New
- **Decision:** Proceed with full triage (default path).
- **Rationale:** Issue is in New status and has not been triaged (no `ai-cve-triaged` label). Standard triage flow starting from Step 0.8 (Assign and Transition to Assigned) through Step 8 (Remediation).
- **Stream scope:** Scoped to 2.2.x (summary suffix `[rhtpa-2.2]`).

### TC-9002 -- CVE-2026-40297 serde_json [rhtpa-2.1]

- **Status:** New
- **Decision:** Proceed with full triage (default path).
- **Rationale:** Issue is in New status and has not been triaged. Standard triage flow applies.
- **Stream scope:** Scoped to 2.1.x (summary suffix `[rhtpa-2.1]`).

### TC-9003 -- CVE-2026-40455 tokio [rhtpa-2.2]

- **Status:** In Progress
- **Decision:** Warn before proceeding.
- **Warning:** "This issue is already in `In Progress`. It may be actively worked on."
- **Options presented to engineer:**
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue
- **Rationale:** The In Progress status indicates someone may already be working on this issue. The engineer must decide whether to proceed or skip. If they choose to proceed, triage continues from Step 0.8 with awareness that some fields may already be populated. If they choose to skip, return to the discovery list.
- **Stream scope:** Scoped to 2.2.x (summary suffix `[rhtpa-2.2]`).

### TC-9004 -- CVE-2026-40518 ring [rhtpa-2.2]

- **Status:** New
- **Decision:** Proceed with full triage (default path).
- **Rationale:** Issue is in New status and has not been triaged. Standard triage flow applies.
- **Stream scope:** Scoped to 2.2.x (summary suffix `[rhtpa-2.2]`).

---

## Query 2: Triaged but still New

### TC-9010 -- CVE-2026-39874 quinn-proto [rhtpa-2.2]

- **Status:** New
- **Decision:** Proceed with full triage (default path), flagged for follow-up.
- **Warning:** This issue carries the `ai-cve-triaged` label but remains in New status. It was previously triaged but never actioned -- it may need follow-up or re-triage.
- **Rationale:** Despite having the `ai-cve-triaged` label, the New status indicates that no downstream action was taken (no assignment, no transition, no remediation tasks created or linked). The engineer should investigate why the prior triage did not result in progress. Since the status is New, the standard triage path applies if the engineer selects this issue. Re-triage may update version impact analysis, correct Affects Versions, or create remediation tasks that were missed previously.
- **Stream scope:** Scoped to 2.2.x (summary suffix `[rhtpa-2.2]`).

---

## Query 3: Ready for QA Candidates

### TC-9020 -- CVE-2026-38901 hyper [rhtpa-2.2]

- **Status:** Modified
- **Decision:** Ready for QA transition candidate.
- **Proposed action:** Transition TC-9020 to ON_QA.
- **Rationale:** All linked remediation Tasks are completed:
  - TC-9021 (Task) -- Done
  - TC-9022 (Task) -- Closed
- **Evidence:** Both linked Depend-type Tasks have reached a terminal status (Done or Closed), confirming that all remediation work for this CVE has been completed. The issue is a candidate for QA verification and ON_QA transition.

### TC-9023 -- CVE-2026-39102 rustls [rhtpa-2.1]

- **Status:** In Progress
- **Decision:** Not ready for QA -- excluded.
- **Rationale:** Remediation task TC-9025 is still In Progress. Only TC-9024 is Done. Until all linked Depend-type Tasks reach Done or Closed status, this CVE cannot move to ON_QA. No action proposed.

### TC-9026 -- CVE-2026-39330 openssl [rhtpa-2.2]

- **Status:** Modified
- **Decision:** Not ready for QA -- excluded.
- **Rationale:** No linked Tasks with Depend type exist. This means either no remediation tasks were created during triage, or the links were not established. Without remediation tasks to verify, this issue cannot be assessed for QA readiness. The engineer should investigate whether remediation tasks need to be created or linked.

---

## Summary of Handling Decisions

| Issue | Status | Category | Decision |
|-------|--------|----------|----------|
| TC-9001 | New | Untriaged | Proceed with full triage |
| TC-9002 | New | Untriaged | Proceed with full triage |
| TC-9003 | In Progress | Untriaged | Warn -- engineer chooses proceed or skip |
| TC-9004 | New | Untriaged | Proceed with full triage |
| TC-9010 | New | Triaged but still New | Proceed with full triage (flagged for follow-up) |
| TC-9020 | Modified | Ready for QA | Propose transition to ON_QA |
| TC-9023 | In Progress | Ready for QA candidate | Excluded -- remediation still in progress |
| TC-9026 | Modified | Ready for QA candidate | Excluded -- no remediation tasks linked |
