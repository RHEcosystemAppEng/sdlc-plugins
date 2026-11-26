# Step 1 – Data Extraction: TC-8010

Mode: interactive (FULLSEND_OUTPUT_DIR absent, so Step 0.7 is skipped). Jira, git, and
external calls are simulated from the eval input files. No real calls were made.

## Step 0 – Configuration Validation (from claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | customfield_10632 (from task context; not listed in the mock CLAUDE.md) |
| PS Component field | customfield_10669 (from task context and issue fields) |
| Stream field | customfield_10832 (from task context and issue fields) |
| ProdSec Jira account ID | not configured, so no @mention |
| Embargo policy URL | not configured, so Step 1.7 is skipped |
| Version Streams | 2.1.x -> rhtpa-release.0.3.z; 2.2.x -> rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (deployment context column absent, so default `upstream`) |

All required sections exist (Repository Registry, Jira Configuration, Code Intelligence,
Security Configuration with Product Lifecycle, Version Streams, Source Repositories).

**Config gap:** the mock CLAUDE.md does not list the three optional overlap fields
(Upstream Affected Component, PS Component, Stream). The task gives them explicitly
(customfield_10632 = axios) and the issue carries all three, so Step 4.3 runs with
those IDs. Add them to Security Configuration so future runs do not skip Step 4.3.

## Step 0.3 – Matrix Staleness

The matrix file has `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-26, so the
matrix is 151 days old, which is over the 14-day threshold. **Warning:** the matrix may
not reflect recent releases. The options are Refresh / Proceed / Stop. This analysis
proceeds with the current matrix. The outcome rests on Jira remediation coverage
(Step 4.3), not on matrix contents.

## Step 0.8 – Assign and Transition (proposed, needs confirmation)

- Assign TC-8010 to the current user. It is currently Unassigned.
- Transition New -> Assigned, using the transition ID discovered dynamically through `get_transitions`.

## Extracted Fields

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8010 | Issue |
| Status | New, so full triage runs | Issue |
| CVE ID | CVE-2026-44492 | Label + summary |
| Summary | CVE-2026-44492 axios - Server-Side Request Forgery via crafted URL [rhtpa-2.2] | Issue |
| Affected component | `pscomponent:org/rhtpa-ui` | Label (matches `pscomponent:` pattern) |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira) | RHTPA 2.2.0 | `versions` field |
| Vulnerable library | axios | Description |
| Affected version range | < 1.8.2 ("versions before 1.8.2") | Description |
| Fixed version (fix threshold) | **1.8.2** | Description |
| CVSS | 8.1 (High) | Description |
| Upstream fix PR | none in remote links | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 | Remote links |
| Due date | 2026-08-01, already past as of 2026-11-26 | `duedate` |
| Existing comments | none | Comments |
| Existing issue links | none | `issuelinks` |
| customfield_10632 (Upstream Affected Component) | axios | Custom field |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-ui | Custom field |
| customfield_10832 (Stream) | rhtpa-2.2 | Custom field |

## Stream Scope Resolution

The suffix `[rhtpa-2.2]` maps to stream **2.2.x**, which is configured
(git.example.com/rhtpa/rhtpa-release.0.4.z). The issue is **scoped** to 2.2.x.

## Ecosystem Detection

- axios is an **npm** package, so its category is source dependency.
- **Note:** the 2.2.x `security-matrix.md` Ecosystem Mappings list only Cargo and RPM.
  npm is not mapped, and `org/rhtpa-ui` is not in Source Repositories, so the
  deployment context defaults to `upstream`. Normally lock-file version impact analysis
  (Step 2) for npm would stop with "Unsupported ecosystem: npm is not yet supported for
  automated triage. Manual assessment is required." The mock matrix also has no axios
  lock-file data. In this case Step 4.3 finds existing remediation that already covers
  the fix, so the triage outcome does not depend on npm lock-file evidence. No axios
  versions were invented.

## Step 1.5 – External Enrichment (simulated)

External calls are disallowed in this eval, so MITRE and OSV were not queried and are
treated as unavailable. "External CVE databases unavailable — using Jira description
data only. Fix threshold confidence is reduced." Fix threshold used: **1.8.2**, which
matches the threshold the task states.

## Step 1.7 – Embargo Check

Skipped because no Embargo policy URL is configured. CVSS 8.1 would otherwise trigger
the gate.
