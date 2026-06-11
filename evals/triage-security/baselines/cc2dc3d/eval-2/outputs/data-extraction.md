# Step 1 -- Data Extraction: TC-8002

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-28940 |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` -- maps to stream **2.2.x** |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | serde_json |
| Affected version range | versions before 1.0.135 |
| Fixed version | 1.0.135 |
| CVSS | 5.3 (Medium) |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Upstream fix reference | https://rustsec.org/advisories/RUSTSEC-2026-0019.html |
| Due date | 2026-07-30 |
| Issue status | New |
| Assignee | Unassigned |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream, covered by Konflux release repo `rhtpa-release.0.4.z`.

Because the issue is **stream-scoped** to 2.2.x, Steps 3-4 will apply only to versions within that stream. However, the full version impact analysis (Step 2) covers all streams to provide complete visibility.

## Ecosystem Detection

The vulnerable library `serde_json` is a Rust crate. This maps to the **Cargo** ecosystem. The lock file to inspect is `Cargo.lock`, and the check command is:

```
git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'
```

This is configured in the Ecosystem Mappings table of each stream's security-matrix.md.
