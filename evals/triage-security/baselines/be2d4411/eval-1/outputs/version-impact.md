# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto versions before 0.11.14)

Fix threshold: **0.11.14** (from Jira description; cross-validated with external
CVE databases in Step 1.5)

| Version | Stream | Backend Tag | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | `v0.4.8` | 0.11.12 | YES | retag of 2.2.1 (same backend tag v0.4.8) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | ships fixed version |

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) -> [transitive dependency chain] -> quinn -> quinn-proto
  Profile: production (runtime dependency)

  Present in all versions across both streams (2.1.x and 2.2.x).
```

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Latest Tag | Version at Tag | Fixed? |
|--------|-----------|-----------------|------------|----------------|--------|
| 2.1.x | Cargo | release/0.3.z | v0.3.12 | 0.11.9 | NO |
| 2.2.x | Cargo | release/0.4.z | v0.4.12 | 0.11.14 | YES |

**Summary:**
- Stream 2.2.x: upstream fix already present on release/0.4.z (since v0.4.11).
  Remediation is a downstream propagation to rebuild affected versions (2.2.0,
  2.2.1, 2.2.2) with the updated source reference.
- Stream 2.1.x: upstream fix NOT present on release/0.3.z. Remediation requires
  an upstream backport of the quinn-proto bump to release/0.3.z first, then
  downstream propagation.
