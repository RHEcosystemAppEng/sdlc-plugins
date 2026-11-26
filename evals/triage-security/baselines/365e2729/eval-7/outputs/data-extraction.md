# Step 1 – Data Extraction: TC-8006

Mode: interactive (FULLSEND_OUTPUT_DIR absent). Simulated: no Jira, WebFetch, or git calls were made. All data comes from the mock input files.

## Step 0 – Configuration validation (claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component / PS Component / Stream fields | Not configured, so Step 4.3 and Step 7 are skipped |
| ProdSec contact / Jira account ID | Not configured. No @mention. |
| Embargo policy URL | Not configured, so Step 1.7 is skipped |
| Version Streams | 2.1.x -> rhtpa-release.0.3.z; 2.2.x -> rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

All required sections are present, so triage proceeds.

## Step 0.3 – Matrix staleness

The matrix has `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-26, about 151 days later, which is past the 14-day threshold. In a live run the skill would show the staleness warning and offer Refresh / Proceed / Stop. For this eval we assume "Proceed anyway".

## Extracted CVE data

| Field | Value |
|---|---|
| Issue key | TC-8006 |
| Status | New (full triage path) |
| CVE ID | CVE-2026-31812 (from the label and the summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed, summary suffix) | `[rhtpa-2.1]` |
| Affects Versions (Jira field) | RHTPA 2.1.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 ("versions before 0.11.14") |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | None in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Assignee | Unassigned. In a live run, Step 0.8 would assign the issue to the current user and transition it to Assigned. |
| Existing comments | None |
| Existing issue links | Related -> TC-8001 (link ID 1990401, outward) |

## Stream scope resolution

- The suffix `[rhtpa-2.1]` maps to the configured stream **2.1.x** (Konflux repo `rhtpa-release.0.3.z`).
- The issue is **scoped** to 2.1.x.

## Ecosystem

- quinn-proto is a Rust crate, so the ecosystem is **Cargo**. Cargo is a source dependency: 2 tasks per stream. Lock file: `Cargo.lock` in backend.
- Deployment context for rhtpa-backend: `upstream` (the default).

## Step 1.5 – External enrichment

MITRE and OSV were not queried, per the eval constraints. The skill would treat them as unavailable and fall back to the Jira description (fix threshold 0.11.14), with reduced confidence.

## Step 2 – Version impact (from the mock lock file data)

| Stream | Version | Build | backend tag | quinn-proto | Affected? |
|---|---|---|---|---|---|
| 2.1.x | 2.1.0 | 0.3.8 | v0.3.8 | 0.11.9 | YES |
| 2.1.x | 2.1.1 | 0.3.12 | v0.3.12 | 0.11.9 | YES |
| 2.2.x | 2.2.0 | 0.4.5 | v0.4.5 | 0.11.9 | YES |
| 2.2.x | 2.2.1 | 0.4.8 | v0.4.8 | 0.11.12 | YES |
| 2.2.x | 2.2.2 | 0.4.9 | v0.4.8 (retag) | same as 2.2.1 | YES |
| 2.2.x | 2.2.3 | 0.4.11 | v0.4.11 | 0.11.14 | NO |
| 2.2.x | 2.2.4 | 0.4.12 | v0.4.12 | 0.11.14 | NO |

## Step 3 – Affects Versions correction (scoped to 2.1.x)

- Current: [RHTPA 2.1.0]. Proposed: [RHTPA 2.1.0, RHTPA 2.1.1]. The current value is correct but incomplete.
- This change needs engineer confirmation and a correction comment that includes the Comment Footnote. No ProdSec @mention, because none is configured.
