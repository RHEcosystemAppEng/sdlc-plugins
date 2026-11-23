# Step 2 – Version Impact Analysis: CVE-2026-31812

Sources: supportability matrices for streams 2.1.x (rhtpa-release.0.3.z) and 2.2.x (rhtpa-release.0.4.z); quinn-proto versions from simulated `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'` at each pinned backend tag. Fix threshold: affected < 0.11.14, fixed 0.11.14.

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Stream | Backend tag (pinned) | quinn-proto | Affected? | Notes |
|---------|--------|----------------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | outside issue scope (cross-stream) |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | outside issue scope (cross-stream) |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | in scope |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | in scope |
| 2.2.2 | 2.2.x | `v0.4.8` | — | YES | same as 2.2.1 (backend retag of 2.2.1; lock file check skipped) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | first fixed release in 2.2.x |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | latest release |

**Summary**
- Stream 2.2.x (issue scope): affected = **2.2.0, 2.2.1, 2.2.2**; not affected = 2.2.3, 2.2.4.
- Stream 2.1.x (cross-stream): affected = **2.1.0, 2.1.1** (all released 2.1.x versions).

## Development Stream (Step 2.2)

- Development stream detection requires unreleased RHTPA Jira versions via `getJiraIssueTypeMetaWithFields` (not queried in this eval). Both configured streams have released versions; 2.2.x is the latest stream (no forward pointer). No development-stream HEAD evidence is available — **engineer to confirm** whether an unreleased RHTPA version exists and, if so, check branch HEAD. Latest 2.2.x release (2.2.4) already ships 0.11.14.

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for quinn-proto:
  backend (workspace) -> ... -> quinn -> quinn-proto   (expected path; QUIC stack)
  Type: transitive (likely via quinn / reqwest http3) — must be confirmed against Cargo.toml / Cargo.lock at the pinned tags
  Profile: production (QUIC transport is a runtime dependency; not a dev-only crate)

Present in: all released versions of 2.1.x and 2.2.x
Version changes: 0.11.9 (v0.3.8 – v0.4.5) -> 0.11.12 (v0.4.8) -> 0.11.14 (v0.4.11+)

Remediation: bump the direct dependency (quinn / reqwest) to a release that pulls
quinn-proto >= 0.11.14; fall back to `cargo update -p quinn-proto --precise 0.11.14`.
```

Note: the mock data only provides the quinn-proto version per tag; the exact intermediate crates were not inspectable without `git show`, so the chain above is flagged as needing confirmation.

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | not verified (latest pinned tag `v0.3.12` = 0.11.9) | NO (assumed; engineer to verify `git -C <rhtpa-backend> show release/0.3.z:Cargo.lock`) |
| 2.2.x | Cargo | `release/0.4.z` | >= 0.11.14 (pinned tags `v0.4.11`, `v0.4.12` ship 0.11.14) | YES — already shipped in 2.2.3 |

Remediation path implications:
- **2.2.x**: fix already upstream and already released (2.2.3, 2.2.4). No new code change needed in-stream.
- **2.1.x**: upstream fix not known to be on `release/0.3.z` -> upstream backport (dependency bump) + downstream Konflux propagation.

_Awaiting engineer confirmation of this table before Step 3._
