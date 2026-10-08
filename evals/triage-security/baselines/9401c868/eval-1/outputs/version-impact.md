# Step 2 -- Version Impact Analysis

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | Fixed: ships >= 0.11.14 |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | Fixed: ships >= 0.11.14 |

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (assumed based on Cargo.lock presence)
  Profile: production (quinn-proto is a runtime QUIC protocol dependency)
```

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Latest Tag | Version at Tag | Fixed? |
|--------|-----------|-----------------|------------|----------------|--------|
| 2.1.x | Cargo | release/0.3.z | v0.3.12 | 0.11.9 | NO |
| 2.2.x | Cargo | release/0.4.z | v0.4.12 | 0.11.14 | YES |

**Analysis**:
- **2.2.x stream**: The upstream branch `release/0.4.z` already ships quinn-proto 0.11.14 (fixed) as of build v0.4.11. The fix was incorporated into released versions 2.2.3 and 2.2.4. No new remediation tasks are needed for this stream -- the vulnerability has already been resolved in the latest releases.
- **2.1.x stream**: The upstream branch `release/0.3.z` still ships quinn-proto 0.11.9 (affected). All versions in the 2.1.x stream are affected. Remediation is required -- an upstream backport is needed to bump quinn-proto to >= 0.11.14 on the `release/0.3.z` branch.
