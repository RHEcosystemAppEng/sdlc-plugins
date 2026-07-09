# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

Summary suffix `[rhtpa-2.2]` maps to stream **2.2.x** from the Version Streams table.
Issue is **scoped** to the 2.2.x stream only.

## Ecosystem Detection

Library **quinn-proto** is a Rust crate. The Ecosystem Mappings table for the 2.2.x stream lists **Cargo** as a supported ecosystem with lock file `Cargo.lock`.

Ecosystem: **Cargo** (source dependency)

## Continuation

Step 0.3 staleness check passed silently (matrix is fresh -- 11 days old, within the 14-day threshold). Triage proceeded through Step 0.5 (JIRA Access Initialization) and Step 0.7 (Assign and Transition) without interruption before reaching this Step 1 data extraction.
