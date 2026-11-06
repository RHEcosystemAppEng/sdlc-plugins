# Step 1 – Data Extraction: TC-8001

Mode: interactive (FULLSEND_OUTPUT_DIR absent). Eval simulation: Jira `get_issue` /
`get_issue_remote_links` responses are taken from `vuln-issue-standard-already-triaged.md`.
No live Jira, git, or WebFetch calls were made.

## Step 0 – Configuration (from claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | `pscomponent:` |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component / PS Component / Stream fields | Not configured in Security Configuration, so Steps 4.3, 7 and 7.5.3 are skipped |
| ProdSec contact / account ID | Not configured, so no @mentions |
| Embargo policy URL | Not configured, so Step 1.7 is skipped |
| Version Streams | 2.1.x -> rhtpa-release.0.3.z; 2.2.x -> rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

Configuration validation: PASS. All required sections are present.

## Extracted CVE data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8001 | Issue |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` and summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Issue stream scope | **2.2.x** (scoped) | `[rhtpa-2.2]` matched to Version Streams row 2.2.x |
| Affects Versions (current Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 | `versions` field |
| Vulnerable library | quinn-proto | Description |
| Ecosystem | Cargo (source dependency, 2 tasks per stream) | Library name and 0.4.z Ecosystem Mappings |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| CVSS / Severity | 7.5 (High) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote links and description |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 (past due as of 2026-11-06) | `duedate` |
| Status | In Progress | Issue |
| Assignee | engineer-a@example.com | Issue |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server, **ai-cve-triaged** | Issue |
| Existing links | Depend -> TC-8100, Depend -> TC-8101 (TC-8101 is blocked by TC-8100) | `issuelinks` |
| Existing comments | (1) `[sdlc-workflow] Description digest: sha256-md:a1b2...b2` (2) Post-triage summary, v0.11.1 footnote | Comment history |
| Deployment context | upstream (default) | Source Repositories |

All critical fields (CVE ID, library, affected range) parsed successfully.

## Status-aware handling

The issue is in **In Progress**. Per the skill, the engineer is warned: "This issue is
already in `In Progress`. It may be actively worked on." The options are (1) proceed with
triage to verify version impact or Affects Versions, or (2) skip. This eval assumes
option 1 (re-verify).

## Supporting steps (simulated)

- **Step 0.3 Matrix staleness:** the matrix `Last-Updated` is 2026-06-28T10:00:00Z, about
  131 days before 2026-11-06, which is over the 14-day threshold. This produces a
  **staleness warning** (Refresh / Proceed / Stop). The eval proceeds with the current
  matrix.
- **Step 1.5 External enrichment:** MITRE/OSV were not queried (eval restriction). The
  Jira description threshold (< 0.11.14, fixed 0.11.14) is used, with reduced-confidence
  noted.
- **Step 1.7 Embargo:** skipped because no Embargo policy URL is configured.

## Step 2 – Version impact (stream 2.2.x, scoped)

| Version | Build | backend tag | quinn-proto | Affected (< 0.11.14)? |
|---|---|---|---|---|
| 2.2.0 | 0.4.5 | v0.4.5 | 0.11.9 | YES |
| 2.2.1 | 0.4.8 | v0.4.8 | 0.11.12 | YES |
| 2.2.2 | 0.4.9 | v0.4.8 (retag) | same as 2.2.1 (0.11.12) | **YES** (carried forward from 2.2.1) |
| 2.2.3 | 0.4.11 | v0.4.11 | 0.11.14 | NO |
| 2.2.4 | 0.4.12 | v0.4.12 | 0.11.14 | NO |

Out of scope, for the cross-stream (Case A) check only:

| Version | backend tag | quinn-proto | Affected? |
|---|---|---|---|
| 2.1.0 | v0.3.8 | 0.11.9 | YES |
| 2.1.1 | v0.3.12 | 0.11.9 | YES |

Upstream fix status (Step 2.5): HEAD of `release/0.4.z` was not inspectable in eval. The
latest 2.2.x tags (v0.4.11, v0.4.12) already ship 0.11.14.
