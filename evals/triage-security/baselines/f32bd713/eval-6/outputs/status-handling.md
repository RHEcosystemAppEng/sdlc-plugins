# Status-Aware Handling Decisions

Per the triage-security skill, when the engineer selects an issue (or a specific issue key is provided), the current Jira status determines the handling path. The three status categories are:

- **New** -- proceed with full triage (default path).
- **In Progress / Code Review / QA** -- warn the engineer that the issue may be actively worked on; offer to proceed with triage anyway or skip.
- **Closed / Done / Resolved** -- warn the engineer that the issue is already closed; offer to re-triage or skip.

---

## Untriaged Issues (Query 1)

### TC-9001 — CVE-2026-40112 (h2) — Status: New

**Handling**: Proceed with full triage (default path).

No warnings required. This issue is in New status and has not been triaged. Begin at Step 0.8 (Assign and Transition to Assigned), then proceed through the complete triage workflow (Steps 1-8).

---

### TC-9002 — CVE-2026-40297 (serde_json) — Status: New

**Handling**: Proceed with full triage (default path).

No warnings required. This issue is in New status and has not been triaged. Begin at Step 0.8 (Assign and Transition to Assigned), then proceed through the complete triage workflow (Steps 1-8).

---

### TC-9003 — CVE-2026-40455 (tokio) — Status: In Progress

**Handling**: Warn — issue may be actively worked on.

Present warning to the engineer:

> "This issue is already in `In Progress`. It may be actively worked on."
>
> Options:
> 1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
> 2. Skip this issue

If the engineer chooses to proceed, begin at Step 1 (Data Extraction) — skip Step 0.8 (Assign and Transition) since the issue is already past New status. The assignment in Step 0.8 still proceeds to ensure the current user is recorded, but the status transition is skipped.

If the engineer chooses to skip, return to the discovery list or end the session.

---

### TC-9004 — CVE-2026-40518 (ring) — Status: New

**Handling**: Proceed with full triage (default path).

No warnings required. This issue is in New status and has not been triaged. Begin at Step 0.8 (Assign and Transition to Assigned), then proceed through the complete triage workflow (Steps 1-8).

---

## Triaged but still New (Query 2)

### TC-9010 — CVE-2026-39874 (quinn-proto) — Status: New

**Handling**: Proceed with full triage (default path), but flag as previously triaged.

This issue carries the `ai-cve-triaged` label but remains in New status. This is anomalous — a triaged issue should have been transitioned beyond New. The engineer should be informed:

> "This issue was previously triaged (has `ai-cve-triaged` label) but is still in New status. It may need re-triage or follow-up to determine why it was not actioned."

Since the status is New, no status-based warning is triggered. If the engineer selects it, proceed with full triage (Steps 0.8 through 8). The re-triage will verify whether the prior triage outcome is still valid and whether remediation tasks were created.

---

## Ready for QA Candidates (Query 3)

### TC-9020 — CVE-2026-38901 (hyper) — Status: Modified

**Handling**: Warn — issue may be actively worked on.

This issue is in Modified status, which falls under the "In Progress / Code Review / QA" category for status-aware handling. Present warning:

> "This issue is already in `Modified`. It may be actively worked on."
>
> Options:
> 1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
> 2. Skip this issue

However, since this is a Ready for QA candidate (all remediation tasks completed), the recommended action is not re-triage but rather transitioning to ON_QA. The engineer should consider transitioning TC-9020 to ON_QA status.

---

### TC-9023 — CVE-2026-39102 (rustls) — Status: In Progress

**Handling**: Warn — issue may be actively worked on.

> "This issue is already in `In Progress`. It may be actively worked on."

This issue has remediation still in progress (TC-9025 is In Progress). It is not a candidate for re-triage or ON_QA transition. Skip unless the engineer specifically wants to verify version impact or update Affects Versions.

---

### TC-9026 — CVE-2026-39330 (openssl) — Status: Modified

**Handling**: Warn — issue may be actively worked on.

> "This issue is already in `Modified`. It may be actively worked on."

This issue has no linked remediation Tasks (no Depend links). It is triaged but has no associated remediation. The engineer may want to investigate whether remediation tasks were expected but not created, or whether the issue was closed as not-affected and then reopened.

---

## Summary Table

| Issue | CVE | Status | Handling Decision | Action |
|-------|-----|--------|-------------------|--------|
| TC-9001 | CVE-2026-40112 | New | Full triage | Assign, transition to Assigned, run Steps 1-8 |
| TC-9002 | CVE-2026-40297 | New | Full triage | Assign, transition to Assigned, run Steps 1-8 |
| TC-9003 | CVE-2026-40455 | In Progress | Warn: may be actively worked on | Ask engineer: proceed or skip |
| TC-9004 | CVE-2026-40518 | New | Full triage | Assign, transition to Assigned, run Steps 1-8 |
| TC-9010 | CVE-2026-39874 | New (triaged) | Full triage with re-triage flag | Flag stale triage, proceed if selected |
| TC-9020 | CVE-2026-38901 | Modified | Ready for QA | Recommend transition to ON_QA |
| TC-9023 | CVE-2026-39102 | In Progress | Warn: may be actively worked on | Remediation in progress, skip recommended |
| TC-9026 | CVE-2026-39330 | Modified | Warn: may be actively worked on | No remediation links, investigate |
