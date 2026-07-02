# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0   | 0.11.9      | YES       |       |
| 2.1.1   | 0.11.9      | YES       |       |
| 2.2.0   | 0.11.9      | YES       |       |
| 2.2.1   | 0.11.12     | YES       |       |
| 2.2.2   | --          | YES       | retag of 2.2.1 |
| 2.2.3   | 0.11.14     | NO        | ships fixed version |
| 2.2.4   | 0.11.14     | NO        | ships fixed version |

## Stream Summary

| Stream | Versions Affected | Versions Not Affected |
|--------|-------------------|-----------------------|
| 2.1.x  | 2.1.0, 2.1.1     | (none)                |
| 2.2.x  | 2.2.0, 2.2.1, 2.2.2 | 2.2.3, 2.2.4      |

## Evidence

- quinn-proto at `v0.3.8` (2.1.0, build 0.3.8): **0.11.9** -- AFFECTED (< 0.11.14)
- quinn-proto at `v0.3.12` (2.1.1, build 0.3.12): **0.11.9** -- AFFECTED (< 0.11.14)
- quinn-proto at `v0.4.5` (2.2.0, build 0.4.5): **0.11.9** -- AFFECTED (< 0.11.14)
- quinn-proto at `v0.4.8` (2.2.1, build 0.4.8): **0.11.12** -- AFFECTED (< 0.11.14)
- quinn-proto at `v0.4.9` (2.2.2, build 0.4.9): retag of v0.4.8 -- same as 2.2.1 -- AFFECTED
- quinn-proto at `v0.4.11` (2.2.3, build 0.4.11): **0.11.14** -- NOT AFFECTED (>= 0.11.14)
- quinn-proto at `v0.4.12` (2.2.4, build 0.4.12): **0.11.14** -- NOT AFFECTED (>= 0.11.14)

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x  | Cargo     | release/0.3.z   | (needs check)   | TBD    |
| 2.2.x  | Cargo     | release/0.4.z   | 0.11.14         | YES    |

The 2.2.x upstream branch (`release/0.4.z`) already ships the fix at tag `v0.4.11`+. The fix was introduced between builds 0.4.8 and 0.4.11.

## Cross-Stream Impact

This issue is scoped to stream **2.2.x**, but stream **2.1.x** is also affected (all versions ship quinn-proto 0.11.9). This triggers Case B (cross-stream impact) in Step 8.
