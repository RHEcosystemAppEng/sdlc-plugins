# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-28940 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | serde_json |
| Affected version range | < 1.0.135 |
| Fixed version | 1.0.135 |
| CVSS | 5.3 (Medium) |
| Upstream fix PR | -- |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Due date | 2026-07-30 |
| Existing comments | None |
| Reporter | (PSIRT auto-created) |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table. This issue is **scoped** to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library is **serde_json**, which is a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, the ecosystem is **Cargo**. The lock file to inspect is `Cargo.lock`, and the check command is `git show <tag>:Cargo.lock`.

## Vulnerability Summary

A stack overflow vulnerability exists in serde_json versions before 1.0.135. Deeply nested JSON input causes unbounded recursion during deserialization, leading to a stack overflow and process crash. The fix (1.0.135) introduces a configurable recursion limit defaulting to 128 levels of nesting.
