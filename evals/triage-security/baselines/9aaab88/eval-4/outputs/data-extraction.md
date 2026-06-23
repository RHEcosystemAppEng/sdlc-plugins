# Step 1 -- Data Extraction

## Issue Details

| Field | Value |
|-------|-------|
| Issue Key | TC-8004 |
| Summary | CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames |
| Issue Type | Vulnerability |
| Status | New |
| Labels | CVE-2026-33501, pscomponent:org/rhtpa-server |
| Affects Versions (PSIRT) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Due Date | 2026-08-01 |
| Assignee | Unassigned |

## CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Affected Component | pscomponent:org/rhtpa-server |
| Vulnerable Library | h2 |
| Affected Version Range | versions before 0.4.8 |
| Fixed Version | 0.4.8 |
| CVSS | 7.5 (High) |
| Ecosystem | Cargo (Rust crate) |

## Stream Scope

The issue summary has **no stream suffix** -- this issue is **unscoped** and covers all streams. Version impact analysis will check all configured streams (2.1.x, 2.2.x).

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | [GHSA-2026-kv8p-r3n7](https://github.com/advisories/GHSA-2026-kv8p-r3n7) |
| CVE Record | [CVE-2026-33501](https://www.cve.org/CVERecord?id=CVE-2026-33501) |
| Upstream Fix PR | [hyperium/h2#812](https://github.com/hyperium/h2/pull/812) |

## Description

A vulnerability was found in the h2 crate. Versions of h2 before 0.4.8 are vulnerable to memory exhaustion caused by a peer sending an excessive number of CONTINUATION frames following a HEADERS frame. The h2 library accumulates all CONTINUATION frame data without enforcing a size limit on the accumulated header block, allowing an attacker to consume unbounded memory on the server. The fix adds a configurable maximum header list size that defaults to 16 KiB.

## Existing Comments

No comments on the issue.
