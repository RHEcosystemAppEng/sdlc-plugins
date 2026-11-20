# TC-8050 — Step 1: Data Extraction

Mode: interactive (simulated). `FULLSEND_OUTPUT_DIR` is not set. Jira, git, and WebFetch were **not** called. All data comes from the eval fixtures.

## Step 0: Configuration validation (from claude-md-security-config.md)

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Embargo policy URL | not configured, so Step 1.7 is skipped |
| Upstream Affected Component field | not configured, so Steps 4.3 and 7 are skipped |
| ProdSec contact / account ID | not configured, so no @mentions for ProdSec |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

Result: all required sections are present. **PASS**

## Step 0.3: Matrix staleness check

| Stream | Last-Updated | Age (as of 2026-11-20) | Status |
|--------|--------------|------------------------|--------|
| 2.1.x | 2026-06-28T10:00:00Z | 145 days | STALE (threshold is 14 days) |
| 2.2.x | 2026-06-28T10:00:00Z | 145 days | STALE (threshold is 14 days) |

> Security matrix for stream **2.2.x** was last updated on 2026-06-28 (145 days ago). The matrix may not reflect recent releases.
> Options: 1. Refresh now  2. Proceed anyway  3. Stop

Eval decision: **Proceed anyway**. A refresh needs git access, which this eval does not allow. Any 2.2.x release after 2.2.4 (2026-05-04) is missing from this analysis.

## Step 1: Parsed CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8050 | Issue |
| Issue type / Status | Vulnerability / New | Issue |
| CVE ID | CVE-2026-99001 | Label `CVE-2026-99001` and summary |
| Affected component | `pscomponent:org/rhtpa-server` | Component label |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | `versions` field |
| Vulnerable library | criterion (Rust crate) | Description |
| Affected version range | < 0.5.2 ("versions before 0.5.2") | Description |
| Fixed version | 0.5.2 | Description |
| Vulnerability | Path traversal: crafted benchmark names that contain path separators can write benchmark output files to arbitrary paths | Description |
| CVSS | 5.3 (Medium) | Description |
| Upstream fix PR | none (no GitHub PR remote link) | Remote links |
| Advisory URL | none (no GHSA/advisory remote link) | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99001 | Remote links |
| Due date | 2026-08-01 (**already passed** as of 2026-11-20) | `duedate` |
| Assignee | Unassigned | Issue |
| Existing comments | none | Comments |

All critical fields were parsed: CVE ID, library, and affected range.

### Stream scope resolution

- Summary suffix `[rhtpa-2.2]` maps to stream **2.2.x** (Konflux repo `rhtpa-release.0.4.z`).
- Issue stream scope: **2.2.x (scoped)**. Step 3 corrections and Step 8 standard tasks apply to 2.2.x only. Other streams count as cross-stream impact (Case A).

### Ecosystem detection

- criterion is a Rust crate, so the ecosystem is **Cargo**. It is listed in the 2.2.x Ecosystem Mappings (repo `backend`, lock file `Cargo.lock`, upstream branch `release/0.4.z`).
- Category: **source dependency**, which means 2 remediation tasks per stream.

### Deployment context

- Affected repo: rhtpa-backend (backend). The Source Repositories table has no Deployment Context column, so the context defaults to `upstream`. Following the backward-compatibility rule in remediation-templates.md, the Coordination Guidance subsection is **omitted**.

## Step 0.8: Assign and transition (proposed, not executed)

- Proposed: assign TC-8050 to the current user and transition New → Assigned. Not executed in this eval.

## Step 1.5: External CVE enrichment

- MITRE CVE API and OSV.dev were **not queried** because the eval does not allow external calls. The skill treats this as both sources unavailable:
  > External CVE databases unavailable. Using Jira description data only. Fix threshold confidence is reduced.
- Fix threshold used: **criterion < 0.5.2 (fixed in 0.5.2)**, from the Jira description.

## Step 1.7: Embargo check

- Skipped. No Embargo policy URL is configured, and CVSS 5.3 is below the 7.0 threshold anyway.
