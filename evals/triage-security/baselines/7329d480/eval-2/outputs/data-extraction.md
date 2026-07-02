# Data Extraction: TC-8002

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-28940 |
| Jira Issue Key | TC-8002 |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component | pscomponent:org/rhtpa-server |
| Product Version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable Library | serde_json |
| Affected Version Range | versions before 1.0.135 |
| Fixed Version | 1.0.135 |
| CVSS Score | 5.3 (Medium) |
| Due Date | 2026-07-30 |
| Assignee | Unassigned |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Existing Comments | None |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

This issue is **stream-scoped** to 2.2.x. However, per triage rules, all supported versions across all streams are checked for impact assessment.

## Ecosystem Detection

- **Ecosystem**: Cargo (Rust crate -- serde_json is a Rust crate)
- **Lock File**: `Cargo.lock`
- **Check Command**: `git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'`
- **Source Repository**: backend (rhtpa-backend)

## Deployment Context

- **Repository**: rhtpa-backend
- **Deployment context**: upstream (default, no explicit Deployment Context column in Source Repositories)

## Vulnerability Description

A stack overflow vulnerability in serde_json. Versions before 1.0.135 are vulnerable to unbounded recursion when deserializing deeply nested JSON input. An attacker can craft a JSON payload with thousands of nested arrays or objects causing a process crash. The fix (1.0.135) introduces a configurable recursion limit defaulting to 128 levels of nesting.

## Embargo Check

CVSS 5.3 (Medium) is below the embargo threshold (7.0). No Embargo policy URL is configured. Step 1.7 is skipped.
