# Step 1 – Data Extraction: TC-8011

Mode: interactive (simulated; `FULLSEND_OUTPUT_DIR` not set). No Jira, git, or
external calls were made. All data comes from the provided mock files.

## Step 0 – Configuration validation (from claude-md-security-config.md)

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component field | customfield_10632 (from task context; not listed in the mock CLAUDE.md Security Configuration, see note) |
| PS Component field | customfield_10669 (from issue data) |
| Stream field | customfield_10832 (from issue data) |
| ProdSec Jira account ID | not configured, so @mentions are omitted |
| Embargo policy URL | not configured, so Step 1.7 is skipped |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend only (deployment context defaults to `upstream`) |

Configuration note: the mock CLAUDE.md doesn't declare the Upstream Affected
Component, PS Component, or Stream custom fields. Read strictly, Step 4.3's
prerequisite would skip the overlap check. The task states that
customfield_10632 = `webpack` and that the `cf[10632]` JQL search was run, so
this triage treats those fields as configured. Add them to Security
Configuration so future runs don't depend on this assumption.

## Step 0.3 – Matrix staleness

Both stream matrices have `Last-Updated: 2026-06-28T10:00:00Z`. Today is
2026-11-26, so the matrices are **151 days old**, well past the 14-day
threshold. In a live run the engineer would be asked to choose Refresh / Proceed /
Stop. For this eval the triage continues ("Proceed anyway") and records the
warning.

## Extracted CVE data

| Field | Value |
|-------|-------|
| Issue key | TC-8011 |
| Issue type / Status | Vulnerability / New |
| CVE ID | CVE-2026-45678 (label and summary agree) |
| Summary | CVE-2026-45678 webpack - Arbitrary Code Execution via loader chain [rhtpa-2.2] |
| Affected component | `pscomponent:org/rhtpa-ui` |
| Product version claimed by PSIRT (suffix) | `[rhtpa-2.2]` |
| Affects Versions (Jira) | RHTPA 2.2.0 |
| Vulnerable library | webpack |
| Ecosystem | npm (source dependency) |
| Affected version range | < 5.98.0 ("versions before 5.98.0") |
| Fixed version (fix threshold) | **5.98.0** |
| CVSS | 7.8 (High) |
| Upstream fix PR | none in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Due date | 2026-08-15 (**already past**) |
| Assignee | Unassigned (Step 0.8 would assign it to the current user and move it to Assigned) |
| Existing comments | none |
| Existing issue links | none |
| customfield_10632 (Upstream Affected Component) | webpack |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-ui |
| customfield_10832 (Stream) | rhtpa-2.2 |

## Stream scope resolution

The suffix `[rhtpa-2.2]` maps to the configured Version Stream **2.2.x**
(`git.example.com/rhtpa/rhtpa-release.0.4.z`). The issue is **scoped** to 2.2.x.

## Step 1.5 – External enrichment

MITRE and OSV were not queried because the eval forbids external calls. The fix
threshold comes from the Jira description only (5.98.0), with reduced
confidence:

> External CVE databases unavailable: using Jira description data only.
> Fix threshold confidence is reduced.

## Step 1.7 – Embargo check

CVSS 7.8 meets the threshold (>= 7.0), but no Embargo policy URL is configured,
so this step is skipped silently.

## Ecosystem and deployment-context observations

- webpack is an **npm** package. The 2.2.x stream's Ecosystem Mappings table in
  the mock matrix lists only **Cargo** (backend) and **RPM**. No npm or
  `rhtpa-ui` mapping exists, and the mock lock-file data has no webpack versions.
- `rhtpa-ui` isn't in the Source Repositories table, so the deployment context
  defaults to `upstream`.
- As a result, Step 2 version impact can't be computed from lock-file evidence
  (see triage-outcome.md). No dependency versions were invented.
