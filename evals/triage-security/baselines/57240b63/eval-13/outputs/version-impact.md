# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | ships fixed version |

Fix threshold: 0.11.14 (from Jira description; to be cross-validated with MITRE CVE API and OSV.dev in Step 1.5)

## Lock File Evidence

Each quinn-proto version was extracted by the simulated equivalent of:
```
git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'
```

| Tag | Command Output (quinn-proto version) |
|-----|--------------------------------------|
| `v0.3.8` | 0.11.9 |
| `v0.3.12` | 0.11.9 |
| `v0.4.5` | 0.11.9 |
| `v0.4.8` | 0.11.12 |
| `v0.4.9` | _(retag of v0.4.8 -- skipped, carried forward 0.11.12)_ |
| `v0.4.11` | 0.11.14 |
| `v0.4.12` | 0.11.14 |

## Dependency Chain Context (Step 2.3.5)

Dependency chain for quinn-proto:

- Ecosystem: Cargo (source dependency)
- quinn-proto is a Rust crate used for QUIC transport
- Repository: backend (rhtpa-backend)
- Lock file: `Cargo.lock`
- The dependency is present in all versions checked (0.11.9 in older versions, 0.11.12 in 2.2.1, 0.11.14 in 2.2.3+)
- Profile: production (quinn-proto is a runtime dependency for QUIC transport)

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Latest Tag Version | quinn-proto at HEAD | Fixed? |
|--------|-----------|-----------------|--------------------|--------------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | v0.3.12 | 0.11.9 | NO |
| 2.2.x | Cargo | `release/0.4.z` | v0.4.12 | 0.11.14 | YES |

Remediation path implications:
- **2.2.x stream**: Fix is already on `release/0.4.z` upstream branch and shipped in versions 2.2.3+. Affected versions are 2.2.0, 2.2.1, 2.2.2. Remediation is already deployed -- the fix was picked up in build v0.4.11 (version 2.2.3).
- **2.1.x stream**: Fix is NOT on `release/0.3.z` upstream branch. Remediation requires an upstream PR to bump quinn-proto to >= 0.11.14, then a downstream Konflux release repo update.

## Affects Versions Correction (Step 3)

### Stream-scoped correction (issue scoped to 2.2.x)

- Current Affects Versions: `[RHTPA 2.0.0]`
- RHTPA 2.0.0 does not match any version in the supportability matrix -- PSIRT-assigned version is incorrect
- Affected versions within stream 2.2.x: 2.2.0, 2.2.1, 2.2.2

PROPOSAL: Correct Affects Versions:
```
Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

Rationale: Lock file analysis at pinned commits from security-matrix.md shows quinn-proto < 0.11.14 in versions 2.2.0 (0.11.9), 2.2.1 (0.11.12), and 2.2.2 (retag of 2.2.1). Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fixed version). Scoped to stream 2.2.x per issue suffix `[rhtpa-2.2]`.

Note: Versions 2.1.0 and 2.1.1 (stream 2.1.x) are also affected but belong to a companion CVE Jira if one exists.

## Cross-Stream Impact Summary (Case B)

Stream 2.1.x is also affected:
- 2.1.0 ships quinn-proto 0.11.9 (affected)
- 2.1.1 ships quinn-proto 0.11.9 (affected)
- Upstream branch `release/0.3.z` does NOT have the fix at HEAD

Since the issue is scoped to 2.2.x, the 2.1.x impact is handled via:
1. Cross-stream impact comment on TC-8001
2. Check for existing sibling CVE Jira for 2.1.x
3. If no sibling exists: create preemptive remediation tasks for 2.1.x

## Triage Decision Path

- Step 4.3 (Cross-CVE Overlap Detection): **Skipped** -- Upstream Affected Component custom field not configured
- Step 4.4 (Preemptive Task Reconciliation): Would search for existing preemptive tasks with CVE-2026-31812 label and security-preemptive label
- Step 5 (Version Lifecycle Check): Would verify via Product pages URL whether 2.2.0-2.2.2 and 2.1.0-2.1.1 are still supported
- Step 6 (Already Fixed Check): No resolved sibling issues found (no comments, no siblings)
- Step 7 (Concurrent Triage Detection): **Skipped** -- Upstream Affected Component custom field not configured
- Outcome: **Case A** (affected -- create remediation tasks for 2.2.x) + **Case B** (cross-stream impact -- create preemptive remediation tasks for 2.1.x)
