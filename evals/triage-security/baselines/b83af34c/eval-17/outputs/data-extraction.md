# Step 1 -- Data Extraction

## Issue: TC-8001

### Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (component label pattern: `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | (none) | Issue comment history |

### Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches configured Version Stream `2.2.x`)
- Issue stream scope: **scoped to 2.2.x**

### Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo** (source dependency)
- Classification: Source dependency -- 2 remediation tasks per stream (upstream backport + downstream propagation)

### Deployment Context

- Repository: rhtpa-backend
- Deployment context: **upstream** (default -- Deployment Context column absent from Source Repositories table)

### Configuration Extracted in Step 0

| Config Field | Value | Required/Optional |
|---|---|---|
| Project key | TC | Required |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 | Required |
| Jira version prefix | RHTPA | Required |
| Vulnerability issue type ID | 10024 | Required |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa | Required |
| Component label pattern | pscomponent: | Required |
| VEX Justification custom field | customfield_12345 | Optional |
| Embargo policy URL | https://example.com/security/embargo-policy | Optional |
| ProdSec contact email | (not configured) | Optional -- skipped silently |
| ProdSec Jira account ID | (not configured) | Optional -- skipped silently |
| Upstream Affected Component field | (not configured) | Optional -- Step 4.3 skipped |
| PS Component field | (not configured) | Optional -- Step 4.3 skipped |
| Stream custom field | (not configured) | Optional -- Step 4.3 skipped |

**Note on Embargo policy URL**: This is an optional field per SKILL.md. It was extracted successfully from the Security Configuration without raising an error. When present, it enables Step 1.7 (Embargo Check). When absent, Step 1.7 is skipped entirely. This ensures backward compatibility -- projects without an Embargo policy URL configured continue to function without any errors or interruptions.
