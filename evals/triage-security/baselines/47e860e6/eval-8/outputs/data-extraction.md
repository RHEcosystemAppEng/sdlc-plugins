# TC-8010 — Step 1 Data Extraction

Mode: **interactive** (`FULLSEND_OUTPUT_DIR` is not set). Simulated: no Jira, WebFetch, or git calls were made. All data comes from the mock issue file.

## Step 0 — Configuration (from claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Embargo policy URL | not configured, so Step 1.7 is skipped |
| ProdSec contact / Jira account ID | not configured, so no @mention |
| Upstream Affected Component / PS Component / Stream fields | **not listed in the mock Security Configuration.** The issue carries customfield_10632 / 10669 / 10832, and the task tells me to run Step 4.3, so I treat them as configured (see overlap-check.md) |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

## Step 0.3 — Matrix staleness

The matrix says `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-04, which makes it **129 days old**, past the 14-day limit. **Staleness warning raised.** The engineer would be offered Refresh / Proceed / Stop. This eval proceeds with the current matrix.

## Step 0.8 — Assign / transition (proposed, not executed)

- Assign TC-8010 to the current triager. The issue is currently Unassigned.
- Status is New. Move it to the status named "Assigned", using a transition looked up at run time.

## Extracted CVE data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8010 | issue |
| CVE ID | **CVE-2026-44492** | label + summary |
| Summary | CVE-2026-44492 axios - Server-Side Request Forgery via crafted URL [rhtpa-2.2] | summary |
| Status | New | issue |
| Affected component | `pscomponent:org/rhtpa-ui` | label / customfield_10669 |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | summary suffix |
| Affects Versions (Jira) | RHTPA 2.2.0 | `versions` |
| Vulnerable library | **axios** | description / customfield_10632 |
| Affected version range | **< 1.8.2** ("versions before 1.8.2") | description |
| Fixed version (fix threshold) | **1.8.2** | description |
| CVSS / severity | 8.1 (High) | description |
| Upstream fix PR | none in remote links | remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp | remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 | remote links |
| Due date | 2026-08-01 (already past) | `duedate` |
| Existing comments | none | issue |
| Existing issue links | none | issue |
| Upstream Affected Component (customfield_10632) | axios | custom field |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-ui | custom field |
| Stream (customfield_10832) | rhtpa-2.2 | custom field |

## Stream scope resolution

`[rhtpa-2.2]` maps to configured stream **2.2.x** (rhtpa-release.0.4.z). The issue is **scoped** to 2.2.x.

## Ecosystem detection

- axios is an **npm** package, which is a source-dependency ecosystem (2 tasks per stream if remediation were needed).
- **Gap:** the 2.2.x matrix's Ecosystem Mappings list only Cargo and RPM. npm is not mapped, and `rhtpa-ui` is not in Source Repositories. Under the normal path this triggers the "Unsupported ecosystem: manual assessment required" stop for lock-file analysis, and I have no npm lock-file data. I made up no axios versions per tag.
- Deployment context: `rhtpa-ui` is not in Source Repositories, so it defaults to `upstream`.

## Step 1.5 — External enrichment

Not run, because external calls are forbidden in this eval. As if both APIs were unavailable, I use the Jira description data alone: fix threshold **1.8.2**. Confidence in the threshold is lower.

## Step 1.7 — Embargo check

Skipped. No Embargo policy URL is configured. CVSS 8.1 would otherwise have triggered the gate.
