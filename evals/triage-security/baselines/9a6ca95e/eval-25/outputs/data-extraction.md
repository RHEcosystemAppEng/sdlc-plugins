# Step 1 -- Data Extraction: TC-8040

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` |
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

This issue is **stream-scoped** to 2.2.x. Steps 3-4 will apply only to this stream.

## Ecosystem Detection

The vulnerable library `quinn-proto` was evaluated against the Ecosystem Mappings table in the 2.2.x stream's `security-matrix.md`.

**Configured ecosystems in the 2.2.x stream:**

| Ecosystem | Repository | Lock File | Check Command |
|-----------|------------|-----------|---------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` |

**Ecosystem detection result: Go modules**

The library `quinn-proto` was resolved to the **Go modules** ecosystem based on component context analysis. However, **Go modules** is **not listed** in the Ecosystem Mappings table for any configured version stream (2.1.x or 2.2.x). The only supported ecosystems are **Cargo** and **RPM**.

This means automated lock file inspection and version impact analysis cannot proceed for this ecosystem. Manual assessment is required.

## Deployment Context

The affected component `pscomponent:org/rhtpa-server` maps to repository `rhtpa-backend` in the Source Repositories table. Deployment context: **upstream** (default, as no explicit Deployment Context column is present).
