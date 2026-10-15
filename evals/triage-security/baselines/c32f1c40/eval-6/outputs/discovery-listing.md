# Discovery Mode — Untriaged Vulnerability Issue Listing

No issue key was provided. Running discovery mode to list Vulnerability issues in project **TC**.

## Configuration Used

- **Project key**: TC (from Jira Configuration)
- **Vulnerability issue type ID**: 10024 (from Security Configuration > Product Lifecycle)

---

## Query 1: Untriaged Issues

**JQL query constructed from Security Configuration:**

```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

**Results (4 issues):**

| # | Issue | Status | CVE ID | Summary | Created |
|---|-------|--------|--------|---------|---------|
| 1 | TC-9001 | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 2 | TC-9002 | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 3 | TC-9004 | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |
| 4 | TC-9003 | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

---

## Query 2: Triaged but still New

**JQL query constructed from Security Configuration:**

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

**Results (1 issue):**

| # | Issue | Status | CVE ID | Summary | Created |
|---|-------|--------|--------|---------|---------|
| 1 | TC-9010 | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

This issue was triaged (has `ai-cve-triaged` label) but never moved out of New status. It may need follow-up or re-triage.

---

## Query 3: Ready for QA Candidates

**JQL query constructed from Security Configuration:**

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

**Raw results (3 issues)** — filtered below by linked remediation Task completion status:

### Filtering Logic

For each result, check its `issuelinks` for linked Tasks with link type "Depend":
- **ALL linked remediation Tasks are Done or Closed** --> include in "Ready for QA" list
- **ANY linked Task is still open** --> exclude (remediation in progress)
- **NO linked Tasks with type "Depend" exist** --> exclude (no remediation to verify)

### Filtering Results

| Issue | Status | CVE ID | Linked Remediation Tasks | Qualification |
|-------|--------|--------|--------------------------|---------------|
| TC-9020 | Modified | CVE-2026-38901 | TC-9021 (Done), TC-9022 (Closed) | **Included** -- all Tasks completed |
| TC-9023 | In Progress | CVE-2026-39102 | TC-9024 (Done), TC-9025 (In Progress) | **Excluded** -- TC-9025 still In Progress |
| TC-9026 | Modified | CVE-2026-39330 | (no Depend links) | **Excluded** -- no linked remediation Tasks |

### Ready for QA

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

Consider transitioning TC-9020 to ON_QA -- all linked remediation Tasks are completed.

### Excluded Issues

- **TC-9023** (CVE-2026-39102): Remediation task TC-9025 is still In Progress. Cannot transition to ON_QA until all remediation is complete.
- **TC-9026** (CVE-2026-39330): No linked remediation Tasks with type "Depend". No remediation to verify -- this issue may need investigation.
