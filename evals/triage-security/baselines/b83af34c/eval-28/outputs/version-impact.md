# Step 2 -- Version Impact Analysis: CVE-2026-99010 (h2 < 0.4.5)

## Stream Scope

Issue is scoped to **2.2.x** stream per summary suffix `[rhtpa-2.2]`.

## Version Impact Table

Version Impact for CVE-2026-99010 (h2 < 0.4.5):

| Version | h2 version | Affected? | Notes |
|---------|------------|-----------|-------|
| 2.2.0   | 0.4.4      | YES       |       |
| 2.2.1   | 0.4.4      | YES       |       |
| 2.2.2   | --         | YES       | retag of 2.2.1 |
| 2.2.3   | 0.4.5      | NO        |       |
| 2.2.4   | 0.4.5      | NO        |       |

Affected versions: 2.2.0, 2.2.1, 2.2.2 (h2 0.4.4 < fix threshold 0.4.5)
Not affected: 2.2.3, 2.2.4 (h2 0.4.5 >= fix threshold 0.4.5)

## Step 2.3.5 -- Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> reqwest -> hyper -> h2
  Type: transitive (3 levels deep)
  Profile: production (reqwest is a runtime dependency)

First appeared: 2.1.0 (initial project setup -- reqwest has always depended on hyper/h2)
Present in all versions
```

**Dependency type**: transitive (not direct)
**Full chain path**: backend -> reqwest -> hyper -> h2
**Depth**: 3 levels deep
**Direct dependency in the chain**: reqwest (this is the workspace's direct dependency that ultimately pulls in h2)

**Manifest evidence:**
```toml
# backend/Cargo.toml (all versions)
[dependencies]
reqwest = { version = "0.12", features = ["json"] }
# h2 is NOT a direct dependency -- it comes through reqwest -> hyper -> h2
```

**Lock file evidence (affected versions 2.2.0--2.2.2):**
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

**Lock file evidence (fixed versions 2.2.3+):**
```
[[package]]
name = "h2"
version = "0.4.5"
```

## Cross-Stream Impact

The issue is scoped to 2.2.x. Checking other streams for cross-stream awareness:

| Stream | h2 version | Affected? |
|--------|------------|-----------|
| 2.1.x (v0.3.8, 2.1.0) | 0.4.5 | NO |
| 2.1.x (v0.3.12, 2.1.1) | 0.4.5 | NO |

The 2.1.x stream is NOT affected (h2 is at 0.4.5 which is the fix version). No cross-stream remediation needed.
