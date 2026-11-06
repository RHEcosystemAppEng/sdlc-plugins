# Step 1 – Data Extraction: TC-8001

Mode: interactive (FULLSEND_OUTPUT_DIR not set). Eval run: Jira, git and WebFetch were not called. All data comes from the supplied mock files.

## Step 0 – Configuration check

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| ProdSec contact email | prodsec-team@example.com |
| ProdSec Jira account ID | 557058:prodsec-mock-account-id |
| Upstream Affected Component / PS Component / Stream fields | Not configured, so Steps 4.3, 7 and 7.5.3 are skipped |
| Embargo policy URL | Not configured, so Step 1.7 is skipped |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`; coordination guidance is omitted because the column is absent) |

Step 0.3 – Matrix staleness: the matrix has `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-06, so it is about 131 days old, well past the 14-day threshold. **Staleness warning raised.** For this eval, the engineer chooses "Proceed anyway".

## Parsed CVE data

| Field | Value |
|-------|-------|
| Issue key | TC-8001 |
| Issue type / Status | Vulnerability / New |
| Reporter | psirt-analyst (account ID `557058:psirt-analyst-mock-id`) |
| CVE ID | CVE-2026-31812 (from the label and the summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` maps to stream **2.2.x** |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Ecosystem | Cargo (Rust crate), a source dependency |
| Affected version range | < 0.11.14 ("versions before 0.11.14") |
| Fixed version | 0.11.14 |
| CVSS / Severity | 7.5 (High) |
| Vulnerability class | Denial of service: a panic from an unbounded stream count in a STREAMS frame |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 (already past) |
| Assignee | Unassigned (Step 0.8 would assign it to the current user and transition New to Assigned) |
| Existing comments | None |
| Deployment context | upstream (default) |

## Stream scope resolution

- Suffix `[rhtpa-2.2]` matches the configured Version Stream **2.2.x** (rhtpa-release.0.4.z).
- The issue is **scoped** to stream 2.2.x.

## Step 1.5 – External enrichment

MITRE and OSV were not queried, as instructed for this eval. Fallback: the analysis uses the Jira description data only.

> External CVE databases unavailable. Using Jira description data only. Fix threshold confidence is reduced.

Fix threshold used: **quinn-proto >= 0.11.14 is fixed; < 0.11.14 is affected.**

## Step 1.7 – Embargo check

No Embargo policy URL is configured, so this step is skipped, even though the CVSS of 7.5 is above the threshold.
