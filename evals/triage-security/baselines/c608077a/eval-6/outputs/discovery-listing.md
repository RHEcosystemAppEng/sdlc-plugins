# Discovery Mode — Vulnerability Issue Listing

Mode: interactive (no issue key provided → discovery mode). No Jira calls were made; results come from the supplied mock JQL search results.

## Configuration Used (from CLAUDE.md → Project Configuration / Security Configuration)

| Setting | Value | Used for |
|---|---|---|
| Project key | `TC` | `project = TC` |
| Cloud ID | `2b9e35e3-6bd3-4cec-b838-f4249ee02432` | Jira MCP target |
| Vulnerability issue type ID | `10024` | `issuetype = 10024` |
| Jira version prefix | `RHTPA` | Release Jira summary search (`summary ~ 'RHTPA'`) |
| Component label pattern | `pscomponent:` | Component extraction from labels |
| Triage label | `ai-cve-triaged` | Triaged / untriaged split |

## Constructed JQL Queries

**Query 1 — Untriaged issues** (fields: summary, labels, status, created; maxResults: 20)
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

**Query 2 — Triaged but still New** (fields: summary, labels, status, created; maxResults: 10)
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

**Query 3 — Ready for QA candidates** (fields: summary, labels, status, created, issuelinks; maxResults: 20)
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

**Query 4 — Release Jira summary** (fields: summary, status, issuelinks, parent; maxResults: 10)
```
project = TC AND issuetype = Task AND summary ~ 'RHTPA' AND summary ~ 'CVE triage' ORDER BY created DESC
```

---

## 1. Untriaged (4 issues)

### Status: New (3)

| # | Issue | Status | CVE | Summary | Created |
|---|-------|--------|-----|---------|---------|
| 1 | TC-9001 | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 2 | TC-9002 | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 3 | TC-9004 | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

### Status: In Progress (1)

| # | Issue | Status | CVE | Summary | Created |
|---|-------|--------|-----|---------|---------|
| 4 | TC-9003 | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

> TC-9003 is untriaged but already In Progress — it may be actively worked on (see status-handling.md).

All untriaged issues carry component label `pscomponent:org/rhtpa-server`.

---

## 2. Triaged but still New (1 issue) — STALE, needs follow-up

> These issues have the `ai-cve-triaged` label but were never moved forward from New. They may need follow-up or re-triage.

### Status: New (1)

| # | Issue | Status | CVE | Summary | Created |
|---|-------|--------|-----|---------|---------|
| 5 | TC-9010 | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

---

## 3. Ready for QA (1 issue)

Triaged CVEs where ALL linked "Depend" remediation Tasks are Done or Closed:

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

- **TC-9020**: Consider transitioning to ON_QA.

Excluded Query 3 candidates:

| Issue | Status | CVE | Reason excluded |
|-------|--------|-----|-----------------|
| TC-9023 | In Progress | CVE-2026-39102 | TC-9025 (Task) still In Progress — remediation in progress (TC-9024 Done) |
| TC-9026 | Modified | CVE-2026-39330 | No linked Tasks with link type "Depend" — no remediation to verify |

---

## 4. Release Jira Summary

No mock results were provided for Query 4, so the release remediation-progress table cannot be populated. In a live run each matching release Task's `issuelinks` would be counted (Blocks links → remediation done vs. pending; Related links → CVEs tracked) and shown as:

| Release Epic | Release Task | CVEs Tracked | Remediation Done | Remediation Pending |
|-------------|-------------|-------------|-----------------|-------------------|
| (no data) | (no data) | — | — | — |

---

Select an issue number (1-5) to start triage, or a Ready for QA issue to act on.
