# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Issue Key | TC-8020 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component | pscomponent:org/rhtpa-server |
| Product Version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable Library | quinn-proto |
| Affected Version Range | < 0.11.14 |
| Fixed Version | 0.11.14 |
| CVSS | 7.5 (High) |
| Ecosystem | Cargo (Rust crate -- identified from library name quinn-proto and Cargo ecosystem mapping in security-matrix.md) |
| Due Date | 2026-07-15 |
| Upstream Fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Upstream Affected Component (customfield_10632) | quinn-proto |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in Version Streams configuration. Triage is scoped to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The Ecosystem Mappings table in the 2.2.x stream's security-matrix.md lists **Cargo** as an ecosystem with:
- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`

This is a **source dependency ecosystem**, so remediation will follow the two-task pattern (upstream backport + downstream propagation).
