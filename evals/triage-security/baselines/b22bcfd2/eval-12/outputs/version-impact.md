# Step 2 -- Version Impact Analysis

## Fix Threshold

The enriched fix threshold from Step 1.5 is used for all version impact comparisons:

- **Library**: h2
- **Affected range**: < 0.4.8 (from MITRE CVE API and OSV.dev, cross-validated)
- **Fixed version**: 0.4.8

The imprecise Jira description data ("versions prior to the fix") is NOT used. The enriched threshold from Step 1.5 (0.4.8) is the authoritative value.

## 2.1 -- Supportability Matrix (2.2.x stream)

Issue TC-8030 is scoped to the **2.2.x** stream (`[rhtpa-2.2]`). The supportability matrix for this stream:

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 -- Dependency Version Extraction

For each version, the h2 dependency version is extracted from `Cargo.lock` at the pinned commit tag. Comparison uses the **enriched fix threshold (0.4.8)** from Step 1.5, not the imprecise Jira description.

| Version | Pinned Tag | h2 Version | Comparison vs 0.4.8 | Affected? |
|---------|-----------|------------|---------------------|-----------|
| 2.2.0 | `v0.4.5` | 0.4.5 | 0.4.5 < 0.4.8 | **YES** |
| 2.2.1 | `v0.4.8` | 0.4.8 | 0.4.8 >= 0.4.8 | NO |
| 2.2.2 | `v0.4.8` | _(retag of 2.2.1)_ | same as 2.2.1 | NO |
| 2.2.3 | `v0.4.11` | 0.4.9 | 0.4.9 >= 0.4.8 | NO |
| 2.2.4 | `v0.4.12` | 0.4.9 | 0.4.9 >= 0.4.8 | NO |

## Version Impact Table

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

| Version | h2 Version | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.2.0 | 0.4.5 | **YES** | Ships vulnerable h2 |
| 2.2.1 | 0.4.8 | NO | Ships fixed version |
| 2.2.2 | -- | NO | retag of 2.2.1 |
| 2.2.3 | 0.4.9 | NO | Ships patched version |
| 2.2.4 | 0.4.9 | NO | Ships patched version |

**Summary**: Only version **2.2.0** is affected. Versions 2.2.1 through 2.2.4 ship h2 >= 0.4.8 and are not affected.

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for h2 (Cargo):
  backend (workspace) -> hyper -> h2
  Profile: production (hyper is a runtime dependency)

  First appeared: present in all 2.2.x versions
  Affected version (2.2.0): ships h2 0.4.5 (vulnerable)
  Fixed from: 2.2.1 (ships h2 0.4.8)
```

## Cross-Stream Impact (informational)

Although this issue is scoped to 2.2.x, the 2.1.x stream also ships h2:

| Version | h2 Version | Affected? |
|---------|-----------|-----------|
| 2.1.0 | 0.4.5 | YES |
| 2.1.1 | 0.4.5 | YES |

Both 2.1.x versions ship h2 0.4.5 (< 0.4.8) and are affected. Cross-stream impact will be reported in Step 8 (Case B) if applicable.

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.2.x | Cargo | release/0.4.z | h2 updated to 0.4.8+ from version 2.2.1 onward |
