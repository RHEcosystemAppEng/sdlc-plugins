# Step 1 – Data Extraction: TC-8011

Source: `vuln-issue-overlap-not-covered.md` (simulated `jira.get_issue(TC-8011, fields=["*all"])` + `jira.get_issue_remote_links(TC-8011)`).

## Step 0 – Configuration (from claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | `pscomponent:` |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component field | customfield_10632 (given by the task and present on the issue; the mock Security Configuration does not list it explicitly, see note below) |
| PS Component field | customfield_10669 (present on the issue) |
| Stream field | customfield_10832 (present on the issue) |
| ProdSec Jira account ID | Not configured, so @mentions are left out |
| Embargo policy URL | Not configured, so Step 1.7 is skipped |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |

> Note: The mock CLAUDE.md `### Product Lifecycle` section does not declare the
> Upstream Affected Component, PS Component, or Stream custom fields. The eval task
> says to use `customfield_10632` = `webpack`, and all three fields are filled in
> on the issue. So Step 4.3 is run here with customfield_10632 / 10669 / 10832.
> A real run would ask the engineer to add these fields to Security Configuration
> (via `/setup`). Without them, Step 4.3 would be skipped.

## Extracted CVE data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8011 | Issue |
| Issue type / Status | Vulnerability / New | Issue. Status New, so the full triage path runs |
| CVE ID | **CVE-2026-45678** | Label `CVE-2026-45678` + summary |
| Summary | CVE-2026-45678 webpack - Arbitrary Code Execution via loader chain [rhtpa-2.2] | Issue |
| Affected component | `pscomponent:org/rhtpa-ui` | Label / customfield_10669 |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | `versions` |
| Vulnerable library | **webpack** | Description / customfield_10632 |
| Affected version range | **< 5.98.0** ("versions before 5.98.0") | Description |
| Fixed version (fix threshold) | **5.98.0** | Description |
| CVSS | 7.8 (High) | Description |
| Upstream Affected Component (cf 10632) | webpack | Custom field |
| PS Component (cf 10669) | pscomponent:org/rhtpa-ui | Custom field |
| Stream (cf 10832) | rhtpa-2.2 | Custom field |
| Upstream fix PR | None found in remote links | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 | Remote links |
| Due date | 2026-08-15 | `duedate` |
| Existing issue links | None | `issuelinks` |
| Existing comments | None | Comments |

All critical fields (CVE ID, library, affected range) were parsed, so triage can continue.

## Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to stream **2.2.x** (Konflux repo `git.example.com/rhtpa/rhtpa-release.0.4.z`).
- The issue is **scoped** to 2.2.x.

## Ecosystem detection

- webpack is an **npm** package, which counts as a source dependency (2 remediation tasks per stream).
- Caveat: the mock 2.2.x `security-matrix.md` Ecosystem Mappings table lists only Cargo and RPM. There is no npm row and no `rhtpa-ui` repo, and `rhtpa-ui` is missing from the Source Repositories table, so its deployment context defaults to `upstream`. The mock data has no webpack lock-file versions either. In a real run, Step 2 would stop with "Unsupported ecosystem: npm is not yet supported for automated triage. Manual assessment is required" until an npm mapping (for example `package-lock.json` in rhtpa-ui) is added. No webpack versions are invented here.

## Step 1.5 – External enrichment (simulated)

External calls were not made, as the eval instructions require. The Jira description's fix threshold, **5.98.0**, is the authoritative value for comparisons. Confidence is lower because MITRE and OSV were not cross-checked.
