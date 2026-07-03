# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | >= fix version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | >= fix version |

### Evidence Sources

Each version's quinn-proto dependency version was extracted via:

```
git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'
```

Where `<tag>` is the backend source pinning tag from each stream's supportability matrix (e.g., `v0.3.8`, `v0.4.8`).

Version 2.2.2 was skipped (retag of 2.2.1 -- identical backend tag `v0.4.8`), and the result from 2.2.1 was carried forward.

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) -> quinn -> quinn-proto
  Profile: production (quinn is a runtime dependency)
  Ecosystem: Cargo (source dependency)
```

quinn-proto is a transitive dependency of the backend workspace, pulled in via the quinn QUIC transport crate. It is a production dependency (not dev-only or build-only).

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |

### Remediation Path Implications

- **2.2.x stream**: Fixed upstream. The upstream branch `release/0.4.z` already ships quinn-proto 0.11.14. The latest released versions (2.2.3, 2.2.4) already include the fix. Remediation for this stream confirms the fix is shipped -- no new code change required. Affected versions 2.2.0, 2.2.1, 2.2.2 are historical and documented via Affects Versions.
- **2.1.x stream**: NOT fixed upstream. The upstream branch `release/0.3.z` still ships quinn-proto 0.11.9. Remediation requires an upstream PR to bump the dependency on `release/0.3.z`, followed by a downstream Konflux release repo update in `rhtpa-release.0.3.z`.

## Affects Versions Correction (Step 3)

The issue is scoped to the **2.2.x** stream.

- **Current** (PSIRT-assigned): `[RHTPA 2.0.0]`
- **Proposed** (based on lock file evidence): `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

RHTPA 2.0.0 does not correspond to any version in the supportability matrix. The correct affected versions within the 2.2.x stream are 2.2.0, 2.2.1, and 2.2.2, which ship quinn-proto versions 0.11.9 and 0.11.12, both below the fix threshold of 0.11.14. Versions 2.2.3 and 2.2.4 are NOT affected and should not be included in Affects Versions.

## Cross-Stream Impact Summary

The 2.1.x stream (versions 2.1.0 and 2.1.1) is also affected. Since the current issue TC-8001 is scoped to stream 2.2.x only, the 2.1.x impact is handled via Case B (cross-stream proactive remediation) in Step 8.
