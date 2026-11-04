# TC-8001 — Step 1 Data Extraction

Simulated triage: the Jira issue, remote links, and lock file data came from the eval input files. No Jira, git, or web calls were made.

## Step 0 – Configuration (from CLAUDE.md)

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | not configured (Steps 4.3 and 7 skipped) |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| ProdSec contact / account ID | not configured (no @mentions) |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend → https://github.com/rhtpa/rhtpa-backend |
| Deployment Context column | **Absent.** For backward compatibility, every repo defaults to `upstream` |

## Step 0.3 – Matrix Staleness Check

- Matrix `Last-Updated`: 2026-06-28T10:00:00Z. Today is 2026-11-04, so the matrix is **129 days old**, well past the 14-day limit.
- Warning: "Security matrix for streams 2.1.x and 2.2.x was last updated on 2026-06-28 (129 days ago). The matrix may not reflect recent releases. Options: 1. Refresh now, 2. Proceed anyway, 3. Stop."
- Eval assumption: **Proceed anyway** with the current matrix.

## Step 0.8 – Assign and Transition (proposed, not executed)

- Assign TC-8001 to the current user. It is currently Unassigned.
- Transition New → Assigned, using the target found dynamically from `get_transitions`.

## Step 1 – Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8001 | Issue |
| Status | New | Issue (full triage path) |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` and the summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field. **Wrong: no 2.0.x stream exists** |
| Vulnerable library | quinn-proto (Rust crate) | Description |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| Severity | CVSS 7.5 (High), DoS (panic on excessive stream counts) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote links / description |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 (already past) | `duedate` |
| Existing comments | none | Comment history |
| Reporter | not provided in the mock (needed for the summary @mention) | Issue |

### Stream scope resolution

- The suffix `[rhtpa-2.2]` maps to the configured Version Stream **2.2.x** (rhtpa-release.0.4.z).
- **Issue stream scope: 2.2.x (scoped).** Step 3 corrections apply only to 2.2.x versions. Other affected streams go through Case A, the cross-stream path.

### Ecosystem detection

- quinn-proto is a Rust crate, so the ecosystem is **Cargo**. Cargo appears in both streams' Ecosystem Mappings.
- Category: **source dependency**, which means 2 remediation tasks per stream.
- Lock file: `Cargo.lock` in the `backend` repository. Check command: `git show <tag>:Cargo.lock`.

### Deployment context lookup

- Affected repository: rhtpa-backend. This is the `backend` repo in Ecosystem Mappings and the only Source Repository.
- The Source Repositories table has **no Deployment Context column**, so the context defaults to **`upstream`**.
- Because the column is absent, remediation task descriptions **omit the Coordination Guidance subsection entirely** (backward compatibility rule in remediation-templates.md).

## Step 1.5 – External CVE Data Enrichment

- MITRE and OSV.dev were not queried (eval restriction). Both are treated as unavailable.
- "External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced."
- Fix threshold used: **quinn-proto < 0.11.14, fixed in 0.11.14.**

## Step 1.7 – Embargo Check

- CVSS 7.5 meets the 7.0 threshold, but no Embargo policy URL is configured. **The step is skipped silently.**

## Step 2 – Version Impact Analysis (simulated lock file output)

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | backend tag | quinn-proto | Affected? | Notes |
|--------|---------|-------------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | out of issue scope |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | out of issue scope |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.8 | — | YES | backend retag of 2.2.1 (same as 2.2.1) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | fixed version shipped |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | fixed version shipped |

- Development stream: it cannot be detected without the Jira unreleased-versions lookup (Step 2.2), so no dev-stream row is included.
- Dependency chain (Step 2.3.5): not determinable without `Cargo.lock` contents. The task records the dependency type as "to be confirmed (direct or transitive via quinn)". Because quinn-proto is normally pulled in transitively through `quinn`, the two-tier approach is documented.

Upstream fix status (Step 2.5, inferred from pinned-tag evidence because git is not available):

| Stream | Ecosystem | Upstream Branch | Version at latest release tag | Fixed? |
|--------|-----------|-----------------|-------------------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | NO (assumed; HEAD not inspected) |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.11, v0.4.12) | YES (released builds 2.2.3 and later already ship the fix) |

## Step 3 – Affects Versions Correction (proposed)

- Current: `[RHTPA 2.0.0]` → Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`. This is scoped to 2.2.x. The PSIRT value refers to a 2.0 stream that does not exist.
- RHTPA 2.1.0 and 2.1.1 are also affected but are out of scope. They are handled by Case A, the cross-stream path.
- Version IDs would be discovered at runtime via `getJiraIssueTypeMetaWithFields`.

## Steps 4–7 (simulated)

- Step 4: the sibling JQL `labels = CVE-2026-31812` was not run. Simulated result: no sibling issue for 2.1.x. Step 4.3 is skipped because the Upstream Affected Component field is not configured.
- Step 5: lifecycle data is not available. All listed versions are treated as supported.
- Step 6: no resolved siblings, so the issue is not already fixed.
- Step 7: skipped because the Upstream Affected Component field is not configured.
- Step 7.5: the release Jira for RHTPA 2.2.5 (the next patch after 2.2.4) would be found or created, each with individual confirmation. Preemptive tasks are not linked to release Jira.

## Outcome

- **Case B** applies to stream 2.2.x, which is in scope.
- **Case A** applies to stream 2.1.x: a cross-stream impact comment plus preemptive tasks, because no 2.1.x CVE Jira exists.
- See remediation.md.
