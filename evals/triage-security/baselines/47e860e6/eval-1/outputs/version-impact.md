# TC-8001 — Version Impact Analysis (Step 2)

> Evidence source: the mock supportability matrices and mock lock-file data in
> `security-matrix-mock.md`. That data simulates the output of
> `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`. No real `git show` was run.

## 2.1: Supportability matrix (aggregated)

Matrix format check: both streams contain Supportability Matrix, Ecosystem Mappings
(`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`), Source
Pinning Method, and Forward Pointer. **Pass.** (The staleness warning from Step 0.3 still applies.)

| Stream | Konflux repo | Versions |
|--------|--------------|----------|
| 2.1.x | rhtpa-release.0.3.z | 2.1.0, 2.1.1 |
| 2.2.x | rhtpa-release.0.4.z | 2.2.0, 2.2.1, 2.2.2 (retag), 2.2.3, 2.2.4 |

## 2.2: Development stream

No Jira version metadata (`getJiraIssueTypeMetaWithFields`) was available, so no
unreleased `RHTPA` version could be identified. **The development stream cannot be
determined from the available evidence and was not checked.** The engineer must
confirm whether an unreleased version and stream exist (for example a 2.3/3.0 line
at branch HEAD). If one exists, it must be checked before closing the analysis.

## 2.4: Version impact table

**Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):**

| Version | Stream | Build | backend tag (pinned) | quinn-proto | Affected? | Notes |
|---------|--------|-------|----------------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.3.8 | `v0.3.8` | 0.11.9 | **YES** | outside issue scope (cross-stream) |
| 2.1.1 | 2.1.x | 0.3.12 | `v0.3.12` | 0.11.9 | **YES** | outside issue scope (cross-stream) |
| 2.2.0 | 2.2.x | 0.4.5 | `v0.4.5` | 0.11.9 | **YES** | |
| 2.2.1 | 2.2.x | 0.4.8 | `v0.4.8` | 0.11.12 | **YES** | |
| 2.2.2 | 2.2.x | 0.4.9 | `v0.4.8` | — | **YES** | same as 2.2.1 (backend retag of 2.2.1; lock check skipped, result carried forward) |
| 2.2.3 | 2.2.x | 0.4.11 | `v0.4.11` | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.4.12 | `v0.4.12` | 0.11.14 | NO | ships fixed version |
| dev | — | — | branch HEAD | not determined | not determined | see 2.2 above |

**Summary**
- In scope (2.2.x): **2.2.0, 2.2.1, 2.2.2 affected**. 2.2.3 and 2.2.4 are not affected.
- Cross-stream (2.1.x): **2.1.0 and 2.1.1 affected**. Every released 2.1.x version ships 0.11.9.
- PSIRT's "RHTPA 2.0.0" is not in the supportability matrix. There is no 2.0.x stream.

## 2.3.5: Dependency chain context

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) → ... → quinn-proto
  Type: NOT DETERMINED. Cargo.toml / full Cargo.lock dependency graph is not in the
        available evidence. quinn-proto is usually pulled in transitively
        (e.g. via quinn ← reqwest/h3), but this has not been verified and is not assumed.
  Profile: NOT DETERMINED (must confirm it is a runtime dependency, not
           [dev-dependencies]/[build-dependencies]; if dev/build-only → add
           `dev-dependency` label and use Normal priority)
  Present in: every inspected tag (v0.3.8 through v0.4.12). No introduction point inside
              the supported range.
  Version history: 0.11.9 (2.1.0–2.2.0) → 0.11.12 (2.2.1/2.2.2) → 0.11.14 (2.2.3+)
```

Remediation path: if quinn-proto is direct, bump to >= 0.11.14. If transitive, bump the
direct dependency that pulls it in. As a fallback, pin `quinn-proto@0.11.14`.

## 2.5: Upstream fix status

Branch HEAD could not be read (no `git show` allowed). The table below infers status
from the pinned release tags cut from each upstream branch:

| Stream | Ecosystem | Upstream Branch | Latest evidence | Version | Fixed? |
|--------|-----------|-----------------|-----------------|---------|--------|
| 2.1.x | Cargo | `release/0.3.z` | tag `v0.3.12` (2.1.1) | 0.11.9 | **NO** (no evidence of fix on branch) |
| 2.2.x | Cargo | `release/0.4.z` | tags `v0.4.11`, `v0.4.12` (2.2.3, 2.2.4) | 0.11.14 | **YES** (fix already shipped from this branch) |

What this means for remediation:
- **2.1.x.** The fix is not available upstream. An **upstream backport** on
  `release/0.3.z` is needed first, followed by **downstream propagation** in
  rhtpa-release.0.3.z.
- **2.2.x.** The fix is already on `release/0.4.z`, and the latest 2.2.x release (2.2.4)
  already ships quinn-proto 0.11.14. The **dependency-bump variant** applies. Before
  creating tasks, the engineer should run
  `git -C /home/dev/repos/rhtpa-backend show release/0.4.z:Cargo.lock | grep -A2 'name = "quinn-proto"'`
  to confirm HEAD has not regressed.

**Waiting for engineer review and confirmation of this table before Step 3.**
