# Step 1 -- Data Extraction

## Issue: TC-8001

### Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels (`CVE-2026-31812`) and summary text |
| Affected component | `pscomponent:org/rhtpa-server` | Labels (matches component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text ("A vulnerability was found in quinn-proto") |
| Affected version range | < 0.11.14 (versions before 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS score | 7.5 (High) | Description text |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) | Remote links |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) | Remote links |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | (none) | Issue comment history |
| Issue status | New | Issue `status` field |
| Assignee | Unassigned | Issue `assignee` field |

### Stream Scope Resolution

The summary contains the stream suffix `[rhtpa-2.2]`, which maps to stream **2.2.x** in the configured Version Streams table (Konflux release repo `rhtpa-release.0.4.z`). This issue is **stream-scoped** to the 2.2.x stream.

### Affects Versions Discrepancy (Preliminary)

PSIRT set Affects Versions to **RHTPA 2.0.0**, but there is no 2.0.x version stream configured. The configured streams are 2.1.x and 2.2.x. This will need correction in Step 3 after version impact analysis confirms which versions actually ship the vulnerable dependency.

### Ecosystem Detection

The vulnerable library **quinn-proto** is a Rust crate. Based on the Ecosystem Mappings in the security matrix, the relevant ecosystem is **Cargo**, with lock file `Cargo.lock` and check command `git show <tag>:Cargo.lock`.

Ecosystem classification: **Source dependency** -- remediation produces 2 tasks per affected stream (upstream backport or dependency bump + downstream propagation).

### Deployment Context

The affected repository `rhtpa-backend` is listed in Source Repositories. No explicit Deployment Context column is present, so the default of `upstream` applies.

### Vulnerability Summary

quinn-proto (before version 0.11.14) allows a remote attacker to cause a denial-of-service (DoS) panic by sending a QUIC transport frame that creates an excessive number of streams. The server allocates unbounded stream state objects from a specially crafted STREAMS frame, leading to a panic when allocation exceeds internal limits. Fixed in quinn-proto 0.11.14.

### Version Impact Preview (from mock lock file data)

Using the mock lock file data provided in the security matrix, the quinn-proto versions by tag are:

| Tag | quinn-proto version | Affected (< 0.11.14)? |
|-----|---------------------|-----------------------|
| `v0.3.8` (2.1.0) | 0.11.9 | YES |
| `v0.3.12` (2.1.1) | 0.11.9 | YES |
| `v0.4.5` (2.2.0) | 0.11.9 | YES |
| `v0.4.8` (2.2.1) | 0.11.12 | YES |
| `v0.4.9` (2.2.2) | _(retag of v0.4.8)_ = 0.11.12 | YES (same as 2.2.1) |
| `v0.4.11` (2.2.3) | 0.11.14 | NO (fixed version) |
| `v0.4.12` (2.2.4) | 0.11.14 | NO (fixed version) |

This data will feed Step 2 (Version Impact Analysis) for full triage.
