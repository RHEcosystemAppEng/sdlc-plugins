# Step 0 -- Validate Project Configuration

Configuration validated from CLAUDE.md (claude-md-security-config.md):

| Config Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend (https://github.com/rhtpa/rhtpa-backend) |

All required sections present: Repository Registry, Jira Configuration, Code Intelligence, Security Configuration (Product Lifecycle, Version Streams, Source Repositories).

Optional fields not configured: Upstream Affected Component, PS Component, Stream custom field, ProdSec contact email, ProdSec Jira account ID. Step 4.3 (cross-CVE overlap detection) will be skipped since the Upstream Affected Component field is not configured.

---

# Step 1 -- Data Extraction

Parsed from Vulnerability issue TC-8003:

| Field | Value |
|---|---|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | Not provided |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| Issue status | New |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`.
- Parsed suffix: rhtpa-2.2 -> stream 2.2.x
- Matched to Version Streams table: stream 2.2.x at rhtpa-release.0.4.z
- Issue stream scope: **2.2.x only**

Steps 3-4 will be scoped to the 2.2.x stream. Other streams (2.1.x) are analyzed for cross-stream impact but Affects Versions corrections apply only to 2.2.x versions.

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: Cargo.lock
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
- Upstream branch (2.2.x stream): release/0.4.z

---

# Step 1.5 -- External CVE Data Enrichment

(Simulated -- external APIs not called in eval mode)

The Jira description provides:
- Affected range: versions before 0.11.14
- Fixed version: 0.11.14

In a live triage, MITRE CVE API and OSV.dev would be queried to cross-validate. For this eval, using the Jira description data as the authoritative fix threshold.

**Fix threshold used for Step 2.3: 0.11.14**

---

# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix

Loaded from security-matrix-mock.md. Two streams configured:

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend tag |
|---------|-------|------------|-------------|
| 2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8 |
| 2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12 |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 | |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 | |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 | |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 | |

## 2.3 -- Dependency Version Extraction

quinn-proto versions extracted from lock file data at each pinned commit:

| Tag | quinn-proto version | Affected? (< 0.11.14) |
|-----|---------------------|-----------------------|
| v0.3.8 | 0.11.9 | YES |
| v0.3.12 | 0.11.9 | YES |
| v0.4.5 | 0.11.9 | YES |
| v0.4.8 | 0.11.12 | YES |
| v0.4.9 | (retag of v0.4.8) | YES (same as v0.4.8) |
| v0.4.11 | 0.11.14 | NO (fixed) |
| v0.4.12 | 0.11.14 | NO (fixed) |

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | fixed at 0.11.14 |
| 2.2.4 | 2.2.x | 0.11.14 | NO | fixed at 0.11.14 |

Summary:
- Stream 2.1.x: ALL versions affected (2.1.0, 2.1.1)
- Stream 2.2.x: versions 2.2.0, 2.2.1, 2.2.2 are affected; versions 2.2.3, 2.2.4 are NOT affected (fixed)
- The fix was introduced in build 0.4.11 (version 2.2.3), which ships quinn-proto 0.11.14
