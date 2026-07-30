# Discovery Mode: Untriaged Vulnerability Issues

**Project**: TC
**Vulnerability Issue Type ID**: 10024

These values are extracted from the Security Configuration section of the project CLAUDE.md (Jira Configuration: Project key = TC; Security Configuration: Vulnerability issue type ID = 10024).

---

## 1. Untriaged Issues

**JQL Query**:
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

This query finds all Vulnerability issues that have not yet been triaged (i.e., they do not carry the `ai-cve-triaged` label). Results are ordered by status ascending (so active statuses appear first) then by created date descending.

**Results (4 issues)**:

### Status: In Progress

| # | Key | Status | CVE ID | Summary | Created |
|---|-----|--------|--------|---------|---------|
| 1 | TC-9003 | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

### Status: New

| # | Key | Status | CVE ID | Summary | Created |
|---|-----|--------|--------|---------|---------|
| 2 | TC-9001 | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 3 | TC-9002 | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 4 | TC-9004 | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

---

## 2. Triaged but still New

**JQL Query**:
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

These issues were previously triaged (they carry the `ai-cve-triaged` label) but remain in **New** status, meaning they were never actioned after triage. They may need follow-up or re-triage.

**Results (1 issue)**:

| # | Key | Status | CVE ID | Summary | Created |
|---|-----|--------|--------|---------|---------|
| 1 | TC-9010 | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

---

## 3. Ready for QA

**JQL Query**:
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

This query finds triaged Vulnerability issues that are not yet closed or in QA. From these results, only issues where **all** linked remediation Tasks (link type "Depend") are Done or Closed qualify as Ready for QA. Issues with any open linked Task, or with no Depend-type linked Tasks, are excluded.

**Candidates returned (3 issues)**:

| Issue | Status | CVE | Summary | Created | Remediation Tasks (Depend links) | Ready for QA? |
|-------|--------|-----|---------|---------|----------------------------------|---------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Task, Done), TC-9022 (Task, Closed) | Yes |
| TC-9023 | In Progress | CVE-2026-39102 | rustls - Certificate validation bypass [rhtpa-2.1] | 2026-05-10 | TC-9024 (Task, Done), TC-9025 (Task, In Progress) | No - TC-9025 still In Progress |
| TC-9026 | Modified | CVE-2026-39330 | openssl - Buffer overflow in X.509 parsing [rhtpa-2.2] | 2026-05-05 | (no Depend links) | No - no remediation tasks linked |

### Qualified Ready for QA Issues

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

All linked remediation Tasks for TC-9020 are completed (TC-9021 Done, TC-9022 Closed). Consider transitioning TC-9020 to ON_QA.

### Excluded from Ready for QA

- **TC-9023**: Excluded because linked Task TC-9025 is still In Progress. Remediation is not yet complete.
- **TC-9026**: Excluded because no linked Tasks with link type "Depend" exist. There is no remediation work to verify.

---

**Total**: 8 Vulnerability issues found across all queries (4 untriaged, 1 triaged but still New, 3 Ready for QA candidates with 1 qualifying).

Select an issue key to begin triage, or specify an action.
