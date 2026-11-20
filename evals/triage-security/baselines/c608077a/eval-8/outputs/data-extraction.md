# Step 1 – Data Extraction: TC-8010

Mode: interactive (FULLSEND_OUTPUT_DIR not set). Jira data comes from the mock issue file. No Jira MCP calls were made.

## Step 0 – Configuration check (from claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component field | customfield_10632 (supplied by the task prompt and present on the issue. **Not listed** in the mock CLAUDE.md Security Configuration.) |
| PS Component field | customfield_10669 (present on the issue. Not listed in the mock CLAUDE.md.) |
| Stream field | customfield_10832 (present on the issue. Not listed in the mock CLAUDE.md.) |
| ProdSec Jira account ID | not configured, so no @mention |
| Embargo policy URL | not configured, so Step 1.7 is skipped |
| Version Streams | 2.1.x -> rhtpa-release.0.3.z; 2.2.x -> rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend only |

## Step 0.3 – Matrix staleness

Both streams' matrix files show `Last-Updated: 2026-06-28T10:00:00Z`. That is 145 days before today (2026-11-20), well past the 14-day threshold. In a live run the engineer would be asked to choose Refresh, Proceed or Stop. For this eval: **proceed anyway**, with the staleness noted.

## Step 0.8 – Assign / transition (proposed only, not executed)

- Assign TC-8010 to the current user.
- Transition New -> Assigned. The transition ID would be discovered dynamically with `get_transitions`.

## Extracted CVE data

| Field | Value |
|---|---|
| Issue key | TC-8010 |
| Status | New (full triage path) |
| CVE ID | CVE-2026-44492 (label + summary) |
| Summary | CVE-2026-44492 axios - Server-Side Request Forgery via crafted URL [rhtpa-2.2] |
| Affected component (PS label) | `pscomponent:org/rhtpa-ui` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` |
| Affects Versions (Jira) | RHTPA 2.2.0 |
| Vulnerable library | axios |
| Ecosystem | npm (source dependency) |
| Affected version range | < 1.8.2 ("versions before 1.8.2") |
| Fixed version / fix threshold | **1.8.2** |
| CVSS | 8.1 (High) |
| Upstream fix PR | none in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| Due date | 2026-08-01 (already past) |
| Assignee | Unassigned |
| Existing comments | none |
| Existing issue links | none |
| customfield_10632 (Upstream Affected Component) | axios |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-ui |
| customfield_10832 (Stream) | rhtpa-2.2 |

## Stream scope resolution

The suffix `[rhtpa-2.2]` maps to stream **2.2.x** (rhtpa-release.0.4.z). The issue is **scoped** to 2.2.x.

## Deployment context

The affected repository is rhtpa-ui. It is **not** in the Source Repositories table, so the deployment context defaults to `upstream`.

## Step 1.5 – External enrichment

The task said not to call external tools, so MITRE and OSV were not queried. The Jira description's fix threshold of **1.8.2** is used, with reduced confidence.

## Step 1.7 – Embargo check

Skipped because no Embargo policy URL is configured. CVSS 8.1 would otherwise have triggered the gate.

## Notes and gaps

- The mock security matrices list only the Cargo and RPM ecosystems, for the backend repo. npm/rhtpa-ui is not mapped, and the mock data has no axios lock-file entries. Step 2 version impact therefore cannot be computed from evidence. Per the "do not fabricate" rule, no axios versions per release are claimed. In a live run this would be raised with the engineer (unsupported ecosystem or missing mapping). It does not change the Step 4.3 outcome, which rests on the existing remediation's bump target.
