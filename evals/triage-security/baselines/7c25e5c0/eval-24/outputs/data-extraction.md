# Step 0 — Configuration Extraction

## Source Repositories Parsing

The Source Repositories table in Security Configuration has the following columns:

| Repository | URL | Local Path |
|------------|-----|------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend |

**Deployment Context column: ABSENT.** Per backward compatibility rules (§1.78), when the Deployment Context column is not present in the Source Repositories table, all repositories default to `upstream`. No Coordination Guidance subsection will be included in remediation task descriptions.

Repository mapping (after defaulting):
- rhtpa-backend → { url: "https://github.com/rhtpa/rhtpa-backend", deployment_context: "upstream" (default) }

## Step 0.7 — Early Assignment

**Proposed actions** (not executed — eval prohibits Jira calls):
1. Assign TC-8001 to the current user
2. Transition TC-8001 from New → Assigned status

## Step 1 — Data Extraction

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] → scoped to 2.2.x stream |
| Affects Versions (Jira field) | RHTPA 2.0.0 (incorrect — no 2.0.x stream exists) |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| Ecosystem | Cargo (Rust crate — identified from library name quinn-proto and Ecosystem Mappings) |
| CVSS | 7.5 (High) |
| Due date | 2026-07-15 |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |

### Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]` → maps to configured Version Stream `2.2.x`. Triage is scoped to the 2.2.x stream only.

### Deployment Context Lookup

Affected repository from component label `pscomponent:org/rhtpa-server` → `rhtpa-backend`.
Deployment context: **upstream** (default — Deployment Context column absent from Source Repositories table).
