# Status-Aware Handling Decisions

Per SKILL.md "Status-aware handling" rules, each discovered issue is evaluated based on its current Jira status to determine the appropriate triage path.

---

## Untriaged Issues (Query 1)

### TC-9001 — CVE-2026-40112 (h2) [rhtpa-2.2]
- **Current status:** New
- **Handling decision:** Proceed with full triage (default path).
- **Rationale:** "New" status indicates the issue has not been worked on. Standard triage applies: run Steps 1 through 7 to extract CVE data, analyze version impact across streams 2.1.x and 2.2.x, correct Affects Versions, check for duplicates/siblings, verify lifecycle status, and produce remediation tasks or close recommendation.
- **Stream scope:** 2.2.x (from summary suffix `[rhtpa-2.2]`)

### TC-9002 — CVE-2026-40297 (serde_json) [rhtpa-2.1]
- **Current status:** New
- **Handling decision:** Proceed with full triage (default path).
- **Rationale:** "New" status indicates the issue has not been worked on. Standard triage applies.
- **Stream scope:** 2.1.x (from summary suffix `[rhtpa-2.1]`)

### TC-9003 — CVE-2026-40455 (tokio) [rhtpa-2.2]
- **Current status:** In Progress
- **Handling decision:** Warn the engineer before proceeding.
- **Proposed warning:**
  > "This issue is already in `In Progress`. It may be actively worked on."
  > Options:
  > 1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  > 2. Skip this issue
- **Rationale:** Per the status-aware handling rules, issues in "In Progress" (or Code Review, QA) require a warning that work may already be underway. The engineer must confirm whether to proceed with triage or skip. Triage may still be valuable to verify version impact and Affects Versions accuracy, even if remediation is already in flight.
- **Stream scope:** 2.2.x (from summary suffix `[rhtpa-2.2]`)

### TC-9004 — CVE-2026-40518 (ring) [rhtpa-2.2]
- **Current status:** New
- **Handling decision:** Proceed with full triage (default path).
- **Rationale:** "New" status indicates the issue has not been worked on. Standard triage applies.
- **Stream scope:** 2.2.x (from summary suffix `[rhtpa-2.2]`)

---

## Triaged but still New (Query 2)

### TC-9010 — CVE-2026-39874 (quinn-proto) [rhtpa-2.2]
- **Current status:** New
- **Labels include:** ai-cve-triaged
- **Handling decision:** Proceed with full triage if selected (default "New" path), but flag as stale.
- **Proposed warning:**
  > "This issue was previously triaged (`ai-cve-triaged` label present) but remains in `New` status. It may need follow-up or re-triage."
  > Options:
  > 1. Re-triage (e.g., to verify triage outcomes are still current, check if remediation tasks were created, or update analysis with newer data)
  > 2. Skip this issue
- **Rationale:** The issue carries the `ai-cve-triaged` label indicating prior triage occurred, yet it never progressed past "New". This is a stale issue — either remediation tasks were not created, were created but not linked, or follow-up was dropped. Re-triage can verify whether the prior analysis is still valid and whether remediation exists.
- **Stream scope:** 2.2.x (from summary suffix `[rhtpa-2.2]`)

---

## Ready for QA Candidates (Query 3)

### TC-9020 — CVE-2026-38901 (hyper) [rhtpa-2.2]
- **Current status:** Modified
- **Labels include:** ai-cve-triaged
- **Linked remediation tasks:** TC-9021 (Done), TC-9022 (Closed) — ALL complete
- **Handling decision:** Ready for QA transition.
- **Proposed action:** Transition TC-9020 from Modified to ON_QA. All linked remediation tasks (TC-9021, TC-9022) are in terminal states (Done/Closed), confirming that remediation is complete and the fix is ready for verification.
- **Stream scope:** 2.2.x (from summary suffix `[rhtpa-2.2]`)

### TC-9023 — CVE-2026-39102 (rustls) [rhtpa-2.1]
- **Current status:** In Progress
- **Labels include:** ai-cve-triaged
- **Linked remediation tasks:** TC-9024 (Done), TC-9025 (In Progress)
- **Handling decision:** Not ready for QA — excluded.
- **Rationale:** TC-9025 is still In Progress, meaning remediation is not yet complete. This issue should remain in its current status until all linked remediation tasks reach a terminal state. No action proposed at this time.
- **Stream scope:** 2.1.x (from summary suffix `[rhtpa-2.1]`)

### TC-9026 — CVE-2026-39330 (openssl) [rhtpa-2.2]
- **Current status:** Modified
- **Labels include:** ai-cve-triaged
- **Linked remediation tasks:** None (no Depend links)
- **Handling decision:** Not ready for QA — excluded.
- **Rationale:** No linked remediation tasks with type "Depend" exist. Without remediation tasks, there is nothing to verify in QA. This issue may need investigation: either remediation tasks were never created (incomplete triage), or the issue was handled through a different mechanism. Consider re-triaging to determine if remediation tasks are needed or if the issue should be closed.
- **Proposed follow-up:**
  > "TC-9026 has `ai-cve-triaged` label and `Modified` status but no linked remediation tasks. Consider re-triaging to determine whether remediation is needed or whether the issue should be closed."
