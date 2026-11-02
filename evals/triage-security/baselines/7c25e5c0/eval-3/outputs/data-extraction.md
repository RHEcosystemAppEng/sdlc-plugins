# Step 1 — Data Extraction

## Step 0.7 — Early Assignment

Before data extraction, the following actions are proposed:

1. **Assign TC-8003** to the current user
2. **Transition TC-8003** to Assigned status (current status: New → Assigned)

These actions provide immediate visibility into who is triaging this issue.

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Issue Key | TC-8003 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Affected Component | pscomponent:org/rhtpa-server |
| Stream Suffix | [rhtpa-2.2] → scoped to **2.2.x** stream |
| Vulnerable Library | quinn-proto |
| Affected Version Range | < 0.11.14 |
| Fixed Version | 0.11.14 |
| CVSS | 7.5 (High) |
| Affects Versions (PSIRT) | RHTPA 2.2.0 |
| Due Date | 2026-07-15 |
| Assignee | Unassigned |
| Upstream Fix PR | — |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |

### Ecosystem Detection

- **Ecosystem**: Cargo (quinn-proto is a Rust crate)
- **Lock File**: `Cargo.lock`
- **Check Command**: `git show <tag>:Cargo.lock`

### Stream Scope Resolution

- Issue summary contains stream suffix `[rhtpa-2.2]`
- Mapped to configured Version Stream: **2.2.x** (Konflux release repo: rhtpa-release.0.4.z)
- Triage is scoped to the 2.2.x stream
