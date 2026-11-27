# Data Extraction — TC-8002

Skill: `/sdlc-workflow:triage-security` (Steps 0, 0.3, 0.6, 1, 1.5, 1.7)
Mode: interactive (simulated — `FULLSEND_OUTPUT_DIR` absent; no Jira/Git/WebFetch calls made per eval instructions)

## Step 0 – Configuration Validation

All required sections are present in the project CLAUDE.md (`claude-md-security-config.md`): Repository Registry, Jira Configuration, Code Intelligence, Security Configuration (Product Lifecycle, Version Streams, Source Repositories).

| Setting | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 (configured) |
| Upstream Affected Component field | not configured (Steps 4.3 and 7 skipped) |
| ProdSec Jira account ID | not configured (no ProdSec @mention) |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| Version streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source repositories | rhtpa-backend (https://github.com/rhtpa/rhtpa-backend), deployment context: `upstream` (default, no Deployment Context column) |

## Step 0.3 – Matrix Staleness Check

The matrix carries `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. Today is 2026-11-27, so the matrix is **152 days old**, well past the 14-day threshold.

> Security matrix for streams **2.1.x** and **2.2.x** was last updated on 2026-06-28 (152 days ago). It may not reflect recent releases.
> Options: 1. Refresh now  2. Proceed anyway  3. Stop

Eval handling: the matrix could not be refreshed (no external access), so the triage **proceeds with the current matrix**. The staleness is noted as a caveat in the outcome. Any 2.2.x release after 2.2.4 (2026-05-04) is not covered by this analysis.

## Step 1 – Extracted CVE Data

| Field | Value |
|---|---|
| Issue key | TC-8002 |
| Status | New (full triage path) |
| CVE ID | CVE-2026-28940 (from label and summary) |
| Summary | CVE-2026-28940 serde_json - Stack overflow on deeply nested input [rhtpa-2.2] |
| Affected component | `pscomponent:org/rhtpa-server` → repository `rhtpa-backend` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` → stream **2.2.x** |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | serde_json |
| Ecosystem | Cargo (Rust crate), a source dependency. It is listed in both streams' Ecosystem Mappings (`Cargo.lock`) |
| Affected version range | `< 1.0.135` ("versions before 1.0.135") |
| Fixed version | 1.0.135 |
| CVSS | 5.3 (Medium) |
| Upstream fix PR | none in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Other reference | https://rustsec.org/advisories/RUSTSEC-2026-0019.html |
| Due date | 2026-07-30 (already past) |
| Assignee | Unassigned |
| Reporter | not provided in mock data (needed for the summary @mention) |
| Existing comments | none |
| Deployment context | upstream |

All critical fields (CVE ID, library, affected range) were parsed successfully.

### Stream scope resolution

The suffix `[rhtpa-2.2]` maps to the configured stream **2.2.x** (`git.example.com/rhtpa/rhtpa-release.0.4.z`). The issue is **scoped** to 2.2.x. Stream 2.1.x is still analyzed for the cross-stream check (Case A).

## Step 1.5 – External CVE Data Enrichment

The MITRE CVE API (`https://cveawg.mitre.org/api/cve/CVE-2026-28940`) and OSV.dev (`https://api.osv.dev/v1/vulns/CVE-2026-28940`) were **not queried**, because the eval forbids external calls. This is treated as "both external APIs unavailable":

> External CVE databases unavailable. Using Jira description data only. Fix threshold confidence is reduced.

Fix threshold used: **serde_json < 1.0.135 is vulnerable; >= 1.0.135 is fixed** (from the Jira description).

## Step 1.7 – Embargo Check

Skipped. No Embargo policy URL is configured, and the CVSS of 5.3 (Medium) is below the 7.0 threshold anyway.

## Step 0.8 – Assign and Transition (proposed, not executed)

- `jira.edit_issue(TC-8002, assignee=<current-user-account-id>)`
- `jira.get_transitions(TC-8002)`, then transition to the target status "Assigned" (the issue is currently New)
