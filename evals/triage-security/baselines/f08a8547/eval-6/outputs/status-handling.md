# Status-Aware Handling Decisions

Per the triage-security skill, when a user selects an issue (or provides an issue key directly), its current Jira status determines the handling path. Below is the status-aware handling decision for each issue returned by the discovery queries.

---

## Untriaged Issues (Query 1)

### TC-9001 -- CVE-2026-40112 (h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2])
- **Current status**: New
- **Handling**: Proceed with full triage (default path). No warnings needed. Execute Steps 0.7 through 8 in sequence: assign and transition to Assigned, extract CVE data, enrich from external databases, perform version impact analysis across configured streams (2.1.x, 2.2.x), correct Affects Versions, check for duplicates/siblings, verify lifecycle status, check for already-fixed scenarios, and create remediation tasks or close as appropriate.

### TC-9002 -- CVE-2026-40297 (serde_json - Stack overflow on deeply nested input [rhtpa-2.1])
- **Current status**: New
- **Handling**: Proceed with full triage (default path). No warnings needed. Same full Step 0.7--8 sequence as above.

### TC-9003 -- CVE-2026-40455 (tokio - Race condition in task cancellation [rhtpa-2.2])
- **Current status**: In Progress
- **Handling**: Warn the user before proceeding.

  > "This issue is already in `In Progress`. It may be actively worked on."

  Present the following options:
  1. **Proceed with triage anyway** -- e.g., to verify version impact or update Affects Versions
  2. **Skip this issue** -- return to the discovery list or end the session

  Do not begin triage until the user explicitly chooses an option.

### TC-9004 -- CVE-2026-40518 (ring - Timing side-channel in RSA verification [rhtpa-2.2])
- **Current status**: New
- **Handling**: Proceed with full triage (default path). No warnings needed. Same full Step 0.7--8 sequence as above.

---

## Triaged but Still New (Query 2)

### TC-9010 -- CVE-2026-39874 (quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2])
- **Current status**: New
- **Labels**: ai-cve-triaged (already triaged)
- **Handling**: This issue was previously triaged (carries the `ai-cve-triaged` label) but remains in New status, indicating it was triaged but never actioned (no transition out of New, no remediation tasks moved forward). If the user selects this issue:
  - The status is New, so the default path applies: proceed with full triage.
  - However, since it already has the `ai-cve-triaged` label, this would effectively be a re-triage. The user should be informed that this issue was previously triaged and may need follow-up or re-triage to determine why it stalled in New status.

---

## Ready for QA Candidates (Query 3)

### TC-9020 -- CVE-2026-38901 (hyper - HTTP request smuggling [rhtpa-2.2])
- **Current status**: Modified
- **Labels**: ai-cve-triaged
- **Linked remediation tasks**: TC-9021 (Done), TC-9022 (Closed)
- **Handling**: All linked remediation Tasks (link type "Depend") are completed (Done or Closed). This issue qualifies as Ready for QA. The recommended action is to transition TC-9020 to ON_QA status.

  If the user selects this issue for triage rather than QA transition:
  - The status is Modified, which falls under the "In Progress / Code Review / QA" warning category.
  - Warn the user:

    > "This issue is already in `Modified`. It may be actively worked on."

  - Present options to proceed with triage anyway or skip.

### TC-9023 -- CVE-2026-39102 (rustls - Certificate validation bypass [rhtpa-2.1])
- **Current status**: In Progress
- **Labels**: ai-cve-triaged
- **Linked remediation tasks**: TC-9024 (Done), TC-9025 (In Progress)
- **Handling**: Excluded from Ready for QA because TC-9025 is still In Progress -- remediation is not yet complete. If the user selects this issue:
  - Warn: "This issue is already in `In Progress`. It may be actively worked on."
  - Present options to proceed with triage anyway or skip.
  - Since TC-9025 is still being worked on, the most useful action may be to check on the progress of TC-9025 rather than re-triaging.

### TC-9026 -- CVE-2026-39330 (openssl - Buffer overflow in X.509 parsing [rhtpa-2.2])
- **Current status**: Modified
- **Labels**: ai-cve-triaged
- **Linked remediation tasks**: None (no "Depend" links)
- **Handling**: Excluded from Ready for QA because there are no linked remediation Tasks with link type "Depend" -- there is no remediation to verify. If the user selects this issue:
  - Warn: "This issue is already in `Modified`. It may be actively worked on."
  - Present options to proceed with triage anyway or skip.
  - The absence of remediation tasks despite having the `ai-cve-triaged` label suggests this issue may have been closed as Not a Bug or handled through a different mechanism. Investigation may be warranted.

---

## Summary Table

| Issue | Status | Handling Decision | Action Required Before Triage |
|-------|--------|-------------------|-------------------------------|
| TC-9001 | New | Full triage | None |
| TC-9002 | New | Full triage | None |
| TC-9003 | In Progress | Warn -- may be actively worked on | User must choose: proceed or skip |
| TC-9004 | New | Full triage | None |
| TC-9010 | New (stale) | Full triage (re-triage) | Inform user of prior triage |
| TC-9020 | Modified | Ready for QA transition recommended | User confirmation for ON_QA transition |
| TC-9023 | In Progress | Excluded from QA; warn if selected | User must choose: proceed or skip |
| TC-9026 | Modified | Excluded from QA (no tasks); warn if selected | User must choose: proceed or skip |
