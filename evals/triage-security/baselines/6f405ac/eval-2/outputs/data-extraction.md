# Step 1 -- Data Extraction: TC-8002

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-28940 |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | RHTPA 2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | serde_json |
| Affected version range | versions before 1.0.135 |
| Fixed version | 1.0.135 |
| CVSS | 5.3 (Medium) |
| Upstream fix PR | Not provided |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Due date | 2026-07-30 |
| Status | New |
| Assignee | Unassigned |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`).

This issue is **stream-scoped** to 2.2.x. However, per triage rules, all streams are checked for version impact analysis (Step 2), while Affects Versions correction (Step 3) is scoped to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library is **serde_json**, a Rust crate. This maps to the **Cargo** ecosystem.

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'`
- Source repository: `backend` (rhtpa-backend)

## Additional References

- RustSec Advisory: https://rustsec.org/advisories/RUSTSEC-2026-0019.html
- Vulnerability description: Stack overflow when deserializing deeply nested JSON input. Fix introduces a configurable recursion limit defaulting to 128 levels.
