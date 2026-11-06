# TC-8001 — Version Impact Analysis (Step 2)

> **Simulation notice:** Dependency versions come from the "Mock Lock File Data" in
> `security-matrix-mock.md`, which stands in for
> `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`. No real `git show` ran.

## 2.1 Supportability matrix (both configured streams)

The matrix files are complete. Both streams have a Supportability Matrix, Ecosystem
Mappings, Source Pinning Method and Forward Pointer section. Format validation passes.
Staleness warning: 131 days old (see data-extraction.md).

## 2.2 Development stream

- No Jira version metadata (`getJiraIssueTypeMetaWithFields`, unreleased `RHTPA`
  versions) is available in this eval, so the development stream **could not be
  identified**.
- 2.2.x is the latest configured stream, and its forward pointer says there is no
  newer stream.
- A real run must check the development branch HEAD before final sign-off.

## 2.3 / 2.4 Version impact table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Build | backend pinned tag | quinn-proto | Affected? | Notes |
|--------|---------|-------|--------------------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | 0.3.8 | `v0.3.8` | 0.11.9 | **YES** | Outside this issue's scope |
| 2.1.x | 2.1.1 | 0.3.12 | `v0.3.12` | 0.11.9 | **YES** | Outside this issue's scope |
| 2.2.x | 2.2.0 | 0.4.5 | `v0.4.5` | 0.11.9 | **YES** | |
| 2.2.x | 2.2.1 | 0.4.8 | `v0.4.8` | 0.11.12 | **YES** | |
| 2.2.x | 2.2.2 | 0.4.9 | `v0.4.8` | — | **YES** | Same as 2.2.1 (backend retag of 2.2.1, lock check skipped) |
| 2.2.x | 2.2.3 | 0.4.11 | `v0.4.11` | 0.11.14 | NO | Fixed version shipped |
| 2.2.x | 2.2.4 | 0.4.12 | `v0.4.12` | 0.11.14 | NO | Fixed version shipped |
| dev | — | — | branch HEAD | not determined | not determined | No unreleased Jira version data |

**Summary**

- Affected: 2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2.
- Not affected: 2.2.3, 2.2.4.
- In this issue's scope (2.2.x): **2.2.0, 2.2.1 and 2.2.2 are affected**. The fix
  first shipped in **2.2.3** (backend `v0.4.11`).
- Outside scope (2.1.x): **both supported versions are affected** (0.11.9). The fix
  has never shipped in this stream.
- The PSIRT-claimed version, RHTPA 2.0.0, is not in any supportability matrix. No
  2.0.x stream is configured.

## 2.3.5 Dependency chain context

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) → ... → quinn-proto
  Type: NOT DETERMINED. The mock gives only the resolved version from Cargo.lock,
        not the dependency graph or Cargo.toml manifests. quinn-proto is usually
        pulled in transitively (for example via quinn / an HTTP/3 or QUIC client),
        but this is not verified and is not asserted.
  Profile: NOT DETERMINED. No evidence that it is dev- or build-only, so it is
           treated as a production dependency (no `dev-dependency` label, no
           priority override).
  Introduction point: present in every inspected tag (v0.3.8 through v0.4.12).
                      0.11.9 → 0.11.12 at v0.4.8 → 0.11.14 at v0.4.11.
```

Remediation tasks therefore include both the direct-bump approach and the transitive
two-tier approach. The implementer confirms which one applies with `cargo tree -i quinn-proto`.

## 2.5 Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | not observed (latest tag `v0.3.12` = 0.11.9) | **NO** (no evidence of a fix) |
| 2.2.x | Cargo | `release/0.4.z` | not observed directly. Tags `v0.4.11` and `v0.4.12` = 0.11.14 | **YES** (inferred from released tags on this branch) |

What this means for remediation:

- **2.2.x**: the fix is already upstream, and the Konflux release repo already pins
  `v0.4.12` (0.11.14), which shipped in RHTPA 2.2.4. No source change or reference
  bump is needed for the current 2.2.x release line.
- **2.1.x**: upstream is not fixed. An upstream PR on `release/0.3.z` is needed,
  followed by a Konflux reference update in `rhtpa-release.0.3.z`. If a real
  `git show release/0.3.z:Cargo.lock` shows 0.11.14 or later, use the dependency-bump
  variant instead.

**Engineer review gate:** the table above must be confirmed before Step 3.
