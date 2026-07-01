# Step 2 -- Version Impact Analysis

## CVE Details

- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Affected range**: < 0.11.14
- **Fixed version**: 0.11.14

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1, backend tag v0.4.8) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | ships fixed version |

## Stream-Scoped Analysis

This issue is scoped to the **2.2.x** stream (from the `[rhtpa-2.2]` suffix in the summary). Within the 2.2.x stream:

- **Affected versions**: 2.2.0, 2.2.1, 2.2.2 (ship quinn-proto 0.11.9 or 0.11.12, both < 0.11.14)
- **Not affected versions**: 2.2.3, 2.2.4 (ship quinn-proto 0.11.14, which is the fixed version)

## Cross-Stream Impact

The 2.1.x stream is **also affected** (versions 2.1.0 and 2.1.1 ship quinn-proto 0.11.9). However, this issue is scoped to 2.2.x only. Cross-stream impact for 2.1.x would be handled via Case B (cross-stream impact comment and proactive remediation if no companion CVE Jira exists for 2.1.x).

## Dependency Chain Context

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) -> quinn -> quinn-proto
  Ecosystem: Cargo (source dependency)
  Lock file: Cargo.lock

  Present in all versions across both streams (2.1.x and 2.2.x).
  Fixed in 2.2.3+ (tag v0.4.11 onward).
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |
| 2.1.x | Cargo | release/0.3.z | 0.11.9 | NO |

- **2.2.x stream**: The upstream branch `release/0.4.z` already has quinn-proto 0.11.14 (the fix). Remediation is a downstream propagation -- update the source reference in the Konflux release repo to pick up the fix.
- **2.1.x stream**: The upstream branch `release/0.3.z` still has quinn-proto 0.11.9. Remediation would require an upstream PR first to bump the dependency on the release/0.3.z branch.
