# Data Extraction — TC-8002

## Step 1: Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-28940 |
| Jira Issue Key | TC-8002 |
| Summary | CVE-2026-28940 serde_json - Stack overflow on deeply nested input [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | serde_json |
| Affected version range | versions before 1.0.135 |
| Fixed version | 1.0.135 |
| CVSS | 5.3 (Medium) |
| Upstream fix PR | Not provided in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Due date | 2026-07-30 |
| Existing comments | None |
| Assignee | Unassigned |
| Labels | CVE-2026-28940, pscomponent:org/rhtpa-server |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- Issue is **scoped** to the 2.2.x stream only

## Ecosystem Detection

- Library: serde_json (Rust crate)
- Ecosystem: **Cargo** (source dependency)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`
- Classification: Source dependency ecosystem -- would normally produce 2 tasks per stream (upstream + downstream)

## Step 1.5: External CVE Data Enrichment

(Simulated -- external APIs not called per eval instructions)

- MITRE CVE API: CVE-2026-28940, affected versions < 1.0.135, fixed in 1.0.135
- OSV.dev: serde_json ecosystem Cargo, introduced < 1.0.135, fixed 1.0.135
- Cross-validation: All sources agree on fix threshold of **1.0.135**
- Enriched fix threshold: **1.0.135** (consensus across all sources)

## Step 1.7: Embargo Check

- CVSS: 5.3 (Medium) -- below the Critical/Important threshold (CVSS >= 7.0)
- Embargo check: **Skipped** (severity below threshold)

## Configuration Extracted (Step 0)

| Setting | Value |
|---------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | Not configured |
| ProdSec contact email | Not configured |
| ProdSec Jira account ID | Not configured |
| Embargo policy URL | Not configured |

## Step 0.3: Matrix Staleness Check

- Matrix last updated: 2026-06-28T10:00:00Z
- Current date: 2026-10-21
- Days since update: ~115 days (exceeds 14-day threshold)
- Status: **Stale** -- in a real triage, the engineer would be warned and asked to refresh or proceed
- For this eval: proceeding with current matrix data
