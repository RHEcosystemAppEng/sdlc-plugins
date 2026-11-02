# Discovery Mode — Vulnerability Issue Listing

## Step 0 — Configuration Extraction

- **Project key**: TC
- **Vulnerability issue type ID**: 10024
- **Jira version prefix**: RHTPA
- **Component label pattern**: pscomponent:

---

## Query 1: Untriaged Issues

**JQL constructed from Security Configuration:**

```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

| # | Issue | Status | CVE ID | Summary | Created |
|---|-------|--------|--------|---------|---------|
| 1 | TC-9001 | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 2 | TC-9002 | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 3 | TC-9003 | **In Progress** | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |
| 4 | TC-9004 | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

### Status-Aware Handling

- **TC-9001** (New): Ready for full triage.
- **TC-9002** (New): Ready for full triage.
- **TC-9003** (In Progress): **Warning — this issue is already in `In Progress`. It may be actively worked on.** Ask whether to proceed with triage anyway or skip this issue.
- **TC-9004** (New): Ready for full triage.

---

## Query 2: Triaged but still New

**JQL constructed from Security Configuration:**

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

| # | Issue | Status | CVE ID | Summary | Created |
|---|-------|--------|--------|---------|---------|
| 1 | TC-9010 | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

These issues have been triaged (carry the `ai-cve-triaged` label) but remain in `New` status — they may need follow-up or re-triage.

---

## Query 3: Ready for QA

**JQL constructed from Security Configuration:**

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

**Candidates returned** (3 issues). Each is filtered by checking its `issuelinks` for linked Tasks with link type `Depend`, then fetching each linked Task's status.

### Ready for QA

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

> Consider transitioning TC-9020 to ON_QA.

### Excluded from Ready for QA

| Issue | Status | CVE | Reason |
|-------|--------|-----|--------|
| TC-9023 | In Progress | CVE-2026-39102 | TC-9025 still In Progress — remediation not complete |
| TC-9026 | Modified | CVE-2026-39330 | No linked Tasks with type Depend — no remediation to verify |
