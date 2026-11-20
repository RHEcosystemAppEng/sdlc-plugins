# TC-8011 — Step 1 Data Extraction

Mode: interactive (`FULLSEND_OUTPUT_DIR` absent). Simulated — no Jira/MCP/git calls were made; all values come from the provided mock files.

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
| Upstream Affected Component field | customfield_10632 (supplied by task/issue; not declared in CLAUDE.md Security Configuration — see note) |
| PS Component field | customfield_10669 (from issue; not declared in CLAUDE.md) |
| Stream field | customfield_10832 (from issue; not declared in CLAUDE.md) |
| ProdSec Jira account ID | not configured — @mentions omitted |
| Embargo policy URL | not configured — Step 1.7 skipped |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend only (deployment context column absent → `upstream`) |

Note: the mock CLAUDE.md does not list the three custom-field IDs under Security Configuration. A strict read of the Step 4.3 prerequisite would skip cross-CVE overlap detection. The task explicitly supplies the field (`customfield_10632 = webpack`) and the JQL result, so Step 4.3 was run with those field IDs. Recommend adding them to Security Configuration.

## Step 0.3 – Matrix staleness

`<!-- Last-Updated: 2026-06-28T10:00:00Z -->` → **145 days old** (today 2026-11-20; threshold 14 days). **Stale.** In a live run, the engineer would choose Refresh now / Proceed anyway / Stop. For this eval: proceed anyway, noting the warning.

## Step 1 – Extracted CVE data

| Field | Value |
|---|---|
| Issue key | TC-8011 |
| Status | New (full triage path) |
| CVE ID | CVE-2026-45678 (label and summary agree) |
| Summary | CVE-2026-45678 webpack - Arbitrary Code Execution via loader chain [rhtpa-2.2] |
| Affected component (label) | `pscomponent:org/rhtpa-ui` |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-ui |
| Upstream Affected Component (customfield_10632) | webpack |
| Stream field (customfield_10832) | rhtpa-2.2 |
| PSIRT-claimed version (summary suffix) | `[rhtpa-2.2]` |
| Affects Versions (Jira) | RHTPA 2.2.0 |
| Vulnerable library | webpack |
| Affected version range | < 5.98.0 ("versions before 5.98.0") |
| Fixed version (fix threshold) | **5.98.0** |
| CVSS | 7.8 (High) |
| Upstream fix PR | none in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Due date | 2026-08-15 (already past as of 2026-11-20) |
| Assignee | Unassigned (Step 0.8 would assign to triager and transition New → Assigned, after confirmation) |
| Existing links | none |
| Existing comments | none |

All critical fields (CVE ID, library, affected range) were parsed successfully.

### Stream scope resolution

`[rhtpa-2.2]` → stream **2.2.x** (rhtpa-release.0.4.z). Issue is **scoped** to 2.2.x.

### Ecosystem detection

webpack → **npm** (source dependency category: 2 remediation tasks per stream).

Warning: the 2.2.x `security-matrix.md` Ecosystem Mappings table lists only **Cargo** (backend) and **RPM**. npm is not mapped, and the affected component repo (`rhtpa-ui`) is not in the CLAUDE.md Source Repositories table. Per the skill: "Unsupported ecosystem: npm is not yet supported for automated triage. Manual assessment is required." This blocks automated lock-file version impact analysis (Step 2). It does not affect the Step 4.3 overlap analysis.

### Deployment context

`rhtpa-ui` is not in Source Repositories → defaults to `upstream`.

## Step 1.5 – External enrichment

Not executed (no external calls allowed in this eval). Fix threshold taken from the Jira description: **5.98.0**. Confidence reduced: MITRE/OSV cross-validation not performed.

## Step 1.7 – Embargo check

CVSS 7.8 is above the threshold, but no Embargo policy URL is configured, so this step is skipped.
