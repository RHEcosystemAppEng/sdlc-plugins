# Security Vulnerability Discovery — Project TC

Discovery mode invoked without an issue key. Running three JQL queries to surface untriaged, stale, and QA-ready Vulnerability issues.

## Configuration

- Project key: TC
- Vulnerability issue type ID: 10024
- Jira version prefix: RHTPA

---

## 1. Untriaged Issues

**JQL**: `project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC`

4 untriaged Vulnerability issues found:

### Status: New

1. **TC-9001** — New — CVE-2026-40112 — h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] — Created: 2026-06-08
2. **TC-9002** — New — CVE-2026-40297 — serde_json - Stack overflow on deeply nested input [rhtpa-2.1] — Created: 2026-06-07
3. **TC-9004** — New — CVE-2026-40518 — ring - Timing side-channel in RSA verification [rhtpa-2.2] — Created: 2026-06-04

### Status: In Progress

4. **TC-9003** — In Progress — CVE-2026-40455 — tokio - Race condition in task cancellation [rhtpa-2.2] — Created: 2026-06-05

---

## 2. Triaged but still New

**JQL**: `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC`

1 triaged-but-stale issue found. These issues were triaged but never moved forward and may need follow-up or re-triage:

1. **TC-9010** — New — CVE-2026-39874 — quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] — Created: 2026-05-28

---

## 3. Ready for QA

**JQL**: `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC`

3 candidate issues returned. For each, linked Tasks with link type "Depend" are inspected to determine if all remediation is complete.

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

**TC-9020**: All linked remediation Tasks are completed (TC-9021 Done, TC-9022 Closed). Consider transitioning to ON_QA.

**Excluded from Ready for QA:**
- **TC-9023** (CVE-2026-39102, rustls - Certificate validation bypass [rhtpa-2.1]): TC-9025 is still In Progress -- remediation is not complete.
- **TC-9026** (CVE-2026-39330, openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]): No linked Tasks with type "Depend" -- no remediation to verify.

---

To begin triage on an untriaged issue, provide the issue key (e.g., `/sdlc-workflow:triage-security TC-9001`).
