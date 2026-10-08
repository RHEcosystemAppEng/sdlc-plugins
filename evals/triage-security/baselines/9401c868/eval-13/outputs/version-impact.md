# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Ecosystem Mappings Used

From security-matrix.md Ecosystem Mappings:

| Stream | Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|--------|-----------|------------|-----------|---------------|-----------------|
| 2.1.x | Cargo | backend | Cargo.lock | `git show <tag>:Cargo.lock` | release/0.3.z |
| 2.2.x | Cargo | backend | Cargo.lock | `git show <tag>:Cargo.lock` | release/0.4.z |

## Source Pinning Method

Both streams use `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`) for backend source pinning.

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD (latest tag) | Fixed? |
|--------|-----------|-----------------|------------------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.12) | YES |

- **2.2.x**: The upstream branch `release/0.4.z` already ships quinn-proto 0.11.14 (at tag v0.4.11 and later). The fix is available upstream. Remediation uses the **dependency bump** variant (not upstream backport).
- **2.1.x**: The upstream branch `release/0.3.z` still ships quinn-proto 0.11.9 (at tag v0.3.12). The fix is **not** available upstream. Remediation for this stream (if needed via Case A preemptive tasks) requires an **upstream backport** followed by downstream propagation.

## Stream Scope Impact Summary

- **In-scope (2.2.x)**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 are not affected.
- **Out-of-scope (2.1.x)**: Versions 2.1.0 and 2.1.1 are affected. This triggers **Case A** (cross-stream impact) for the scoped issue.

## Affects Versions Correction (Step 3)

Current Affects Versions on Jira: `RHTPA 2.0.0`
This is wrong -- RHTPA 2.0.0 does not correspond to any configured version stream.

Proposed correction (scoped to 2.2.x stream only):
`Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are not affected (they ship quinn-proto 0.11.14) and are excluded.
