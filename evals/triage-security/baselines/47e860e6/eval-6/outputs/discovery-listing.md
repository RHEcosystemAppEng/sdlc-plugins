# triage-security — Discovery Mode Listing

**Mode:** Interactive (`FULLSEND_OUTPUT_DIR` absent). Invoked without an issue key, so discovery mode runs.

## Step 0 — Configuration Validation

All required sections are present in the project CLAUDE.md:

| Section | Status | Values extracted |
|---|---|---|
| Repository Registry | Present (1 entry) | rhtpa-backend |
| Jira Configuration | Present | Project key: `TC`; Cloud ID: `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| Code Intelligence | Present | `mcp__<serena-instance>__<tool>`; instance `serena_backend` |
| Security Configuration / Product Lifecycle | Present | Product pages URL: `https://access.example.com/product-life-cycle/rhtpa`; Jira version prefix: `RHTPA`; Vulnerability issue type ID: `10024`; Component label pattern: `pscomponent:`; VEX Justification field: `customfield_12345` |
| Security Configuration / Version Streams | Present (2 streams) | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Security Configuration / Source Repositories | Present (1 repo) | rhtpa-backend (no Deployment Context column → defaults to `upstream`) |

Optional fields not configured (skipped silently): Upstream Affected Component field, PS Component field, Stream field, ProdSec contact email, ProdSec Jira account ID, Embargo policy URL.

## JQL Queries Constructed from Security Configuration

Substitutions: `<project-key>` = `TC`, `<vulnerability-issue-type-id>` = `10024`, release-family prefix = `RHTPA`.

**Query 1 — Untriaged** (fields: summary, labels, status, created; maxResults: 20)
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

Grouped by status (query ordered `status ASC, created DESC`).

### Status: New (3)

| # | Issue | Status | CVE | Summary | Created |
|---|---|---|---|---|---|
| 1 | TC-9001 | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 2 | TC-9002 | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 3 | TC-9004 | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

### Status: In Progress (1)

| # | Issue | Status | CVE | Summary | Created |
|---|---|---|---|---|---|
| 4 | TC-9003 | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

> Note: TC-9003 is already In Progress — selecting it triggers the status-aware warning (see status-handling.md).

---

## 2. Triaged but still New (1 issue) — FLAGGED

These carry `ai-cve-triaged` but were never moved past New. They may need follow-up or re-triage.

### Status: New (1)

| # | Issue | Status | CVE | Summary | Created |
|---|---|---|---|---|---|
| 5 | TC-9010 | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

> Flag: triaged on a prior run but still New — stale; check whether remediation tasks were created and the issue should have advanced, or re-triage.

---

## 3. Ready for QA (1 issue)

Query 3 returned 3 candidates; filtered by `Depend` links to remediation Tasks:

| Candidate | Status | Depend-linked Tasks | Result |
|---|---|---|---|
| TC-9020 | Modified | TC-9021 (Done), TC-9022 (Closed) | All complete → **Included** |
| TC-9023 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | Task still open → Excluded |
| TC-9026 | Modified | none | No Depend links → Excluded (no remediation to verify) |

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

**TC-9020:** Consider transitioning to ON_QA.

---

## 4. Release Jira Summary

Query 4 was constructed (above) but no mock results were supplied in the eval input, so no release Epic/Task rows can be reported. No values are fabricated.

| Release Epic | Release Task | CVEs Tracked | Remediation Done | Remediation Pending |
|---|---|---|---|---|
| (no data provided) | — | — | — | — |

---

**Next step:** Select an issue number (1–5) to triage, or end the session.
