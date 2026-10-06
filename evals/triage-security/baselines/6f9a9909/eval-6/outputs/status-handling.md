# Status-Aware Handling Decisions

Per the triage-security skill's status-aware handling rules, each discovered issue
is evaluated based on its current Jira status. The handling determines what happens
when an engineer selects the issue for triage.

---

## Query 1: Untriaged Issues

### TC-9001 -- CVE-2026-40112 (h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2])

- **Current status**: New
- **Handling**: Proceed with full triage (default path).
  - Assign to current user, transition to Assigned, and execute Steps 1-8.
  - Stream scope: 2.2.x (from `[rhtpa-2.2]` suffix).

### TC-9002 -- CVE-2026-40297 (serde_json - Stack overflow on deeply nested input [rhtpa-2.1])

- **Current status**: New
- **Handling**: Proceed with full triage (default path).
  - Assign to current user, transition to Assigned, and execute Steps 1-8.
  - Stream scope: 2.1.x (from `[rhtpa-2.1]` suffix).

### TC-9003 -- CVE-2026-40455 (tokio - Race condition in task cancellation [rhtpa-2.2])

- **Current status**: In Progress
- **Handling**: Warn before proceeding.
  - Present warning: "This issue is already in In Progress. It may be actively worked on."
  - Offer choices:
    1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
    2. Skip this issue
  - If engineer chooses to proceed: assign to current user (skip transition since already past Assigned), execute Steps 1-8.
  - If engineer chooses to skip: return to discovery list or end session.
  - Stream scope: 2.2.x (from `[rhtpa-2.2]` suffix).

### TC-9004 -- CVE-2026-40518 (ring - Timing side-channel in RSA verification [rhtpa-2.2])

- **Current status**: New
- **Handling**: Proceed with full triage (default path).
  - Assign to current user, transition to Assigned, and execute Steps 1-8.
  - Stream scope: 2.2.x (from `[rhtpa-2.2]` suffix).

---

## Query 2: Triaged but Still New

### TC-9010 -- CVE-2026-39874 (quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2])

- **Current status**: New
- **Labels**: includes `ai-cve-triaged`
- **Handling**: Proceed with full triage (default path).
  - Although previously triaged (has `ai-cve-triaged` label), the issue is still in New status, indicating it was triaged but never actioned. This may need follow-up or re-triage.
  - Assign to current user, transition to Assigned, and execute Steps 1-8.
  - Stream scope: 2.2.x (from `[rhtpa-2.2]` suffix).

---

## Query 3: Ready for QA Candidates

### TC-9020 -- CVE-2026-38901 (hyper - HTTP request smuggling [rhtpa-2.2])

- **Current status**: Modified
- **Linked remediation tasks**: TC-9021 (Done), TC-9022 (Closed) -- all completed.
- **Handling**: Ready for QA.
  - All linked remediation Tasks with link type "Depend" are Done or Closed.
  - Recommend transitioning to ON_QA.
  - If the engineer selects this issue for full triage (e.g., re-verification): warn "This issue is already in Modified. It may be actively worked on." Offer choices to proceed or skip.

### TC-9023 -- CVE-2026-39102 (rustls - Certificate validation bypass [rhtpa-2.1])

- **Current status**: In Progress
- **Linked remediation tasks**: TC-9024 (Done), TC-9025 (In Progress) -- not all completed.
- **Handling**: Excluded from Ready for QA.
  - TC-9025 is still In Progress; remediation is not complete.
  - If the engineer selects this issue for full triage: warn "This issue is already in In Progress. It may be actively worked on." Offer choices to proceed or skip.
  - Stream scope: 2.1.x (from `[rhtpa-2.1]` suffix).

### TC-9026 -- CVE-2026-39330 (openssl - Buffer overflow in X.509 parsing [rhtpa-2.2])

- **Current status**: Modified
- **Linked remediation tasks**: none with link type "Depend".
- **Handling**: Excluded from Ready for QA.
  - No linked Tasks with type "Depend" found. No remediation to verify.
  - If the engineer selects this issue for full triage: warn "This issue is already in Modified. It may be actively worked on." Offer choices to proceed or skip.
  - Stream scope: 2.2.x (from `[rhtpa-2.2]` suffix).
