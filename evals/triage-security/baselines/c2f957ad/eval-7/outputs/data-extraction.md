# Step 1 – Data Extraction: TC-8006

**Mode:** Interactive (Step 0.6: `FULLSEND_OUTPUT_DIR` is not set). Eval simulation: no Jira MCP, git, or WebFetch calls were made. All values come from the provided mock files.

## Step 0 – Configuration Validation (from claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | `pscomponent:` |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component field | Not configured, so Step 4.3 is skipped |
| PS Component / Stream fields | Not configured |
| ProdSec contact / account ID | Not configured, so no @mentions |
| Embargo policy URL | Not configured, so Step 1.7 is skipped |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

All required sections are present, so validation passes.

## Step 0.3 – Matrix Staleness

The matrix has `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-26, so the matrix is about 151 days old, well past the 14-day threshold. **Staleness warning:** in a live run the engineer would be offered Refresh / Proceed / Stop. For this eval we proceed with the current matrix.

## Step 0.8 – Assign and Transition (simulated)

The issue is Unassigned and in status New. Proposed actions (not executed): assign TC-8006 to the current user, then transition it New → Assigned.

## Extracted CVE Data

| Field | Value |
|---|---|
| Issue key | TC-8006 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.1] |
| Status | New (full triage path) |
| CVE ID | CVE-2026-31812 (label and summary agree) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `[rhtpa-2.1]` |
| Affects Versions (Jira field) | RHTPA 2.1.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 ("versions before 0.11.14") |
| Fixed version | 0.11.14 |
| CVSS / Severity | 7.5 (High) |
| Upstream fix PR | None in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| Existing issue links | Related → TC-8001 (link ID 1990401, outward, TC-8006 → TC-8001) |
| Reporter | Not provided in mock data (needed later for the summary @mention) |

## Stream Scope Resolution

- The suffix `[rhtpa-2.1]` maps to the configured Version Stream **2.1.x** (rhtpa-release.0.3.z).
- **Issue stream scope: 2.1.x.** The issue is scoped, not unscoped.

## Ecosystem Detection

- quinn-proto is a Rust crate, so the ecosystem is **Cargo**. Cargo appears in the Ecosystem Mappings for both streams (lock file `Cargo.lock`, repo backend).
- Category: source dependency, which means 2 remediation tasks per affected stream.
- Deployment context: rhtpa-backend defaults to `upstream`.

## Step 1.5 – External Enrichment (simulated)

MITRE and OSV were not queried, per eval constraints. The fix threshold from the Jira description (< 0.11.14, fixed in 0.11.14) is used, with reduced confidence noted.

## Step 1.7 – Embargo Check

Skipped because no Embargo policy URL is configured. CVSS 7.5 would otherwise have met the threshold.

## Step 2 – Version Impact Analysis (simulated lock-file data from matrix mock)

| Stream | Version | backend tag | quinn-proto | Affected (< 0.11.14)? |
|---|---|---|---|---|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES |
| 2.2.x | 2.2.2 | v0.4.8 (retag) | same as 2.2.1 (0.11.12) | YES |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO |

## Step 3 – Affects Versions Correction (scoped to 2.1.x)

- Current value: [RHTPA 2.1.0]. Proposed value: [RHTPA 2.1.0, RHTPA 2.1.1]. The PSIRT value is correct but incomplete.
- This correction requires engineer confirmation and was not executed.
