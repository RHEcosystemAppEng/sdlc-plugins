# Step 1 – Data Extraction: TC-8010

**Mode:** Interactive (Step 0.6: `FULLSEND_OUTPUT_DIR` absent). Step 0.7 skipped.
**Source:** Simulated `jira.get_issue(TC-8010)` + `jira.get_issue_remote_links(TC-8010)` (taken from `vuln-issue-overlap-covered.md`; no Jira calls made).

## Step 0 – Configuration (from claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component field | **Not declared in Security Configuration** (value `customfield_10632` supplied by the task/issue data) |
| PS Component field | **Not declared** (`customfield_10669` present on issue) |
| Stream field | **Not declared** (`customfield_10832` present on issue) |
| ProdSec contact email / Jira account ID | Not configured, so @mentions are skipped |
| Embargo policy URL | Not configured, so Step 1.7 is skipped |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend only (no Deployment Context column, so it defaults to `upstream`) |

## Step 0.3 – Matrix staleness

`security-matrix-mock.md` has `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-23, so the matrix is **148 days old**, past the 14-day threshold. In a live run the engineer would get the Refresh / Proceed / Stop prompt. For this eval it is recorded as **Proceed anyway**. The outcome does not depend on the matrix because the Step 4.3 overlap result decides it.

## Step 0.8 – Assign / transition (proposed, not executed)

- Assign TC-8010 to the current user.
- Transition New to Assigned, using the transition discovered dynamically.

## Extracted CVE data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8010 | issue |
| CVE ID | **CVE-2026-44492** | label + summary |
| Summary | CVE-2026-44492 axios - Server-Side Request Forgery via crafted URL [rhtpa-2.2] | issue |
| Status | New | issue (status-aware handling: full triage path) |
| Affected component | `pscomponent:org/rhtpa-ui` | label (Component label pattern) |
| PSIRT-claimed product version | `[rhtpa-2.2]` | summary suffix |
| Affects Versions (Jira) | RHTPA 2.2.0 | `versions` field |
| Vulnerable library | **axios** | description |
| Affected version range | **< 1.8.2** ("versions before 1.8.2") | description |
| Fixed version (fix threshold) | **1.8.2** | description |
| CVSS / severity | 8.1 (High) | description |
| Upstream fix PR | None in remote links | remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp | remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 | remote links |
| Due date | 2026-08-01 (**already past**) | `duedate` |
| Assignee | Unassigned | issue |
| Existing links | None | `issuelinks` |
| Existing comments | None | comments |
| customfield_10632 (Upstream Affected Component) | **axios** | custom field |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-ui | custom field |
| customfield_10832 (Stream) | rhtpa-2.2 | custom field |

All critical fields (CVE ID, library, affected range) were parsed, so extraction does not block.

## Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to configured Version Stream **2.2.x** (rhtpa-release.0.4.z).
- The issue is **scoped** to stream 2.2.x.

## Ecosystem detection

- axios is a JavaScript package, so the ecosystem is **npm** (source dependency: 2 tasks per stream if remediation were needed).
- **Gap:** the 2.2.x `security-matrix.md` Ecosystem Mappings table lists only Cargo (backend) and RPM. It has no npm row and no `rhtpa-ui` repository. The mock lock-file data also has no axios versions. Under the skill rules, npm is an **unsupported ecosystem for automated lock-file analysis** in this configuration, so the version impact (Step 2) cannot be determined from evidence and **was not fabricated**.

## Deployment context

- Affected repo `rhtpa-ui` (from `pscomponent:org/rhtpa-ui`) is **not in** the Source Repositories table, so deployment context defaults to `upstream`.

## Step 1.5 – External enrichment (simulated)

No external calls were allowed (MITRE and OSV not queried). Per the skill's "Unavailable" branch, the run continues with Jira description data only: **fix threshold = 1.8.2**, with reduced confidence.

> External CVE databases unavailable. Using Jira description data only. Fix threshold confidence is reduced.

## Step 1.7 – Embargo check

Skipped because no Embargo policy URL is configured. CVSS 8.1 would otherwise trigger the gate.
