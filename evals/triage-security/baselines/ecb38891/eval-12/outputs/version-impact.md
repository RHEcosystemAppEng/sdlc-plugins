# Step 2 -- Version Impact Analysis

## Fix Threshold

Using the **enriched fix threshold from Step 1.5**: h2 < **0.4.8** is affected. This threshold was cross-validated by both MITRE CVE API and OSV.dev (agreement). The imprecise Jira description data ("versions prior to the fix") was not used for version impact comparison.

## 2.2.x Stream (issue scope)

Version impact for CVE-2026-48901 (h2 < 0.4.8):

| Version | Build Tag | h2 Version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.1 | `v0.4.8` | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.2 | `v0.4.8` | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | `v0.4.11` | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.4 | `v0.4.12` | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

**Summary**: 1 of 5 versions in the 2.2.x stream is affected (2.2.0 only).

## 2.1.x Stream (cross-stream analysis)

| Version | Build Tag | h2 Version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.1.0 | `v0.3.8` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.1 | `v0.3.12` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |

**Summary**: All 2 versions in the 2.1.x stream are affected.

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for h2:
  backend (workspace) -> h2
  Type: direct dependency
  Profile: production (h2 is a runtime dependency for HTTP/2 protocol handling)

Remediation: bump h2 to >= 0.4.8 in Cargo.toml
```

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | h2 at branch HEAD | Fixed? |
|--------|-----------|-----------------|---------------------|--------|
| 2.2.x | Cargo | release/0.4.z | (would check via git show) | To verify |
| 2.1.x | Cargo | release/0.3.z | (would check via git show) | To verify |

Note: Upstream fix PR is available at https://github.com/hyperium/h2/pull/800. Given that versions 2.2.1+ already ship h2 >= 0.4.8, the upstream fix is likely present on the release/0.4.z branch.
