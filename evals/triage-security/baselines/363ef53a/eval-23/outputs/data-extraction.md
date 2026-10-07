# Step 1 — Data Extraction: TC-8001

## Parsed CVE Data

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
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | _(none)_ |

## Stream Scope Resolution

Issue summary suffix: `[rhtpa-2.2]` maps to stream **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`).

This issue is **scoped** to the 2.2.x stream only. Steps 3-4 apply to the 2.2.x stream; cross-stream impact on 2.1.x is handled via Case A.

## Ecosystem Detection

Library: quinn-proto (Rust crate) -- Ecosystem: **Cargo**

Classification: **Source dependency** -- produces 2 remediation tasks per stream (upstream fix + downstream propagation).

## Deployment Context Lookup

| Component Label | Matched Repository | URL | Deployment Context |
|-----------------|--------------------|-----|--------------------|
| pscomponent:org/rhtpa-server | rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | **customer-shipped** |

The affected repository `rhtpa-backend` is found in the Source Repositories table with Deployment Context = `customer-shipped`. This deployment context will be used in Step 8 (Remediation) to generate coordination guidance in remediation task descriptions.

## Version Impact Analysis

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Source Tag | quinn-proto | Affected? | Notes |
|---------|--------|------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | |

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Latest Tag Version | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.11+) | YES |

## Affects Versions Correction (Step 3)

PSIRT-assigned Affects Versions: `RHTPA 2.0.0` (incorrect -- no such version exists in this product).

Scoped to stream 2.2.x per issue suffix `[rhtpa-2.2]`:

- Current: `[RHTPA 2.0.0]`
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are NOT affected (ship quinn-proto 0.11.14, which is the fixed version).

Versions 2.1.0 and 2.1.1 are also affected but belong to stream 2.1.x -- tracked separately via cross-stream impact (Case A).
