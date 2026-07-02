# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| Issue Key | TC-8001 |
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 (versions before 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |
| Assignee | Unassigned |
| Status | New |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the configured Version Stream **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

This issue is **stream-scoped** to the 2.2.x stream.

## Ecosystem Detection

The vulnerable library is **quinn-proto**. Based on the task's assumed ecosystem detection, the resolved ecosystem is **Go modules**.

The Ecosystem Mappings table in the 2.2.x stream's `security-matrix.md` lists the following supported ecosystems:

| Ecosystem | Repository | Lock File | Check Command |
|-----------|------------|-----------|---------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` |

**Result**: The detected ecosystem **Go modules** is **not listed** in the Ecosystem Mappings table. Automated triage cannot proceed for this ecosystem.

## Deployment Context Lookup

The affected component label `pscomponent:org/rhtpa-server` maps to repository `rhtpa-backend` in the Source Repositories table. The deployment context defaults to `upstream` (no Deployment Context column is present in the Source Repositories configuration).
