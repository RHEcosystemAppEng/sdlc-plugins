# Step 2 -- Version Impact Analysis

## Step 2.1 -- Supportability Matrix (2.2.x stream)

Loaded from security-matrix.md for stream 2.2.x (rhtpa-release.0.4.z).

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## Step 2.3 -- Dependency Version Extraction

Ecosystem: **Cargo**
Lock file: `Cargo.lock`
Check command: `git show <tag>:Cargo.lock`
Fix threshold: **0.4.5** (from Step 1 data extraction)

Simulated `git show` output for h2 at each pinned commit:

| Tag | h2 version | Comparison to fix threshold (>= 0.4.5) |
|-----|------------|----------------------------------------|
| `v0.4.5` (2.2.0) | 0.4.4 | AFFECTED (0.4.4 < 0.4.5) |
| `v0.4.8` (2.2.1) | 0.4.4 | AFFECTED (0.4.4 < 0.4.5) |
| `v0.4.8` (2.2.2) | _(retag of 2.2.1)_ | AFFECTED (same as 2.2.1) |
| `v0.4.11` (2.2.3) | 0.4.5 | NOT affected (0.4.5 >= 0.4.5) |
| `v0.4.12` (2.2.4) | 0.4.5 | NOT affected (0.4.5 >= 0.4.5) |

## Step 2.4 -- Version Impact Table

Version Impact for CVE-2026-99010 (h2 < 0.4.5):

| Version | h2 version | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.2.0 | 0.4.4 | YES | |
| 2.2.1 | 0.4.4 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.4.5 | NO | |
| 2.2.4 | 0.4.5 | NO | |

**Affected versions (2.2.x stream):** 2.2.0, 2.2.1, 2.2.2
**Unaffected versions (2.2.x stream):** 2.2.3, 2.2.4

## Step 2.3.5 -- Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> reqwest -> hyper -> h2
  Type: transitive (3 levels deep)
  Profile: production (reqwest is a runtime dependency)

First appeared: 2.1.0 (initial project setup -- reqwest has always depended on hyper/h2)
Present in all versions
```

**Manifest evidence:**

h2 is NOT a direct dependency of the backend workspace. It is pulled in transitively through the following chain:

1. `backend/Cargo.toml` declares `reqwest = { version = "0.12", features = ["json"] }` as a direct dependency
2. `reqwest` depends on `hyper`
3. `hyper` depends on `h2`

h2 does not appear in `[dependencies]`, `[dev-dependencies]`, or `[build-dependencies]` of the workspace manifest. It is a **transitive production dependency** -- it is shipped in the production binary.

**Remediation complexity:** Transitive dependency (3 levels deep). A simple `cargo update` of h2 may not be sufficient if intermediate packages (reqwest, hyper) pin specific h2 versions. The preferred approach is to bump `reqwest` (the direct dependency) to a version whose transitive closure includes h2 >= 0.4.5. The fallback is to pin h2 directly via `cargo add h2@0.4.5`.

## Step 2.5 -- Upstream Fix Check

| Stream | Ecosystem | Upstream Branch | h2 version at HEAD | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.4.5 | YES |

The upstream source repository on branch `release/0.4.z` already ships h2 0.4.5, which is at or above the fix threshold. The remediation path is a Konflux release repo change: update the source reference to pick up the fix from the upstream branch.
