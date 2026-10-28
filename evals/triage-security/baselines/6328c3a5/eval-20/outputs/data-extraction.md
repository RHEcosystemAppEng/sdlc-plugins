# Step 1 -- Data Extraction

## Issue: TC-8001

Parsed CVE data from Vulnerability issue TC-8001:

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | (none) |

## Stream Scope Resolution

- **Summary suffix:** [rhtpa-2.2]
- **Mapped stream:** 2.2.x (rhtpa-release.0.4.z)
- **Scope:** Scoped to stream 2.2.x only

The summary suffix `[rhtpa-2.2]` maps to the configured Version Stream `2.2.x` (Konflux release repo `git.example.com/rhtpa/rhtpa-release.0.4.z`). This issue is stream-scoped: Steps 3-4 will apply to the 2.2.x stream only, with cross-stream impact analysis (Case A) checking whether other streams are also affected.

## Ecosystem Detection

- **Library:** quinn-proto (Rust crate)
- **Ecosystem:** Cargo
- **Category:** Source dependency
- **Lock file:** Cargo.lock
- **Check command:** `git show <tag>:Cargo.lock`
- **Remediation tasks per stream:** 2 (upstream backport or dependency bump + downstream propagation)

## Affects Versions Mismatch (Preliminary)

The PSIRT-assigned Affects Versions field shows **RHTPA 2.0.0**, but the issue summary suffix indicates stream **2.2.x**. Additionally, there is no configured 2.0.x version stream in Security Configuration. This discrepancy will be corrected in Step 3 (Affects Versions Correction) after version impact analysis confirms which versions actually ship the vulnerable quinn-proto dependency.

## Version Impact Preview (from Mock Lock File Data)

Based on the security matrix mock data, the quinn-proto versions by tag are:

| Stream | Version | Build Tag | quinn-proto version | Affected? (< 0.11.14) |
|--------|---------|-----------|---------------------|-----------------------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES |
| 2.2.x | 2.2.2 | v0.4.9 | (retag of v0.4.8) 0.11.12 | YES (same as 2.2.1) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO (fixed) |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO (fixed) |

### Summary

- **Stream 2.1.x:** All versions (2.1.0, 2.1.1) ship vulnerable quinn-proto (0.11.9 < 0.11.14)
- **Stream 2.2.x:** Versions 2.2.0-2.2.2 are affected; versions 2.2.3-2.2.4 ship the fixed version (0.11.14)
- **Cross-stream impact:** Stream 2.1.x is also affected (all versions), but this issue is scoped to 2.2.x -- Case A cross-stream impact notice applies
