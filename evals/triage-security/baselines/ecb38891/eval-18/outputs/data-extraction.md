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
| Ecosystem | Cargo (Rust crate) |

## Stream Scope

Issue summary contains stream suffix `[rhtpa-2.2]` -- mapped to stream **2.2.x** from the Version Streams table.

## Current Issue State (Pre-Existing Triage Artifacts)

| Artifact | Value | Implication |
|----------|-------|-------------|
| Status | In Progress | Issue has already been transitioned past New/Assigned |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server, **ai-cve-triaged** | Triage label already applied |
| Assignee | engineer-a@example.com | Already assigned |
| Existing Depend links | TC-8100 (upstream backport, In Progress), TC-8101 (downstream propagation, Open) | Remediation tasks already created and linked |
| Description digest comment | `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2` (created 2026-07-01T10:00:00Z) | Digest comment already exists |
| Post-triage summary comment | Present (created 2026-07-01T10:01:00Z) -- documents version impact, actions taken, remediation task keys | Summary comment already exists |

This issue has been fully triaged in a prior run. All triage artifacts are present. The re-run must detect these artifacts and skip all mutations to ensure idempotency.
