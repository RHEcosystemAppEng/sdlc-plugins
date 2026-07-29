# Step 1 -- Data Extraction: TC-8002

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-28940 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | serde_json |
| Affected version range | versions before 1.0.135 |
| Fixed version | 1.0.135 |
| CVSS | 5.3 (Medium) |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Due date | 2026-07-30 |
| Existing comments | None |
| Issue status | New |
| Assignee | Unassigned |

## Additional References

- GHSA: https://github.com/advisories/GHSA-2026-j9r2-m5vk
- RustSec: https://rustsec.org/advisories/RUSTSEC-2026-0019.html

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`). This issue is **stream-scoped** to the 2.2.x stream.

However, all configured streams (2.1.x and 2.2.x) must still be checked for version impact analysis per the skill methodology (Step 2 checks all streams, while Steps 3-4 scope corrections to the issue's stream).

## Ecosystem Detection

- **Ecosystem**: Cargo (Rust crate -- serde_json is a Rust crate)
- **Category**: Source dependency
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'`
- **Upstream branches**: `release/0.3.z` (2.1.x stream), `release/0.4.z` (2.2.x stream)

## Vulnerability Description

A stack overflow vulnerability in serde_json versions before 1.0.135 allows an attacker to craft deeply nested JSON input (thousands of nested arrays or objects) causing unbounded recursion during deserialization, leading to a process crash. The fix in 1.0.135 introduces a configurable recursion limit defaulting to 128 levels.
