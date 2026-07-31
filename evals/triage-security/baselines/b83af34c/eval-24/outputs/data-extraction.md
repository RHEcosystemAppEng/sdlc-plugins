# Step 0 -- Validate Project Configuration

## Configuration Validated

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **Upstream Affected Component custom field**: not configured (Step 4.3 skipped)
- **PS Component custom field**: not configured
- **Stream custom field**: not configured
- **ProdSec contact email**: not configured
- **ProdSec Jira account ID**: not configured
- **Embargo policy URL**: not configured (Step 1.7 skipped)

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories

The Source Repositories table does NOT contain a Deployment Context column.
Per SKILL.md Step 0 (backward compatibility rule): all repositories default to deployment context `upstream`.

Parsed Source Repositories mapping:

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | upstream (defaulted -- no Deployment Context column) |

---

# Step 1 -- Data Extraction

## Parsed CVE Data from TC-8001

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |

### Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]` which maps to configured Version Stream **2.2.x**.
This issue is **scoped** to stream 2.2.x only.

### Ecosystem Detection

Vulnerable library: quinn-proto (Rust crate)
Ecosystem: **Cargo** (source dependency)
Classification: Source dependency ecosystem -- remediation produces **2 tasks** per stream (upstream backport + downstream propagation).

### Deployment Context Lookup

Affected repository from component label `pscomponent:org/rhtpa-server` maps to **rhtpa-backend**.
Source Repositories table has no Deployment Context column.
Per backward compatibility rule (SKILL.md Step 0): deployment context defaulted to **upstream**.
Per remediation-templates.md: Coordination Guidance subsection is **omitted entirely** when the Deployment Context column is absent.

---

# Step 2 -- Version Impact Analysis

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same source commits as v0.4.8) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | at fix threshold |
| 2.2.4 | 2.2.x | 0.11.14 | NO | |

## Summary

- **In-scope stream (2.2.x)**: versions 2.2.0, 2.2.1, 2.2.2 are AFFECTED; versions 2.2.3, 2.2.4 are NOT affected.
- **Cross-stream (2.1.x)**: versions 2.1.0, 2.1.1 are AFFECTED (Case A applies -- cross-stream impact notification).
