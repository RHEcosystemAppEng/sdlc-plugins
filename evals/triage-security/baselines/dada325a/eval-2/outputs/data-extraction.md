# Data Extraction — TC-8002

Skill: `sdlc-workflow:triage-security` (interactive mode; eval simulation, so no Jira, WebFetch or git calls were made)

## Step 0 – Configuration Validation

All required sections are present in the project CLAUDE.md (`claude-md-security-config.md`):

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 (configured) |
| Upstream Affected Component field | not configured, so Steps 4.3, 7 and 7.5.3 are skipped |
| ProdSec contact / Jira account ID | not configured, so no @mention |
| Embargo policy URL | not configured, so Step 1.7 is skipped |
| Version Streams | 2.1.x (`rhtpa-release.0.3.z`), 2.2.x (`rhtpa-release.0.4.z`) |
| Source Repositories | rhtpa-backend: https://github.com/rhtpa/rhtpa-backend. Deployment Context column is absent, so it defaults to `upstream` |

## Step 0.3 – Matrix Staleness Check

- Matrix `Last-Updated`: 2026-06-28T10:00:00Z. Today is 2026-11-06, so the matrix is about 131 days old. That is more than the 14-day threshold.
- **Warning (would be shown to the engineer):** "Security matrix for streams 2.1.x and 2.2.x was last updated on 2026-06-28 (131 days ago). The matrix may not reflect recent releases. Options: 1. Refresh now, 2. Proceed anyway, 3. Stop."
- Eval assumption: **Proceed anyway**, using the mock matrix as supplied. The outcome below covers only the versions listed in the matrix. A 2.2.5+ release made after 2026-06-28 would not be included.

## Step 0.8 – Assign and Transition (proposed only)

- Issue status is **New**, so the full triage path applies.
- Proposed: assign TC-8002 to the current user and transition it to **Assigned**. The transition ID would be discovered dynamically with `get_transitions`.

## Step 1 – Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8002 | Issue |
| CVE ID | CVE-2026-28940 | Label and summary |
| Summary | CVE-2026-28940 serde_json - Stack overflow on deeply nested input [rhtpa-2.2] | Issue |
| Status | New | Issue |
| Affected component | `pscomponent:org/rhtpa-server`, which maps to `org/rhtpa-server` (backend, rhtpa-backend) | Label |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]`, which maps to stream **2.2.x** | Summary suffix |
| Affects Versions (Jira) | RHTPA 2.2.0 | `versions` field |
| Vulnerable library | serde_json | Description |
| Affected version range | `< 1.0.135` ("versions before 1.0.135") | Description |
| Fixed version | 1.0.135 | Description |
| Severity | CVSS 5.3 (Medium) | Description |
| Vulnerability | Unbounded recursion while deserializing deeply nested JSON causes a stack overflow and process crash. The fix adds a configurable recursion limit (default 128) | Description |
| Upstream fix PR | none in remote links | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 | Remote links |
| Other references | https://rustsec.org/advisories/RUSTSEC-2026-0019.html | Description |
| Due date | 2026-07-30 (already in the past) | `duedate` |
| Assignee | Unassigned | Issue |
| Existing comments | none | Comments |

All critical fields (CVE ID, library, affected range) were parsed successfully.

### Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to stream **2.2.x**, which matches the configured stream `git.example.com/rhtpa/rhtpa-release.0.4.z`.
- The issue is **scoped to 2.2.x**. Stream 2.1.x is still analyzed so that any cross-stream impact can be reported (Case A check).

### Ecosystem detection

- serde_json is a Rust crate, so the ecosystem is **Cargo**. Cargo is a source dependency ecosystem and appears in both streams' Ecosystem Mappings.
- Lock file: `Cargo.lock` in the backend repo. Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'`.
- Deployment context: `upstream` (the default).

## Step 1.5 – External CVE Data Enrichment

- MITRE (`https://cveawg.mitre.org/api/cve/CVE-2026-28940`) and OSV.dev (`https://api.osv.dev/v1/vulns/CVE-2026-28940`) were **not queried** because the eval does not allow external calls. Both are treated as unavailable.
- "External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced."
- Fix threshold used for Step 2: **serde_json < 1.0.135 is affected, and 1.0.135 is fixed** (from the Jira description). The lowest shipped version is 1.0.137, which is two patch releases above the threshold. A small difference between sources would not change the result.

## Step 1.7 – Embargo Check

Skipped. No Embargo policy URL is configured, and CVSS 5.3 is below the 7.0 threshold anyway.
