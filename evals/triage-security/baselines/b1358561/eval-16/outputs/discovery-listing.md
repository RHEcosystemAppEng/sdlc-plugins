# triage-security — Discovery Mode Listing

**Project:** TC | **Vulnerability issue type ID:** 10024 | **Jira version prefix:** RHTPA
**Mode:** Interactive discovery (no issue key provided)

Configuration check (Step 0): Repository Registry, Jira Configuration (Project key TC,
Cloud ID present), Code Intelligence, and Security Configuration (Product Lifecycle,
Version Streams 2.1.x / 2.2.x, Source Repositories) are all present — proceeding.

> Source: mock JQL results (discovery-mode-results.md). No live Jira calls were made.

---

## 1. Untriaged (4 issues)

JQL: `project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC`

### Status: In Progress

1. **TC-9003** — In Progress — CVE-2026-40455 — tokio - Race condition in task cancellation [rhtpa-2.2] — created 2026-06-05
   - Note: already In Progress; if selected, you will be warned it may be actively worked on.

### Status: New

2. **TC-9001** — New — CVE-2026-40112 — h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] — created 2026-06-08
3. **TC-9002** — New — CVE-2026-40297 — serde_json - Stack overflow on deeply nested input [rhtpa-2.1] — created 2026-06-07
4. **TC-9004** — New — CVE-2026-40518 — ring - Timing side-channel in RSA verification [rhtpa-2.2] — created 2026-06-04

---

## 2. Triaged but still New (1 issue) — needs follow-up

JQL: `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC`

1. **TC-9010** — New — CVE-2026-39874 — quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] — created 2026-05-28
   - FLAG: carries `ai-cve-triaged` but was never moved past New. May need follow-up or re-triage.

---

## 3. Ready for QA (1 issue)

JQL: `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC`
(3 candidates returned; filtered on "Depend" issue links — see ready-for-qa.md)

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

- **TC-9020:** Consider transitioning to ON_QA.

Excluded candidates:
- TC-9023 (CVE-2026-39102, rustls, In Progress) — remediation still in progress (TC-9025 In Progress).
- TC-9026 (CVE-2026-39330, openssl, Modified) — no "Depend" links; no remediation to verify.

---

## 4. Release Jira Summary

JQL: `project = TC AND issuetype = Task AND summary ~ 'RHTPA' AND summary ~ 'CVE triage' ORDER BY created DESC`

No release Task results were provided in the mock data, so this summary can't be
populated. (No data was invented.)

---

**Next step:** Select an issue key to triage (e.g. `TC-9001`), or choose a Ready for QA
issue to transition to ON_QA. Any Jira transition will need your explicit confirmation.
