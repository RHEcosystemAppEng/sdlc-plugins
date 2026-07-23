# Step 1 -- Data Extraction: TC-8040

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | `pscomponent:org/rhtpa-server` |
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

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

This is a **scoped** issue -- triage Steps 3-4 apply to the 2.2.x stream only, with cross-stream impact checked for the 2.1.x stream.

## Ecosystem Detection

The vulnerable library `quinn-proto` was evaluated for ecosystem classification based on the library name and component context.

**Detected ecosystem: Go modules**

### Ecosystem Mappings (from 2.2.x stream security-matrix.md)

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

**Result: Go modules is NOT listed in the Ecosystem Mappings table.**

The supported ecosystems for this stream are Cargo and RPM. The detected ecosystem (Go modules) does not match any configured ecosystem mapping, so automated lock file inspection and version impact analysis cannot proceed.

## Deployment Context Lookup

The component label `pscomponent:org/rhtpa-server` was checked against the Source Repositories table. The repository `org/rhtpa-server` does not directly match any entry in the Source Repositories table (which contains `rhtpa-backend`). Defaulting deployment context to: **upstream**.
