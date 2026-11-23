# Step 1 – Data Extraction: TC-8021

Mode: interactive (Step 0.6: `FULLSEND_OUTPUT_DIR` not present). Step 0.7 skipped.

> Note: the task targets **TC-8021**. The mock issue file shows `Key: TC-8001`. All
> other data comes from that file. This analysis uses TC-8021 as the issue key.

## Step 0 – Configuration Validation (claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component field | customfield_10632 (configured, per the eval assumption) |
| PS Component field | not configured |
| Stream field | not configured |
| ProdSec contact / Jira account ID | not configured (no @mentions) |
| Embargo policy URL | not configured, so Step 1.7 is skipped |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

All required sections are present (Repository Registry, Jira Configuration, Code Intelligence, Security Configuration).

## Step 0.3 – Matrix Staleness Check

Both matrices carry `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. Today is 2026-11-23, so they were last updated **148 days ago**. That is past the 14-day limit.

> Warning: the security matrix for streams **2.1.x** and **2.2.x** was last updated on 2026-06-28 (148 days ago). It may not list recent releases. Options: 1. Refresh now, 2. Proceed anyway, 3. Stop.

For this eval, triage **proceeds anyway** using the supplied matrix data. Any 2.2.x/2.1.x release after 2026-05-04 is missing from this analysis.

## Step 0.8 – Assign and Transition (proposed, not executed)

- Assign TC-8021 to the current user.
- Transition New → Assigned. The target status is found with `get_transitions`.

## Extracted CVE Data

| Field | Value |
|---|---|
| Issue key | TC-8021 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Status | New (full triage path) |
| CVE ID | CVE-2026-31812 (from the label and summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Upstream Affected Component (customfield_10632) | quinn-proto |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 ("versions before 0.11.14") |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Vulnerability class | DoS: panic from unbounded STREAMS frame stream allocation |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 (already passed as of 2026-11-23) |
| Assignee | Unassigned |
| Existing comments | none |

All critical fields (CVE ID, library, affected range) were parsed.

## Stream Scope Resolution

The suffix `[rhtpa-2.2]` maps to the configured stream **2.2.x** (rhtpa-release.0.4.z). The issue is **scoped** to 2.2.x.

## Ecosystem Detection

quinn-proto is a Rust crate, so the ecosystem is **Cargo**. Cargo is listed in both streams' Ecosystem Mappings (repo `backend`, `Cargo.lock`). It is classed as a source dependency, which means 2 remediation tasks per stream.

## Deployment Context

The repository is rhtpa-backend. It has no Deployment Context column, so it defaults to `upstream`.

## Step 1.5 – External CVE Data Enrichment

MITRE and OSV.dev were not queried, because the eval forbids external calls. This counts as the "both unavailable" path:

> Warning: external CVE databases unavailable. Using Jira description data only. Fix threshold confidence is reduced.

The fix threshold used is **0.11.14** (affected: < 0.11.14).

## Step 1.7 – Embargo Check

No Embargo policy URL is configured, so this step is skipped silently. CVSS 7.5 would otherwise have triggered the gate.

## Step 2 – Version Impact Analysis (simulated `git show <tag>:Cargo.lock` from the mock data)

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | backend tag | quinn-proto | Affected? | Notes |
|---|---|---|---|---|---|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.8 | — | YES | same as 2.2.1 (backend retag) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | fixed version shipped |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | |
| dev | unknown | branch HEAD | not available | not determined | No Jira unreleased-version data or HEAD lock data was provided |

Dependency chain (Step 2.3.5): no `Cargo.lock` dependency-tree data was provided. Whether quinn-proto is direct or transitive (it most likely comes in through `quinn` for HTTP/3) cannot be confirmed from the evidence.

Upstream fix status (Step 2.5):

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|---|---|---|---|---|
| 2.2.x | Cargo | release/0.4.z | not provided; tag v0.4.11+ already ships 0.11.14 | YES (from released-tag evidence) |
| 2.1.x | Cargo | release/0.3.z | not provided; latest tag v0.3.12 ships 0.11.9 | Unknown / likely NO |
