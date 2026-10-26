# Step 1 — Data Extraction: TC-8050

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99001 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | criterion |
| Affected version range | versions before 0.5.2 |
| Fixed version | 0.5.2 |
| CVSS | 5.3 (Medium) |
| Upstream fix PR | (none in remote links) |
| Advisory URL | (none in remote links) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99001 |
| Due date | 2026-08-01 |
| Existing comments | (no comments) |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration Version Streams table. Triage is scoped to the 2.2.x stream only.

## Ecosystem Detection

- **Ecosystem**: Cargo (criterion is a Rust crate)
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock | grep -A2 'name = "criterion"'`
- **Upstream branch**: `release/0.4.z`
- **Category**: Source dependency

## Embargo Check (Step 1.7)

CVSS is 5.3 (Medium), which is below the Critical/Important threshold (CVSS >= 7.0). Embargo check skipped.
