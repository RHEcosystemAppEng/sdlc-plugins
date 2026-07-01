# Step 0 -- Validate Project Configuration

Configuration extracted from CLAUDE.md (claude-md-security-config-prodsec.md):

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **ProdSec contact email**: prodsec-team@example.com
- **ProdSec Jira account ID**: 557058:prodsec-mock-account-id
- **Embargo policy URL**: not configured (skip Step 1.7)
- **Upstream Affected Component custom field**: not configured (skip Steps 4.3, 7)
- **PS Component custom field**: not configured
- **Stream custom field**: not configured
- **Version Streams**:
  - 2.1.x: Konflux Release Repo git.example.com/rhtpa/rhtpa-release.0.3.z, Local Path /home/dev/repos/rhtpa-release.0.3.z
  - 2.2.x: Konflux Release Repo git.example.com/rhtpa/rhtpa-release.0.4.z, Local Path /home/dev/repos/rhtpa-release.0.4.z
- **Source Repositories**:
  - rhtpa-backend: URL https://github.com/rhtpa/rhtpa-backend, Local Path /home/dev/repos/rhtpa-backend
  - Deployment Context column: absent -- default all repos to `upstream`
    (per backward compatibility, Coordination Guidance subsection is omitted from remediation tasks)

## Step 0.3 -- Matrix Staleness Check

Security matrix Last-Updated timestamp: `2026-06-28T10:00:00Z`
Current date: 2026-07-01
Days since last update: 3 days
Threshold: 14 days

Result: Matrix is **fresh** (3 days < 14 days). Proceeding without warning.

## Step 0.5 -- JIRA Access Initialization

(Skipped per eval instructions -- no external tools.)

---

# Step 1 -- Data Extraction

**Issue**: TC-8001

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, Summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (pscomponent: pattern) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | < 0.11.14 | Description: "versions before 0.11.14" |
| Fixed version | 0.11.14 | Description: "Fixed version: 0.11.14" |
| CVSS | 7.5 (High) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Reporter | psirt-analyst (account ID: 557058:psirt-analyst-mock-id) | Issue `reporter` field |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

Summary suffix: `[rhtpa-2.2]` maps to stream **2.2.x** from the Version Streams table.
Issue stream scope: **2.2.x** (scoped issue -- Steps 3 and 4 apply only to 2.2.x versions).

## Ecosystem Detection

Library: quinn-proto (Rust crate)
Ecosystem: **Cargo** (identified from the Ecosystem Mappings table in security-matrix.md for stream 2.2.x)

The Cargo ecosystem is listed in the Ecosystem Mappings table with:
- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`

## Deployment Context Lookup

Affected repository from component label `pscomponent:org/rhtpa-server`: rhtpa-backend
Deployment Context column: **absent** from Source Repositories table
Default deployment context: `upstream` (backward compatibility)
Coordination Guidance: omitted (no Deployment Context column)

## Step 1.5 -- External CVE Data Enrichment

(Skipped per eval instructions -- no WebFetch calls to external APIs.)

Note: In a real triage, MITRE CVE API and OSV.dev would be queried. Using Jira description data as the fix threshold: **0.11.14**.

## Step 1.7 -- Embargo Check

Embargo policy URL: not configured in Security Configuration.
Result: Step 1.7 **skipped silently** -- no embargo gate presented.
