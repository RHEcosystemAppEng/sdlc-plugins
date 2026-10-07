# Discovery Mode: Untriaged Vulnerability Issues

**Project**: TC
**Vulnerability issue type ID**: 10024
**Jira version prefix**: RHTPA
**Date**: 2026-10-07

---

## 1. Untriaged Issues

**JQL**:
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

**Results**: 4 issues

### Status: New (3 issues)

| # | Issue | CVE | Summary | Created |
|---|-------|-----|---------|---------|
| 1 | TC-9001 | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 2 | TC-9002 | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 3 | TC-9004 | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

### Status: In Progress (1 issue)

| # | Issue | CVE | Summary | Created |
|---|-------|-----|---------|---------|
| 4 | TC-9003 | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

---

## 2. Triaged but still New

**JQL**:
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

**Results**: 1 issue

These issues were triaged (carry the `ai-cve-triaged` label) but remain in New status -- they may need follow-up or re-triage.

| # | Issue | CVE | Summary | Created |
|---|-------|-----|---------|---------|
| 1 | TC-9010 | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

---

## 3. Ready for QA

**JQL**:
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

**Results**: 3 candidates evaluated, 1 qualifies

### Qualified for QA transition

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

All linked remediation Tasks are completed. Consider transitioning to ON_QA.

### Excluded from Ready for QA

| Issue | Status | CVE | Reason |
|-------|--------|-----|--------|
| TC-9023 | In Progress | CVE-2026-39102 | Remediation in progress -- TC-9025 still In Progress |
| TC-9026 | Modified | CVE-2026-39330 | No linked remediation Tasks (no Depend links) |

---

## 4. Release Jira Summary

**JQL**:
```
project = TC AND issuetype = Task AND summary ~ 'RHTPA' AND summary ~ 'CVE triage' ORDER BY created DESC
```

**Results**: No release Tasks found matching the query pattern.

No release Jira structure has been created yet. Release Epics and Tasks will be created during individual issue triage (Step 7.5) as needed.
