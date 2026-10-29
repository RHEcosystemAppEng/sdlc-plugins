# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Stream | Backend Tag | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

**Fix threshold**: quinn-proto >= 0.11.14 (from Jira description; external CVE enrichment not performed per eval constraints).

## Dependency Chain Context (Step 2.3.5)

quinn-proto is a Cargo (Rust) dependency in the backend repository. Based on the lock file data, it is present across all versions in both streams. The dependency is a source-level Cargo dependency used for QUIC transport protocol handling.

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Latest Tag Version | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (at v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (at v0.4.12) | YES |

**Analysis**:
- **2.2.x stream**: The upstream branch `release/0.4.z` already ships quinn-proto 0.11.14 (the fixed version) as of tag v0.4.11. The fix is already available upstream. Remediation uses the **dependency bump** variant.
- **2.1.x stream**: The upstream branch `release/0.3.z` still ships quinn-proto 0.11.9 at its latest tag (v0.3.12). The fix is NOT yet available on this branch. Remediation would require an **upstream backport**.

## Summary

- **2.2.x stream** (issue scope): 3 of 5 versions affected (2.2.0, 2.2.1, 2.2.2). Fix already present in 2.2.3+.
- **2.1.x stream** (cross-stream): All 2 versions affected (2.1.0, 2.1.1). Fix not yet available upstream.
