# Step 1 – Data Extraction: TC-8010

Source: `vuln-issue-overlap-covered.md` (simulated `jira.get_issue(TC-8010)` + `jira.get_issue_remote_links(TC-8010)`).

## Step 0 – Configuration (from claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component field | customfield_10632 (supplied by the task context and present on the issue. **Not listed** in the mock CLAUDE.md Security Configuration) |
| PS Component field | customfield_10669 (present on the issue. Not listed in the mock CLAUDE.md) |
| Stream field | customfield_10832 (present on the issue. Not listed in the mock CLAUDE.md) |
| ProdSec Jira account ID | Not configured, so no @mention |
| Embargo policy URL | Not configured, so Step 1.7 is skipped |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |

> Configuration note: strictly, Step 4.3 needs the three custom fields declared in
> Security Configuration. The mock CLAUDE.md omits them. The task gives
> customfield_10632 = `axios` explicitly and the issue carries all three fields, so
> the overlap check was run with those field IDs. In a real project, add them to
> CLAUDE.md through `/setup`.

## Step 0.3 – Matrix Staleness

`security-matrix-mock.md` has `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-03, so the matrix is **128 days** old, which is past the 14-day threshold. **Warning:** the matrix may not reflect recent releases. Proceeding for this eval, which is equivalent to choosing "Proceed anyway".

## Step 0.8 – Assign / Transition (proposed, not executed)

- The issue is currently **Unassigned** with status **New**.
- Proposed actions: assign it to the current triager, then transition to **Assigned** using a transition discovered at runtime.

## Extracted CVE Data

| Field | Value |
|---|---|
| Issue key | TC-8010 |
| Summary | CVE-2026-44492 axios - Server-Side Request Forgery via crafted URL [rhtpa-2.2] |
| Status | New |
| CVE ID | **CVE-2026-44492** (label + summary) |
| Affected component | `pscomponent:org/rhtpa-ui` |
| PSIRT-claimed product version | `[rhtpa-2.2]`, which maps to stream **2.2.x** |
| Affects Versions (Jira) | RHTPA 2.2.0 |
| Vulnerable library | **axios** |
| Ecosystem | **npm** |
| Affected version range | **< 1.8.2** ("versions before 1.8.2") |
| Fixed version (fix threshold) | **1.8.2** |
| CVSS | 8.1 (High) |
| Upstream fix PR | None in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| Due date | 2026-08-01 (already past as of 2026-11-03) |
| Existing comments | None |
| Existing issue links | None |
| customfield_10632 (Upstream Affected Component) | axios |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-ui |
| customfield_10832 (Stream) | rhtpa-2.2 |

## Stream Scope Resolution

- Suffix `[rhtpa-2.2]` maps to the configured Version Stream **2.2.x** (git.example.com/rhtpa/rhtpa-release.0.4.z).
- The issue is **scoped** to 2.2.x.

## Ecosystem / Deployment Context

- axios belongs to the **npm** ecosystem, a source dependency category. If new remediation were needed, that would mean 2 tasks per stream.
- **Caveat:** the mock 2.2.x `security-matrix.md` Ecosystem Mappings list only Cargo (backend) and RPM. It has no npm/rhtpa-ui row, and `rhtpa-ui` is not in the Source Repositories table. As a result:
  - No lock-file evidence exists for axios at pinned commits. Step 2 cannot produce verified per-version axios versions, and no version numbers have been invented.
  - The deployment context defaults to `upstream`.
- This gap does not change the outcome, because Step 4.3 finds that existing remediation already covers the fix threshold (see overlap-check.md).

## Step 1.5 – External Enrichment

Not performed. External calls are prohibited in this eval. The fix threshold of **1.8.2** comes from the Jira description and is used as-is. Confidence is reduced because there was no MITRE/OSV cross-validation.

## Step 1.7 – Embargo Check

CVSS 8.1 meets the >= 7.0 threshold. However, no Embargo policy URL is configured, so the step is **skipped**.
