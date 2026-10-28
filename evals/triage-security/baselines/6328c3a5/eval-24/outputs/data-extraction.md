# Step 1 -- Data Extraction: TC-8001

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Stream scope | **2.2.x** (scoped -- matches configured Version Stream 2.2.x) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Ecosystem | Cargo (Rust crate) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |

## Deployment Context

Source Repositories table does NOT have a Deployment Context column. Per backward-compatibility rules, all repos default to `upstream`. Coordination guidance subsection is omitted from remediation task descriptions because the column is absent.

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]` maps to configured Version Stream **2.2.x**
- Issue is **scoped** to 2.2.x only
- Other streams (2.1.x) will be checked for cross-stream impact (Case A)

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
- Classification: Source dependency ecosystem -- 2 tasks per stream (dependency bump + downstream propagation, since upstream fix is available)

## Version Impact Analysis (Step 2)

### Version Impact Table

| Stream | Version | Build Tag | quinn-proto version | Affected? | Notes |
|--------|---------|-----------|---------------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.9 | 0.11.12 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | ships fixed version |

All versions shipping quinn-proto < 0.11.14 are affected. Versions 2.2.3+ ship the fix (0.11.14).

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix available? | Evidence |
|--------|-----------|-----------------|----------------|----------|
| 2.1.x | Cargo | release/0.3.z | Unknown | Latest tag v0.3.12 ships 0.11.9 (still affected) |
| 2.2.x | Cargo | release/0.4.z | YES | Tags v0.4.11 and v0.4.12 ship 0.11.14 (fixed) |

Since v0.4.11+ on the 2.2.x stream already ships the fixed version (0.11.14), the remediation for 2.2.x uses the **dependency bump** variant rather than upstream backport.

For 2.1.x, the latest tag (v0.3.12) still ships 0.11.9. The fix availability on release/0.3.z branch HEAD is not confirmed from the mock data, so the 2.1.x stream may require upstream backport.

### Affects Versions Correction (Step 3)

- **Current (PSIRT-assigned)**: RHTPA 2.0.0
- **Corrected (based on lock file evidence)**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Rationale**: RHTPA 2.0.0 does not correspond to any configured version stream. The issue is scoped to 2.2.x, and lock file analysis shows versions 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto < 0.11.14. Versions 2.2.3 and 2.2.4 ship the fixed version and are NOT affected.

### Cross-Stream Impact (Case A)

This issue is scoped to 2.2.x, but 2.1.x (versions 2.1.0 and 2.1.1) is also affected:
- 2.1.0 ships quinn-proto 0.11.9 (affected)
- 2.1.1 ships quinn-proto 0.11.9 (affected)

Case A applies: post cross-stream impact comment and create preemptive remediation tasks for 2.1.x if no sibling CVE Jira exists for that stream.
