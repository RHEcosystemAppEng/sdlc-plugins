# Step 1 -- Data Extraction

## Vulnerability Issue: TC-8040

### Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE Record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |
| Issue status | New |
| Assignee | Unassigned |

### Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

This is a **scoped** issue -- triage Steps 3-8 apply to the 2.2.x stream, with cross-stream impact checks for other streams (2.1.x).

### Deployment Context Lookup

The affected component `pscomponent:org/rhtpa-server` maps to the `rhtpa-backend` source repository. Deployment context: **upstream** (default, as no Deployment Context column is present in the Source Repositories table).

### Ecosystem Detection

The vulnerable library `quinn-proto` was evaluated for ecosystem classification. Based on the task parameters, the detected ecosystem resolves to **Go modules**.

**Ecosystem Mappings check**: The configured Ecosystem Mappings tables for both version streams (2.1.x and 2.2.x) list the following ecosystems:

| Ecosystem | Category |
|-----------|----------|
| Cargo | Source dependency |
| RPM | System package |

**Go modules** is NOT listed in the Ecosystem Mappings table for any configured version stream.

**Result**: Unsupported ecosystem detected. Automated triage cannot proceed for this ecosystem. Manual assessment is required.
