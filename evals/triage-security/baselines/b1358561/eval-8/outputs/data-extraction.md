# Step 1 – Data Extraction: TC-8010

Source: mock Jira issue (`vuln-issue-overlap-covered.md`). No Jira MCP calls were made.

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8010 | Issue |
| Issue type | Vulnerability | Issue |
| Status | New | Issue (full-triage path) |
| CVE ID | CVE-2026-44492 | Label `CVE-2026-44492` + summary |
| Summary | CVE-2026-44492 axios - Server-Side Request Forgery via crafted URL [rhtpa-2.2] | Issue |
| Affected component | `pscomponent:org/rhtpa-ui` | Label matching the `pscomponent:` pattern |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` → stream **2.2.x** | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | `versions` field |
| Vulnerable library | axios | Description |
| Ecosystem | npm (JavaScript package) | Library name / component (rhtpa-ui) |
| Affected version range | `< 1.8.2` ("versions before 1.8.2") | Description |
| Fixed version (fix threshold) | **1.8.2** | Description |
| CVSS | 8.1 (High) | Description |
| Vulnerability class | SSRF: hostname validation bypassed when following redirects | Description |
| Upstream fix PR | None in remote links | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 | Remote links |
| Due date | 2026-08-01 | `duedate` |
| Assignee | Unassigned | Issue |
| Existing comments | None | Issue |
| Existing issue links | None | Issue |

## Custom Fields

| Field | Value |
|-------|-------|
| customfield_10632 (Upstream Affected Component) | axios |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-ui |
| customfield_10832 (Stream) | rhtpa-2.2 |

## Stream Scope Resolution

- The suffix `[rhtpa-2.2]` maps to the configured Version Stream **2.2.x**
  (`git.example.com/rhtpa/rhtpa-release.0.4.z`).
- **Issue stream scope: 2.2.x (scoped).** Steps 3, 4 and 8 apply to the 2.2.x stream only.

## Step 1.5 – External enrichment (simulated)

The eval does not allow external calls, so MITRE and OSV.dev were not queried. The
fix threshold comes from the Jira description: **axios >= 1.8.2**. The task statement
gives the same threshold (1.8.2), so there is nothing to reconcile.
> ⚠ External CVE databases were not queried. This analysis uses the Jira description only, so confidence in the fix threshold is lower.

## Step 1.7 – Embargo check

CVSS 8.1 is at or above the 7.0 trigger, but the project CLAUDE.md does not configure an
Embargo policy URL. The step is skipped silently.

## Configuration observations (Step 0 / Step 1)

- Security Configuration has everything Step 0 requires: product pages URL, version
  prefix `RHTPA`, Vulnerability issue type `10024`, component label pattern `pscomponent:`,
  version streams and source repositories. The VEX Justification field `customfield_12345`
  is also configured.
- The mock CLAUDE.md does **not** declare the Upstream Affected Component, PS Component or
  Stream custom-field IDs under Security Configuration. The task statement and the issue
  data supply them (`customfield_10632`, `customfield_10669`, `customfield_10832`), and the
  task explicitly asks for Step 4.3, so Step 4.3 runs with those IDs. Recommendation: add
  these three fields to Security Configuration (via `/setup`) so that Step 4.3 and
  Step 7.5.3 run without this override.
- The affected repository `rhtpa-ui` is not in the Source Repositories table. Deployment
  context therefore defaults to `upstream`.
- The 2.2.x `security-matrix.md` Ecosystem Mappings table lists only Cargo (backend) and
  RPM. It has **no npm mapping** and contains no axios lock-file data. A full Step 2 run
  would hit the "Unsupported ecosystem / manual assessment" path for the npm lock-file
  inspection, and no axios version can be claimed for any RHTPA release (no fabricated
  data). The cross-CVE overlap result below does not depend on lock-file versions. If the
  existing remediation is in place, the threshold is satisfied whatever version ships
  today.
- Matrix staleness: `Last-Updated` is 2026-06-28, which is 152 days before 2026-11-27 and
  over the 14-day threshold. Interactively, the engineer would be offered
  Refresh / Proceed / Stop. This eval proceeds with the current matrix.
