# Step 1 – Data Extraction: TC-8040

> Simulated triage. No Jira MCP, `git show`, or external calls were made. The issue data comes from `vuln-issue-standard.md`.
> Note: the mock issue file shows key **TC-8001**, but the task names **TC-8040**. This triage treats them as the same issue and uses TC-8040.

## Step 0 – Configuration Validation (passed)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | not configured (Steps 4.3 and 7 would be skipped) |
| Embargo policy URL | not configured (Step 1.7 would be skipped) |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

Step 0.3 staleness note: the matrix is stamped `Last-Updated: 2026-06-28T10:00:00Z`, which is 152 days before today (2026-11-27) and past the 14-day threshold. In a live run the engineer would get the Refresh / Proceed / Stop choice first. The ecosystem result below does not depend on that choice.

## Extracted CVE Data

| Field | Value |
|---|---|
| Issue key | TC-8040 |
| Status | New |
| CVE ID | CVE-2026-31812 (from the label and the summary) |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 (does not match the 2.2 suffix, and no 2.0.x stream is configured; would be fixed in Step 3) |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 ("versions before 0.11.14") |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 (already past) |
| Assignee | Unassigned |
| Existing comments | none |
| Deployment context | `upstream` (default value) |

All critical fields (CVE ID, library, affected range) were parsed.

## Stream Scope Resolution

- Suffix `[rhtpa-2.2]` maps to stream **2.2.x** (Konflux repo `git.example.com/rhtpa/rhtpa-release.0.4.z`).
- Issue stream scope: **scoped to 2.2.x**.

## Ecosystem Detection

| Item | Result |
|---|---|
| Detected ecosystem | **Go modules** (given as the detection result for this scenario) |
| Ecosystem Mappings, stream 2.1.x | Cargo, RPM |
| Ecosystem Mappings, stream 2.2.x (issue scope) | Cargo, RPM |
| Listed in Ecosystem Mappings? | **No**, in neither stream |
| Ecosystem classification | none (Go modules has no category in the classification table) |
| Lock file / check command | none configured for Go modules (e.g. no `go.sum` / `go.mod` mapping) |
| Outcome | **Unsupported ecosystem. Automated triage stops here.** See `unsupported-ecosystem.md`. |

## Steps Not Executed

Automated triage stopped at the ecosystem detection in Step 1, as the skill requires. These steps were not run: Step 1.5 (MITRE/OSV enrichment), Step 2 (version impact analysis / lock file inspection), Steps 3–7.5, and Step 8 (remediation).

No Jira mutations were proposed or made. That covers Affects Versions correction, the `ai-cve-triaged` label, comments, remediation tasks, and links. No version-impact data was invented.
