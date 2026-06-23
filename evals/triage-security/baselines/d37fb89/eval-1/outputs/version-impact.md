# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Dependency Chain Context

quinn-proto is a Cargo (Rust) dependency in the backend repository. It is inspected via `Cargo.lock` at the pinned source tags in the supportability matrix.

- **Ecosystem**: Cargo (source dependency)
- **Lock file**: `Cargo.lock`
- **Source repository**: backend
- The dependency was present from the earliest checked version (2.1.0 / v0.3.8 at 0.11.9) and was updated to the fixed version 0.11.14 starting with build v0.4.11 (version 2.2.3).

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Check Command | Notes |
|--------|-----------|-----------------|---------------|-------|
| 2.1.x | Cargo | release/0.3.z | `git show release/0.3.z:Cargo.lock` | Upstream branch status would be checked at HEAD |
| 2.2.x | Cargo | release/0.4.z | `git show release/0.4.z:Cargo.lock` | Latest released build (v0.4.12) already ships 0.11.14 -- fix is present in upstream branch |

The 2.2.x stream's latest builds (2.2.3 and 2.2.4) already ship quinn-proto 0.11.14, confirming the upstream fix has been integrated on the `release/0.4.z` branch. Affected versions in this stream are 2.2.0, 2.2.1, and 2.2.2 only.

The 2.1.x stream is also affected (both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9), but this issue is scoped to the 2.2.x stream. Cross-stream impact is noted for informational purposes.
