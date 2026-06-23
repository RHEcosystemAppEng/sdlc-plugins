# Step 1 -- Data Extraction: TC-8002

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-28940 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | serde_json |
| Affected version range | versions before 1.0.135 |
| Fixed version | 1.0.135 |
| Upstream fix PR | N/A |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Due date | 2026-07-30 |
| CVSS | 5.3 (Medium) |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table. This issue is scoped to stream 2.2.x only.

## Ecosystem Detection

The vulnerable library `serde_json` is a Rust crate. The ecosystem is **Cargo**. The lock file to inspect is `Cargo.lock`, per the Ecosystem Mappings table for the 2.2.x stream.

## Vulnerability Description

Versions of serde_json before 1.0.135 are vulnerable to a stack overflow when deserializing deeply nested JSON input. An attacker can craft a JSON payload with thousands of nested arrays or objects that causes unbounded recursion during deserialization, leading to a stack overflow and process crash. The fix (1.0.135) introduces a configurable recursion limit that defaults to 128 levels of nesting.

## References

- https://github.com/advisories/GHSA-2026-j9r2-m5vk
- https://rustsec.org/advisories/RUSTSEC-2026-0019.html
