# Discovery Mode — Vulnerability Issue Listing

No issue key was provided. Running discovery mode to list untriaged and actionable Vulnerability issues in project **TC**.

## Configuration Used

- **Project key**: TC (from Jira Configuration)
- **Vulnerability issue type ID**: 10024 (from Security Configuration)

---

## Query 1: Untriaged Issues

**JQL constructed from Security Configuration:**

```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

The project key `TC` and vulnerability issue type ID `10024` are read from the project's CLAUDE.md Security Configuration -- not hardcoded.

**Results** (4 issues):

### Status: New

| # | Issue | Status | CVE ID | Summary | Created |
|---|-------|--------|--------|---------|---------|
| 1 | TC-9001 | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 2 | TC-9002 | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 3 | TC-9004 | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

### Status: In Progress

| # | Issue | Status | CVE ID | Summary | Created |
|---|-------|--------|--------|---------|---------|
| 4 | TC-9003 | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

> **Warning**: TC-9003 is already in `In Progress`. It may be actively worked on. Selecting this issue for triage will prompt whether to proceed or skip.

---

## Query 2: Triaged but still New

**JQL constructed from Security Configuration:**

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

**Results** (1 issue):

| # | Issue | Status | CVE ID | Summary | Created |
|---|-------|--------|--------|---------|---------|
| 1 | TC-9010 | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

> These issues were previously triaged (labeled `ai-cve-triaged`) but remain in `New` status. They may need follow-up or re-triage to determine why they were never actioned.

---

## Query 3: Ready for QA

**JQL constructed from Security Configuration:**

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

This query finds triaged CVEs that are still in a pre-QA state. For each result, the linked remediation Tasks (link type "Depend") are inspected to determine if all remediation is complete.

**Candidates returned** (3 issues evaluated):

### Filtering Analysis

| Issue | Status | CVE | Linked Remediation Tasks | All Tasks Complete? | Ready for QA? |
|-------|--------|-----|--------------------------|---------------------|---------------|
| TC-9020 | Modified | CVE-2026-38901 | TC-9021 (Done), TC-9022 (Closed) | Yes | **Yes** |
| TC-9023 | In Progress | CVE-2026-39102 | TC-9024 (Done), TC-9025 (In Progress) | No -- TC-9025 still In Progress | **No** (excluded) |
| TC-9026 | Modified | CVE-2026-39330 | (no Depend links) | N/A -- no remediation tasks linked | **No** (excluded) |

### Ready for QA

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

> Consider transitioning TC-9020 to ON_QA. All linked remediation Tasks (TC-9021, TC-9022) are completed.

### Excluded from Ready for QA

- **TC-9023** (CVE-2026-39102): Excluded because linked Task TC-9025 is still `In Progress`. Remediation is not complete.
- **TC-9026** (CVE-2026-39330): Excluded because no linked Tasks with type "Depend" exist. There is no remediation to verify.

---

## Summary

- **Untriaged**: 4 issues available for triage (3 New, 1 In Progress)
- **Triaged but still New**: 1 issue may need follow-up
- **Ready for QA**: 1 issue (TC-9020) is ready for ON_QA transition

Select an issue key from the untriaged list to begin full triage, or choose a triaged-but-new issue to re-examine.
