# Step 1 -- Data Extraction: TC-8040

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the configured Version Stream **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

- Issue stream scope: **2.2.x** (scoped to a single stream)

## Ecosystem Detection

The vulnerable library is **quinn-proto**, which is a QUIC protocol implementation. Based on the task-specified override, the ecosystem detection resolves to **Go modules**.

### Ecosystem Mappings check (stream 2.2.x)

The Ecosystem Mappings table for the 2.2.x stream (`security-matrix.md`) lists the following supported ecosystems:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

**Supported ecosystems**: Cargo, RPM

**Detected ecosystem**: Go modules

**Result**: Go modules is **NOT** listed in the Ecosystem Mappings table. Automated triage cannot proceed for this ecosystem.

## Deployment Context Lookup

The affected repository is identified from the component label `pscomponent:org/rhtpa-server`. Looking up the Source Repositories table in the project CLAUDE.md:

| Repository | URL | Local Path |
|------------|-----|------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend |

The Deployment Context column is absent from the Source Repositories table, so the default deployment context of `upstream` applies.

## Configuration Extracted (Step 0)

| Configuration | Value |
|---------------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |

## Triage Halted

Triage cannot proceed past Step 1 because the detected ecosystem (Go modules) is not supported in the Ecosystem Mappings table. See `outputs/unsupported-ecosystem.md` for the notification presented to the user.
