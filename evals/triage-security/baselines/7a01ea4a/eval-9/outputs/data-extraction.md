# Step 1 -- Data Extraction: TC-8011

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-45678 |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | webpack |
| Affected version range | versions before 5.98.0 |
| Fixed version | 5.98.0 |
| CVSS | 7.8 (High) |
| Upstream fix PR | (none in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Due date | 2026-08-15 |
| Existing comments | (none) |
| Assignee | Unassigned |
| Status | New |

## Custom Fields

| Custom Field | Value |
|---|---|
| customfield_10632 (Upstream Affected Component) | webpack |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-ui |
| customfield_10832 (Stream) | rhtpa-2.2 |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. Mapping to configured
Version Streams:

- `[rhtpa-2.2]` maps to stream **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`)

The issue is **scoped** to stream 2.2.x only. Steps 3-4 will be scoped to this
single stream.

## Ecosystem Detection

The vulnerable library is **webpack**, which is a JavaScript/TypeScript package.
This maps to the **npm** ecosystem.

Checking the stream's `security-matrix.md` Ecosystem Mappings table for stream 2.2.x:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

The npm ecosystem is **not listed** in the Ecosystem Mappings table. This means
automated lock file inspection for webpack is not available via the standard
triage process.

Note: While automated version impact analysis via lock files is not available for
npm in this configuration, the CVE metadata (affected range, fix threshold) is
fully extracted and available for cross-CVE overlap analysis in Step 4.3.

## Vulnerability Description

A vulnerability was found in webpack. The webpack package before version 5.98.0
allows arbitrary code execution through a specially crafted loader chain
configuration. An attacker with control over a project's webpack configuration can
execute arbitrary code during the build process. The vulnerability exists because
webpack does not properly sanitize loader paths when resolving the loader chain,
allowing path traversal to execute arbitrary modules.
