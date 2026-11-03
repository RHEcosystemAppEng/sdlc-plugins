# Step 1 – Data Extraction: TC-8020

> Note: the mock issue file lists key `TC-8001`; per the eval task the issue under
> triage is **TC-8020**. All other data is taken verbatim from
> `vuln-issue-standard.md`.

## Step 0 – Configuration (from claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component field | customfield_10632 (configured, per eval assumption) |
| Embargo policy URL | not configured, so Step 1.7 is skipped |
| ProdSec contact / account ID | not configured, so @mentions are skipped silently |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend (no Deployment Context column, defaults to `upstream`) |

Mode: interactive (no `FULLSEND_OUTPUT_DIR`). Steps 0.6/0.7 are therefore no-ops.

### Step 0.3 – Matrix staleness warning

`security-matrix-mock.md` has `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-03,
so the matrix is **128 days old**, well past the 14-day threshold. In a live run the
engineer would choose Refresh / Proceed / Stop. For this eval the analysis continues
with the current matrix, and its conclusions should be read with that caveat.

### Step 0.8 – Assign / transition (simulated, not executed)

Status is `New` and the issue is unassigned. Proposed: assign TC-8020 to the current
user and transition it to `Assigned`. No Jira call was made.

## Extracted fields

| Field | Value |
|---|---|
| Issue key | TC-8020 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Status | New |
| CVE ID | CVE-2026-31812 |
| Affected component (label) | `pscomponent:org/rhtpa-server` |
| Upstream Affected Component (customfield_10632) | quinn-proto |
| PSIRT-claimed product version (suffix) | `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 (**incorrect**: no 2.0.x stream exists) |
| Vulnerable library | quinn-proto (Rust crate) |
| Ecosystem | Cargo (source dependency, so 2 tasks per affected stream) |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS / severity | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 (already past as of 2026-11-03) |
| Existing comments | none |
| Deployment context | upstream (default) |

### Stream scope resolution

Suffix `[rhtpa-2.2]` maps to configured stream **2.2.x**, so the issue is **scoped**
to 2.2.x.

### Step 1.5 – External enrichment

External lookups (MITRE, OSV) were not run because the eval forbids external tools.
The fix threshold therefore comes from the Jira description only (< 0.11.14 / fixed
in 0.11.14), at reduced confidence.

### Step 1.7 – Embargo check

Skipped because no Embargo policy URL is configured. CVSS 7.5 would otherwise
trigger the gate.

## Step 2 – Version impact (from mock lock-file data)

| Stream | Version | backend tag | quinn-proto | Affected? |
|---|---|---|---|---|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES |
| 2.2.x | 2.2.2 | v0.4.8 (retag) | same as 2.2.1 (0.11.12) | YES |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO |

Development stream (Step 2.2): no unreleased Jira version data was provided, so no
development stream could be identified.

### Step 2.5 – Upstream fix status

| Stream | Ecosystem | Upstream Branch | Evidence | Fixed? |
|---|---|---|---|---|
| 2.2.x | Cargo | release/0.4.z | v0.4.11 and v0.4.12 already ship 0.11.14 | YES (released in 2.2.3) |
| 2.1.x | Cargo | release/0.3.z | latest tag v0.3.12 ships 0.11.9; HEAD not provided | Unknown / likely NO |

## Steps 3–6 summary (simulated)

- **Step 3 – Affects Versions correction (scoped to 2.2.x):**
  `Current: [RHTPA 2.0.0] → Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`.
  Version IDs would come from `getJiraIssueTypeMetaWithFields`. The 2.1.x versions
  belong to a companion issue.
- **Step 4 – Siblings / overlap:** no sibling or cross-CVE search results were
  supplied, so none are assumed. Cross-stream impact on 2.1.x is noted for Case A.
- **Step 5 – Lifecycle:** product pages were not fetched. All versions are assumed
  supported pending verification.
- **Step 6 – Already fixed:** no resolved siblings were supplied.
