# Step 1 -- Data Extraction: TC-8040

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Due date | 2026-07-15 |
| Assignee | Unassigned |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in Security Configuration.

- Parsed suffix: `[rhtpa-2.2]` -> stream `2.2.x`
- Matched Version Stream: 2.2.x (Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.4.z)
- Issue stream scope: **2.2.x only** (Steps 3-4 will be scoped to this stream)

## Deployment Context Lookup

The affected repository `org/rhtpa-server` (from component label `pscomponent:org/rhtpa-server`) was looked up in the Source Repositories table. The matching repository is `rhtpa-backend`.

- Deployment context: `upstream` (default -- no Deployment Context column present in Source Repositories table)

## Ecosystem Detection

The vulnerable library `quinn-proto` was analyzed for ecosystem classification.

**Detection result: Go modules**

The stream's Ecosystem Mappings table (from 2.2.x stream `security-matrix.md`) lists the following supported ecosystems:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

**Go modules is NOT listed in the Ecosystem Mappings table.**

Automated triage cannot proceed for this ecosystem. The skill does not have a configured lock file path, check command, or upstream branch mapping for Go modules. Manual assessment is required.
