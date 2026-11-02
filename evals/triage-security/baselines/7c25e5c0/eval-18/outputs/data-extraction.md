# Step 1 — Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Issue Key | TC-8001 |
| Status | **In Progress** |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] → 2.2.x stream |
| Affects Versions | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | quinn-rs/quinn#2048 |
| Advisory URL | GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Assignee | engineer-a@example.com |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server, **ai-cve-triaged** |
| Ecosystem | Cargo |
| Stream scope | 2.2.x (scoped via summary suffix [rhtpa-2.2]) |

## Pre-existing Triage Artifacts Detected

This issue has **already been triaged**. The following artifacts are present:

1. **Label `ai-cve-triaged`** — already present in the issue's labels array
2. **Status `In Progress`** — issue has already been transitioned past New/Assigned
3. **Existing Depend links to remediation tasks**:
   - TC-8100 (upstream backport) — Status: In Progress
   - TC-8101 (downstream propagation) — Status: Open, Blocks: TC-8100
4. **Description digest comment** — `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5...` posted at 2026-07-01T10:00:00Z
5. **Post-triage summary comment** — posted at 2026-07-01T10:01:00Z documenting version impact, actions taken, and remediation task keys
