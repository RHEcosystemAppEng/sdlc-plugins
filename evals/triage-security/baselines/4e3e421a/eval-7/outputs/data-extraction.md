# Step 1 – Data Extraction: TC-8006

Mode: interactive (FULLSEND_OUTPUT_DIR absent). Eval simulation: no Jira MCP, `git show`, or WebFetch calls were made. All data comes from the provided mock files.

## Step 0 – Configuration (from claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component field | not configured, so Step 4.3 is skipped |
| PS Component / Stream fields | not configured |
| ProdSec contact / account ID | not configured, so @mentions are omitted |
| Embargo policy URL | not configured, so Step 1.7 is skipped |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

All required sections are present, so the configuration is valid.

## Step 0.3 – Matrix Staleness

`Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-03, which is about 128 days later and over the 14-day threshold. Interactive mode would warn here and offer Refresh / Proceed / Stop. For this eval we proceed with the current matrix.

## Step 0.8 – Assign / Transition (simulated, not executed)

Status is New and Assignee is Unassigned. The proposed actions are: assign TC-8006 to the current user, then transition New to Assigned using a dynamically discovered transition.

## Extracted CVE Data

| Field | Value |
|---|---|
| Issue key | TC-8006 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.1] |
| Status | New |
| CVE ID | CVE-2026-31812 (from label and summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `[rhtpa-2.1]` |
| Affects Versions (Jira) | RHTPA 2.1.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 ("versions before 0.11.14") |
| Fixed version | 0.11.14 |
| CVSS / severity | 7.5 (High) |
| Upstream fix PR | none in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | none |
| Existing issue links | Related, outward: TC-8006 → TC-8001 (link ID 1990401) |

## Stream Scope Resolution

The suffix `[rhtpa-2.1]` maps to the configured stream **2.1.x** (rhtpa-release.0.3.z). The issue is therefore **scoped** to 2.1.x.

## Ecosystem and Deployment Context

- Ecosystem: **Cargo** (quinn-proto is a Rust crate). It is listed in the Ecosystem Mappings table and classified as a source dependency, so remediation needs 2 tasks per stream.
- Deployment context: `upstream` (default, because the Deployment Context column is absent).

## Step 1.5 – External Enrichment (simulated)

MITRE and OSV were not queried, per the eval rules. The Jira description threshold (< 0.11.14, fixed in 0.11.14) is used and confidence is reduced.

## Step 1.7 – Embargo Check

CVSS 7.5 meets the threshold, but no Embargo policy URL is configured, so the step is skipped silently.

## Step 2 – Version Impact Analysis (from simulated lock-file data)

| Stream | Version | backend tag | quinn-proto | Affected? |
|---|---|---|---|---|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES |
| 2.2.x | 2.2.2 | v0.4.8 (retag) | same as 2.2.1 | YES |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO |

quinn-proto is pulled in transitively through quinn, probably via the HTTP/3 or QUIC client stack. The exact chain would come from Cargo.lock in a real run.

Step 2.5 upstream fix status: the 2.2.x line already ships 0.11.14 from v0.4.11. For `release/0.3.z` (2.1.x), branch HEAD would need to be checked with `git show`. That was not done here.

## Step 3 – Affects Versions Correction (scoped to 2.1.x)

`Current: [RHTPA 2.1.0] → Proposed: [RHTPA 2.1.0, RHTPA 2.1.1]` (correct but incomplete). This is a proposal only and was not executed.
