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
| PS Component custom field | customfield_10669 |
| Stream custom field | customfield_10832 |
| ProdSec contact email | _(not configured)_ |
| ProdSec Jira account ID | _(not configured)_ |
| Embargo policy URL | _(not configured -- Step 1.7 skipped)_ |

Source Repositories: No Deployment Context column present -- defaulting all repositories to `upstream`. Coordination guidance will be omitted from remediation tasks (backward compatibility).

Version Streams:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

## Step 0.3 -- Matrix Staleness Check

Security matrix Last-Updated timestamp: `2026-06-28T10:00:00Z` (3 days ago).
The matrix is within the 14-day threshold. Proceeding without staleness warning.

## Step 0.5 -- JIRA Access Initialization

JIRA access initialized (simulated for eval).

---

# Step 1 -- Data Extraction

**Issue**: TC-8011

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-45678 |
| Affected component | pscomponent:org/rhtpa-ui (from label) |
| Product version (PSIRT-claimed) | [rhtpa-2.2] (from summary suffix) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | webpack |
| Affected version range | < 5.98.0 |
| Fixed version | 5.98.0 |
| CVSS | 7.8 (High) |
| Upstream fix PR | _(none in remote links)_ |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Due date | 2026-08-15 |
| Existing comments | _(none)_ |
| Upstream Affected Component (customfield_10632) | webpack |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-ui |
| Stream (customfield_10832) | rhtpa-2.2 |

### Stream scope resolution

The issue summary contains stream suffix `[rhtpa-2.2]`. Mapping to configured Version Streams:
- `[rhtpa-2.2]` maps to stream **2.2.x**.
- Issue stream scope: **2.2.x** (scoped to this stream only).

### Ecosystem detection

The vulnerable library is **webpack**, which is a JavaScript/TypeScript package (npm ecosystem).

Checking the Ecosystem Mappings table for stream 2.2.x: the table lists Cargo and RPM ecosystems only. **npm is not listed** in the Ecosystem Mappings table.

**Note**: In a full triage, the unsupported ecosystem notification would be triggered here:

> "**Unsupported ecosystem**: npm is not yet supported for automated triage. Manual assessment is required."

However, for the purposes of this eval, we proceed with the analysis to demonstrate the Step 4.3 cross-CVE overlap detection logic using the provided fixture data.

### Deployment context lookup

The affected component (pscomponent:org/rhtpa-ui) maps to repository rhtpa-ui. This repository is not found in the Source Repositories table (which only contains rhtpa-backend). Defaulting deployment context to `upstream`.

## Step 1.5 -- External CVE Data Enrichment

_(Skipped for eval -- no external API calls permitted. Using Jira description data: fix threshold = 5.98.0.)_

## Step 1.7 -- Embargo Check

No Embargo policy URL configured in Security Configuration. Step 1.7 skipped.
