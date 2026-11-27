# Step 2 – Version Impact Analysis: TC-8001

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

Evidence: simulated `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'` output at the pinned backend tags in security-matrix.md (mock lock file data).

| Stream | Version | Build | backend tag | quinn-proto | Affected? | Notes |
|--------|---------|-------|-------------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | 0.3.8 | `v0.3.8` | 0.11.9 | YES | outside issue scope |
| 2.1.x | 2.1.1 | 0.3.12 | `v0.3.12` | 0.11.9 | YES | outside issue scope |
| 2.2.x | 2.2.0 | 0.4.5 | `v0.4.5` | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | 0.4.8 | `v0.4.8` | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | 0.4.9 | `v0.4.8` | — | YES | same as 2.2.1 (backend retag of 2.2.1; lock check skipped) |
| 2.2.x | 2.2.3 | 0.4.11 | `v0.4.11` | 0.11.14 | NO | fixed version shipped |
| 2.2.x | 2.2.4 | 0.4.12 | `v0.4.12` | 0.11.14 | NO | |
| dev | — | — | branch HEAD | not determined | — | No Jira unreleased-version data available (Step 2.2 not executable offline); development stream not identified. Not fabricated. |

**Summary**
- Issue scope (2.2.x): affected = RHTPA 2.2.0, 2.2.1, 2.2.2; not affected = 2.2.3, 2.2.4 (fix 0.11.14 already shipped since 2.2.3).
- Other stream (2.1.x): RHTPA 2.1.0 and 2.1.1 are affected (cross-stream impact – Case A).
- RHTPA 2.0.0 (PSIRT-assigned) does not exist in the supportability matrix.

## Step 2.3.5 – Dependency chain

quinn-proto is a Cargo crate in rhtpa-backend's `Cargo.lock`. Direct vs. transitive classification could not be determined from the provided data (no `Cargo.toml` / `cargo tree` output available); quinn-proto is normally pulled transitively via `quinn` (QUIC, e.g. via an HTTP/3-capable client). Scope: runtime dependency (not dev-only) assumed pending verification. Remediation approach: bump the direct dependency (e.g. `quinn`) first; fall back to `cargo update -p quinn-proto --precise 0.11.14`.

## Step 2.5 – Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | not available (no branch HEAD data) | Unknown – last tag `v0.3.12` ships 0.11.9 |
| 2.2.x | Cargo | release/0.4.z | not available (no branch HEAD data) | Fix already released in tags `v0.4.11`/`v0.4.12` (0.11.14) |

Remediation path implications:
- 2.2.x: fix already shipped in RHTPA 2.2.3 (and 2.2.4); no new code change needed for the stream – current release is not vulnerable.
- 2.1.x: no evidence of a fix on `release/0.3.z` -> upstream backport (bump quinn-proto to >= 0.11.14) + downstream propagation in rhtpa-release.0.3.z.
