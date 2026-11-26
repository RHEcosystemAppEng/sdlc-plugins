# Step 2 – Version Impact Analysis: CVE-2026-48901 (h2 < 0.4.8)

## 2.1 Supportability matrix (aggregated)

Both streams loaded from `security-matrix-mock.md`. Format is valid: Supportability
Matrix, Ecosystem Mappings, Source Pinning Method, and Forward Pointer are all present.
The staleness warning from Step 0.3 still applies: last updated 2026-06-28, 151 days ago.

## 2.2 Development stream

Jira unreleased-version metadata (`getJiraIssueTypeMetaWithFields`) is not
available in this eval and was not queried. No development-stream HEAD lock file
data is in the fixture. **The development stream could not be identified or
checked.** It is listed below as not determined rather than assumed.

## 2.3 Dependency versions (lock file: `Cargo.lock`, check command `git show <tag>:Cargo.lock`)

Simulated `git show` output comes from the fixture's "h2 versions by tag" table.
Comparisons use the **enriched threshold from Step 1.5 (fixed in 0.4.8)**, not
the imprecise Jira prose.

## 2.4 Version impact table

Version Impact for CVE-2026-48901 (h2 < 0.4.8, fixed 0.4.8):

| Stream | Version | backend tag | h2 | Affected? | Notes |
|--------|---------|-------------|----|-----------|-------|
| 2.1.x | 2.1.0 | `v0.3.8` | 0.4.5 | **YES** | 0.4.5 < 0.4.8. Outside issue scope |
| 2.1.x | 2.1.1 | `v0.3.12` | 0.4.5 | **YES** | 0.4.5 < 0.4.8. Outside issue scope |
| 2.2.x | 2.2.0 | `v0.4.5` | 0.4.8 | NO | 0.4.8 is the fixed version |
| 2.2.x | 2.2.1 | `v0.4.8` | 0.4.8 | NO | 0.4.8 is the fixed version |
| 2.2.x | 2.2.2 | `v0.4.8` | — | NO | same as 2.2.1 (backend retag of 2.2.1) |
| 2.2.x | 2.2.3 | `v0.4.11` | 0.4.9 | NO | |
| 2.2.x | 2.2.4 | `v0.4.12` | 0.4.9 | NO | |
| dev | — | branch HEAD | not determined | not determined | No Jira unreleased-version data or HEAD lock file in fixture |

### Summary

- **Issue scope (2.2.x): NOT affected.** Every released 2.2.x version ships h2 >= 0.4.8.
- **Out-of-scope stream 2.1.x: AFFECTED.** 2.1.0 and 2.1.1 both ship h2 0.4.5.
- The PSIRT-assigned Affects Version **RHTPA 2.2.0 is incorrect**. 2.2.0 ships
  h2 0.4.8, which is the fixed release.

## 2.3.5 Dependency chain context (affected versions: 2.1.0, 2.1.1)

```
Dependency chain for h2:
  backend (workspace) → ... → h2 0.4.5
  Type: not determined from available evidence
  Profile: not determined from available evidence
```

The fixture provides only the resolved h2 version per tag, not `Cargo.toml`
manifests or the `Cargo.lock` dependents graph. In a real triage, inspect
`git show v0.3.12:Cargo.lock` / `Cargo.toml` to confirm whether h2 is direct or
transitive (h2 usually enters through `hyper` / `reqwest`, but that is not verified here
and is not asserted) and whether it is a production dependency.

Introduction point: the 2.1.x to 2.2.x transition (`v0.3.12` to `v0.4.5`) bumped
h2 from 0.4.5 to 0.4.8, which removed the vulnerability from 2.2.x.

## 2.5 Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | not available (no fixture data) | unknown |
| 2.2.x | Cargo | `release/0.4.z` | not checked (stream not affected; latest released tag `v0.4.12` ships 0.4.9) | n/a |

The 2.1.x upstream fix is not confirmed. Remediation uses the upstream backport
variant. If a `git show release/0.3.z:Cargo.lock` check shows h2 >= 0.4.8, switch
to the dependency bump variant.

## Steps 3–6 outcomes (from the impact table)

- **Step 3 – Affects Versions correction (proposed, requires confirmation):**
  remove `RHTPA 2.2.0`. No 2.2.x version is affected. Because the issue is scoped
  to 2.2.x, 2.1.x versions are not added to this issue (cross-stream impact goes
  in a comment instead).
- **Step 4 – Duplicates/siblings:** JQL not run (eval). The fixture shows no
  sibling issues, so this eval assumes no 2.1.x CVE Jira exists for CVE-2026-48901.
- **Step 5 – Lifecycle:** product pages not queried (eval). 2.1.x support status
  is unverified and must be confirmed before preemptive tasks are created.
- **Step 6 – Already fixed:** no resolved siblings in fixture.
- **Steps 7 / 7.5:** Upstream Affected Component field not configured, so Step 7
  is skipped. No release Jira data is available, so release Epic/Task orchestration
  for 2.1.x is left to the engineer. Preemptive tasks are not linked to release
  Jira either way.
