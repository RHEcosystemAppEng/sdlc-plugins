# Step 1 -- Data Extraction

## Issue Details

**Issue Key**: TC-8003
**Summary**: CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**Issue Type**: Vulnerability
**Status**: New
**Assignee**: Unassigned
**Due Date**: 2026-07-15

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary text |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches Component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | < 0.11.14 (versions before 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | -- | No GitHub PR in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links (GitHub Advisory) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links (CVE Record) |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. Mapping to configured Version Streams:

- `[rhtpa-2.2]` maps to stream **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`)

**Issue stream scope**: 2.2.x (scoped to a single stream)

## Ecosystem Detection

The vulnerable library is **quinn-proto**, which is a Rust crate. Checking the 2.2.x stream's Ecosystem Mappings table in `security-matrix.md`:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

quinn-proto is a Cargo (Rust) dependency. **Ecosystem: Cargo** -- this is a supported ecosystem listed in the Ecosystem Mappings table.

## Note

Data extraction is complete. However, before proceeding to version impact analysis (Step 2), the duplicate check in Step 4 will be evaluated. If a same-stream duplicate is detected, triage will short-circuit and skip Steps 2-8.
