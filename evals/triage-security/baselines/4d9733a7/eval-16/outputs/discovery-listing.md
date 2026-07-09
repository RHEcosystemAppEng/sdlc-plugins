# Discovery Mode -- Vulnerability Issue Listing

## Step 0 -- Configuration

From Security Configuration:
- Project key: **TC**
- Vulnerability issue type ID: **10024**

## Query 1: Untriaged Issues

**JQL constructed**:
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

### Results (4 issues)

| # | Issue | Status | CVE ID | Summary | Created |
|---|-------|--------|--------|---------|---------|
| 1 | TC-9001 | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 2 | TC-9002 | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 3 | TC-9004 | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |
| 4 | TC-9003 | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

**Status-aware handling:**
- TC-9001 (New): Ready for full triage
- TC-9002 (New): Ready for full triage
- TC-9004 (New): Ready for full triage
- TC-9003 (In Progress): **WARNING** -- This issue is already in `In Progress`. It may be actively worked on. Proceed with caution or skip.

---

## Query 2: Triaged but still New

**JQL constructed**:
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

### Results (1 issue)

| # | Issue | Status | CVE ID | Summary | Created |
|---|-------|--------|--------|---------|---------|
| 1 | TC-9010 | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

This issue was previously triaged (has `ai-cve-triaged` label) but remains in New status. It may need follow-up or re-triage.

---

## Query 3: Ready for QA Candidates

**JQL constructed**:
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

### Results (3 issues returned, 1 qualified)

For each result, the skill checks `issuelinks` for linked Tasks with link type "Depend" and fetches each linked Task's status to determine if all remediation is complete.

#### Ready for QA

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

**TC-9020**: ALL linked remediation Tasks are completed (TC-9021 Done, TC-9022 Closed). Consider transitioning to ON_QA.

#### Excluded from Ready for QA

| Issue | Status | CVE | Reason for Exclusion |
|-------|--------|-----|----------------------|
| TC-9023 | In Progress | CVE-2026-39102 | TC-9025 still In Progress -- remediation not complete |
| TC-9026 | Modified | CVE-2026-39330 | No linked Tasks with type "Depend" -- no remediation to verify |
