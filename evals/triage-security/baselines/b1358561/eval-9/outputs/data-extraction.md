# Step 1 – Data Extraction: TC-8011

Mode: interactive (FULLSEND_OUTPUT_DIR not set). Simulated eval run: no Jira MCP, git, or WebFetch calls were made. All data comes from the supplied mock files.

## Step 0 – Configuration (from claude-md-security-config.md)

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component field | Not in the Security Configuration. The task supplies `customfield_10632` |
| PS Component field | Not in the Security Configuration. The issue carries `customfield_10669` |
| Stream field | Not in the Security Configuration. The issue carries `customfield_10832` |
| ProdSec Jira account ID | Not configured, so no @mention |
| Embargo policy URL | Not configured, so Step 1.7 is skipped |
| Version Streams | 2.1.x -> rhtpa-release.0.3.z; 2.2.x -> rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend only (no Deployment Context column, so it defaults to `upstream`) |

Step 0 validation passes because all required sections are present.

## Step 0.3 – Matrix Staleness

The mock matrix says `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. Today is 2026-11-27, so the matrix is **152 days old**, well past the 14-day threshold. In a live run the skill would warn the engineer here and offer three choices: Refresh now, Proceed anyway, or Stop. For this eval the analysis goes ahead with the matrix as supplied, and the staleness is flagged.

## Step 0.8 – Assign and transition (proposed, not executed)

- Assign TC-8011 to the current user.
- Move it from New to Assigned. The issue status is New.

## Extracted CVE data

| Field | Value |
|-------|-------|
| Issue key | TC-8011 |
| Status | New |
| CVE ID | CVE-2026-45678 (from the label and the summary) |
| Summary | CVE-2026-45678 webpack - Arbitrary Code Execution via loader chain [rhtpa-2.2] |
| Affected component (PS label) | `pscomponent:org/rhtpa-ui` |
| PSIRT-claimed product version (summary suffix) | `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | webpack |
| Affected version range | < 5.98.0 ("versions before 5.98.0") |
| Fixed version / fix threshold | **5.98.0** |
| CVSS | 7.8 (High) |
| Upstream fix PR | None in the remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Due date | 2026-08-15 (already past) |
| Assignee | Unassigned |
| Existing issue links | None |
| Existing comments | None |
| customfield_10632 (Upstream Affected Component) | webpack |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-ui |
| customfield_10832 (Stream) | rhtpa-2.2 |

All critical fields parsed: the CVE ID, the library, and the affected range.

## Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to the configured stream **2.2.x** (rhtpa-release.0.4.z).
- The issue is **scoped** to the 2.2.x stream.

## Ecosystem detection

- webpack is a JavaScript package, so the ecosystem is **npm**. That makes it a source dependency, which normally means 2 remediation tasks per stream.
- **Gap:** the 2.2.x Ecosystem Mappings table (and the 2.1.x one) lists only Cargo (backend) and RPM. It has **no npm row**. Under the skill's ecosystem rule, the result is:
  > **Unsupported ecosystem**: npm is not yet supported for automated triage. Manual assessment is required.
- No lock-file data for webpack exists in the mock matrix. `package-lock.json` versions are not available for any tag.

## Deployment context

- The affected repository, implied by `pscomponent:org/rhtpa-ui`, is rhtpa-ui. It is **not** in the Source Repositories table, so its deployment context defaults to `upstream`.

## Step 1.5 – External enrichment

This step was not performed because the eval forbids external calls. The skill's rule is to fall back to the Jira description data, so the fix threshold is 5.98.0, taken from the description. Confidence is reduced:
> External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced.

## Step 1.7 – Embargo check

Skipped. No Embargo policy URL is configured, even though CVSS 7.8 is above the threshold.
