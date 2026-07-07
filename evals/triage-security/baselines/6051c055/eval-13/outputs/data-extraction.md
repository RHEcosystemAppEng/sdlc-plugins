# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | (none) |

## Stream Scope Resolution

Summary: `CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]`

- Parsed suffix: `[rhtpa-2.2]` maps to stream **2.2.x**
- Matched to Version Streams table row: 2.2.x at `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Issue stream scope: **2.2.x** (scoped)

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
- Upstream branch (2.1.x): `release/0.3.z`
- Upstream branch (2.2.x): `release/0.4.z`

## Affects Versions Mismatch

The PSIRT-assigned Affects Versions (`RHTPA 2.0.0`) does not correspond to any configured version stream. The configured streams are 2.1.x and 2.2.x. This will be corrected in Step 3 after version impact analysis confirms which versions are actually affected.
