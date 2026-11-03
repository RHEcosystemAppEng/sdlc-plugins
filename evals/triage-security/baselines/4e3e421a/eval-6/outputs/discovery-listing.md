# triage-security — Discovery Mode Listing

Invoked without an issue key, so the skill runs in discovery mode (interactive; `FULLSEND_OUTPUT_DIR` not set).

## Step 0 — Configuration values used

The values come from the `# Project Configuration` section of the project CLAUDE.md. All required sections are present: Repository Registry, Jira Configuration, Code Intelligence, and Security Configuration (Product Lifecycle, Version Streams, Source Repositories).

| Setting | Value | Source |
|---|---|---|
| Project key | `TC` | Jira Configuration |
| Cloud ID | `2b9e35e3-6bd3-4cec-b838-f4249ee02432` | Jira Configuration |
| Vulnerability issue type ID | `10024` | Security Configuration > Product Lifecycle |
| Jira version prefix | `RHTPA` | Security Configuration > Product Lifecycle |
| Component label pattern | `pscomponent:` | Security Configuration > Product Lifecycle |
| VEX Justification field | `customfield_12345` | Security Configuration > Product Lifecycle |
| Version streams | `2.1.x` (rhtpa-release.0.3.z), `2.2.x` (rhtpa-release.0.4.z) | Security Configuration > Version Streams |

## JQL queries built from the Security Configuration

**Query 1 — Untriaged** (maxResults 20, fields: summary, labels, status, created)
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

**Query 2 — Triaged but still New** (maxResults 10, fields: summary, labels, status, created)
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

**Query 3 — Ready for QA candidates** (maxResults 20, fields: summary, labels, status, created, issuelinks)
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

**Query 4 — Release Jira summary** (maxResults 10, fields: summary, status, issuelinks, parent)
```
project = TC AND issuetype = Task AND summary ~ 'RHTPA' AND summary ~ 'CVE triage' ORDER BY created DESC
```

Queries 1–3 match the JQL shown in the mock results file exactly.

---

## 1. Untriaged (4 issues)

Grouped by status (the query orders by `status ASC, created DESC`).

### Status: New (3)

| # | Issue | Status | CVE | Stream | Summary | Created |
|---|-------|--------|-----|--------|---------|---------|
| 1 | TC-9001 | New | CVE-2026-40112 | 2.2.x | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 2 | TC-9002 | New | CVE-2026-40297 | 2.1.x | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 3 | TC-9004 | New | CVE-2026-40518 | 2.2.x | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

### Status: In Progress (1)

| # | Issue | Status | CVE | Stream | Summary | Created |
|---|-------|--------|-----|--------|---------|---------|
| 4 | TC-9003 | In Progress | CVE-2026-40455 | 2.2.x | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

All four carry component label `pscomponent:org/rhtpa-server`.

Note: TC-9003 is In Progress but has no `ai-cve-triaged` label. Someone may be working on it without having run AI triage. See status-handling.md.

---

## 2. Triaged but still New (1 issue) — FLAGGED

These issues have the `ai-cve-triaged` label but are still New, so nobody has acted on them since triage. They may need follow-up or re-triage.

### Status: New (1)

| # | Issue | Status | CVE | Stream | Summary | Created |
|---|-------|--------|-----|--------|---------|---------|
| 5 | TC-9010 | New | CVE-2026-39874 | 2.2.x | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

Flag: TC-9010 (created 2026-05-28) has the triaged label but is still New. Check whether its remediation tasks were created or whether it needs re-triage.

---

## 3. Ready for QA (1 issue)

Query 3 returned 3 candidates. The skill then checked each one's `issuelinks` for "Depend"-type linked Tasks:

| Candidate | Status | Depend-linked Tasks | Decision |
|-----------|--------|---------------------|----------|
| TC-9020 | Modified | TC-9021 (Done), TC-9022 (Closed) | All Done/Closed, so **include** |
| TC-9023 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | One task still open, so **exclude** (remediation in progress) |
| TC-9026 | Modified | none | No Depend links, so **exclude** (no remediation to verify) |

### Ready for QA list

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

Suggestion for TC-9020: Consider transitioning to ON_QA.

Note on TC-9026: it is in Modified with the triaged label but has no Depend-linked remediation Tasks. Its remediation may have been tracked outside the standard link topology, or it may have been dedup'd onto another CVE's task. Check this by hand before moving it to QA.

---

## 4. Release Jira summary

Query 4 was built from the config (shown above). The mock data has no results for it, so there are no release Epic or release Task rows to show. In a live run this table lists each `RHTPA <version> CVE triage` Task with its counts of tracked CVEs (Related links) and done/pending remediation (Blocks links).

| Release Epic | Release Task | CVEs Tracked | Remediation Done | Remediation Pending |
|-------------|-------------|-------------|-----------------|-------------------|
| (no data supplied) | — | — | — | — |

---

**Next step:** pick an issue number (1–5) to start triage, or pick TC-9020 for the ON_QA transition. Nothing is changed in Jira until you confirm explicitly.
