# Step 1 – Data Extraction: TC-8001 (re-run)

Mode: interactive (FULLSEND_OUTPUT_DIR absent). Jira reads are simulated from
`vuln-issue-standard-already-triaged.md`; no live Jira or git calls were made.

## Step 0 – Configuration (from claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component field (config) | not configured, so Steps 4.3, 7 and 7.5.3 are skipped |
| ProdSec contact / account ID | not configured, so no @mentions |
| Embargo policy URL | not configured, so Step 1.7 is skipped |
| Version Streams | 2.1.x -> rhtpa-release.0.3.z; 2.2.x -> rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (no Deployment Context column, so the default is `upstream`) |

All required sections exist, so validation passes.

## Extracted CVE data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8001 | Issue |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` + summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label (matches `pscomponent:`) / customfield_10669 |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Issue stream scope | **2.2.x** (scoped) | Suffix `rhtpa-2.2` matches the configured stream 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 | `versions` field (already corrected by the prior run) |
| Vulnerable library | quinn-proto | Description / customfield_10632 |
| Ecosystem | Cargo (source dependency, so 2 tasks per stream) | Library + Ecosystem Mappings |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| CVSS / severity | 7.5 (High) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote links / description |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | `duedate` |
| Status | In Progress | Issue |
| Assignee | engineer-a@example.com | Issue |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server, **ai-cve-triaged** | Issue |
| Existing issue links | Depend -> TC-8100, Depend -> TC-8101 | Issue links |
| Existing comments | (1) `[sdlc-workflow] Description digest: sha256-md:a1b2…b2` (2026-07-01T10:00Z); (2) Post-triage summary with footnote, v0.11.1 (2026-07-01T10:01Z) | Comment history |
| Deployment context | upstream (default) | Source Repositories |

All critical fields (CVE ID, library, affected range) were parsed, so there is no need to stop.

## Status-aware handling

The status is **In Progress**, so the skill warns: "This issue is already in In Progress. It may
be actively worked on." The task explicitly asks for a re-run, so option 1 (proceed
with triage to verify) is assumed.

## Supporting analysis (Steps 1.5–2, simulated)

- Step 1.5: MITRE and OSV were not queried (external calls are not allowed in this eval). The skill falls back
  to the Jira description threshold `< 0.11.14` with reduced confidence.
- Step 0.3: The mock matrices have no `Last-Updated` timestamp. This produces a non-blocking warning.
- Step 2 version impact (quinn-proto, fix threshold 0.11.14):

| Stream | Version | Backend tag | quinn-proto | Affected? |
|---|---|---|---|---|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES (out of issue scope) |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES (out of issue scope) |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES |
| 2.2.x | 2.2.2 | v0.4.8 (retag of 2.2.1) | 0.11.12 | **YES (same as 2.2.1)** |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO |

Note: the prior run's summary comment says "RHTPA 2.2.2 and later ship quinn-proto
0.11.14 (not affected)". The matrix shows that 2.2.2's backend is a retag of `v0.4.8`
(quinn-proto 0.11.12), which makes it **affected**. See idempotency-check.md and triage-outcome.md.
