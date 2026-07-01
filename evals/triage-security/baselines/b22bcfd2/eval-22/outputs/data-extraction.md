# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| **CVE ID** | CVE-2026-31812 |
| **Issue Key** | TC-8021 |
| **Summary** | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| **Issue Type** | Vulnerability |
| **Status** | New |
| **Labels** | CVE-2026-31812, pscomponent:org/rhtpa-server |
| **Affects Versions (PSIRT-assigned)** | RHTPA 2.0.0 |
| **Due Date** | 2026-07-15 |
| **Vulnerable library** | quinn-proto |
| **Affected version range** | < 0.11.14 |
| **Fixed version** | 0.11.14 |
| **CVSS** | 7.5 (High) |
| **Upstream Affected Component** | quinn-proto (customfield_10632) |
| **Ecosystem** | Cargo (Rust crate -- identified from library name `quinn-proto` and component context `pscomponent:org/rhtpa-server`; Cargo is listed in the Ecosystem Mappings table for both streams) |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table. Triage is scoped to the 2.2.x stream.

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |

## Deployment Context Lookup

The Source Repositories table does not have a Deployment Context column. All repositories default to `upstream` (backward compatibility).
