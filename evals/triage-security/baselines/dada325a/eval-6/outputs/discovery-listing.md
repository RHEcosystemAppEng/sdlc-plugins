# triage-security: Discovery Mode Listing

You ran the skill without an issue key (`/sdlc-workflow:triage-security`), so it ran in **discovery mode**
(SKILL.md, Inputs, "Discovery mode (no issue key provided)").

## Step 0: Configuration validation

`FULLSEND_OUTPUT_DIR` is absent, so the skill ran in interactive mode (Step 0.6). Step 0.7 was skipped.

Every section that Step 0 requires is present in the project CLAUDE.md (`claude-md-security-config.md`):

| Required section | Status | Extracted value |
|---|---|---|
| Repository Registry | Present (1 entry) | rhtpa-backend |
| Jira Configuration | Present | Project key: **TC**, Cloud ID: `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| Code Intelligence | Present | `mcp__<serena-instance>__<tool>`, instance `serena_backend` |
| Security Configuration / Product Lifecycle | Present | Product pages URL: `https://access.example.com/product-life-cycle/rhtpa`; Jira version prefix: **RHTPA**; Vulnerability issue type ID: **10024**; Component label pattern: `pscomponent:`; VEX Justification field: `customfield_12345` |
| Security Configuration / Version Streams | Present (2) | 2.1.x -> rhtpa-release.0.3.z; 2.2.x -> rhtpa-release.0.4.z |
| Security Configuration / Source Repositories | Present (1) | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

The discovery queries need two values from this configuration:
- `<project-key>` = `TC` (from Jira Configuration)
- `<vulnerability-issue-type-id>` = `10024` (from Security Configuration / Product Lifecycle)

## Constructed JQL queries

**Query 1: Untriaged issues** (maxResults: 20, fields: summary, labels, status, created)
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

**Query 2: Triaged but still New** (maxResults: 10, fields: summary, labels, status, created)
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

**Query 3: Ready for QA candidates** (maxResults: 20, fields: summary, labels, status, created, issuelinks)
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

**Query 4: Release Jira summary** (maxResults: 10, fields: summary, status, issuelinks, parent)
```
project = TC AND issuetype = Task AND summary ~ 'RHTPA' AND summary ~ 'CVE triage' ORDER BY created DESC
```

Queries 1 to 3 match the mock JQL in `discovery-mode-results.md` exactly.

---

## 1. Untriaged (4 issues)

Grouped by status, in the order `ORDER BY status ASC` returns them. Within each group, issues are sorted by created date, newest first.

### Status: In Progress

| # | Issue | Status | CVE | Summary | Created |
|---|-------|--------|-----|---------|---------|
| 1 | TC-9003 | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

> Warning: TC-9003 is already **In Progress** and may be actively worked on. If you select it, you are asked whether to proceed or skip.

### Status: New

| # | Issue | Status | CVE | Summary | Created |
|---|-------|--------|-----|---------|---------|
| 2 | TC-9001 | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 3 | TC-9002 | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 4 | TC-9004 | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

All four issues carry the component label `pscomponent:org/rhtpa-server`. Each stream suffix maps to a configured stream: `[rhtpa-2.2]` maps to 2.2.x and `[rhtpa-2.1]` maps to 2.1.x.

---

## 2. Triaged but still New (1 issue)

> **Stale:** these issues were triaged (`ai-cve-triaged`) but never moved forward. They may need follow-up or re-triage.

| # | Issue | Status | CVE | Summary | Created |
|---|-------|--------|-----|---------|---------|
| 5 | TC-9010 | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

TC-9010 was triaged about 5 months ago (created 2026-05-28) and is still in New.

---

## 3. Ready for QA (1 issue)

The skill checked each Query 3 candidate's "Depend" issue links:

| Candidate | Status | Depend-linked Tasks | Result |
|---|---|---|---|
| TC-9020 | Modified | TC-9021 (Done), TC-9022 (Closed) | **Included**: all remediation Tasks are Done or Closed |
| TC-9023 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | Excluded: TC-9025 is still open, so remediation is in progress |
| TC-9026 | Modified | (none) | Excluded: no "Depend" Tasks, so there is no remediation to verify |

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

**TC-9020:** Consider transitioning to ON_QA.

---

## 4. Release Jira summary

The input files contain no results for Query 4, so no release Epic or Task rows are shown. The skill did not invent any. When the query runs against Jira, the table uses this format:

| Release Epic | Release Task | CVEs Tracked | Remediation Done | Remediation Pending |
|---|---|---|---|---|
| (no data provided) | | | | |

---

**Next step:** Select an issue by number (1 to 5) or key to start the full 8-step triage. TC-9020 can also be selected for the ON_QA transition. Every Jira change needs your explicit confirmation.
