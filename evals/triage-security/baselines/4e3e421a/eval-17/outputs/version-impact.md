# Step 2 – Version Impact Analysis: CVE-2026-31812 (quinn-proto < 0.11.14)

## 2.1 Supportability matrix

Loaded from `security-matrix-mock.md`, which has two streams: 2.1.x (rhtpa-release.0.3.z) and 2.2.x (rhtpa-release.0.4.z). The format check passed: Supportability Matrix, Ecosystem Mappings, Source Pinning Method and Forward Pointer are all present, and the Ecosystem Mappings columns match the template. There is a staleness warning from Step 0.3 (last updated 2026-06-28, 128 days ago).

## 2.2 Development stream

Finding the development stream requires Jira unreleased-version metadata (`getJiraIssueTypeMetaWithFields`), which was not queried in this eval. Neither the provided matrix nor the configuration names a development stream or branch. **The development stream is not assessed.** In a real run, the engineer must confirm it or provide the lookup. No version is assumed.

## 2.3 Dependency versions (simulated `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`)

Pinned tags come from the matrix `backend` column. Lock data comes from the mock lock-file section.

## 2.4 Version Impact Table

```
Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):
```

| Stream | Version | Backend tag (pinned) | quinn-proto | Affected? | Notes |
|--------|---------|----------------------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | `v0.3.8` | 0.11.9 | **YES** | outside issue scope (cross-stream) |
| 2.1.x | 2.1.1 | `v0.3.12` | 0.11.9 | **YES** | outside issue scope (cross-stream) |
| 2.2.x | 2.2.0 | `v0.4.5` | 0.11.9 | **YES** | in scope |
| 2.2.x | 2.2.1 | `v0.4.8` | 0.11.12 | **YES** | in scope |
| 2.2.x | 2.2.2 | `v0.4.8` | — | **YES** | in scope; backend retag of 2.2.1, same as 2.2.1 (lock check skipped) |
| 2.2.x | 2.2.3 | `v0.4.11` | 0.11.14 | NO | fixed version shipped |
| 2.2.x | 2.2.4 | `v0.4.12` | 0.11.14 | NO | fixed version shipped |
| dev | — | branch HEAD | not checked | UNKNOWN | development stream not found (no Jira metadata) |

Summary:
- **In scope (2.2.x):** 2.2.0, 2.2.1 and 2.2.2 are affected. 2.2.3 and later ship quinn-proto 0.11.14 and are not affected.
- **Out of scope (2.1.x):** both 2.1.0 and 2.1.1 are affected (quinn-proto 0.11.9). This triggers Case A, cross-stream impact.

## 2.3.5 Dependency chain context

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) → ... → quinn-proto
  Type: NOT DETERMINED. The provided evidence has only Cargo.lock version data,
        with no Cargo.toml or lock dependency edges, so direct vs. transitive
        cannot be confirmed. quinn-proto is usually pulled in transitively through
        `quinn` (for example via reqwest's http3 feature). Confirm with
        `git show <tag>:Cargo.lock` dependency edges and `cargo tree -i quinn-proto`.
  Profile: assumed production. It is present in every shipped tag's Cargo.lock,
           and no dev-dependency evidence was found. Confirm before task creation.
  Introduction point: present in all released tags, from v0.3.8 through v0.4.12.
  Fix point: bumped to 0.11.14 between v0.4.8 (2.2.1/2.2.2) and v0.4.11 (2.2.3).
```

## 2.5 Upstream fix status

| Stream | Ecosystem | Repository | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|------------|-----------------|-----------------|--------|
| 2.2.x | Cargo | backend | `release/0.4.z` | not read (no HEAD data). Released tags v0.4.11 and v0.4.12 on this line already ship 0.11.14 | YES (inferred from released tags; HEAD must be confirmed) |
| 2.1.x | Cargo | backend | `release/0.3.z` | not read (no HEAD data). Latest released tag v0.3.12 ships 0.11.9 | NO evidence of a fix, so treat as **not fixed** |

Remediation path:
- **2.2.x:** the fix has already shipped in 2.2.3 (`v0.4.11`) and 2.2.4 (`v0.4.12`). No new code change is needed on `release/0.4.z`. The current 2.2.x release is not vulnerable.
- **2.1.x:** an upstream backport is needed on `release/0.3.z` (bump quinn-proto to >= 0.11.14), followed by a Konflux propagation in rhtpa-release.0.3.z.

## Step 3 – Affects Versions Correction (proposed, requires confirmation)

| | Value |
|--|--|
| Current (PSIRT) | RHTPA 2.0.0 |
| Proposed (scoped to 2.2.x, lock-file evidence) | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |
| Removed | RHTPA 2.0.0. There is no 2.0.x stream in the supportability matrix, and it is outside the `[rhtpa-2.2]` scope |
| Not added | RHTPA 2.2.3 and 2.2.4 (they ship 0.11.14), and RHTPA 2.1.0 and 2.1.1 (out of scope; covered by a cross-stream notice) |

Jira version IDs would be found dynamically through `getJiraIssueTypeMetaWithFields`. No IDs are hard-coded.

## Steps 4–7 (not executable in eval)

- Step 4: no sibling JQL was run, so we cannot tell whether a 2.1.x CVE Jira exists. For this eval we assume none exists, which makes 2.1.x tasks preemptive. Step 4.3 is skipped because Upstream Affected Component is not configured.
- Step 5: the lifecycle page was not queried. 2.1.x and 2.2.x are treated as supported because they are in the matrix.
- Step 6: no resolved siblings are known, so the issue is not already fixed.
- Step 7: skipped because Upstream Affected Component is not configured.
- Step 7.5: release Epic/Task lookup was not performed. Release linking is listed in remediation.md as pending.
