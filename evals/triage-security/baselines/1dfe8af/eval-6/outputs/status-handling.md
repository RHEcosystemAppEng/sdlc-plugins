# Status-Aware Handling Decisions

This document describes the handling decision for each issue found during discovery, based on its current Jira status and the status-aware handling rules defined in the triage-security skill.

---

## Untriaged Issues

### TC-9001 — Status: New

**Decision**: Proceed with full triage (default path).

TC-9001 is in New status, which is the standard entry point for triage. This issue tracks CVE-2026-40112 (h2 - HTTP/2 rapid reset vulnerability) scoped to stream rhtpa-2.2. Full triage steps 1 through 7 apply: data extraction, version impact analysis, Affects Versions correction, duplicate/sibling check, lifecycle check, already-fixed check, and remediation.

---

### TC-9002 — Status: New

**Decision**: Proceed with full triage (default path).

TC-9002 is in New status. This issue tracks CVE-2026-40297 (serde_json - Stack overflow on deeply nested input) scoped to stream rhtpa-2.1. Full triage steps 1 through 7 apply.

---

### TC-9003 — Status: In Progress

**Decision**: Warn — this issue is already actively being worked on.

> Warning: TC-9003 is currently in `In Progress` status. It may be actively worked on.

This issue tracks CVE-2026-40455 (tokio - Race condition in task cancellation) scoped to stream rhtpa-2.2. Before proceeding, the engineer should choose:

1. **Proceed with triage anyway** — useful to verify version impact or update Affects Versions even while work is in progress.
2. **Skip this issue** — return to the discovery list.

---

### TC-9004 — Status: New

**Decision**: Proceed with full triage (default path).

TC-9004 is in New status. This issue tracks CVE-2026-40518 (ring - Timing side-channel in RSA verification) scoped to stream rhtpa-2.2. Full triage steps 1 through 7 apply.

---

## Triaged but still New

### TC-9010 — Status: New (previously triaged)

**Decision**: Flag for follow-up or re-triage.

TC-9010 carries the `ai-cve-triaged` label but remains in New status, meaning it was triaged previously but never moved forward. This issue tracks CVE-2026-39874 (quinn-proto - Panic on malformed QUIC frame) scoped to stream rhtpa-2.2.

The engineer should determine why it stalled:
- Were remediation tasks created but not linked?
- Was it triaged as "not affected" but never closed?
- Does it need re-triage with updated data?

If the engineer selects this issue, full triage (steps 1-7) applies since the status is New.

---

## Ready for QA Candidates

### TC-9020 — Status: Modified

**Decision**: Ready for QA transition.

All linked remediation Tasks are complete:
- TC-9021: Done
- TC-9022: Closed

This issue tracks CVE-2026-38901 (hyper - HTTP request smuggling) scoped to stream rhtpa-2.2. All remediation work is finished. Consider transitioning to ON_QA for verification.

---

### TC-9023 — Status: In Progress

**Decision**: Excluded from Ready for QA — remediation still in progress.

Linked Task status:
- TC-9024: Done
- TC-9025: **In Progress**

This issue tracks CVE-2026-39102 (rustls - Certificate validation bypass) scoped to stream rhtpa-2.1. TC-9025 is still being worked on, so this CVE is not ready for QA verification. It will become eligible once TC-9025 reaches Done or Closed status.

---

### TC-9026 — Status: Modified

**Decision**: Excluded from Ready for QA — no remediation tasks to verify.

This issue tracks CVE-2026-39330 (openssl - Buffer overflow in X.509 parsing) scoped to stream rhtpa-2.2. It has no linked Tasks with link type "Depend", meaning there is no remediation work to verify. This issue may need investigation to determine whether remediation tasks should be created or whether it should be closed.
