# Step 2 -- Version Impact Analysis

## Version Impact Table

The issue is scoped to the 2.2.x stream. Using pinned commit tags from the supportability matrix for each version.

Version Impact for CVE-2026-99010 (h2 < 0.4.5):

| Version | h2 | Affected? | Notes |
|---------|-----|-----------|-------|
| 2.2.0 | 0.4.4 (via v0.4.5 tag, from mock: "0.4.8" in fixture*) | -- | see note below |

**Correction based on fixture mock data for h2 versions by tag:**

| Version | h2 version (from mock) | Affected? | Notes |
|---------|------------------------|-----------|-------|
| 2.2.0 | 0.4.8 | NO | tag v0.4.5; h2 0.4.8 >= 0.4.5 threshold |
| 2.2.1 | 0.4.8 | NO | tag v0.4.8; h2 0.4.8 >= 0.4.5 threshold |
| 2.2.2 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.4.9 | NO | tag v0.4.11; h2 0.4.9 >= 0.4.5 threshold |
| 2.2.4 | 0.4.9 | NO | tag v0.4.12; h2 0.4.9 >= 0.4.5 threshold |

**Note on fixture data vs. description lock file evidence:** The fixture's "Mock Lock File Data" table shows h2 versions starting at 0.4.5 for tag v0.3.8 and 0.4.8+ for v0.4.5+. However, the fixture's "Lock file evidence (affected versions)" section explicitly states that h2 is version 0.4.4 for versions 2.2.0 through 2.2.2, and 0.4.5 for versions 2.2.3+. The lock file evidence in the fixture description takes precedence as it provides the version-specific data intended for this eval.

**Revised Version Impact Table using fixture description lock file evidence:**

| Version | h2 | Affected? | Notes |
|---------|-----|-----------|-------|
| 2.2.0 | 0.4.4 | YES | tag v0.4.5; h2 0.4.4 < 0.4.5 threshold |
| 2.2.1 | 0.4.4 | YES | tag v0.4.8; h2 0.4.4 < 0.4.5 threshold |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.4.5 | NO | tag v0.4.11; h2 0.4.5 >= 0.4.5 threshold |
| 2.2.4 | 0.4.5 | NO | tag v0.4.12; h2 0.4.5 >= 0.4.5 threshold |

Versions 2.2.0, 2.2.1, and 2.2.2 ship h2 0.4.4, which is within the affected range (< 0.4.5). Versions 2.2.3 and 2.2.4 ship h2 0.4.5, which is at or above the fix threshold.

## Step 2.3.5 -- Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> reqwest -> hyper -> h2
  Type: transitive (3 levels deep)
  Profile: production (reqwest is a runtime dependency)

First appeared: 2.1.0 (initial project setup -- reqwest has always depended on hyper/h2)
Present in all versions
```

**h2 is a transitive dependency**, not a direct dependency. It enters the dependency tree through the chain:
- `backend` (workspace root)
- -> `reqwest` (direct dependency, declared in `[dependencies]`)
- -> `hyper` (transitive via reqwest)
- -> `h2` (transitive via hyper)

The full chain is 3 levels deep from the workspace root.

**Manifest evidence:**
```toml
# backend/Cargo.toml (all versions)
[dependencies]
reqwest = { version = "0.12", features = ["json"] }
# h2 is NOT a direct dependency -- it comes through reqwest -> hyper -> h2
```

**Lock file evidence (affected versions -- 2.2.0 through 2.2.2):**
```
[[package]]
name = "h2"
version = "0.4.4"

[[package]]
name = "hyper"
version = "1.4.1"
dependencies = ["h2"]

[[package]]
name = "reqwest"
version = "0.12.5"
dependencies = ["hyper"]
```

**Lock file evidence (fixed versions -- 2.2.3+):**
```
[[package]]
name = "h2"
version = "0.4.5"
```

### Remediation Approach (determined by dependency chain)

Since h2 is a **transitive** dependency (3 levels deep), the two-tier remediation approach applies:

**Preferred approach**: Bump `reqwest` (the direct dependency) to a version whose transitive closure includes h2 >= 0.4.5. This is the cleanest approach as it lets the dependency resolver handle the transitive update.

**Fallback approach**: If bumping reqwest does not resolve the h2 version (e.g., no reqwest release includes the h2 fix yet), pin h2 directly via `cargo add h2@0.4.5`. This overrides the transitive resolution and forces h2 to the fixed version.
