# Version Impact Analysis — TC-8004 (CVE-2026-33501)

## Step 2: Version Impact Table

Version Impact for CVE-2026-33501 (h2 < 0.4.8):

| Version | Stream | Source Tag | h2 Version | Affected? | Notes |
|---------|--------|------------|------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.4.5 | **YES** | < 0.4.8 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.4.5 | **YES** | < 0.4.8 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.4.8 | NO | = 0.4.8 (at fix threshold) |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.4.8 | NO | = 0.4.8 (at fix threshold) |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.4.9 | NO | > 0.4.8 |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.4.9 | NO | > 0.4.8 |

## Stream Impact Summary

| Stream | Affected Versions | Unaffected Versions | Stream Status |
|--------|-------------------|---------------------|---------------|
| 2.1.x | 2.1.0, 2.1.1 | _(none)_ | **ALL versions affected** |
| 2.2.x | _(none)_ | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | **No versions affected** |

**Mixed impact across streams**: The 2.1.x stream ships h2 0.4.5 (vulnerable), while the 2.2.x stream ships h2 >= 0.4.8 (patched). Remediation is needed only for the 2.1.x stream.

## Dependency Chain Context (Step 2.3.5)

Dependency chain for h2 (Cargo):

- **Ecosystem**: Cargo
- **Library**: h2
- **Type**: Would require `git show <tag>:Cargo.toml` and `git show <tag>:Cargo.lock` inspection to determine direct vs. transitive dependency chain. Based on typical Rust HTTP service patterns, h2 is commonly a transitive dependency pulled in through hyper/tonic.
- **Profile**: Production dependency (h2 is a runtime HTTP/2 protocol implementation, not dev-only or build-only)

_(Exact dependency chain not determinable from mock data without running git show commands. In a real triage, the skill would inspect Cargo.lock and Cargo.toml at the pinned commits.)_

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Latest Tag Version | h2 at Latest Tag | Fixed? |
|--------|-----------|-----------------|--------------------|-----------------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | `v0.3.12` | 0.4.5 | **NO** |
| 2.2.x | Cargo | `release/0.4.z` | `v0.4.12` | 0.4.9 | YES |

For stream 2.1.x: The latest released version (2.1.1, tag v0.3.12) ships h2 0.4.5, which is below the fix threshold of 0.4.8. Without being able to check the current branch HEAD of release/0.3.z via `git show`, the upstream fix status for the 2.1.x stream cannot be confirmed from the mock data alone. The remediation plan assumes the fix is **not yet available** on release/0.3.z, requiring an upstream backport task.

For stream 2.2.x: All versions already ship h2 >= 0.4.8. No remediation needed.
