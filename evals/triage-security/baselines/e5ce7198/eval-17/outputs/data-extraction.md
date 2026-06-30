# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

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
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |
| Issue status | New |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the configured Version Stream **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`). This issue is **scoped to the 2.2.x stream only**.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Based on the Ecosystem Mappings in the 2.2.x stream's security matrix, this maps to the **Cargo** ecosystem with:
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Repository: backend
- Upstream Branch: `release/0.4.z`

## Observations

- **Affects Versions mismatch**: PSIRT assigned `RHTPA 2.0.0`, but no 2.0.x stream exists in the Security Configuration. The Version Streams table only defines 2.1.x and 2.2.x. This will need correction in Step 3.
- **Issue is stream-scoped** to 2.2.x per the `[rhtpa-2.2]` suffix. Affects Versions correction (Step 3) will be limited to 2.2.x versions.
