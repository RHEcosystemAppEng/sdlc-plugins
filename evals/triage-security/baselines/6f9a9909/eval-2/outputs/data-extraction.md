# Data Extraction -- TC-8002

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-28940 |
| Jira Issue Key | TC-8002 |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component | pscomponent:org/rhtpa-server |
| Product Version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable Library | serde_json |
| Affected Version Range | versions before 1.0.135 |
| Fixed Version | 1.0.135 |
| CVSS Score | 5.3 (Medium) |
| Due Date | 2026-07-30 |
| Assignee | Unassigned |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Existing Comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped to stream: **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`)
- Issue is **scoped** to the 2.2.x stream

## Ecosystem Detection

- Library: serde_json (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'`

## Vulnerability Description

A stack overflow vulnerability in serde_json. Versions before 1.0.135 are vulnerable to unbounded recursion when deserializing deeply nested JSON input. An attacker can craft a JSON payload with thousands of nested arrays or objects causing a stack overflow and process crash. The fix introduces a configurable recursion limit defaulting to 128 levels of nesting.

## External References

- GitHub Advisory: https://github.com/advisories/GHSA-2026-j9r2-m5vk
- CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-28940
- RustSec Advisory: https://rustsec.org/advisories/RUSTSEC-2026-0019.html
