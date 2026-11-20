# Step 1 – Data Extraction: TC-8021

> Simulated triage. No Jira MCP, `git show`, WebFetch, or other external calls were made.
> Source: `vuln-issue-standard.md` (mock Jira issue), `claude-md-security-config.md`, `security-matrix-mock.md`.

**Note on the issue key:** the mock issue file shows key `TC-8001`, but the task names
**TC-8021**. This triage uses TC-8021 as the target and treats the file as that issue's
content.

## Step 0 – Configuration validation

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component custom field | customfield_10632 (configured, as the task says to assume) |
| Embargo policy URL | not configured, so Step 1.7 is skipped |
| ProdSec contact / account ID | not configured, so no @mentions |
| Version Streams | 2.1.x (`rhtpa-release.0.3.z`), 2.2.x (`rhtpa-release.0.4.z`) |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

All required sections are present (Repository Registry, Jira Configuration, Code
Intelligence, Security Configuration). Validation passes.

## Step 0.3 – Matrix staleness check

The matrix shows `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. Today is 2026-11-20, so the
matrix is **145 days old**, well past the 14-day threshold.

> Security matrix was last updated on 2026-06-28 (145 days ago). The matrix may not
> reflect recent releases. Options: 1. Refresh now, 2. Proceed anyway, 3. Stop.

In this eval there is no engineer to answer, so the triage continues with the current
matrix ("Proceed anyway"). Any 2.2.x or 2.1.x release made after 2026-06-28 is missing
from this analysis.

## Step 0.8 – Assign / transition (simulated, not executed)

- Issue status is **New** and unassigned. Proposed actions: assign TC-8021 to the
  current user and move it to Assigned. The transition would be discovered with
  `get_transitions`.

## Extracted CVE data

| Field | Value |
|---|---|
| Issue key | TC-8021 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Status | New |
| CVE ID | **CVE-2026-31812** (from the label and the summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Upstream Affected Component (customfield_10632) | **quinn-proto** |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]`, which maps to stream **2.2.x** |
| Affects Versions (Jira) | **RHTPA 2.0.0** (does not match the 2.2 suffix, and no 2.0.x stream is configured) |
| Vulnerable library | **quinn-proto** (Rust crate) |
| Ecosystem | **Cargo** (source dependency, listed in Ecosystem Mappings for both streams) |
| Affected version range | **< 0.11.14** |
| Fixed version | **0.11.14** |
| CVSS | 7.5 (High), DoS |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 (already past as of 2026-11-20) |
| Assignee | Unassigned |
| Reporter | not present in the mock data (needed for the post-triage @mention) |
| Existing comments | none |
| Deployment context (rhtpa-backend) | `upstream` (default) |

## Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to the **2.2.x** stream (`git.example.com/rhtpa/rhtpa-release.0.4.z`).
- The issue is **scoped** to 2.2.x. Other affected streams are handled through Case A
  (cross-stream).

## Step 1.5 – External enrichment

MITRE and OSV were not queried because external calls are disabled in this eval. The
triage uses the Jira description data only (fix threshold 0.11.14), so confidence in the
threshold is lower than it would be with external confirmation.

## Step 1.7 – Embargo check

No Embargo policy URL is configured, so this step was skipped silently. CVSS 7.5 would
otherwise have triggered the gate.

## Step 2 – Version impact analysis (from mock lock-file data)

| Stream | Version | Build | Backend tag | quinn-proto | Affected (< 0.11.14)? |
|---|---|---|---|---|---|
| 2.1.x | 2.1.0 | 0.3.8 | v0.3.8 | 0.11.9 | **YES** |
| 2.1.x | 2.1.1 | 0.3.12 | v0.3.12 | 0.11.9 | **YES** |
| 2.2.x | 2.2.0 | 0.4.5 | v0.4.5 | 0.11.9 | **YES** |
| 2.2.x | 2.2.1 | 0.4.8 | v0.4.8 | 0.11.12 | **YES** |
| 2.2.x | 2.2.2 | 0.4.9 | v0.4.8 (retag) | same as 2.2.1 (0.11.12) | **YES** (carried over from 2.2.1) |
| 2.2.x | 2.2.3 | 0.4.11 | v0.4.11 | 0.11.14 | NO |
| 2.2.x | 2.2.4 | 0.4.12 | v0.4.12 | 0.11.14 | NO |

Development stream: there is no unreleased-version data in this eval (Step 2.2 needs Jira),
so no development-stream row was evaluated.

Upstream fix status (inferred from released tags; branch HEAD was not read):

| Stream | Ecosystem | Upstream Branch | Evidence | Fixed? |
|---|---|---|---|---|
| 2.2.x | Cargo | release/0.4.z | v0.4.11 and v0.4.12 ship 0.11.14 | YES (inferred) |
| 2.1.x | Cargo | release/0.3.z | latest tag v0.3.12 ships 0.11.9 | NO (HEAD not verified) |

## Step 3 – Affects Versions correction (proposed)

- Current: `RHTPA 2.0.0`. This is wrong: no 2.0.x stream is configured, and it does not
  match the `[rhtpa-2.2]` scope.
- Proposed (scoped to 2.2.x): **RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2**. Remove RHTPA 2.0.0.
  Version IDs would come from `getJiraIssueTypeMetaWithFields`.
