# Step 0 -- Validate Project Configuration

Configuration validated from CLAUDE.md:

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **Upstream Affected Component custom field**: not configured
- **PS Component custom field**: not configured
- **Stream custom field**: not configured
- **ProdSec contact email**: not configured
- **ProdSec Jira account ID**: not configured
- **Embargo policy URL**: not configured (Step 1.7 will be skipped)
- **Version Streams**:
  - 2.1.x: git.example.com/rhtpa/rhtpa-release.0.3.z (local: /home/dev/repos/rhtpa-release.0.3.z)
  - 2.2.x: git.example.com/rhtpa/rhtpa-release.0.4.z (local: /home/dev/repos/rhtpa-release.0.4.z)
- **Source Repositories**:
  - rhtpa-backend: https://github.com/rhtpa/rhtpa-backend (local: /home/dev/repos/rhtpa-backend)
  - Deployment Context column: absent -- defaulting all repos to `upstream`

## Step 0.3 -- Matrix Staleness Check

Security matrix `Last-Updated` timestamp: `2026-06-28T10:00:00Z` (3 days ago as of 2026-07-01).
The matrix is within the 14-day freshness threshold. Proceeding without warning.

## Step 0.5 -- JIRA Access Initialization

(Simulated -- eval mode, no actual Jira connection)

## Step 1.7 -- Embargo Check

Skipped -- no Embargo policy URL configured in Security Configuration.

---

# Step 1 -- Data Extraction

**Issue**: TC-8001
**Status**: New -- proceeding with full triage.

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
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
| Reporter | (extracted from Jira issue -- account ID from reporter field) |

## Stream Scope Resolution

Issue summary suffix: `[rhtpa-2.2]`
Mapped to configured Version Stream: **2.2.x**
Issue stream scope: **2.2.x only**

Steps 3 and 4 will be scoped to the 2.2.x stream. Other streams (2.1.x) will be analyzed for cross-stream impact in Step 8 Case B.

## Ecosystem Detection

Library: quinn-proto (a Rust crate)
Ecosystem: **Cargo**

Verified against Ecosystem Mappings table in the 2.2.x stream's security-matrix.md:
- Cargo ecosystem is listed with Repository: backend, Lock File: `Cargo.lock`, Check Command: `git show <tag>:Cargo.lock`, Upstream Branch: `release/0.4.z`

Cargo is a source dependency ecosystem, so remediation will produce two tasks: upstream backport + downstream propagation subtask (per Important Rule 8).

## Deployment Context Lookup

Affected component label: `pscomponent:org/rhtpa-server`
Matched repository: rhtpa-backend
Source Repositories table has no Deployment Context column -- defaulting to `upstream`.

## Step 1.5 -- External CVE Data Enrichment

(Simulated -- eval mode, no actual WebFetch calls)

In a real triage, the skill would query:
1. MITRE CVE API: `https://cveawg.mitre.org/api/cve/CVE-2026-31812`
2. OSV.dev API: `https://api.osv.dev/v1/vulns/CVE-2026-31812`

Using the Jira description data as the authoritative source for this eval:
- **Affected range**: < 0.11.14
- **Fixed version**: 0.11.14

The enriched fix threshold for Step 2.3 comparisons: **0.11.14**
