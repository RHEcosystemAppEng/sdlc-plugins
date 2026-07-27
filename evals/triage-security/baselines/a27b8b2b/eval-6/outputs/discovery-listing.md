# Discovery Mode — Vulnerability Issue Listing

No issue key was provided. Running discovery mode to list untriaged and actionable
Vulnerability issues in the project.

## Configuration Used

- **Project key**: TC (from Jira Configuration)
- **Vulnerability issue type ID**: 10024 (from Security Configuration > Product Lifecycle)

---

## Query 1: Untriaged Issues

**JQL query constructed from Security Configuration:**

```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

**Results** (4 issues):

| # | Issue | Status | CVE ID | Summary | Created |
|---|-------|--------|--------|---------|---------|
| 1 | TC-9001 | New | CVE-2026-40112 | CVE-2026-40112 h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 2 | TC-9002 | New | CVE-2026-40297 | CVE-2026-40297 serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 3 | TC-9003 | In Progress | CVE-2026-40455 | CVE-2026-40455 tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |
| 4 | TC-9004 | New | CVE-2026-40518 | CVE-2026-40518 ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

> **Warning**: TC-9003 is currently **In Progress**. It may be actively worked on by
> another engineer. If selected for triage, you will be prompted to confirm whether
> to proceed or skip.

---

## Query 2: Triaged but still New

**JQL query constructed from Security Configuration:**

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

These issues were previously triaged (they carry the `ai-cve-triaged` label) but remain
in **New** status, meaning they were never actioned after triage. They may need follow-up
or re-triage.

**Results** (1 issue):

| # | Issue | Status | CVE ID | Summary | Created |
|---|-------|--------|--------|---------|---------|
| 1 | TC-9010 | New | CVE-2026-39874 | CVE-2026-39874 quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

> **Note**: TC-9010 was triaged but never moved beyond New status. Consider re-triaging
> to verify the original assessment is still valid, or manually transitioning to the
> appropriate status.

---

## Query 3: Ready for QA

**JQL query constructed from Security Configuration:**

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

This query returns triaged CVEs still in a pre-QA state. Each result is then filtered
by checking whether ALL linked remediation Tasks (via "Depend" link type) have been
completed (status Done or Closed).

**Candidate Results** (3 issues before filtering):

### Filtering Analysis

- **TC-9020** (CVE-2026-38901): Linked remediation tasks: TC-9021 (Done), TC-9022 (Closed).
  ALL linked Tasks are completed. **INCLUDED** in Ready for QA.

- **TC-9023** (CVE-2026-39102): Linked remediation tasks: TC-9024 (Done), TC-9025 (In Progress).
  TC-9025 is still In Progress -- remediation is not yet complete. **EXCLUDED**.

- **TC-9026** (CVE-2026-39330): No linked Tasks with type "Depend" found.
  No remediation to verify. **EXCLUDED**.

### Ready for QA Issues

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

> Consider transitioning TC-9020 to **ON_QA** -- all linked remediation tasks have been completed.

---

## Summary

- **3 untriaged New issues** ready for full triage: TC-9001, TC-9002, TC-9004
- **1 untriaged In Progress issue** requiring caution: TC-9003 (may be actively worked on)
- **1 triaged-but-still-New issue** needing follow-up: TC-9010
- **1 issue ready for QA transition**: TC-9020

Select an issue key to begin triage, or choose from the Ready for QA list to
transition to ON_QA.
