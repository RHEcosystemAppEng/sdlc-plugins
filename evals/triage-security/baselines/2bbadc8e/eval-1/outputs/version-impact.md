# Step 2 -- Version Impact Analysis

## Supportability Matrix (aggregated from all streams)

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend tag |
|---------|-------|------------|-------------|
| 2.1.0   | 0.3.8 | 2025-09-15 | v0.3.8      |
| 2.1.1   | 0.3.12| 2025-11-20 | v0.3.12     |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0   | 0.4.5 | 2025-12-03 | v0.4.5      |       |
| 2.2.1   | 0.4.8 | 2026-02-05 | v0.4.8      |       |
| 2.2.2   | 0.4.9 | 2026-02-23 | v0.4.8      | backend retag of 2.2.1 |
| 2.2.3   | 0.4.11| 2026-03-23 | v0.4.11     |       |
| 2.2.4   | 0.4.12| 2026-05-04 | v0.4.12     |       |

## Dependency Version Extraction (quinn-proto)

Extracted from `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'` at each pinned backend commit:

| Tag | quinn-proto version |
|-----|---------------------|
| v0.3.8  | 0.11.9  |
| v0.3.12 | 0.11.9  |
| v0.4.5  | 0.11.9  |
| v0.4.8  | 0.11.12 |
| v0.4.9  | _(retag of v0.4.8 -- same as v0.4.8)_ |
| v0.4.11 | 0.11.14 |
| v0.4.12 | 0.11.14 |

## Version Impact Table

CVE-2026-31812 (quinn-proto < 0.11.14): fix threshold = **0.11.14**

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0   | 2.1.x  | 0.11.9      | **YES**   | 0.11.9 < 0.11.14 |
| 2.1.1   | 2.1.x  | 0.11.9      | **YES**   | 0.11.9 < 0.11.14 |
| 2.2.0   | 2.2.x  | 0.11.9      | **YES**   | 0.11.9 < 0.11.14 |
| 2.2.1   | 2.2.x  | 0.11.12     | **YES**   | 0.11.12 < 0.11.14 |
| 2.2.2   | 2.2.x  | --          | **YES**   | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3   | 2.2.x  | 0.11.14     | NO        | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4   | 2.2.x  | 0.11.14     | NO        | 0.11.14 >= 0.11.14 (fixed) |

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Latest Tag | Version at Latest Tag | Fixed? |
|--------|-----------|-----------------|------------|-----------------------|--------|
| 2.1.x  | Cargo     | release/0.3.z   | v0.3.12    | 0.11.9                | **NO** |
| 2.2.x  | Cargo     | release/0.4.z   | v0.4.12    | 0.11.14               | **YES** |

**Summary:**
- **2.2.x stream**: The fix (quinn-proto 0.11.14) is already present in versions 2.2.3 and 2.2.4. The upstream branch `release/0.4.z` already ships the fix at HEAD (v0.4.12 has 0.11.14). Remediation for affected versions (2.2.0, 2.2.1, 2.2.2) is a **dependency bump** (not an upstream backport) since the upstream branch already has the fix.
- **2.1.x stream**: All versions (2.1.0, 2.1.1) are affected. The upstream branch `release/0.3.z` does NOT ship the fix (v0.3.12 still has 0.11.9). Remediation for 2.1.x would require an **upstream backport** followed by downstream propagation.
