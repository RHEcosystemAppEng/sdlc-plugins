# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

All supported version streams are analyzed to determine which product versions ship the vulnerable dependency.

### 2.1.x Stream (rhtpa-release.0.3.z)

| Version | Build | quinn-proto | Affected? | Notes |
|---------|-------|-------------|-----------|-------|
| 2.1.0 | 0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 0.3.12 | 0.11.9 | YES | < 0.11.14 |

### 2.2.x Stream (rhtpa-release.0.4.z)

| Version | Build | quinn-proto | Affected? | Notes |
|---------|-------|-------------|-----------|-------|
| 2.2.0 | 0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | 0.4.9 | 0.11.12 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | 0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed) |

### Combined Version Impact Table

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | |
| 2.1.1 | 0.11.9 | YES | |
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | 0.11.12 | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | |
| 2.2.4 | 0.11.14 | NO | |

## Dependency Chain Context (Step 2.3.5)

Ecosystem: Cargo (source-level dependency)

quinn-proto is a Rust crate providing the QUIC protocol implementation. Based on the component label `pscomponent:org/rhtpa-server`, it is a dependency of the `backend` (rhtpa-backend) repository.

Dependency chain for quinn-proto:
```
backend (workspace) -> [QUIC transport chain] -> quinn -> quinn-proto
Profile: production (runtime dependency)

First appeared: present in all analyzed versions (2.1.0 through 2.2.4)
Fixed starting from: 2.2.3 (build 0.4.11, tag v0.4.11)
```

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (at v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (at v0.4.12) | YES |

### Summary

- **2.2.x stream**: Fix already present in releases 2.2.3+ (quinn-proto 0.11.14). The upstream branch `release/0.4.z` has the fix at HEAD. No new upstream backport or downstream propagation needed for this stream.
- **2.1.x stream**: All versions (2.1.0, 2.1.1) ship vulnerable quinn-proto 0.11.9. The upstream branch `release/0.3.z` does NOT have the fix at HEAD. Remediation required.
