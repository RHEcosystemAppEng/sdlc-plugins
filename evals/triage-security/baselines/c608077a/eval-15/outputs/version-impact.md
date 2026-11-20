# Step 2 – Version Impact Analysis: CVE-2026-31812

Sources: the supportability matrices for streams 2.1.x (`rhtpa-release.0.3.z`) and 2.2.x
(`rhtpa-release.0.4.z`), with simulated `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
output taken from the mock lock-file data. All supported versions were checked, including the
out-of-scope stream.

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Stream | Version | Backend tag (pinned) | quinn-proto | Affected? | Notes |
|--------|---------|----------------------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | `v0.3.8` | 0.11.9 | YES | out of issue scope (cross-stream) |
| 2.1.x | 2.1.1 | `v0.3.12` | 0.11.9 | YES | out of issue scope (cross-stream) |
| 2.2.x | 2.2.0 | `v0.4.5` | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | `v0.4.8` | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | `v0.4.8` | — | YES | same as 2.2.1 (backend retag of 2.2.1; lock check skipped, result carried forward) |
| 2.2.x | 2.2.3 | `v0.4.11` | 0.11.14 | NO | fixed version shipped |
| 2.2.x | 2.2.4 | `v0.4.12` | 0.11.14 | NO | |
| dev | — | branch HEAD | not determined | not determined | see Step 2.2 note |

**In-scope (2.2.x) affected versions:** 2.2.0, 2.2.1, 2.2.2
**Out-of-scope affected versions:** 2.1.0, 2.1.1 (stream 2.1.x)
**Not affected:** 2.2.3, 2.2.4

## Step 2.2 – Development stream

Finding the development stream requires unreleased `RHTPA` Jira versions (from
`getJiraIssueTypeMetaWithFields`), and that call was not made. 2.2.x is the latest stream in the
matrix (no forward pointer), and no HEAD lock-file data is available. The development-stream result
is left as **not determined** rather than guessed. The engineer should confirm it before Step 3 is finalized.

## Step 2.3.5 – Dependency chain context

The mock data has no dependency-tree (`cargo tree`) output, so I could not confirm whether
quinn-proto is a direct or transitive dependency of `backend`. quinn-proto is normally pulled in
transitively through `quinn` (QUIC, which reqwest/h3 use). Treat it as **likely transitive
(backend -> ... -> quinn -> quinn-proto), to be confirmed**. Recommended remediation order:
1. Bump the direct dependency (`quinn` or whichever crate depends on it).
2. If that is not possible, use `cargo update -p quinn-proto --precise 0.11.14`, since 0.11.14 is
   semver-compatible with 0.11.x.

Scope: runtime (not dev-only/build-only), so the normal priority rules apply.

## Step 2.5 – Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | not inspected (no data) | UNKNOWN — the latest release tag `v0.3.12` still ships 0.11.9 |
| 2.2.x | Cargo | `release/0.4.z` | not inspected (no data) | Very likely YES: tags `v0.4.11` and `v0.4.12`, cut from this branch, already ship 0.11.14. Branch HEAD itself was not checked |

## Interpretation

- **2.2.x (in scope):** the fix was already delivered in 2.2.3 (`v0.4.11`, 2026-03-23) and carried
  into 2.2.4. Only the older z-stream releases 2.2.0–2.2.2 are affected.
- **2.1.x (out of scope):** both supported releases ship quinn-proto 0.11.9, and there is no
  evidence of a fix on `release/0.3.z`. This triggers Case A, cross-stream impact.
