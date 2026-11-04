# Step 1 – Data Extraction: TC-8006

Mode: interactive (FULLSEND_OUTPUT_DIR absent). Jira reads simulated from the eval input file; no external calls made.

## Step 0 – Configuration check (claude-md-security-config.md)

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | `pscomponent:` |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component field | not configured (Step 4.3 skipped) |
| ProdSec Jira account ID | not configured (no @mentions) |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| Version Streams | 2.1.x -> rhtpa-release.0.3.z; 2.2.x -> rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (no Deployment Context column -> `upstream`) |

All required sections are present; triage proceeds.

## Extracted CVE data

| Field | Value |
|-------|-------|
| Issue key | TC-8006 |
| Status | New (full triage path) |
| CVE ID | CVE-2026-31812 (label + summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| PSIRT-claimed product version (suffix) | `[rhtpa-2.1]` |
| Affects Versions (Jira field) | RHTPA 2.1.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 ("versions before 0.11.14") |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | none in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| Additional reference | https://rustsec.org/advisories/RUSTSEC-2026-0042.html |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Assignee | Unassigned |
| Existing comments | none |
| Existing issue links | Related -> TC-8001 (link ID 1990401, outward) |

## Stream scope resolution

- Suffix `[rhtpa-2.1]` -> stream `2.1.x`, which matches the configured Version Stream `git.example.com/rhtpa/rhtpa-release.0.3.z`.
- **Issue stream scope: 2.1.x** (scoped issue). Steps 3–4 are scoped to this stream.

## Ecosystem detection

- quinn-proto is a Rust crate -> **Cargo** (listed in the 2.1.x Ecosystem Mappings: repo `backend`, lock file `Cargo.lock`, upstream branch `release/0.3.z`).
- Category: source dependency -> 2 remediation tasks per affected stream (upstream backport + downstream propagation).
- Deployment context for rhtpa-backend: `upstream` (default).

## Step 1.5 / 1.7 notes

- External MITRE/OSV queries were not executed (eval forbids external calls); Jira description threshold (< 0.11.14, fixed 0.11.14) is used, with reduced-confidence note.
- Embargo check skipped: no Embargo policy URL configured (CVSS 7.5 would otherwise trigger it).

## Step 2 – Version impact (mock lock file data, stream 2.1.x)

Matrix Last-Updated 2026-06-28 is >14 days old relative to today (2026-11-04); in a live run the engineer would be offered refresh/proceed/stop. Proceeding with the provided matrix for the eval.

| Version | Build | Backend tag | quinn-proto | Affected? |
|---------|-------|-------------|-------------|-----------|
| RHTPA 2.1.0 | 0.3.8 | v0.3.8 | 0.11.9 | YES (< 0.11.14) |
| RHTPA 2.1.1 | 0.3.12 | v0.3.12 | 0.11.9 | YES (< 0.11.14) |

Out-of-scope reference (2.2.x, owned by sibling TC-8001): 2.2.0 (0.11.9) YES, 2.2.1 (0.11.12) YES, 2.2.2 (retag of v0.4.8, 0.11.12) YES, 2.2.3 (0.11.14) NO, 2.2.4 (0.11.14) NO.

## Step 3 – Affects Versions correction (proposed, scoped to 2.1.x)

`Current: [RHTPA 2.1.0] -> Proposed: [RHTPA 2.1.0, RHTPA 2.1.1]` (correct but incomplete; requires engineer confirmation; not executed in eval).
