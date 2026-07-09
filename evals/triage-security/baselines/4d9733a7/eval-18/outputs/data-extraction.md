# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | 2 comments (description digest + post-triage summary) |
| Status | In Progress |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server, ai-cve-triaged |
| Assignee | engineer-a@example.com |

## Stream Scope Resolution

Summary suffix `[rhtpa-2.2]` maps to stream **2.2.x** from the Version Streams table.
Issue is **scoped** to the 2.2.x stream only.

## Ecosystem Detection

Library **quinn-proto** is a Rust crate. Ecosystem: **Cargo** (source dependency)

## Pre-existing Triage Artifacts Detected

This issue has already been triaged in a prior run. The following artifacts exist:

1. **Label `ai-cve-triaged`**: Present in the issue's labels array
2. **Status**: In Progress (already transitioned from New)
3. **Assignee**: engineer-a@example.com (already assigned)
4. **Issue Links (Depend)**:
   - TC-8100: upstream backport task (Status: In Progress)
   - TC-8101: downstream propagation task (Status: Open, blocked by TC-8100)
5. **Description digest comment**: Found -- `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2` (created 2026-07-01T10:00:00Z)
6. **Post-triage summary comment**: Found -- summary documenting version impact, Affects Versions correction, and remediation tasks (created 2026-07-01T10:01:00Z)
