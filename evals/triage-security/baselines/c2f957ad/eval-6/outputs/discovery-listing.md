# triage-security — Discovery Mode Listing

Invoked without an issue key → discovery mode (interactive; `FULLSEND_OUTPUT_DIR` not set).

## Step 0 – Configuration validation

All required sections are present in CLAUDE.md (`claude-md-security-config.md`):

| Required item | Value |
|---|---|
| Repository Registry | rhtpa-backend (1 entry) |
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Code Intelligence | present, naming convention `mcp__<serena-instance>__<tool>` |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field (optional) | customfield_12345 |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend |

Optional fields not configured (skipped silently): Upstream Affected Component, PS Component, Stream custom field, ProdSec contact email / account ID, Embargo policy URL.

## JQL queries constructed from Security Configuration

Substitutions: `<project-key>` = `TC`, `<vulnerability-issue-type-id>` = `10024`, release prefix = `RHTPA`.

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

Queries 1–3 match the JQL recorded in the mock results file exactly.

---

## 1. Untriaged (4 issues)

### Status: New

1. **TC-9001** — New — CVE-2026-40112 — CVE-2026-40112 h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] — created 2026-06-08
2. **TC-9002** — New — CVE-2026-40297 — CVE-2026-40297 serde_json - Stack overflow on deeply nested input [rhtpa-2.1] — created 2026-06-07
3. **TC-9004** — New — CVE-2026-40518 — CVE-2026-40518 ring - Timing side-channel in RSA verification [rhtpa-2.2] — created 2026-06-04

### Status: In Progress

4. **TC-9003** — In Progress — CVE-2026-40455 — CVE-2026-40455 tokio - Race condition in task cancellation [rhtpa-2.2] — created 2026-06-05
   - Warning: already In Progress; may be actively worked on.

## 2. Triaged but still New (1 issue) — FLAGGED

> These issues carry the `ai-cve-triaged` label but were never moved past New. They may need follow-up or re-triage.

### Status: New

1. **TC-9010** — New — CVE-2026-39874 — CVE-2026-39874 quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] — created 2026-05-28  (STALE: triaged but never actioned)

## 3. Ready for QA (1 issue)

Depend-link filtering of the 3 candidates returned by Query 3:

| Candidate | Status | Depend-linked Tasks | Decision |
|---|---|---|---|
| TC-9020 | Modified | TC-9021 (Done), TC-9022 (Closed) | All Done/Closed → **Included** |
| TC-9023 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | Open task remaining → Excluded (remediation in progress) |
| TC-9026 | Modified | none | No Depend links → Excluded (no remediation to verify) |

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

- TC-9020: Consider transitioning to ON_QA.

## 4. Release Jira Summary

Query 4 was constructed (above), but no results for it were provided in the mock data. Per the "do not fabricate data" guardrail, no release Epic/Task rows are reported.

| Release Epic | Release Task | CVEs Tracked | Remediation Done | Remediation Pending |
|---|---|---|---|---|
| (no data supplied) | — | — | — | — |

---

Select an issue key to triage, or end the session.
