# TC-8001 — Step 2 Version Impact Analysis

All lock-file values come from the "Mock Lock File Data" section of
`security-matrix-mock.md`. That section is the simulated output of
`git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`. No real git commands were run.

## 2.1 Supportability matrix (aggregated)

| Stream | Konflux release repo | Versions | Upstream branch (Cargo) |
|--------|----------------------|----------|-------------------------|
| 2.1.x | rhtpa-release.0.3.z | 2.1.0 (`v0.3.8`), 2.1.1 (`v0.3.12`) | `release/0.3.z` |
| 2.2.x | rhtpa-release.0.4.z | 2.2.0 (`v0.4.5`), 2.2.1 (`v0.4.8`), 2.2.2 (retag of 2.2.1, `v0.4.8`), 2.2.3 (`v0.4.11`), 2.2.4 (`v0.4.12`) | `release/0.4.z` |

Format validation: PASS. Both streams have Supportability Matrix, Source Pinning
Method, Ecosystem Mappings (with the expected columns) and Forward Pointer.

## 2.2 Development stream

Not determinable from the provided inputs. Finding it requires
`getJiraIssueTypeMetaWithFields` (unreleased `RHTPA` versions) and the branch HEAD
of the source repo, and neither is available in the mock data. **The development
stream is reported as NOT CHECKED.** The engineer must confirm it before Step 3 is
finalised.

## 2.3 / 2.4 Version impact table

```
Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Pinned tag | quinn-proto | Affected? | Notes                              |
|---------|--------|------------|-------------|-----------|------------------------------------|
| 2.1.0   | 2.1.x  | v0.3.8     | 0.11.9      | YES       | outside issue scope (cross-stream) |
| 2.1.1   | 2.1.x  | v0.3.12    | 0.11.9      | YES       | outside issue scope (cross-stream) |
| 2.2.0   | 2.2.x  | v0.4.5     | 0.11.9      | YES       | in scope                           |
| 2.2.1   | 2.2.x  | v0.4.8     | 0.11.12     | YES       | in scope                           |
| 2.2.2   | 2.2.x  | v0.4.8     | —           | YES       | same as 2.2.1 (backend retag)      |
| 2.2.3   | 2.2.x  | v0.4.11    | 0.11.14     | NO        | fixed version shipped              |
| 2.2.4   | 2.2.x  | v0.4.12    | 0.11.14     | NO        | fixed version shipped              |
| dev     | —      | HEAD       | not checked | UNKNOWN   | no unreleased-version data in eval |
```

Summary:
- **In scope (2.2.x):** 2.2.0, 2.2.1 and 2.2.2 are affected. 2.2.3 and 2.2.4 are not.
- **Cross-stream (2.1.x):** all released versions (2.1.0, 2.1.1) are affected.

## 2.3.5 Dependency chain context

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) → ? → quinn-proto
  Type: NOT DETERMINED. The mock provides only resolved Cargo.lock versions,
        not Cargo.toml manifests or the lock-file dependency graph.
        quinn-proto is usually pulled in transitively (e.g. via quinn / an
        HTTP/3-enabled client), but that is not confirmed by the evidence.
  Profile: NOT DETERMINED (no manifest evidence for dev/build-only scope).
  Present in: every version of both streams (2.1.0 onward).
  Fix introduced: between v0.4.8 (0.11.12) and v0.4.11 (0.11.14) on release/0.4.z.

Remediation: if direct, bump quinn-proto to >= 0.11.14. If transitive, bump the
direct dependency that pulls it in. If that is not viable, pin with
`cargo add quinn-proto@0.11.14`.
```

The engineer should confirm direct versus transitive with
`cargo tree -i quinn-proto` at the pinned tag before the tasks are created.

## 2.5 Upstream fix status

| Stream | Ecosystem | Upstream branch | Evidence | Fixed? |
|--------|-----------|-----------------|----------|--------|
| 2.1.x | Cargo | release/0.3.z | Latest released tag `v0.3.12` ships 0.11.9. Branch HEAD was not inspected (no git in eval). | NO (not shown to be fixed) |
| 2.2.x | Cargo | release/0.4.z | Released tags `v0.4.11` and `v0.4.12` ship 0.11.14. Branch HEAD was not inspected, but the fix is on the branch. | YES |

Implications for remediation:
- **2.1.x:** the fix is not on the upstream branch. Use the **upstream backport +
  downstream propagation** pair.
- **2.2.x:** the fix is already on `release/0.4.z` and is shipped in 2.2.3 and 2.2.4.
  The skill would select the **dependency bump + downstream propagation** variant.
  However, the current stream release already contains the fix, so the engineer
  may decide that no new 2.2.x code change is needed and that the affected 2.2.0
  to 2.2.2 users are fixed by upgrading to 2.2.4. See `remediation.md`.

## Step 3 preview – Affects Versions correction (planned, needs confirmation)

| | Value |
|---|---|
| Current (PSIRT) | RHTPA 2.0.0 |
| Proposed (scoped to 2.2.x) | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |
| Rationale | No 2.0.x stream is configured, and lock-file evidence shows quinn-proto < 0.11.14 only in 2.2.0 to 2.2.2 within the issue's stream. Version IDs would be looked up at run time via `getJiraIssueTypeMetaWithFields`. The correction comment includes the Comment Footnote (`sdlc-workflow/triage-security v0.14.0`). |

## Steps 4–7 (not runnable in this eval)

- **Step 4:** a JQL sibling search for `labels = CVE-2026-31812` was not run. For this
  analysis I assume no sibling CVE Jira exists for 2.1.x, so Case A
  preemptive tasks are planned for 2.1.x. Step 4.3 is skipped because the Upstream
  Affected Component field is not configured.
- **Step 5:** lifecycle was not checked (no access to the product pages URL).
  2.1.x and 2.2.x are assumed to be supported.
- **Step 6:** no resolved siblings are known.
- **Step 7:** skipped because the Upstream Affected Component field is not configured.
