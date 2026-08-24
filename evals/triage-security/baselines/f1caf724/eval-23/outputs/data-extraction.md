# Step 1 -- Data Extraction: TC-8001

## Extracted CVE Metadata

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | (none) |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (Konflux release repo: rhtpa-release.0.4.z)
- This issue is **scoped** to the 2.2.x stream only.

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Category: **Source dependency** -- remediation produces 2 tasks per stream (upstream backport + downstream propagation)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`

## Deployment Context Lookup

- Affected repository: rhtpa-backend
- Source Repositories table entry: rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | **customer-shipped**
- Deployment context: **customer-shipped**

This deployment context will be used in Step 8 (Remediation) to generate coordination guidance in remediation task descriptions. Per the "customer-shipped" policy: "This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping."

## Version Impact Analysis (Step 2)

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14, fixed in 0.11.14):

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |

### Stream 2.2.x (rhtpa-release.0.4.z) -- issue scope

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | v0.4.9 | 0.11.12 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed) |

### Summary

- **In-scope stream (2.2.x)**: versions 2.2.0, 2.2.1, and 2.2.2 are **affected**. Versions 2.2.3 and 2.2.4 are **not affected** (already ship quinn-proto 0.11.14).
- **Cross-stream (2.1.x)**: versions 2.1.0 and 2.1.1 are **affected**. This triggers Case A (cross-stream impact notification and preemptive remediation).

### Affects Versions Correction (Step 3)

- **Current (PSIRT-assigned)**: RHTPA 2.0.0 (incorrect -- no 2.0.x stream exists)
- **Proposed (scoped to 2.2.x stream)**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- Rationale: Lock file analysis confirms quinn-proto < 0.11.14 in versions 2.2.0 through 2.2.2. Versions 2.2.3+ already ship the fix. RHTPA 2.0.0 does not correspond to any configured version stream.

### Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Fix Status |
|--------|-----------|-----------------|------------|
| 2.2.x | Cargo | release/0.4.z | YES -- v0.4.11+ ships quinn-proto 0.11.14 |
| 2.1.x | Cargo | release/0.3.z | UNKNOWN -- latest tag v0.3.12 still ships 0.11.9; upstream branch HEAD not checked |
