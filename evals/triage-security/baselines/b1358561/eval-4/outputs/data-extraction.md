# TC-8004 — Step 1 Data Extraction (with Step 0 / 0.3 / 1.5 / 1.7 notes)

## Step 0 — Configuration validation

Source: `claude-md-security-config.md` (mock project CLAUDE.md)

| Item | Value | Status |
|---|---|---|
| Repository Registry | rhtpa-backend (serena_backend) | OK |
| Project key | TC | OK |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 | OK |
| Code Intelligence | present, naming convention `mcp__<serena-instance>__<tool>` | OK |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa | OK |
| Jira version prefix | RHTPA | OK |
| Vulnerability issue type ID | 10024 | OK |
| Component label pattern | `pscomponent:` | OK |
| VEX Justification custom field | customfield_12345 | configured (optional) |
| Upstream Affected Component field | not configured | Steps 4.3, 7 and 7.5.3 are skipped |
| PS Component / Stream custom fields | not configured | — |
| ProdSec contact / Jira account ID | not configured | @mentions for ProdSec omitted |
| Embargo policy URL | not configured | Step 1.7 skipped |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z | OK |
| Source Repositories | rhtpa-backend (https://github.com/rhtpa/rhtpa-backend) | OK (no Deployment Context column → default `upstream`) |

## Step 0.3 — Matrix staleness check

Both stream matrices carry `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. Today is
2026-11-27, which makes the matrices **152 days old**, past the 14-day threshold.

> Security matrix for streams **2.1.x** and **2.2.x** was last updated on 2026-06-28
> (152 days ago). The matrix may not reflect recent releases.
> Options: 1. Refresh now, 2. Proceed anyway, 3. Stop

Eval mode: the matrix cannot be refreshed because external git access is not allowed.
I chose **Proceed anyway**. Any 2.1.x or 2.2.x release published after 2026-06-28 is
not covered by this analysis.

## Step 0.6 — Mode

`FULLSEND_OUTPUT_DIR` absent → interactive mode. The eval does not allow Jira, git or
WebFetch calls, so every Jira mutation appears below as a proposal and is not executed.

## Step 0.8 — Assign and transition (proposed, not executed)

- Assign TC-8004 to the current user (the issue is currently unassigned)
- Transition New → Assigned (target status found dynamically through `get_transitions`)

## Step 1 — Extracted CVE data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8004 | issue |
| Issue type / Status | Vulnerability / New | issue |
| CVE ID | CVE-2026-33501 | label `CVE-2026-33501` + summary |
| Summary | CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames | issue |
| Affected component | `pscomponent:org/rhtpa-server` | component label |
| Affected repository | rhtpa-backend (Cargo, `backend` in Ecosystem Mappings) | matrix Ecosystem Mappings |
| Deployment context | `upstream` (default, no Deployment Context column) | Source Repositories |
| Product version (PSIRT-claimed) | **none, so the issue is unscoped** | summary has no `[rhtpa-x.y]` suffix |
| Affects Versions (current Jira field) | RHTPA 2.1.0, RHTPA 2.2.0 | `versions` field |
| Vulnerable library | h2 (Rust crate) | description |
| Ecosystem | Cargo, a source dependency, so 2 tasks per affected stream | library + Ecosystem Mappings |
| Affected version range | `< 0.4.8` ("versions before 0.4.8") | description |
| Fixed version | 0.4.8 | description |
| CVSS | 7.5 (High) | description |
| Upstream fix PR | https://github.com/hyperium/h2/pull/812 | remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-kv8p-r3n7 | remote links |
| Additional reference | https://rustsec.org/advisories/RUSTSEC-2026-0055.html | description |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-33501 | remote links |
| Due date | 2026-08-01 (**already past** as of 2026-11-27) | `duedate` |
| Assignee | Unassigned | issue |
| Existing comments | none | issue |
| Reporter (for summary @mention) | not present in mock data. Read it from the live issue. | — |
| Security level | not present in mock data. Copy the live `security` value to every created Task. | — |

Note: the description says this CVE is distinct from CVE-2024-2758 (httpd CONTINUATION
flood). That CVE is not related and plays no part in this triage.

### Stream scope resolution

The summary has **no bracketed stream suffix**, so the issue is **UNSCOPED** and covers
every configured stream (2.1.x and 2.2.x). Effects:
- Step 3 corrects Affects Versions across all streams, listing affected versions only.
- Step 8 skips Case A (it applies to scoped issues only). Case B creates remediation for
  each affected stream.

## Step 1.5 — External CVE enrichment

MITRE (`cveawg.mitre.org/api/cve/CVE-2026-33501`) and OSV.dev
(`api.osv.dev/v1/vulns/CVE-2026-33501`) were **not queried** because the eval forbids
external calls. I treated both as unavailable:

> External CVE databases unavailable — using Jira description data only.
> Fix threshold confidence is reduced.

Fix threshold used in Step 2: **h2 < 0.4.8 is vulnerable, and 0.4.8 is fixed.**

## Step 1.7 — Embargo check

No Embargo policy URL is configured, so this step was skipped. CVSS 7.5 would otherwise
meet the trigger threshold.
