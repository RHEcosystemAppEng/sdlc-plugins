# Step 1 – Data Extraction: TC-8003

Mode: interactive (simulated; `FULLSEND_OUTPUT_DIR` not set). All Jira and git data here comes from the eval input files. No Jira MCP, `git show`, or WebFetch calls were made.

## Step 0 – Configuration Validation (from claude-md-security-config.md)

| Item | Value | Status |
|------|-------|--------|
| Repository Registry | rhtpa-backend (serena_backend) | present |
| Project key | TC | present |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 | present |
| Code Intelligence | `mcp__<instance>__<tool>` convention | present |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa | present |
| Jira version prefix | RHTPA | present |
| Vulnerability issue type ID | 10024 | present |
| Component label pattern | `pscomponent:` | present |
| VEX Justification custom field | customfield_12345 | present (optional) |
| Upstream Affected Component / PS Component / Stream fields | not configured | Step 4.3 and Step 7 are skipped |
| ProdSec contact / account ID | not configured | @mentions skipped |
| Embargo policy URL | not configured | Step 1.7 is skipped |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) | present |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) | present |

Result: the configuration is valid, so triage proceeds.

## Step 0.3 – Matrix Staleness Check

- `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. Today is 2026-11-27, so the matrix is **152 days old**, well past the 14-day threshold.
- **Warning to engineer:** "Security matrix for streams **2.1.x** and **2.2.x** was last updated on 2026-06-28 (152 days ago). The matrix may not reflect recent releases. Options: 1. Refresh now, 2. Proceed anyway, 3. Stop."
- For this eval, I chose **Proceed anyway** (no interactive engineer, and no external access to refresh). The outcome is a duplicate closure, and stale data does not change it.

## Step 0.8 – Assign and Transition (proposed, not executed)

- Proposed: assign TC-8003 to the current user and move it New → Assigned. These are Jira mutations that need confirmation, and none were executed.

## Extracted Fields

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8003 | Issue |
| Issue type | Vulnerability | Issue |
| Status | New | Issue (status-aware handling: full triage path) |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` and summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Affected repository | rhtpa-backend (backend, Cargo) | Matrix Ecosystem Mappings |
| Deployment context | upstream (default; no column in Source Repositories) | Step 0 mapping |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | Issue `versions` |
| Vulnerable library | quinn-proto | Description |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| CVSS | 7.5 (High) | Description |
| Vulnerability class | Denial of service (panic from unbounded stream allocation in a STREAMS frame) | Description |
| Upstream fix PR | none in remote links | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Other references | https://rustsec.org/advisories/RUSTSEC-2026-0042.html | Description |
| Due date | 2026-07-15 (already past as of 2026-11-27) | Issue `duedate` |
| Assignee | Unassigned | Issue |
| Existing comments | none | Issue |

All critical fields (CVE ID, library, affected range) were parsed.

## Stream Scope Resolution

- Suffix `[rhtpa-2.2]` maps to configured stream **2.2.x** (`git.example.com/rhtpa/rhtpa-release.0.4.z`).
- Issue stream scope: **scoped to 2.2.x**.

## Ecosystem Detection

- quinn-proto is a Rust crate, so the ecosystem is **Cargo**. Cargo is listed in the 2.2.x Ecosystem Mappings (repo `backend`, lock file `Cargo.lock`, upstream branch `release/0.4.z`).
- Category: source dependency, which means 2 remediation tasks per stream if remediation were needed.

## Step 1.5 – External CVE Data Enrichment

- MITRE CVE API and OSV.dev were **not queried** because the eval forbids external calls. Both count as unavailable.
- "⚠ External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced."
- Fix threshold in use: **quinn-proto < 0.11.14 is affected; 0.11.14 is fixed.**

## Step 1.7 – Embargo Check

- No Embargo policy URL is configured, so this step is skipped silently. CVSS 7.5 would otherwise have met the threshold.

## Step 2 – Version Impact Analysis (simulated lock file data from security-matrix-mock.md)

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Backend tag | quinn-proto | Affected? | Notes |
|--------|---------|-------------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | outside issue scope |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | outside issue scope |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.8 | — | YES | same as 2.2.1 (backend retag of 2.2.1) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | fixed version shipped |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | fixed version shipped |
| dev | unknown | branch HEAD | not evaluated | — | Development stream detection (Step 2.2) needs unreleased Jira versions. None were provided, and no Jira query is allowed. |

Dependency chain (Step 2.3.5): not determinable without a `Cargo.lock` / `cargo tree` read. quinn-proto is usually a transitive dependency via `quinn`, but I have not confirmed that.

Upstream fix status (Step 2.5, inferred from the latest released pinned tag; branch HEAD was not read):

| Stream | Ecosystem | Upstream Branch | Version at latest release tag | Fixed? |
|--------|-----------|-----------------|-------------------------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.12) | YES (from 2.2.3 onward) |
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | not known at HEAD; the latest release is vulnerable |

Stream-scoped (2.2.x) affected versions: **RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2**.

## Step 3 – Affects Versions Correction (assessment)

- Current: `[RHTPA 2.2.0]`. Proposed per evidence: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`. This is correct but incomplete.
- Jira version IDs could not be discovered because `getJiraIssueTypeMetaWithFields` was not called. Whether a Jira version exists for each one is unverified.
- **Not applied.** Step 4 finds that TC-8003 is a same-stream duplicate of TC-7999, so the correction belongs on the surviving issue, TC-7999. See duplicate-check.md.
