# TC-8001 Triage — Data Extraction (Steps 0 and 1)

Mode: interactive (FULLSEND_OUTPUT_DIR absent). Eval run: no Jira MCP, git, or
WebFetch calls were made; all data comes from the supplied mock files.

## Step 0 – Project Configuration (from claude-md-security-config-deploy-ctx.md)

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | not configured (Steps 4.3 and 7 skipped) |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| ProdSec contact / account ID | not configured (skipped silently) |

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories mapping (Deployment Context column present)

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | **customer-shipped** |

The Deployment Context column exists, so no backward-compatibility default to
`upstream` is applied. Parsed mapping:
`rhtpa-backend → { url: https://github.com/rhtpa/rhtpa-backend, deployment_context: customer-shipped }`

## Step 0.3 – Matrix Staleness Check

Matrix `Last-Updated: 2026-06-28T10:00:00Z`. Relative to today (2026-11-26) that is
151 days old, which is over the 14-day threshold. Interactively, the engineer would be
offered Refresh now / Proceed anyway / Stop. For this eval: **Proceed anyway** with
the supplied matrix.

## Step 1 – Parsed CVE Data

| Field | Value |
|-------|-------|
| Issue key | TC-8001 |
| Status | New (full triage path) |
| CVE ID | CVE-2026-31812 (from label and summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Affected repository (resolved) | rhtpa-backend (the `backend` repository in Ecosystem Mappings, which builds the rhtpa-server image) |
| **Deployment context (lookup result)** | **customer-shipped** (from the Source Repositories table, row `rhtpa-backend`) |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` |
| Issue stream scope | **2.2.x** (scoped: suffix `rhtpa-2.2` matches the configured stream 2.2.x) |
| Affects Versions (Jira field) | RHTPA 2.0.0 (does not match the scoped stream; corrected in Step 3) |
| Vulnerable library | quinn-proto |
| Ecosystem | Cargo (Rust crate), a source dependency: 2 tasks per stream |
| Affected version range | < 0.11.14 ("versions before 0.11.14") |
| Fixed version | 0.11.14 |
| CVSS / severity | 7.5 (High), DoS (panic on excessive stream count) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Assignee | Unassigned (Step 0.8 would assign to current user and transition to Assigned) |
| Existing comments | none |

### Deployment context lookup

- Affected component label `pscomponent:org/rhtpa-server` maps to the source repository **rhtpa-backend**.
- Looked up in the Source Repositories mapping from Step 0: **found**.
- Recorded deployment context: **`customer-shipped`**. Step 8 uses this to add the
  customer-shipped Coordination Guidance to every remediation task.

## Step 1.5 – External enrichment

MITRE and OSV were not queried because the eval forbids external calls. Treated as
"unavailable": the Jira description data (< 0.11.14, fixed 0.11.14) is used, and
fix-threshold confidence is lower as a result.

## Step 1.7 – Embargo check

Skipped. No Embargo policy URL is configured, even though CVSS 7.5 is at or above the threshold.

## Step 2 – Version Impact (simulated lock-file data)

| Version | Tag | quinn-proto | Affected? | Notes |
|---------|-----|-------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | outside issue scope (stream 2.1.x) |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | outside issue scope (stream 2.1.x) |
| 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | v0.4.8 | — | YES | backend retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | |

Dependency type: direct/transitive could not be determined. No Cargo.toml or
`cargo tree` data was supplied, so remediation templates carry both approaches.

Upstream fix status (inferred from the latest pinned tags; branch HEAD not inspected):

| Stream | Ecosystem | Upstream Branch | Latest evidence | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | v0.4.12 → 0.11.14 | YES (dependency bump variant) |
| 2.1.x | Cargo | release/0.3.z | v0.3.12 → 0.11.9 | NO (upstream backport variant) |

## Step 3 – Affects Versions correction (proposed)

Change Affects Versions from `RHTPA 2.0.0` to `RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2`.
This needs engineer confirmation and dynamic version-ID discovery.
