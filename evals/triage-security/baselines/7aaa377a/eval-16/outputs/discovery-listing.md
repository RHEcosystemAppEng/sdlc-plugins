# Discovery Mode — Vulnerability Issue Listing

No issue key was provided. Running discovery mode to list untriaged and actionable
Vulnerability issues in project **TC**.

Configuration used (from Security Configuration in CLAUDE.md):
- Project key: **TC**
- Vulnerability issue type ID: **10024**
- Jira version prefix: **RHTPA**

---

## Query 1: Untriaged Issues

**JQL:**
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

**Results (4 issues):**

### Status: New

1. **TC-9001** — New — CVE-2026-40112 — CVE-2026-40112 h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] — Created: 2026-06-08
2. **TC-9002** — New — CVE-2026-40297 — CVE-2026-40297 serde_json - Stack overflow on deeply nested input [rhtpa-2.1] — Created: 2026-06-07
3. **TC-9004** — New — CVE-2026-40518 — CVE-2026-40518 ring - Timing side-channel in RSA verification [rhtpa-2.2] — Created: 2026-06-04

### Status: In Progress

4. **TC-9003** — In Progress — CVE-2026-40455 — CVE-2026-40455 tokio - Race condition in task cancellation [rhtpa-2.2] — Created: 2026-06-05

   > **Warning**: This issue is already in `In Progress`. It may be actively worked on.
   > Options:
   > 1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
   > 2. Skip this issue

### Status-aware handling summary

| Issue | Status | Handling |
|-------|--------|----------|
| TC-9001 | New | Ready for full triage |
| TC-9002 | New | Ready for full triage |
| TC-9004 | New | Ready for full triage |
| TC-9003 | In Progress | Warning — may be actively worked on |

---

## Query 2: Triaged but still New

**JQL:**
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

**Results (1 issue):**

1. **TC-9010** — New — CVE-2026-39874 — CVE-2026-39874 quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] — Created: 2026-05-28

   > This issue was triaged (has `ai-cve-triaged` label) but remains in New status.
   > It may need follow-up or re-triage.

---

## Query 3: Ready for QA Candidates

**JQL:**
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

This query finds triaged CVEs that are still in a pre-QA state. For each result,
linked remediation Tasks (link type "Depend") are checked — only issues where ALL
linked Tasks are Done or Closed qualify as Ready for QA.

**Raw results (3 issues):**

| Key | Summary | Status | Labels | Created | Issue Links |
|-----|---------|--------|--------|---------|-------------|
| TC-9020 | CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2] | Modified | CVE-2026-38901, pscomponent:org/rhtpa-server, ai-cve-triaged | 2026-05-15 | Depend: TC-9021 (Task, Done), TC-9022 (Task, Closed) |
| TC-9023 | CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1] | In Progress | CVE-2026-39102, pscomponent:org/rhtpa-server, ai-cve-triaged | 2026-05-10 | Depend: TC-9024 (Task, Done), TC-9025 (Task, In Progress) |
| TC-9026 | CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2] | Modified | CVE-2026-39330, pscomponent:org/rhtpa-server, ai-cve-triaged | 2026-05-05 | (no Depend links) |

**Filtering results:**

After checking each issue's linked remediation Tasks via the Depend link type:

### Ready for QA

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

> **TC-9020**: All linked remediation Tasks are completed. Consider transitioning to ON_QA.

### Excluded from Ready for QA

| Issue | Status | CVE | Summary | Reason |
|-------|--------|-----|---------|--------|
| TC-9023 | In Progress | CVE-2026-39102 | rustls - Certificate validation bypass [rhtpa-2.1] | TC-9025 still In Progress — remediation not complete |
| TC-9026 | Modified | CVE-2026-39330 | openssl - Buffer overflow in X.509 parsing [rhtpa-2.2] | No linked Tasks with type Depend — no remediation to verify |

---

## Summary

- **3 untriaged issues** ready for full triage (TC-9001, TC-9002, TC-9004)
- **1 untriaged issue** already In Progress — may be actively worked on (TC-9003)
- **1 triaged issue** still in New status — may need follow-up (TC-9010)
- **1 issue** ready for QA transition (TC-9020)
