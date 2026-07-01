# Step 0 -- Validate Project Configuration

Configuration extracted from CLAUDE.md:

| Setting | Value |
|---------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component custom field | customfield_10632 |
| ProdSec contact email | _(not configured)_ |
| ProdSec Jira account ID | _(not configured)_ |
| Embargo policy URL | _(not configured)_ |

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories

| Repository | URL | Local Path |
|------------|-----|------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend |

The Source Repositories table does NOT have a Deployment Context column. All repositories default to `upstream`. Coordination Guidance subsection is omitted from remediation tasks (backward compatibility).

## Step 0.3 -- Matrix Staleness Check

Read `security-matrix-mock.md` and extracted the `Last-Updated` timestamp:
`2026-06-28T10:00:00Z`

Current date: 2026-07-01. Matrix age: 3 days. Threshold: 14 days.

The matrix is within the 14-day threshold. Proceeding silently without staleness warning.

## Step 1 -- Data Extraction

**Issue**: TC-8021

Parsed CVE data from the Vulnerability issue:

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server (from labels) |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| Upstream Affected Component (customfield_10632) | quinn-proto |

### Stream scope resolution

Summary contains stream suffix `[rhtpa-2.2]`. Mapped to configured Version Stream **2.2.x**.

Issue stream scope: **2.2.x** (scoped). Steps 3 and 8 will be scoped to the 2.2.x stream only.

### Ecosystem detection

Library `quinn-proto` is a Rust crate. Ecosystem Mappings table for stream 2.2.x lists:
- Cargo: Repository=backend, Lock File=`Cargo.lock`, Check Command=`git show <tag>:Cargo.lock`, Upstream Branch=`release/0.4.z`

Detected ecosystem: **Cargo**

### Deployment context lookup

Repository `rhtpa-backend` found in Source Repositories table. No Deployment Context column present -- defaulting to `upstream`.

## Step 1.5 -- External CVE Data Enrichment

*(External API calls are not executed in this eval. Using Jira description data.)*

The Jira description provides a clear fix threshold: quinn-proto < 0.11.14, fixed in 0.11.14.

Since external tools are not called, proceeding with the Jira description fix threshold: **0.11.14**.

> Note: In production, MITRE CVE API and OSV.dev would be queried to cross-validate this threshold.

## Step 1.7 -- Embargo Check

No Embargo policy URL is configured in Security Configuration. Skipping Step 1.7 silently.
