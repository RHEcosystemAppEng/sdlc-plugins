# Step 1 -- Data Extraction

## Issue Details

**Key**: TC-8050
**Summary**: CVE-2026-99001 criterion - Path traversal in benchmark output [rhtpa-2.2]
**Issue Type**: Vulnerability
**Status**: New

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99001 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | criterion |
| Affected version range | versions before 0.5.2 |
| Fixed version | 0.5.2 |
| CVSS | 5.3 (Medium) |
| Upstream fix PR | _(none in remote links)_ |
| Advisory URL | _(none in remote links)_ |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99001 |
| Due date | 2026-08-01 |
| Existing comments | _(none)_ |

## Stream Scope Resolution

Issue summary suffix: `[rhtpa-2.2]` maps to stream **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`).

Triage is scoped to the 2.2.x stream only.

## Ecosystem Detection

**Ecosystem**: Cargo (Rust crate -- criterion is a Rust benchmarking library)
**Category**: Source dependency
**Remediation tasks per stream**: 2 (upstream backport + downstream propagation)
