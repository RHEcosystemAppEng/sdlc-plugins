# Step 0.7 — Early Assignment

**Proposed actions (not executed — eval mode):**

1. **Assign TC-8002** to the current user
2. **Transition TC-8002** to Assigned status (current status: New → target: Assigned)

These actions provide immediate visibility into who is actively triaging the issue and enable Step 7 (Concurrent Triage Detection).

---

# Step 1 — Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-28940 |
| Issue Key | TC-8002 |
| Summary | CVE-2026-28940 serde_json - Stack overflow on deeply nested input [rhtpa-2.2] |
| Affected Component | pscomponent:org/rhtpa-server |
| Stream Suffix | [rhtpa-2.2] → scoped to **2.2.x** stream |
| Vulnerable Library | serde_json |
| Affected Version Range | versions before 1.0.135 (< 1.0.135) |
| Fixed Version | 1.0.135 |
| CVSS | 5.3 (Medium) |
| Affects Versions (Jira) | RHTPA 2.2.0 |
| Due Date | 2026-07-30 |
| Assignee | Unassigned |
| Upstream Fix PR | — |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |

## Ecosystem Detection

- **Library**: serde_json
- **Ecosystem**: Cargo (Rust crate — identified from library name and component context)
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`

## Stream Scope Resolution

- Issue summary contains stream suffix `[rhtpa-2.2]`
- Mapped to Version Streams entry: **2.2.x** (Konflux release repo: rhtpa-release.0.4.z)
- Triage is **scoped** to the 2.2.x stream only
