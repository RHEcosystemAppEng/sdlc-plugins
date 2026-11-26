# Step 1 – Data Extraction: TC-8001

**Mode:** Interactive (Step 0.6: `FULLSEND_OUTPUT_DIR` is absent). Jira reads are simulated from
`vuln-issue-standard-already-triaged.md`; no Jira MCP, REST, or `git show` calls were made.

## Pre-step results

| Step | Result |
|------|--------|
| 0 – Validate configuration | PASS. Repository Registry, Jira Configuration (Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`), Code Intelligence, and Security Configuration (Product Lifecycle, Version Streams 2.1.x / 2.2.x, Source Repositories) are all present. |
| Security config values | Jira version prefix `RHTPA`; Vulnerability issue type ID `10024`; Component label pattern `pscomponent:`; VEX field `customfield_12345`; Product pages URL `https://access.example.com/product-life-cycle/rhtpa` |
| Optional fields not configured | Upstream Affected Component, PS Component, and Stream custom fields; ProdSec email and account ID; Embargo policy URL |
| 0.3 – Matrix staleness | **WARNING.** `Last-Updated: 2026-06-28T10:00:00Z` is 151 days old as of 2026-11-26, which exceeds the 14-day threshold. In a live run the engineer picks Refresh / Proceed / Stop. This eval assumes **Proceed anyway**. |
| 0.8 – Assign / transition | Status is already `In Progress`, later than Assigned, so the transition is skipped. The issue is already assigned (`engineer-a@example.com`). If the current user is that engineer, the assignment is a no-op (see idempotency-check.md). |
| Status-aware handling | Issue is `In Progress`, so the skill warns: "This issue is already in In Progress. It may be actively worked on." It offers (1) proceed with triage to verify, or (2) skip. This eval assumes (1), a verification re-run. |

## Extracted CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8001 | Issue |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` and summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Issue stream scope | **2.2.x** (scoped) | `[rhtpa-2.2]` matches Version Stream `2.2.x` |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 | `versions` field (already corrected by the prior run) |
| Vulnerable library | quinn-proto | Description |
| Ecosystem | Cargo (source dependency: 2 tasks per stream) | Rust crate; Cargo is in the 2.2.x Ecosystem Mappings (`Cargo.lock`, repo `backend`, branch `release/0.4.z`) |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| CVSS / severity | 7.5 (High) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote link |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote link / description |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote link |
| Due date | 2026-07-15 (past due as of 2026-11-26) | `duedate` |
| Status | In Progress | Issue |
| Assignee | engineer-a@example.com | Issue |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server, **ai-cve-triaged** | Issue |
| Custom fields present on issue | customfield_10632 = quinn-proto; customfield_10669 = pscomponent:org/rhtpa-server; customfield_10832 = rhtpa-2.2 | Issue (these fields are not configured in Security Configuration, so Steps 4.3 and 7 cannot use them) |
| Existing issue links | Depend → TC-8100 (upstream backport, In Progress); Depend → TC-8101 (downstream propagation, Open; TC-8101 Blocks link with TC-8100) | `issuelinks` |
| Existing comments | (1) `[sdlc-workflow] Description digest: sha256-md:a1b2…b2` from 2026-07-01T10:00:00Z; (2) Post-triage summary with the triage-security footnote (v0.11.1) from 2026-07-01T10:01:00Z | Comment history |
| Deployment context | `upstream` (default) | The Source Repositories table has no Deployment Context column, and `rhtpa-server` is not listed |

All critical fields (CVE ID, library, affected range) parsed successfully, so execution continues.

## Steps 1.5 / 1.7

- **1.5 External enrichment:** MITRE and OSV were not queried, because external calls are forbidden in this eval. They are treated as unavailable, so the fix threshold comes from the Jira description only (< 0.11.14, fixed 0.11.14). Confidence is reduced.
- **1.7 Embargo check:** Skipped. No Embargo policy URL is configured, even though CVSS 7.5 is above the threshold.

## Step 2 – Version impact (simulated lock-file evidence from security-matrix-mock.md)

| Version | Stream | Pinned tag (backend) | quinn-proto | Affected? | Notes |
|---------|--------|----------------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | outside issue scope |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | outside issue scope |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | `v0.4.8` (build 0.4.9) | 0.11.12 | **YES** | backend retag of 2.2.1, same as 2.2.1 |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | ships fix |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | ships fix |

The development stream (Step 2.2) cannot be determined without Jira unreleased-version metadata. It is not simulated here.
