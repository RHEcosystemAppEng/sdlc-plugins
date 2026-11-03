# Step 1 – Data Extraction: TC-8011

Source: `vuln-issue-overlap-not-covered.md` (simulated `jira.get_issue(TC-8011, fields=*all)` and `jira.get_issue_remote_links(TC-8011)`). No live Jira calls were made.

## Mode

- Step 0.6: `FULLSEND_OUTPUT_DIR` is not set, so this is **interactive mode** (simulated). Jira mutations are written here as proposals and are not executed.

## Step 0 – Configuration (from claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |
| Upstream Affected Component field | customfield_10632. The task scenario supplies it and the issue has it populated. The mock CLAUDE.md does not list it explicitly. |
| PS Component field | customfield_10669 (populated on the issue) |
| Stream field | customfield_10832 (populated on the issue) |
| ProdSec Jira account ID | Not configured, so @mentions are omitted |
| Embargo policy URL | Not configured, so Step 1.7 is skipped |

## Step 0.3 – Matrix Staleness Check

- `security-matrix-mock.md` has `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-03, so the matrix is **128 days old**, well past the 14-day threshold.
- In a live run the engineer would get three choices: Refresh now, Proceed anyway, or Stop. This eval assumes **Proceed anyway**.

## Step 0.8 – Assign and Transition (proposed, not executed)

- Status is **New** and the issue is unassigned. Proposed actions: assign TC-8011 to the current user, then transition it to **Assigned** using a transition discovered dynamically with `get_transitions`.

## Extracted CVE Data

| Field | Value |
|---|---|
| Issue key | TC-8011 |
| Summary | CVE-2026-45678 webpack - Arbitrary Code Execution via loader chain [rhtpa-2.2] |
| Status | New |
| CVE ID | **CVE-2026-45678** (from the label and the summary) |
| Affected component | `pscomponent:org/rhtpa-ui` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` |
| Affects Versions (Jira) | RHTPA 2.2.0 |
| Vulnerable library | **webpack** |
| Affected version range | **< 5.98.0** ("versions before 5.98.0") |
| Fixed version (fix threshold) | **5.98.0** |
| CVSS | 7.8 (High) |
| Upstream fix PR | None in the remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Due date | 2026-08-15 (already past as of 2026-11-03) |
| Existing comments | None |
| Existing issue links | None |
| customfield_10632 (Upstream Affected Component) | webpack |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-ui |
| customfield_10832 (Stream) | rhtpa-2.2 |

All critical fields (CVE ID, library, affected range) were parsed.

## Stream Scope Resolution

- Suffix `[rhtpa-2.2]` maps to the configured stream **2.2.x** (rhtpa-release.0.4.z).
- The issue is **scoped** to stream 2.2.x.

## Ecosystem Detection

- webpack is an **npm** package, which falls in the source dependency category: 2 tasks per stream (dependency bump or upstream backport, plus downstream propagation).
- **Gap:** the Ecosystem Mappings table for stream 2.2.x lists only Cargo (backend) and RPM. npm and the `rhtpa-ui` repository are not listed. `rhtpa-ui` is also missing from the Source Repositories table, so its deployment context defaults to `upstream`.
- Under the skill rules this means an **unsupported ecosystem** for automated lock-file inspection: "npm is not yet supported for automated triage. Manual assessment is required." That affects Step 2 (version impact). It does not affect the Step 4.3 overlap check, which uses only Jira data.

## Step 1.5 – External CVE Data Enrichment

- MITRE and OSV were not queried, per the eval constraint that no external calls are allowed. This is treated as "both unavailable", so the Jira description's fix threshold of **5.98.0** is used with reduced confidence.

## Step 1.7 – Embargo Check

- CVSS 7.8 meets the threshold of 7.0 or higher, but no Embargo policy URL is configured, so the step is skipped silently.
