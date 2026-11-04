# Step 1 – Data Extraction: TC-8003

## Step 0 – Configuration check (from claude-md-security-config.md)

Every section the skill needs is present: Repository Registry, Jira Configuration, Code Intelligence, Security Configuration (Product Lifecycle, Version Streams, Source Repositories).

| Setting | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Upstream Affected Component / PS Component / Stream fields | Not configured (so Step 4.3 and Step 7 are skipped) |
| ProdSec contact / account ID | Not configured (no @mention) |
| Embargo policy URL | Not configured (so Step 1.7 is skipped) |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

Mode: interactive. `FULLSEND_OUTPUT_DIR` is not set, so this is not sandbox mode. Jira calls and `git show` are simulated from the eval input files.

## Step 0.3 – Matrix staleness check

- `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. Today is 2026-11-04, so the matrix is **129 days old**, well past the 14-day threshold.
- **Warning:** "Security matrix for streams 2.1.x / 2.2.x was last updated on 2026-06-28 (129 days ago). The matrix may not reflect recent releases." Options are Refresh now, Proceed anyway, or Stop. For this eval the triage proceeds with the current matrix. Releases newer than 2.2.4 may be missing, but that does not change the duplicate outcome.

## Step 0.8 – Assign / transition (proposed, not executed)

- TC-8003 is in status **New** and Unassigned.
- Proposed action: assign TC-8003 to the current user and transition it to Assigned (status found dynamically via `get_transitions`).

## Extracted CVE data

| Field | Value |
|---|---|
| Issue key | TC-8003 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Issue type / Status | Vulnerability / New |
| CVE ID | **CVE-2026-31812** (label and summary agree) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed, suffix) | `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | **quinn-proto** (Rust crate) |
| Affected version range | **< 0.11.14** ("versions before 0.11.14") |
| Fixed version | **0.11.14** |
| Severity | CVSS 7.5 (High), DoS |
| Upstream fix PR | None in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042 in the description) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 (**past due** as of 2026-11-04) |
| Assignee | Unassigned |
| Existing comments | None |

### Stream scope resolution
- Suffix `[rhtpa-2.2]` maps to the configured Version Stream **2.2.x** (rhtpa-release.0.4.z).
- The issue is **scoped** to the 2.2.x stream.

### Ecosystem detection
- quinn-proto is a Rust crate, so the ecosystem is **Cargo**. Cargo is listed in the 2.2.x Ecosystem Mappings (`Cargo.lock` in `backend`, upstream branch `release/0.4.z`).
- Category: source dependency. A normal remediation would be 2 tasks per stream.

### Deployment context
- Affected repo: rhtpa-backend. The Source Repositories table has no Deployment Context column, so it defaults to `upstream`.

## Step 1.5 – External enrichment (simulated)
- The MITRE and OSV queries were not run (no external calls allowed in this eval). The triage falls back to the Jira description data: fix threshold **0.11.14**. Confidence is lower because the threshold was not cross-validated.

## Step 1.7 – Embargo check
- CVSS 7.5 meets the threshold, but no Embargo policy URL is configured, so this step is skipped silently.

## Step 2 – Version impact analysis (simulated `git show <tag>:Cargo.lock`)

| Stream | Version | backend tag | quinn-proto | Affected (< 0.11.14)? |
|---|---|---|---|---|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES |
| 2.2.x | 2.2.2 | v0.4.8 (retag) | same as 2.2.1 (0.11.12) | YES (same as 2.2.1) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO |

- In scope (2.2.x): **2.2.0, 2.2.1, 2.2.2 affected**. 2.2.3 and later already ship the fix.
- Out of scope: 2.1.0 and 2.1.1 are affected (cross-stream). They are not tracked by any sibling found in the JQL result.
- Development stream: no unreleased-version data was provided, so it was not assessed.
- Upstream fix (Step 2.5): `release/0.4.z` already ships 0.11.14 as of tag v0.4.11, so the fix is available upstream for 2.2.x.

## Step 3 – Affects Versions comparison (scoped to 2.2.x)
- Current: `[RHTPA 2.2.0]`. Evidence-based: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`.
- PSIRT's value is correct but incomplete. The correction is **superseded by the Duplicate closure in Step 4**: TC-8003 will be closed, so it is not corrected. The gap is reported against the canonical issue TC-7999 instead (see duplicate-check.md).
