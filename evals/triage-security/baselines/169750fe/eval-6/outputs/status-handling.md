# Status-Aware Handling Decisions

Per the triage-security skill's status-aware handling rules, each discovered issue is assessed based on its current Jira status to determine the appropriate triage action.

---

## Untriaged Issues

### TC-9001 -- CVE-2026-40112 (Status: New)

**Decision:** Proceed with full triage (default path).

New status indicates this issue has not been worked on. Standard triage workflow applies: data extraction, version impact analysis, Affects Versions correction, duplicate check, lifecycle check, and remediation task creation.

### TC-9002 -- CVE-2026-40297 (Status: New)

**Decision:** Proceed with full triage (default path).

New status indicates this issue has not been worked on. Standard triage workflow applies.

### TC-9003 -- CVE-2026-40455 (Status: In Progress)

**Decision:** Warning required before proceeding.

This issue is already in "In Progress" status. It may be actively worked on. The engineer must be warned:

> "This issue is already in `In Progress`. It may be actively worked on."

Options presented to the engineer:
1. **Proceed with triage anyway** -- e.g., to verify version impact or update Affects Versions
2. **Skip this issue** -- return to the discovery list or end the session

If the user chooses to skip, return to the discovery list.

### TC-9004 -- CVE-2026-40518 (Status: New)

**Decision:** Proceed with full triage (default path).

New status indicates this issue has not been worked on. Standard triage workflow applies.

---

## Triaged but still New

### TC-9010 -- CVE-2026-39874 (Status: New)

**Decision:** Flag for follow-up or re-triage.

This issue carries the `ai-cve-triaged` label but remains in New status. It was previously triaged but never actioned (no status transition occurred). The engineer should determine whether:
1. The previous triage outcome needs to be reviewed or re-applied
2. Remediation tasks were created but not linked, or failed to create
3. The issue was intentionally left in New after triage (e.g., awaiting upstream fix)

If selected for re-triage, proceed with the full triage workflow (New status allows standard processing).

---

## Ready for QA Candidates

### TC-9020 -- CVE-2026-38901 (Status: Modified)

**Decision:** Ready for QA transition.

All linked remediation Tasks are completed:
- TC-9021: Done
- TC-9022: Closed

Recommendation: Consider transitioning TC-9020 to ON_QA. All remediation work is complete and the CVE is a candidate for QA verification.

### TC-9023 -- CVE-2026-39102 (Status: In Progress)

**Decision:** Not ready for QA -- excluded.

Remediation is still in progress. Linked Task TC-9025 is still in "In Progress" status. TC-9024 is Done, but not all remediation Tasks are complete.

This issue cannot be transitioned to ON_QA until TC-9025 reaches Done or Closed status.

### TC-9026 -- CVE-2026-39330 (Status: Modified)

**Decision:** Not ready for QA -- excluded.

No linked Tasks with type "Depend" exist on this issue. Without remediation Tasks to verify, this issue cannot be evaluated for QA readiness. This may indicate:
- Remediation tasks were never created
- Tasks were created but not linked with "Depend" link type
- The issue was closed as Not a Bug but the status was not updated

The engineer should investigate whether remediation tasks need to be created or linked.
