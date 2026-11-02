# Discovery Mode — Vulnerability Issue Listing

## Step 0 — Configuration Extracted

- **Project key**: TC
- **Vulnerability issue type ID**: 10024
- **Jira version prefix**: RHTPA

---

## Query 1: Untriaged Issues

**JQL:**
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

**Results (4 issues):**

| # | Issue | Status | CVE ID | Summary | Created |
|---|-------|--------|--------|---------|---------|
| 1 | TC-9001 | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 2 | TC-9002 | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 3 | TC-9003 | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |
| 4 | TC-9004 | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

---

## Query 2: Triaged but still New

**JQL:**
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

**Results (1 issue):**

| # | Issue | Status | CVE ID | Summary | Created |
|---|-------|--------|--------|---------|---------|
| 1 | TC-9010 | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

> **Note:** This issue was previously triaged (has `ai-cve-triaged` label) but remains in New status. It may need follow-up or re-triage to determine why it was not actioned.

---

## Query 3: Ready for QA

**JQL:**
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

**Candidates evaluated (3 issues):**

For each candidate, linked remediation Tasks (link type "Depend") were inspected to determine completion status.

### Qualified — Ready for QA

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

> Consider transitioning TC-9020 to ON_QA — all linked remediation Tasks are completed.

### Excluded

| Issue | Status | CVE | Reason for Exclusion |
|-------|--------|-----|---------------------|
| TC-9023 | In Progress | CVE-2026-39102 | TC-9025 still In Progress — remediation is not complete |
| TC-9026 | Modified | CVE-2026-39330 | No linked Tasks with type "Depend" — no remediation to verify |
