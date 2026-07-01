# Status-Aware Handling Decisions

This document describes the handling decision for each issue listed in the discovery results, based on the status-aware handling rules defined in the triage-security skill.

---

## Untriaged Issues

### TC-9001 — CVE-2026-40112 h2 (Status: New)

**Decision:** Proceed with full triage (default path).

New issues receive standard triage: data extraction, version impact analysis, Affects Versions correction, duplicate/sibling check, lifecycle check, already-fixed check, and remediation task creation (Steps 1-8).

---

### TC-9002 — CVE-2026-40297 serde_json (Status: New)

**Decision:** Proceed with full triage (default path).

New issues receive standard triage: data extraction, version impact analysis, Affects Versions correction, duplicate/sibling check, lifecycle check, already-fixed check, and remediation task creation (Steps 1-8).

---

### TC-9003 — CVE-2026-40455 tokio (Status: In Progress)

**Decision:** Warning required before proceeding.

This issue is already in `In Progress`. It may be actively worked on. The engineer must be asked:

> "This issue is already in `In Progress`. It may be actively worked on."
>
> 1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
> 2. Skip this issue

If the engineer chooses to skip, return to the discovery list or end the session.

---

### TC-9004 — CVE-2026-40518 ring (Status: New)

**Decision:** Proceed with full triage (default path).

New issues receive standard triage: data extraction, version impact analysis, Affects Versions correction, duplicate/sibling check, lifecycle check, already-fixed check, and remediation task creation (Steps 1-8).

---

## Triaged but Still New

### TC-9010 — CVE-2026-39874 quinn-proto (Status: New)

**Decision:** Proceed with full triage if selected (default path for New status).

Although this issue has been previously triaged (labeled `ai-cve-triaged`), it remains in New status and was never actioned. If selected by the engineer, full triage proceeds. The engineer may also choose to investigate why the issue stalled after initial triage -- it may need follow-up or re-triage with updated data.

---

## Ready for QA Candidates

### TC-9020 — CVE-2026-38901 hyper (Status: Modified)

**Decision:** Ready for QA transition.

All linked remediation tasks are complete:
- TC-9021: Done
- TC-9022: Closed

This issue qualifies for transition to ON_QA. Consider transitioning TC-9020 to ON_QA.

---

### TC-9023 — CVE-2026-39102 rustls (Status: In Progress)

**Decision:** Not ready for QA -- excluded.

Remediation is still in progress. Linked task status:
- TC-9024: Done
- TC-9025: In Progress

TC-9025 must be completed before this issue can be considered for QA transition.

Additionally, since the status is `In Progress`, if the engineer selects this issue for triage, a warning is required:

> "This issue is already in `In Progress`. It may be actively worked on."

---

### TC-9026 — CVE-2026-39330 openssl (Status: Modified)

**Decision:** Not ready for QA -- excluded.

No linked Tasks with link type "Depend" exist. There is no remediation to verify. This issue may need investigation to determine whether remediation tasks were never created or were removed.
