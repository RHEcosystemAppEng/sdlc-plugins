# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix

Loaded security-matrix.md from local files. Two streams loaded:

- **2.1.x** (rhtpa-release.0.3.z) -- 2 versions
- **2.2.x** (rhtpa-release.0.4.z) -- 5 versions

## 2.3 -- Dependency Version Extraction

Using mock lock file data for `quinn-proto` at each pinned commit tag.

Fix threshold: **0.11.14** (from Jira description; external CVE data enrichment via Step 1.5 would cross-validate this value).

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

**Stream 2.1.x** (informational -- outside this issue's scope):

| Version | Tag | quinn-proto | Affected? | Notes |
|---------|-----|-------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | |

**Stream 2.2.x** (this issue's scope):

| Version | Tag | quinn-proto | Affected? | Notes |
|---------|-----|-------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | ships fixed version |

### Dependency chain context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency
  Profile: production (quinn-proto is a runtime dependency)
  Ecosystem: Cargo
  Lock file: Cargo.lock

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```

## 2.5 -- Upstream Fix Check

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.2.x | Cargo | release/0.4.z | Upstream fix PR: quinn-rs/quinn#2048 |
| 2.1.x | Cargo | release/0.3.z | Outside this issue's scope |

The upstream fix PR (quinn-rs/quinn#2048) is available. Versions 2.2.3+ already ship the fix (0.11.14).
