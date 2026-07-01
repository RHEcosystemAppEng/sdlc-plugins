# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | tokio |
| Affected version range | versions before 1.42.0 (< 1.42.0) |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Upstream fix PR | [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) |
| Advisory URL | [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) |
| CVE record URL | [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) |
| Due date | 2026-08-15 |
| Existing comments | (none) |
| Status | New |
| Assignee | Unassigned |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the configured **2.2.x** Version Stream (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

**Issue stream scope**: 2.2.x

Since this is a scoped issue, Steps 3 and 4 will be scoped to the 2.2.x stream. However, version impact analysis (Step 2) checks all streams to detect cross-stream impact.

## Ecosystem Detection

The vulnerable library is **tokio**, a Rust crate. Based on the Ecosystem Mappings table in both stream security matrices, `Cargo` is a supported ecosystem with:
- **Lock File**: `Cargo.lock`
- **Check Command**: `git show <tag>:Cargo.lock`
- **Upstream Branch**: `release/0.4.z` (for 2.2.x stream), `release/0.3.z` (for 2.1.x stream)

**Detected ecosystem**: Cargo (source dependency)

This means remediation will follow the two-task pattern: upstream backport task + downstream propagation subtask.

## Custom Fields

| Custom Field | Value |
|-------------|-------|
| customfield_10632 (Upstream Affected Component) | tokio |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-server |
| customfield_10832 (Stream) | rhtpa-2.2 |

## Issue Links

No existing issue links on TC-8020.
