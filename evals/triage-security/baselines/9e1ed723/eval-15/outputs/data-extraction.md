# Step 1 – Data Extraction: TC-8001

## Pre-flight (Steps 0 – 0.8)

- **Step 0.6 – Mode**: interactive mode (`FULLSEND_OUTPUT_DIR` absent). Eval constraint: no Jira / git / external calls; all Jira mutations are written as proposals to these files.
- **Step 0 – Configuration**: Repository Registry, Jira Configuration (Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`), Code Intelligence, and Security Configuration all present.
  - Jira version prefix: `RHTPA`
  - Vulnerability issue type ID: `10024`
  - Component label pattern: `pscomponent:`
  - VEX Justification custom field: `customfield_12345`
  - ProdSec contact email: `prodsec-team@example.com`
  - ProdSec Jira account ID: `557058:prodsec-mock-account-id` (used for @mention in Step 3 comment)
  - Embargo policy URL: not configured (Step 1.7 skipped)
  - Upstream Affected Component custom field: not configured (Steps 4.3 and 7 skipped)
  - Version Streams: `2.1.x` (rhtpa-release.0.3.z), `2.2.x` (rhtpa-release.0.4.z)
  - Source Repositories: `rhtpa-backend` (no Deployment Context column -> defaults to `upstream`)
- **Step 0.3 – Matrix staleness**: `Last-Updated: 2026-06-28T10:00:00Z` -> **148 days old** (threshold 14 days). Warning: "Security matrix was last updated on 2026-06-28 (148 days ago). The matrix may not reflect recent releases." Options: Refresh now / Proceed anyway / Stop. For this eval run: **Proceed anyway** with the supplied matrix (any 2.2.5+ or 2.1.2+ releases after 2026-05-04 are not reflected).
- **Step 0.8 – Assign and transition** (proposed): assign TC-8001 to the current user; status is `New` -> transition to `Assigned` (transition discovered dynamically via `get_transitions`).

## Parsed CVE Data

| Field | Value |
|-------|-------|
| Issue key | TC-8001 |
| Issue type | Vulnerability |
| Status | New |
| Reporter | psirt-analyst (account ID `557058:psirt-analyst-mock-id`) |
| CVE ID | CVE-2026-31812 (from label and summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` -> stream **2.2.x** |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 ("versions before 0.11.14") |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) – Denial of Service (panic on excessive stream count) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 (quinn-rs/quinn#2048) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (GHSA-2026-qp73-x4mq); also RUSTSEC-2026-0042 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 (already past as of 2026-11-23) |
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix `[rhtpa-2.2]` -> maps to configured Version Stream **2.2.x** (`git.example.com/rhtpa/rhtpa-release.0.4.z`).
- Issue is **scoped** to stream 2.2.x. Affects Versions correction (Step 3) is limited to 2.2.x versions; 2.1.x impact is handled as cross-stream (Case A).

## Ecosystem Detection

- quinn-proto is a Rust crate -> **Cargo** ecosystem (listed in both streams' Ecosystem Mappings: repo `backend`, lock file `Cargo.lock`).
- Category: **Source dependency** -> 2 remediation tasks per affected stream (upstream backport/dependency bump + downstream propagation).

## Deployment Context

- Affected repository: `rhtpa-backend` (backend). Source Repositories table has no Deployment Context column -> default **upstream**.

## Step 1.5 – External CVE Data Enrichment

- MITRE CVE API and OSV.dev were **not queried** (eval constraint: no external tools).
- "External CVE databases unavailable – using Jira description data only. Fix threshold confidence is reduced."
- Fix threshold used for Step 2: **quinn-proto < 0.11.14 affected; 0.11.14 fixed** (Jira description, consistent with RUSTSEC reference).

## Step 1.7 – Embargo Check

- No Embargo policy URL configured -> step skipped silently (CVSS 7.5 would otherwise have triggered the gate).
