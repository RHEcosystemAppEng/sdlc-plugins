# Step 2 – Version Impact Analysis: CVE-2026-48901 (h2 < 0.4.8)

Fix threshold used: **affected < 0.4.8, fixed 0.4.8**. This is the enriched, cross-validated value from Step 1.5 (MITRE `lessThan: 0.4.8` + OSV `fixed: 0.4.8`). The imprecise Jira prose ("versions prior to the fix") was not used.

Dependency versions come from the fixture's "h2 versions by tag" mock table. It simulates `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'` at each pinned backend tag from the supportability matrix.

## 2.1 – Supportability Matrix (aggregated, all streams)

- Stream 2.1.x (rhtpa-release.0.3.z): 2.1.0 (backend v0.3.8), 2.1.1 (backend v0.3.12)
- Stream 2.2.x (rhtpa-release.0.4.z): 2.2.0 (v0.4.5), 2.2.1 (v0.4.8), 2.2.2 (v0.4.8, retag of 2.2.1), 2.2.3 (v0.4.11), 2.2.4 (v0.4.12)
- Format validation: required sections present (Supportability Matrix, Source Pinning Method, Ecosystem Mappings, Forward Pointer). Ecosystem Mappings columns match the template. Result: Pass.
- Staleness: Last-Updated 2026-06-28 (152 days). The user chose to proceed (see data-extraction.md).

## 2.2 – Development Stream

Development stream detection needs unreleased RHTPA versions from `getJiraIssueTypeMetaWithFields`. The skill did not call Jira in this eval, and the fixture has no unreleased-version or branch-HEAD lock data. **The development stream cannot be determined from the provided evidence.** It is reported as a gap and not assumed. In a live run, check the dev stream's source repo at branch HEAD.

## 2.4 – Version Impact Table

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

| Version | Stream | Backend tag | h2 | Affected? | Notes |
|---------|--------|-------------|-----|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | **YES** | Out of issue scope (cross-stream) |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | **YES** | Out of issue scope (cross-stream) |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | 0.4.8 = fixed version (lessThan is exclusive) |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | 0.4.8 = fixed version |
| 2.2.2 | 2.2.x | v0.4.8 | — | NO | same as 2.2.1 (backend retag of 2.2.1; lock check skipped) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | |
| dev | — | branch HEAD | unknown | UNKNOWN | No Jira unreleased-version data or HEAD lock evidence in fixture |

### Summary

- **In-scope stream 2.2.x: NOT affected.** Every 2.2.x release ships h2 >= 0.4.8.
- **Out-of-scope stream 2.1.x: AFFECTED.** 2.1.0 and 2.1.1 ship h2 0.4.5.
- The PSIRT-assigned Affects Version **RHTPA 2.2.0 is incorrect**. 2.2.0 (build 0.4.5, backend v0.4.5) ships h2 0.4.8, which is exactly the fixed version. Note the version-number trap: the *backend tag* v0.4.5 is not the h2 version. The h2 version at that tag is 0.4.8.
- If the Jira text's imprecise range had been read loosely (for example, "everything up to and including 0.4.8"), 2.2.0 to 2.2.2 would have been wrongly marked affected. The exclusive `lessThan 0.4.8` from MITRE/OSV prevents that.

## 2.3.5 – Dependency Chain Context (affected versions: 2.1.0, 2.1.1)

```
Dependency chain for h2 (Cargo):
  backend (workspace) → ? → h2 0.4.5
  Type: UNDETERMINED — the fixture provides only Cargo.lock version lines, not
        Cargo.toml manifests or lock-file dependency graphs. h2 is commonly
        pulled in transitively (e.g. via hyper / reqwest / tonic), but this is
        NOT asserted without evidence.
  Profile: UNDETERMINED (assume production until manifest evidence shows
        dev/build-only scope)
  Present in: all 2.1.x and 2.2.x versions (0.4.5 in 2.1.x, 0.4.8+ in 2.2.x)

Remediation: if direct → bump h2 to >= 0.4.8 in Cargo.toml/Cargo.lock;
if transitive → bump the direct dependency that pulls in h2, fall back to
`cargo add h2@0.4.8` pin.
```

Action for a live run: `git show v0.3.12:Cargo.lock` (dependents of h2) and `git show v0.3.12:Cargo.toml` to classify direct vs transitive and the profile.

## 2.5 – Upstream Fix Status (affected streams)

| Stream | Ecosystem | Repository | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|------------|-----------------|-----------------|--------|
| 2.1.x | Cargo | backend | release/0.3.z | unknown (no HEAD lock data in fixture) | UNKNOWN |

The fixture has no `release/0.3.z` HEAD evidence, so the skill cannot confirm a fix is already on the branch. Remediation for 2.1.x therefore uses the **upstream backport + downstream propagation** variant, not the dependency-bump variant. Live check: `git -C /home/dev/repos/rhtpa-backend show release/0.3.z:Cargo.lock | grep -A2 'name = "h2"'`. If that shows h2 >= 0.4.8, switch the upstream task to the dependency-bump template.

(2.2.x is not affected, so no upstream check is needed. Its release/0.4.z branch already ships h2 >= 0.4.8 at every released tag.)

## Step 3 – Affects Versions Correction (proposed, requires confirmation)

| | Value |
|---|---|
| Current Affects Versions | RHTPA 2.2.0 |
| Evidence-based affected versions in scope (2.2.x) | none |
| Proposed correction | Remove RHTPA 2.2.0. No 2.2.x version is affected. The issue goes to Case C closure, so it is not re-pointed to a 2.1.x version (out of scope, tracked via cross-stream handling). |
