# Step 1 -- Data Extraction: TC-8006

## Step 0 -- Configuration Validation

Configuration validated from project CLAUDE.md:

| Setting | Value |
|---------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | Not configured |
| PS Component field | Not configured |
| Stream custom field | Not configured |
| ProdSec contact email | Not configured |
| ProdSec Jira account ID | Not configured |
| Embargo policy URL | Not configured |

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | upstream (default) |

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.1] |
| Affects Versions (Jira field) | RHTPA 2.1.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| Issue status | New |

## Stream Scope Resolution

Summary suffix: `[rhtpa-2.1]` maps to stream **2.1.x** (Konflux release repo: rhtpa-release.0.3.z).

This is a **scoped** issue -- Steps 3 and 4 will be scoped to the 2.1.x stream only.

## Ecosystem Detection

Vulnerable library `quinn-proto` is a Rust crate. Ecosystem: **Cargo**.

From the 2.1.x stream security-matrix.md Ecosystem Mappings:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | Cargo.lock | `git show <tag>:Cargo.lock` | release/0.3.z |

Cargo is a supported source dependency ecosystem. Remediation will require two tasks: upstream backport + downstream propagation.

## Deployment Context

Repository `rhtpa-backend` deployment context: **upstream** (default -- no explicit Deployment Context column present).

## Existing Issue Links

The issue has the following pre-existing links:

- **Related**: TC-8001 (CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2])
  - Link ID: 1990401
  - Type: Related
  - Direction: outward (TC-8006 -> TC-8001)

## Version Impact Analysis (Step 2)

Using data from security-matrix.md, the quinn-proto versions at each pinned tag are:

### Stream 2.1.x (issue scope)

| Version | Build Tag | quinn-proto version | Vulnerable (< 0.11.14)? |
|---------|-----------|---------------------|--------------------------|
| RHTPA 2.1.0 | v0.3.8 | 0.11.9 | YES |
| RHTPA 2.1.1 | v0.3.12 | 0.11.9 | YES |

### Stream 2.2.x (out of scope for this issue, but analyzed for cross-stream awareness)

| Version | Build Tag | quinn-proto version | Vulnerable (< 0.11.14)? |
|---------|-----------|---------------------|--------------------------|
| RHTPA 2.2.0 | v0.4.5 | 0.11.9 | YES |
| RHTPA 2.2.1 | v0.4.8 | 0.11.12 | YES |
| RHTPA 2.2.2 | v0.4.9 | (retag of v0.4.8 = 0.11.12) | YES (same as 2.2.1) |
| RHTPA 2.2.3 | v0.4.11 | 0.11.14 | NO (fixed) |
| RHTPA 2.2.4 | v0.4.12 | 0.11.14 | NO (fixed) |

### Summary

All versions in the 2.1.x stream are affected. The vulnerability was fixed in the 2.2.x stream starting at version RHTPA 2.2.3 (build v0.4.11, quinn-proto 0.11.14).
