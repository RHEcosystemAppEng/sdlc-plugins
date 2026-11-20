# TC-8001 — Version Impact Analysis (Step 2)

> **Simulation notice:** No `git show` command was run. Dependency versions come from the
> "Mock Lock File Data" section of `security-matrix-mock.md`, which stands in for the output of
> `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'` at each pinned tag.

## 2.1 — Supportability matrix (aggregated)

The Version Streams table lists two streams: 2.1.x (`rhtpa-release.0.3.z`) and 2.2.x
(`rhtpa-release.0.4.z`). Both matrix sections contain Supportability Matrix, Source Pinning
Method, Ecosystem Mappings (with the expected `Ecosystem | Repository | Lock File | Check
Command | Upstream Branch` columns), and Forward Pointer. Format validation passes. Staleness
warning: see data-extraction.md. The matrix is 145 days old.

## 2.2 — Development stream

Jira version metadata (`getJiraIssueTypeMetaWithFields`, unreleased `RHTPA` versions) was
**not available** in this eval, so no development stream could be identified. No branch-HEAD
row is shown. The skill forbids inventing one. In a live run, an unreleased version (for
example RHTPA 2.2.5 or 3.0) would add a dev row checked at branch HEAD.

## 2.3 / 2.4 — Version impact table

**Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):**

| Version | Stream | Build | backend tag (pinned) | quinn-proto | Affected? | Notes |
|---------|--------|-------|----------------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.3.8 | `v0.3.8` | 0.11.9 | **YES** | outside issue scope (2.1.x) |
| 2.1.1 | 2.1.x | 0.3.12 | `v0.3.12` | 0.11.9 | **YES** | outside issue scope (2.1.x) |
| 2.2.0 | 2.2.x | 0.4.5 | `v0.4.5` | 0.11.9 | **YES** | in scope |
| 2.2.1 | 2.2.x | 0.4.8 | `v0.4.8` | 0.11.12 | **YES** | in scope |
| 2.2.2 | 2.2.x | 0.4.9 | `v0.4.8` | — | **YES** | same as 2.2.1 (backend retag of 2.2.1; lock check skipped, result carried forward) |
| 2.2.3 | 2.2.x | 0.4.11 | `v0.4.11` | 0.11.14 | NO | ships the fixed version |
| 2.2.4 | 2.2.x | 0.4.12 | `v0.4.12` | 0.11.14 | NO | ships the fixed version |
| (dev) | — | — | branch HEAD | n/a | n/a | development stream not determinable (no Jira version data) |

Summary:
- **2.2.x (issue scope):** 2.2.0, 2.2.1, 2.2.2 are affected. 2.2.3 and 2.2.4 are **not** affected. quinn-proto was bumped to 0.11.14 between backend `v0.4.8` and `v0.4.11`, so the fix first shipped in **RHTPA 2.2.3**.
- **2.1.x (other stream):** every released version (2.1.0, 2.1.1) is affected, including the latest, so **2.1.x is still unremediated**. This triggers Case A (cross-stream impact).
- PSIRT's "RHTPA 2.0.0" does not match any version in the supportability matrix.

## 2.3.5 — Dependency chain context

The fixture provides Cargo.lock version lines only. It has no `Cargo.toml` manifests and no
reverse-dependency data, so the chain **could not be determined** from evidence and is not
guessed. quinn-proto is usually pulled in transitively (for example via `quinn`, often through
`reqwest`'s `http3` feature or `h3-quinn`), but this is unverified. In a live run, inspect
`git show v0.3.12:Cargo.toml`, the workspace member manifests, and `Cargo.lock` dependents
of `quinn-proto` to get:

```
Dependency chain for quinn-proto:
  backend (workspace) → ? → quinn → quinn-proto   (UNVERIFIED — to be traced)
  Type: unknown (likely transitive)
  Profile: unknown (assumed production until shown otherwise; it is a QUIC network stack)
```

The quinn-proto version is the same across 2.1.0, 2.1.1 and 2.2.0 (0.11.9). It moves to
0.11.12 in 2.2.1 and to 0.11.14 in 2.2.3. The remediation tasks therefore include both the
direct-bump and the transitive two-tier approaches. The implementer confirms which applies.

## 2.5 — Upstream fix status

The fixture does not include lock-file output for upstream branch HEADs. The best available
evidence is the latest released tag cut from each branch:

| Stream | Ecosystem | Upstream Branch | Latest released tag | quinn-proto at that tag | Fixed upstream? |
|--------|-----------|-----------------|---------------------|-------------------------|-----------------|
| 2.1.x | Cargo | `release/0.3.z` | `v0.3.12` | 0.11.9 | **NO (presumed)**. No evidence of a fix on this branch. HEAD needs confirming with `git -C /home/dev/repos/rhtpa-backend show release/0.3.z:Cargo.lock`. |
| 2.2.x | Cargo | `release/0.4.z` | `v0.4.12` | 0.11.14 | **YES**. `v0.4.11` and `v0.4.12` already ship 0.11.14. HEAD should be confirmed to still be ≥ 0.11.14. |

Remediation path implied:
- **2.1.x:** fix not available upstream, so **upstream backport + downstream propagation** (2 tasks).
- **2.2.x:** fix already upstream and already shipped since 2.2.3. If tasks are created, use the **dependency bump + downstream propagation** variant (see remediation.md for the recommendation and caveat).

**Engineer review gate:** a live run waits here for the engineer to confirm this table before Step 3.
