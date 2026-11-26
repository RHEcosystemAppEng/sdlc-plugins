# Step 1 – Data Extraction: TC-8010

Mode: interactive (FULLSEND_OUTPUT_DIR absent). Simulated. No Jira or external calls were made. Data comes from the provided mock issue file.

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
| Upstream Affected Component field | customfield_10632 (from the task context and issue data; **not listed** in the mock CLAUDE.md Security Configuration) |
| PS Component field | customfield_10669 (from the issue data; not listed in CLAUDE.md) |
| Stream field | customfield_10832 (from the issue data; not listed in CLAUDE.md) |
| ProdSec Jira account ID | not configured (so no @mention) |
| Embargo policy URL | not configured (so Step 1.7 is skipped) |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend only |

All required sections are present, so validation passes.

## Step 0.3 – Matrix staleness

Both matrices have `Last-Updated: 2026-06-28T10:00:00Z`. That is **151 days old** as of 2026-11-26, past the 14-day threshold. **Staleness warning raised.** The options are Refresh / Proceed / Stop. This simulation proceeds because the triage result depends on the cross-CVE overlap, not on matrix contents.

## Extracted CVE data

| Field | Value |
|---|---|
| Issue key | TC-8010 |
| Status | New (full triage path) |
| CVE ID | CVE-2026-44492 (label and summary agree) |
| Summary | CVE-2026-44492 axios - Server-Side Request Forgery via crafted URL [rhtpa-2.2] |
| Affected component | `pscomponent:org/rhtpa-ui` |
| PSIRT-claimed product version (suffix) | `[rhtpa-2.2]` |
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

The suffix `[rhtpa-2.2]` maps to configured stream **2.2.x** (rhtpa-release.0.4.z). The issue is **scoped** to 2.2.x.

## Deployment context

`rhtpa-ui` is not listed in the Source Repositories table, so it defaults to `upstream`.

## Step 1.5 – External enrichment

MITRE and OSV were not queried because the eval forbids external calls. The fix threshold comes from the Jira description only (1.8.2), so confidence is reduced. The task context gives the same threshold (1.8.2).

## Step 1.7 – Embargo

CVSS 8.1 is above the threshold, but no Embargo policy URL is configured, so this step is skipped.

## Step 2 notes (version impact)

The ecosystem is npm. The provided security-matrix.md files list Cargo and RPM ecosystem mappings only. They have no npm mapping and no `rhtpa-ui` repository or package-lock data. The mock lock data has no axios entries. Under the guardrails ("do not fabricate"; unsupported ecosystem means manual assessment), I cannot build a lock-file version impact table for axios from the provided evidence. I did not invent one. This does not block the outcome, because Step 4.3 resolves the triage. See overlap-check.md.
