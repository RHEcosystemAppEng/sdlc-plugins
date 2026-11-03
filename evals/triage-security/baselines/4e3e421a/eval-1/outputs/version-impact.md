# TC-8001 — Version Impact Analysis (Step 2)

> Eval simulation: no `git show` was run. Dependency versions come from the
> "Mock Lock File Data" section of `security-matrix-mock.md`, which stands in for
> the output of `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'` at
> each pinned tag.

## 2.1 – Supportability matrix loaded

Both rows of the Version Streams table were enumerated directly, with no forward-pointer chaining:

| Stream | Konflux release repo | Released versions | Upstream branch (Cargo) |
|--------|----------------------|-------------------|-------------------------|
| 2.1.x | rhtpa-release.0.3.z | 2.1.0, 2.1.1 | `release/0.3.z` |
| 2.2.x | rhtpa-release.0.4.z | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | `release/0.4.z` |

Matrix format check (2.1.1) passed for both streams. The required sections (Supportability Matrix, Ecosystem Mappings, Source Pinning Method, Forward Pointer) are present, and the Ecosystem Mappings columns are `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`.

Staleness caveat from Step 0.3: the matrix is 128 days old. Releases after 2026-06-28 would not appear here.

## 2.2 – Development stream

This step needs `getJiraIssueTypeMetaWithFields` (unreleased `RHTPA` versions, earliest `releaseDate`). No Jira data is available in this eval and no development-head lock data was provided. The **development stream could not be determined**, and its branch HEAD has **not been assessed**. Nothing has been assumed about it. The engineer must supply it, or a live run must discover it, before Step 3 is finalized.

## 2.3 / 2.4 – Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Pinned backend tag (from matrix) | quinn-proto | Affected? | Notes |
|---------|--------|----------------------------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | **YES** | Outside issue scope (2.1.x) |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | **YES** | Outside issue scope (2.1.x) |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | **YES** | |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | **YES** | |
| 2.2.2 | 2.2.x | `v0.4.8` (retag) | — | **YES** | Same as 2.2.1. Backend retag of 2.2.1 (build 0.4.9 reuses backend `v0.4.8`), so the lock check was skipped and the result carried forward |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | Ships fixed version |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | Ships fixed version |
| dev (unknown) | — | branch HEAD | not assessed | UNKNOWN | Development stream not identifiable without Jira version metadata (see 2.2) |

All released versions use the **pinned tags from the supportability matrix**, never a branch HEAD (Rule 13). Every matrix row is included (Rule 4).

**Summary:**
- In issue scope (2.2.x): **2.2.0, 2.2.1, 2.2.2 affected**. 2.2.3 and 2.2.4 are not affected, because the fix entered with backend `v0.4.11`.
- Outside issue scope: **2.1.0 and 2.1.1 affected**. This triggers Case A (cross-stream impact) in Step 8.

### 2.3.5 – Dependency chain context

```
Dependency chain for quinn-proto:
  backend (rhtpa-backend workspace) → ... → quinn-proto
  Type: NOT DETERMINED. The mock supplies only the version line per tag, not
        Cargo.toml manifests or the full Cargo.lock dependency graph. quinn-proto
        is normally pulled in transitively via quinn (e.g. reqwest http3 /
        quinn → quinn-proto), but that has NOT been verified and is not asserted.
  Profile: not determined (no evidence of [dev-dependencies]/[build-dependencies]
        or feature gating), so it is treated as a production dependency. No
        dev-dependency label and no priority override.
  Introduction point: present in every released version of both streams
        (0.11.9 since 2.1.0). Bumped to 0.11.12 in v0.4.8 and to 0.11.14 in v0.4.11.

Remediation: if direct, bump quinn-proto to >= 0.11.14 in Cargo.lock. If
transitive, bump the direct dependency that pulls it in (preferred), else pin
with `cargo add quinn-proto@0.11.14` (fallback).
```

Action for the live run: confirm direct or transitive status with `git show v0.3.12:Cargo.lock` and `git show v0.4.8:Cargo.lock` (look for reverse dependencies of quinn-proto) and the workspace `Cargo.toml`.

## 2.5 – Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | not inspected (no mock data for branch HEAD) | UNKNOWN |
| 2.2.x | Cargo | `release/0.4.z` | not inspected (no mock data for branch HEAD) | UNKNOWN. Note that tags `v0.4.11` and `v0.4.12` cut from this line already ship 0.11.14, which strongly suggests the branch HEAD is fixed. This is unverified. |

Required check: `git -C /home/dev/repos/rhtpa-backend show release/0.4.z:Cargo.lock | grep -A2 'quinn-proto'` (and the same for `release/0.3.z`).

Effect on remediation:
- **Fixed upstream:** use the *dependency bump / reference bump* variant, plus downstream propagation.
- **Not fixed upstream:** use the *upstream backport* task, plus downstream propagation.

Both paths give 2 tasks per stream, with the downstream task blocked by the first. Because Step 2.5 could not be verified, `remediation.md` drafts the **upstream backport** template and notes where the dependency bump variant would replace it.

**Engineer review required:** confirm this table before Step 3.
