# TC-8001 — Step 2 Version Impact Analysis

## 2.1 – Supportability matrix (aggregated)

Both streams were loaded from `security-matrix-mock.md`. All required sections are present: Supportability Matrix, Source Pinning Method, Ecosystem Mappings and Forward Pointer. Ecosystem Mappings columns match the template, so format validation passes.

| Stream | Konflux repo | Versions | Cargo upstream branch |
|---|---|---|---|
| 2.1.x | rhtpa-release.0.3.z | 2.1.0, 2.1.1 | release/0.3.z |
| 2.2.x | rhtpa-release.0.4.z | 2.2.0, 2.2.1, 2.2.2 (retag of 2.2.1), 2.2.3, 2.2.4 | release/0.4.z |

## 2.2 – Development stream

Finding the development stream needs a Jira `getJiraIssueTypeMetaWithFields` call to list unreleased RHTPA versions. Jira was not available in this eval, so **no development stream was identified** and no branch-HEAD row is included. In a live run, the engineer would be asked to confirm this gap.

## 2.3 – Dependency versions

Simulated output of `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`, taken from the matrix mock data. Fix threshold: affected below 0.11.14, fixed at 0.11.14 (Jira description; external sources unavailable).

## 2.4 – Version impact table

```
Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):
```

| Version | Stream | backend tag | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | **YES** | outside issue scope (cross-stream) |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | **YES** | outside issue scope (cross-stream) |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | **YES** | in scope |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | **YES** | in scope |
| 2.2.2 | 2.2.x | v0.4.8 | — | **YES** | same as 2.2.1 (backend retag; lock-file check skipped) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | fixed version shipped |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | fixed version shipped |
| dev | — | branch HEAD | not determined | — | development stream unknown (Jira unavailable) |

Summary:
- **In scope (2.2.x):** 2.2.0, 2.2.1 and 2.2.2 are affected. The fix first shipped in **2.2.3** (backend v0.4.11).
- **Cross-stream (2.1.x):** 2.1.0 and 2.1.1 are affected and no release in that stream has the fix.
- PSIRT's Affects Versions value, **RHTPA 2.0.0**, is wrong. That version is not in the supportability matrix and no lock-file evidence covers it.

### 2.3.5 – Dependency chain context

```
Dependency chain for quinn-proto:
  backend (workspace) → ... → quinn-proto
  Type: NOT DETERMINED. Cargo.toml / full Cargo.lock dependency graph not
        available in this eval (only resolved versions were provided).
        quinn-proto is normally pulled in transitively via `quinn`
        (e.g. through reqwest/http3 or a direct quinn dependency). Confirm
        with `cargo tree -i quinn-proto` at each pinned tag.
  Profile: assumed production (no evidence of dev-/build-only scope).
  Present in: all supported versions (2.1.0 onward).
```

Remediation therefore documents both the direct and the transitive approach (bump the direct parent, usually `quinn`, then fall back to `cargo add quinn-proto@0.11.14`).

## 2.5 – Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | ≥ 0.11.14 (inferred: released tags v0.4.11 and v0.4.12 on this line ship 0.11.14) | YES (branch HEAD not read directly) |
| 2.1.x | Cargo | release/0.3.z | not read (no `git show` in eval). Latest released tag v0.3.12 ships 0.11.9 | NOT CONFIRMED, treated as not fixed |

Remediation path per stream:
- **2.2.x:** already fixed upstream and shipped in 2.2.3 and 2.2.4. No new code change is needed in the supported stream. The fix for the affected 2.2.0–2.2.2 builds is to upgrade to 2.2.3 or later.
- **2.1.x:** not fixed. Needs an upstream PR on release/0.3.z, then a Konflux release repo update in rhtpa-release.0.3.z.

## Step 3 – Affects Versions correction (proposed)

Issue scope is 2.2.x, so the correction is limited to that stream.

| | Versions |
|---|---|
| Current | RHTPA 2.0.0 |
| Proposed | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |
| Remove | RHTPA 2.0.0 (not a supported version; no evidence) |

Version IDs would be discovered dynamically through `getJiraIssueTypeMetaWithFields`. The change needs engineer confirmation, and the correction comment includes the Comment Footnote.

Engineer confirmation of the version impact table (simulated): **confirmed**.
