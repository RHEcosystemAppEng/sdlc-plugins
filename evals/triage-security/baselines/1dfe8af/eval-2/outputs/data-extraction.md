# Data Extraction -- TC-8002

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-28940 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Stream scope | 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | serde_json |
| Affected version range | versions before 1.0.135 |
| Fixed version | 1.0.135 |
| CVSS | 5.3 (Medium) |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Due date | 2026-07-30 |
| Existing comments | None |

## Ecosystem Detection

- **Ecosystem**: Cargo (Rust crate -- serde_json is a well-known Rust serde library)
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'`

## Stream Scope Resolution

The issue summary contains `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Version Streams configuration table. This issue is scoped to the 2.2.x stream only.

However, per the triage-security skill's rules, ALL supported versions across ALL streams must be checked for impact (Step 2), even though Affects Versions corrections (Step 3) are scoped to the issue's stream.

## Vulnerability Description

A stack overflow vulnerability in serde_json versions before 1.0.135. An attacker can craft a JSON payload with thousands of nested arrays or objects that causes unbounded recursion during deserialization, leading to a stack overflow and process crash. The fix (1.0.135) introduces a configurable recursion limit defaulting to 128 levels of nesting.
