# Version Impact Analysis -- CVE-2026-28940

## Step 2.3 -- Dependency Version Extraction

Extracted serde_json versions from Cargo.lock at each pinned source commit (from security-matrix.md mock lock file data):

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Tag | serde_json version | Fix threshold (1.0.135) | Affected? |
|---------|-------|-----|--------------------|------------------------|-----------|
| 2.1.0 | 0.3.8 | v0.3.8 | 1.0.137 | 1.0.137 >= 1.0.135 | NO |
| 2.1.1 | 0.3.12 | v0.3.12 | 1.0.137 | 1.0.137 >= 1.0.135 | NO |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Tag | serde_json version | Fix threshold (1.0.135) | Affected? |
|---------|-------|-----|--------------------|------------------------|-----------|
| 2.2.0 | 0.4.5 | v0.4.5 | 1.0.138 | 1.0.138 >= 1.0.135 | NO |
| 2.2.1 | 0.4.8 | v0.4.8 | 1.0.138 | 1.0.138 >= 1.0.135 | NO |
| 2.2.2 | 0.4.9 | v0.4.9 | -- | retag of v0.4.8 (same as 2.2.1) | NO |
| 2.2.3 | 0.4.11 | v0.4.11 | 1.0.139 | 1.0.139 >= 1.0.135 | NO |
| 2.2.4 | 0.4.12 | v0.4.12 | 1.0.139 | 1.0.139 >= 1.0.135 | NO |

## Step 2.4 -- Version Impact Table (Combined)

```
Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

| Version | Stream | serde_json | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0   | 2.1.x  | 1.0.137    | NO        |       |
| 2.1.1   | 2.1.x  | 1.0.137    | NO        |       |
| 2.2.0   | 2.2.x  | 1.0.138    | NO        |       |
| 2.2.1   | 2.2.x  | 1.0.138    | NO        |       |
| 2.2.2   | 2.2.x  | --         | NO        | retag of 2.2.1 |
| 2.2.3   | 2.2.x  | 1.0.139    | NO        |       |
| 2.2.4   | 2.2.x  | 1.0.139    | NO        |       |
```

## Key Finding

**No supported version is affected.** Every shipped version across both streams (2.1.x and 2.2.x) includes serde_json >= 1.0.137, which is above the fix threshold of 1.0.135. The vulnerability was patched in the dependency before any of these product versions were built.

- Earliest serde_json version across all builds: **1.0.137** (streams 2.1.x builds v0.3.8 and v0.3.12)
- CVE fix threshold: **1.0.135**
- Margin: all versions ship serde_json at least 2 patch versions above the fix

## Step 2.5 -- Upstream Fix Status

Not applicable -- no versions are affected, so upstream fix status is moot. For completeness, the upstream branches both carry fixed versions:

| Stream | Ecosystem | Upstream Branch | Latest shipped serde_json | Fixed? |
|--------|-----------|-----------------|---------------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 1.0.137 | YES (already fixed) |
| 2.2.x | Cargo | release/0.4.z | 1.0.139 | YES (already fixed) |
