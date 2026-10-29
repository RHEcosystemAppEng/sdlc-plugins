# Step 1 -- Data Extraction: TC-8051

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99002 |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` |
| Stream scope | **2.2.x** (mapped from summary suffix `[rhtpa-2.2]` to Version Streams table entry `2.2.x`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | rustls |
| Affected version range | versions before 0.23.5 (< 0.23.5) |
| Fixed version | 0.23.5 |
| CVSS | 8.1 (High) |
| Upstream fix PR | [rustls/rustls#2100](https://github.com/rustls/rustls/pull/2100) |
| Advisory URL | -- |
| CVE record URL | [CVE-2026-99002](https://www.cve.org/CVERecord?id=CVE-2026-99002) |
| Due date | 2026-08-01 |
| Existing comments | (none) |
| Ecosystem | Cargo |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. This maps to the **2.2.x** stream in the Security Configuration Version Streams table (`git.example.com/rhtpa/rhtpa-release.0.4.z`). Triage is scoped to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library `rustls` is a Rust crate. The 2.2.x stream's Ecosystem Mappings table includes `Cargo` with:
- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`

Classification: **Source dependency** (Cargo). Standard remediation would produce 2 tasks per stream (upstream fix + downstream propagation), subject to the dependency chain analysis in Step 2.3.5.

## Deployment Context

The affected repository `rhtpa-backend` is listed in Source Repositories. Deployment context defaults to `upstream` (no Deployment Context column present).
