# Step 1 – Data Extraction: TC-8001 (re-run)

Source: `vuln-issue-standard-already-triaged.md` (simulated `jira.get_issue` and
`jira.get_issue_remote_links` output). Interactive mode (`FULLSEND_OUTPUT_DIR` absent),
so Steps 0.6/0.7 select the interactive workflow. No Jira, git, or WebFetch calls were made.

## Step 0 – Configuration (from `claude-md-security-config.md`)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component / PS Component / Stream fields | Not configured in Security Configuration, so Step 4.3 (cross-CVE overlap) and Step 7 (concurrent triage) are skipped |
| Embargo policy URL | Not configured, so Step 1.7 is skipped |
| ProdSec contact / account ID | Not configured, so no @mentions |
| Version Streams | 2.1.x -> rhtpa-release.0.3.z; 2.2.x -> rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

Validation result: all required sections are present. Proceed.

## Extracted CVE data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8001 | Issue |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` and summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Issue stream scope | **2.2.x** (rhtpa-release.0.4.z), scoped | Suffix matched to Version Streams |
| Affects Versions (Jira field, current) | RHTPA 2.2.0, RHTPA 2.2.1 | `versions` field (already corrected by the prior run) |
| Vulnerable library | quinn-proto | Description |
| Ecosystem | Cargo (source dependency, so 2 remediation tasks per stream) | Library name and the matrix Ecosystem Mappings |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| Severity | CVSS 7.5 (High) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Additional reference | https://rustsec.org/advisories/RUSTSEC-2026-0042.html | Description references |
| Due date | 2026-07-15 | `duedate` |
| Status | In Progress | Issue |
| Assignee | engineer-a@example.com | Issue |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server, **ai-cve-triaged** | Issue |
| Existing issue links | Depend -> TC-8100 (upstream backport, In Progress); Depend -> TC-8101 (downstream propagation, Open; TC-8101 is blocked by TC-8100) | `issuelinks` |
| Existing comments | (1) `[sdlc-workflow] Description digest: sha256-md:a1b2...a1b2` (2026-07-01T10:00Z); (2) Post-triage summary with footnote, sdlc-workflow/triage-security v0.11.1 (2026-07-01T10:01Z) | Comment history |
| Deployment context | upstream (default) | Source Repositories |

All critical fields (CVE ID, library, affected range) parsed successfully.

## Status-aware handling

The issue is **In Progress**. The skill warns: "This issue is already in `In Progress`.
It may be actively worked on." It also asks whether to (1) proceed with triage anyway,
to verify version impact, or (2) skip. This eval follows option (1), a verification
re-run.

## Step 1.5 – External enrichment

Not executed in this eval (no WebFetch). The Jira description threshold (`< 0.11.14`,
fixed in 0.11.14) is used, which degrades confidence.

## Step 2 – Version impact (simulated lock-file data from `security-matrix-mock.md`)

Matrix `Last-Updated: 2026-06-28T10:00:00Z`. Step 0.3: against the session date
(2026-11-26) this is about 151 days old, past the 14-day threshold. In a real run the
skill would show the staleness warning and offer Refresh / Proceed / Stop. This eval
proceeds with the mock matrix.

| Version | Stream | backend tag | quinn-proto | Affected (< 0.11.14)? | In issue scope? |
|---|---|---|---|---|---|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | No (other stream) |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | No (other stream) |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | Yes |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | Yes |
| 2.2.2 | 2.2.x | v0.4.8 (retag of 2.2.1) | 0.11.12 (same as 2.2.1) | **YES** | Yes |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | Yes |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | Yes |

Discrepancy: the matrix lists 2.2.2 as a backend retag of 2.2.1 (`v0.4.8`), so 2.2.2
ships quinn-proto 0.11.12 and is affected. The prior run's summary says "RHTPA 2.2.2
and later ship quinn-proto 0.11.14 (not affected)", and the current Affects Versions
leave out 2.2.2. See `triage-outcome.md`.
