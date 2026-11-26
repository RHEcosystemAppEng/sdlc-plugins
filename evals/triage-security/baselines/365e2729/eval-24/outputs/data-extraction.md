# Triage TC-8001 — Step 1 Data Extraction

## Step 0 — Configuration validation (from claude-md-security-config.md)

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | not configured (Step 4.3 cross-CVE overlap and Step 7 concurrent triage skipped) |
| ProdSec contact / account ID | not configured (no @mentions of ProdSec) |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| Version Streams | 2.1.x → git.example.com/rhtpa/rhtpa-release.0.3.z; 2.2.x → git.example.com/rhtpa/rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend → https://github.com/rhtpa/rhtpa-backend |

**Source Repositories parsing:** the table has columns `Repository | URL | Local Path`. There is
**no Deployment Context column**, so (backward compatibility) every repository defaults to
`upstream`:

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | upstream (default — column absent) |

All required sections are present, so triage continues.

## Step 0.3 — Matrix staleness check

The matrix has `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. Today is 2026-11-26, so the matrix
is **151 days old**, well past the 14-day threshold.

> Security matrix for streams **2.1.x** and **2.2.x** was last updated on 2026-06-28 (151 days
> ago). It may not include recent releases. Options: 1. Refresh now, 2. Proceed anyway, 3. Stop.

For this eval run I chose **Proceed anyway** with the current matrix. Any release after 2.2.4
(2026-05-04) is not covered.

## Step 0.8 — Assign / transition (proposed, not executed)

- Assign TC-8001 to the current user (it is currently Unassigned).
- Move TC-8001 from New to Assigned.

## Step 1 — Extracted CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8001 | Issue |
| Status | New (so full triage runs) | Issue |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` and summary |
| Affected component | `pscomponent:org/rhtpa-server` → org/rhtpa-server | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field |
| Vulnerable library | quinn-proto (Rust crate) | Description |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| Severity | CVSS 7.5 (High), DoS (panic on excessive stream count) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote links / description |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 (already past) | `duedate` |
| Existing comments | none | Comment history |
| Reporter | not present in the mock issue data (needed for the summary-comment @mention) | — |

All three critical fields (CVE ID, library, affected range) were parsed.

### Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to the configured stream **2.2.x** (rhtpa-release.0.4.z).
- The issue is **scoped** to 2.2.x. Stream 2.1.x is outside its scope, so Case A cross-stream
  handling applies.

### Ecosystem detection

- quinn-proto is a Rust crate, so the ecosystem is **Cargo**. Cargo is in both streams' Ecosystem
  Mappings tables.
- Category: **source dependency**, so each stream needs 2 remediation tasks.
- Lock file `Cargo.lock` in repository `backend`. Check command: `git show <tag>:Cargo.lock`.

### Deployment context lookup

- The affected repository is `backend` / rhtpa-backend (the Rust backend that ships in
  `org/rhtpa-server`).
- Deployment context is **upstream (default)**, because the Source Repositories table has no
  Deployment Context column.
- Because the column is absent (backward compatibility), the remediation tasks **leave out** the
  `### Coordination Guidance` subsection, as `remediation-templates.md` requires.

## Step 1.5 — External enrichment

I did not query MITRE or OSV. The eval forbids external calls, so both sources count as
unavailable.

> External CVE databases unavailable — using Jira description data only. Fix threshold
> confidence is reduced.

Fix threshold used: **quinn-proto < 0.11.14 affected; 0.11.14 fixed.**

## Step 1.7 — Embargo check

Skipped. No embargo policy URL is configured, even though CVSS is 7.5.

## Step 2 — Version impact analysis (simulated `git show` data from the matrix mock)

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | backend tag | quinn-proto | Affected? | Notes |
|--------|---------|-------------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | outside issue scope |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | outside issue scope |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.8 | — | YES | same as 2.2.1 (backend retag) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | |
| dev | — | — | — | not determined | Step 2.2 needs Jira unreleased-version metadata, and Jira was not queried |

**Dependency chain (2.3.5):** the mock data gives only the resolved Cargo.lock versions. It does
not include Cargo.toml manifests or the dependency graph, so I could not determine whether
quinn-proto is a direct or transitive dependency, or which build profile pulls it in. I did not
guess. The task descriptions mark this "to be confirmed", and the engineer or `/implement-task`
should run `cargo tree -i quinn-proto`.

**Upstream fix status (2.5):** branch HEADs could not be inspected (no git access). Inference
from the latest tagged evidence:

| Stream | Ecosystem | Upstream Branch | Latest tagged version | Fixed? |
|--------|-----------|-----------------|-----------------------|--------|
| 2.2.x | Cargo | release/0.4.z | v0.4.12 → 0.11.14 | YES (inferred; HEAD should be at or after v0.4.12) |
| 2.1.x | Cargo | release/0.3.z | v0.3.12 → 0.11.9 | NO (inferred) |

## Step 3 — Affects Versions correction (proposed)

- PSIRT value: **RHTPA 2.0.0**. This is wrong: no 2.0.x stream is supported or configured, and
  the issue is scoped to 2.2.x.
- Corrected value (scoped to 2.2.x, from lock file evidence): **RHTPA 2.2.0, RHTPA 2.2.1, RHTPA
  2.2.2**.
- Remove RHTPA 2.0.0. Do not add 2.2.3 or 2.2.4, which are not affected.
- Version IDs would be looked up at runtime with `getJiraIssueTypeMetaWithFields`, not hardcoded.
- Correction comment, with the Comment Footnote: "Affects Versions corrected from RHTPA 2.0.0 to
  RHTPA 2.2.0, 2.2.1, 2.2.2 based on Cargo.lock analysis at the pinned tags (quinn-proto
  0.11.9/0.11.12 < 0.11.14). 2.2.3+ ship quinn-proto 0.11.14 and are not affected."

## Steps 4–7 (not executed, since Jira was not queried)

- **Step 4:** sibling JQL for label CVE-2026-31812 was not run. I assumed no sibling exists for
  stream 2.1.x, so 2.1.x gets preemptive tasks. If a 2.1.x sibling CVE Jira is found, skip the
  2.1.x tasks and add a Related link instead. Step 4.3 was skipped (Upstream Affected Component
  field not configured).
- **Step 5:** lifecycle was not checked against the product pages URL. I assumed 2.1.x and 2.2.x
  are both supported.
- **Step 6:** I assumed no resolved siblings, so no already-fixed closure.
- **Step 7:** skipped (Upstream Affected Component field not configured).
- **Step 7.5:** finding or creating the release Epic/Task ("RHTPA 2.2.x Release Tasks" / "RHTPA
  2.2.x CVE triage") requires Jira and an engineer decision on the version, so it is left as a
  placeholder.

## Step 8 outcome

- **Case A** (scoped issue, and stream 2.1.x is also affected): post a cross-stream impact
  comment and create preemptive 2.1.x tasks.
- **Case B** (2.2.x affected): create 2 tasks for 2.2.x (dependency bump variant plus downstream
  propagation).

Full descriptions are in `remediation.md`.
