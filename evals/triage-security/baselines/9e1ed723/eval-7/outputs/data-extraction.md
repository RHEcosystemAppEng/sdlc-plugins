# Step 1 – Data Extraction: TC-8006

Mode: interactive (simulated; `FULLSEND_OUTPUT_DIR` not set). No Jira MCP, `git show`, or external calls were made — all data comes from the provided eval input files.

## Step 0 – Configuration validation

All required sections are present in the project CLAUDE.md (`claude-md-security-config.md`):

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component / PS Component / Stream fields | Not configured (Step 4.3 and Step 7 skipped) |
| ProdSec contact / account ID | Not configured (@mentions omitted) |
| Embargo policy URL | Not configured (Step 1.7 skipped) |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (no Deployment Context column → default `upstream`) |

Step 0.3 matrix staleness: matrix `Last-Updated: 2026-06-28T10:00:00Z`, which is more than 14 days before today (2026-11-23), so it is stale. In a live run the engineer would get the choice to Refresh / Proceed / Stop. For this eval the run proceeds with the current matrix.

## Extracted CVE data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8006 | Issue |
| CVE ID | CVE-2026-31812 | Label + summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label |
| Product version (PSIRT-claimed) | `[rhtpa-2.1]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.1.0 | `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| CVSS | 7.5 (High) | Description |
| Upstream fix PR | None among the remote links | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote links / description |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | `duedate` |
| Status | New | Issue |
| Assignee | Unassigned | Issue |
| Existing comments | None | Comment history |
| Existing issue links | Related → TC-8001 (link ID 1990401, outward) | `issuelinks` |

## Stream scope resolution

- Suffix `[rhtpa-2.1]` → stream **2.1.x**, which matches the configured Version Streams row (`rhtpa-release.0.3.z`).
- **Issue stream scope: 2.1.x (scoped).**

## Ecosystem detection

- quinn-proto is a Rust crate, so the ecosystem is **Cargo**. Cargo is listed in the 2.1.x Ecosystem Mappings (`Cargo.lock`, repo `backend`, upstream branch `release/0.3.z`).
- Category: source dependency, so 2 remediation tasks per affected stream.
- Deployment context for rhtpa-backend: `upstream` (default).

## Step 1.5 – External enrichment

This step was not executed because the eval forbids external calls. The Jira description threshold (< 0.11.14, fixed 0.11.14) is used, with reduced confidence noted.

## Step 1.7 – Embargo check

Skipped because no Embargo policy URL is configured. CVSS 7.5 would otherwise have triggered the gate.

## Step 2 – Version impact (from mock lock file data)

| Version | Stream | Backend tag | quinn-proto | Affected (< 0.11.14)? |
|---|---|---|---|---|
| RHTPA 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES |
| RHTPA 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES |
| RHTPA 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES |
| RHTPA 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES |
| RHTPA 2.2.2 | 2.2.x | v0.4.8 (retag) | same as 2.2.1 | YES (same as 2.2.1) |
| RHTPA 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO |
| RHTPA 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO |

In-scope (2.1.x) result: both 2.1.0 and 2.1.1 are affected.

## Step 3 – Affects Versions correction (scoped to 2.1.x)

`Current: [RHTPA 2.1.0] → Proposed: [RHTPA 2.1.0, RHTPA 2.1.1]` (correct but incomplete). Engineer confirmation would be required before the edit.
