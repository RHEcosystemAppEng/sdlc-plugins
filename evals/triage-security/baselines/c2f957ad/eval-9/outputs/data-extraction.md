# Step 1 – Data Extraction: TC-8011

Mode: interactive (FULLSEND_OUTPUT_DIR absent). Eval mode is on: no Jira MCP, WebFetch or `git show` calls were made. All data comes from the provided mock files and the eval task statement.

## Step 0 – Configuration validation (from claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | Not declared in Security Configuration. The eval task says it is customfield_10632 |
| PS Component field | Not declared. The issue data shows customfield_10669 |
| Stream field | Not declared. The issue data shows customfield_10832 |
| ProdSec Jira account ID | Not configured, so @mentions are left out |
| Embargo policy URL | Not configured, so Step 1.7 is skipped |
| Version Streams | 2.1.x -> rhtpa-release.0.3.z; 2.2.x -> rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend. No Deployment Context column, so it defaults to `upstream` |

All required sections are present, so validation passes.

**Configuration gap:** Step 4.3 needs the Upstream Affected Component, PS Component and Stream custom fields to be declared in Security Configuration. The mock CLAUDE.md does not declare them. The eval task gives the field values (customfield_10632 = webpack) and the JQL result, so Step 4.3 runs here using those values. In a real run, add these fields to Security Configuration or Step 4.3 would be skipped.

## Step 0.3 – Matrix staleness

`<!-- Last-Updated: 2026-06-28T10:00:00Z -->` is 151 days old as of 2026-11-26, past the 14-day threshold. **Warning:** the matrix may not reflect recent 2.2.x releases. A real run would offer Refresh / Proceed / Stop. This eval proceeds with the current matrix.

## Extracted CVE data

| Field | Value |
|---|---|
| Issue key | TC-8011 |
| Status | New (full triage path) |
| CVE ID | CVE-2026-45678 (label and summary) |
| Summary | CVE-2026-45678 webpack - Arbitrary Code Execution via loader chain [rhtpa-2.2] |
| Affected component | `pscomponent:org/rhtpa-ui` |
| PSIRT-claimed product version | `[rhtpa-2.2]` |
| Affects Versions (Jira) | RHTPA 2.2.0 |
| Vulnerable library | webpack |
| Affected version range | < 5.98.0 |
| Fixed version (fix threshold) | **5.98.0** |
| CVSS | 7.8 (High) |
| Upstream fix PR | None in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Due date | 2026-08-15 (already passed as of 2026-11-26) |
| Existing comments | None |
| Existing issue links | None |
| customfield_10632 (Upstream Affected Component) | webpack |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-ui |
| customfield_10832 (Stream) | rhtpa-2.2 |

The critical fields (CVE ID, library, affected range) were all parsed.

## Stream scope resolution

Suffix `[rhtpa-2.2]` maps to stream **2.2.x** (Konflux repo `git.example.com/rhtpa/rhtpa-release.0.4.z`). The issue is **scoped** to 2.2.x.

## Ecosystem detection

- webpack is an **npm** package, which the classification table treats as a source dependency. Remediation would be 2 tasks per stream.
- **Gap:** the 2.2.x Ecosystem Mappings table lists only Cargo (backend) and RPM. It has no npm row, and `rhtpa-ui` is not in Source Repositories. Under the skill rules, an ecosystem missing from the mapping table means "Unsupported ecosystem: manual assessment is required" for the version impact analysis in Step 2. The mock lock-file data also has no webpack versions. Per the "do not fabricate data" guardrail, **no per-version webpack impact table can be produced**. The PSIRT-claimed version (RHTPA 2.2.0) is not verified.
- Deployment context: `rhtpa-ui` is not in Source Repositories, so it defaults to `upstream`.

## Step 1.5 – External enrichment

Not run in this eval (no WebFetch). The Jira description value **5.98.0** is used as the fix threshold, with reduced confidence because MITRE and OSV were not cross-checked.

## Step 1.7 – Embargo check

Skipped because no Embargo policy URL is configured. CVSS 7.8 would otherwise have triggered the gate.
