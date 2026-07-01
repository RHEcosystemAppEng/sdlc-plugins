# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.1 (from summary suffix `[rhtpa-2.1]`) |
| Affects Versions (Jira field) | RHTPA 2.1.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | -- (not provided in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.1]`. Mapping to configured Version Streams:

- `[rhtpa-2.1]` maps to stream **2.1.x** (Konflux release repo: `rhtpa-release.0.3.z`)

**Issue stream scope**: 2.1.x -- triage is scoped to the 2.1.x stream only.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, which is a Rust crate. Checking the Ecosystem Mappings table in the 2.1.x stream's security-matrix.md:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

quinn-proto is a Cargo (Rust crate) dependency. **Ecosystem: Cargo** -- supported by the Ecosystem Mappings table.

## Existing Issue Links

The following links already exist on TC-8006:

| Link Type | Direction | Linked Issue | Summary |
|-----------|-----------|--------------|---------|
| Related | outward (TC-8006 -> TC-8001) | TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |

This pre-existing link will be checked in Step 4.2 before attempting sibling link creation.
