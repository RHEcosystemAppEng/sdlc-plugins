# Data Extraction -- TC-8002

## Step 0 -- Configuration Validation

Configuration validated from project CLAUDE.md:

| Parameter | Value |
|-----------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories

| Repository | URL | Local Path |
|------------|-----|------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend |

## Step 1 -- Extracted CVE Data

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

### Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: rhtpa-release.0.4.z). This issue is **scoped** to the 2.2.x stream.

### Ecosystem Detection

The vulnerable library is **serde_json**, a Rust crate. This maps to the **Cargo** ecosystem. The lock file is `Cargo.lock` and the check command is `git show <tag>:Cargo.lock`.

### Additional References

- GitHub Advisory: https://github.com/advisories/GHSA-2026-j9r2-m5vk
- RustSec Advisory: https://rustsec.org/advisories/RUSTSEC-2026-0019.html
- CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-28940

### Vulnerability Description

A stack overflow vulnerability in serde_json. Versions before 1.0.135 are vulnerable to a stack overflow when deserializing deeply nested JSON input. An attacker can craft a JSON payload with thousands of nested arrays or objects that causes unbounded recursion during deserialization, leading to a stack overflow and process crash. The fix introduces a configurable recursion limit that defaults to 128 levels of nesting.
