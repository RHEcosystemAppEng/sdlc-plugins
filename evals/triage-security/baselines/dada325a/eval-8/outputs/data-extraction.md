# Step 1 – Data Extraction: TC-8010

Source: `vuln-issue-overlap-covered.md` (simulated `jira.get_issue(TC-8010, fields=["*all"])` and `jira.get_issue_remote_links(TC-8010)`). No live Jira calls were made.

## Step 0 – Configuration (from `claude-md-security-config.md`)

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | `pscomponent:` |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component field | customfield_10632 (given in the task; not listed in the mock Security Configuration) |
| PS Component field | customfield_10669 (on the issue; not listed in the mock Security Configuration) |
| Stream field | customfield_10832 (on the issue; not listed in the mock Security Configuration) |
| ProdSec Jira account ID | Not configured, so no @mention |
| Embargo policy URL | Not configured, so Step 1.7 is skipped |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend only |

Matrix staleness (Step 0.3): `Last-Updated: 2026-06-28T10:00:00Z` is 131 days before today (2026-11-06), which is past the 14-day limit. In an interactive run, triage would stop here and offer three options: Refresh, Proceed anyway, or Stop. For this eval, triage proceeds with the current matrix.

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8010 | Issue |
| CVE ID | CVE-2026-44492 | Label + summary |
| Summary | CVE-2026-44492 axios - Server-Side Request Forgery via crafted URL [rhtpa-2.2] | Issue |
| Status | New (full triage path) | Issue |
| Affected component | `pscomponent:org/rhtpa-ui` | Label / customfield_10669 |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira) | RHTPA 2.2.0 | `versions` field |
| Vulnerable library | axios | Description / customfield_10632 |
| Ecosystem | npm (source dependency) | Library name |
| Affected version range | < 1.8.2 ("versions before 1.8.2") | Description |
| Fixed version (fix threshold) | **1.8.2** | Description |
| CVSS | 8.1 (High) | Description |
| Upstream fix PR | None in remote links | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 | Remote links |
| Due date | 2026-08-01 (already past) | `duedate` |
| Assignee | Unassigned | Issue |
| Existing links | None | `issuelinks` |
| Existing comments | None | Comments |
| Upstream Affected Component (customfield_10632) | axios | Custom field |
| Stream (customfield_10832) | rhtpa-2.2 | Custom field |

## Stream Scope Resolution

- Suffix `[rhtpa-2.2]` maps to stream **2.2.x** (Konflux repo `git.example.com/rhtpa/rhtpa-release.0.4.z`).
- The issue is **scoped** to 2.2.x. Steps 3 and 4 are limited to this stream.

## Step 1.5 – External Enrichment

No external calls were made (MITRE and OSV were not queried, per eval constraints). The fix threshold from the Jira description, **1.8.2**, is used and marked as reduced confidence.

## Step 1.7 – Embargo Check

Skipped because no Embargo policy URL is configured. The CVSS of 8.1 would otherwise trigger the gate.

## Observations / Gaps

1. **Unsupported ecosystem in the matrix**: the 2.2.x `security-matrix.md` Ecosystem Mappings list only Cargo and RPM. npm (axios, `package-lock.json`) is not mapped, and the mock lock-file data has no axios versions. Step 2 version impact therefore cannot be computed from lock-file evidence. In a real run the skill would report "Unsupported ecosystem: npm is not yet supported for automated triage. Manual assessment is required." No axios version is assumed here.
2. **Repository not registered**: `rhtpa-ui` is not in the Source Repositories table. Deployment context defaults to `upstream`.
3. **Overlap-field configuration**: the mock Security Configuration does not declare the Upstream Affected Component, PS Component, or Stream custom fields that Step 4.3 requires. The task states customfield_10632 = axios and supplies the JQL result, so Step 4.3 was run with customfield_10632 / 10669 / 10832. In production, these fields must be added to Security Configuration, or Step 4.3 is skipped.
