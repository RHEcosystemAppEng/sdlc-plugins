# Step 2 — Version Impact Analysis

## Version Impact for CVE-2026-99010 (h2 < 0.4.5)

Stream scope: **2.2.x** (per issue suffix `[rhtpa-2.2]`)

| Version | h2 version | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.2.0 | 0.4.4 | YES | Pinned commit `v0.4.5` |
| 2.2.1 | 0.4.4 | YES | Pinned commit `v0.4.8` |
| 2.2.2 | — | YES | Retag of 2.2.1 — same as 2.2.1 |
| 2.2.3 | 0.4.5 | NO | Pinned commit `v0.4.11` |
| 2.2.4 | 0.4.5 | NO | Pinned commit `v0.4.12` |

Versions 2.2.0 through 2.2.2 ship h2 0.4.4, which is within the affected range (< 0.4.5).
Versions 2.2.3 and 2.2.4 ship h2 0.4.5, which is the fixed version — not affected.

---

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for h2:
  backend (workspace) → reqwest → hyper → h2
  Type: transitive (3 levels deep)
  Profile: production (reqwest is a runtime dependency)

First appeared: 2.1.0 (initial project setup — reqwest has always depended on hyper/h2)
Present in all versions
```

**Classification**: h2 is a **transitive** dependency, NOT a direct dependency of the backend workspace.

**Manifest evidence**: h2 does NOT appear in `backend/Cargo.toml` `[dependencies]`. It is pulled in through:
1. **reqwest** (direct dependency, version 0.12, with `json` feature)
2. reqwest depends on **hyper** (version 1.4.1)
3. hyper depends on **h2** (version 0.4.x)

**Remediation implications**: Because h2 is transitive (3 levels deep), a direct version bump of h2 in the manifest is not the primary approach. The two-tier remediation strategy applies:
- **Preferred**: bump **reqwest** (the direct dependency) to a version whose transitive closure includes h2 >= 0.4.5
- **Fallback**: pin h2 directly via `cargo add h2@0.4.5`

---

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | h2 version at HEAD | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.4.5 | YES |

The upstream branch `release/0.4.z` already ships h2 0.4.5 (the fixed version).
Remediation can use a dependency bump approach (`cargo update`) rather than requiring a source-level backport.
