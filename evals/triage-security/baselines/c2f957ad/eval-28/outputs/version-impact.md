# TC-8060 — Step 2: Version Impact Analysis

Simulated. Lock file values come from the fixture mock data in place of `git show <tag>:Cargo.lock` output.

## 2.1 – Supportability Matrix (aggregated)

| Stream | Version | Build | backend tag | Notes |
|--------|---------|-------|-------------|-------|
| 2.1.x | 2.1.0 | 0.3.8 | `v0.3.8` | |
| 2.1.x | 2.1.1 | 0.3.12 | `v0.3.12` | |
| 2.2.x | 2.2.0 | 0.4.5 | `v0.4.5` | |
| 2.2.x | 2.2.1 | 0.4.8 | `v0.4.8` | |
| 2.2.x | 2.2.2 | 0.4.9 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.x | 2.2.3 | 0.4.11 | `v0.4.11` | |
| 2.2.x | 2.2.4 | 0.4.12 | `v0.4.12` | |

Matrix format validation (2.1.1): PASS for both streams. All required sections are present and the Ecosystem Mappings columns match the template.

## 2.2 – Development Stream

No unreleased Jira version data is available because Jira was not queried. 2.2.x is the latest configured stream and has no forward pointer, so no separate development stream was identified. In a live run, `getJiraIssueTypeMetaWithFields` would decide this. Any dev stream would be checked at branch HEAD.

## 2.3 – Version Impact Table

Version Impact for CVE-2026-99010 (h2 < 0.4.5), fix threshold 0.4.5 (Jira description; external enrichment unavailable):

| Version | Stream | backend tag | h2 | Affected? | Notes |
|---------|--------|-------------|----|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.4.5 | NO | Outside issue scope (matrix mock h2 table) |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.4.5 | NO | Outside issue scope (matrix mock h2 table) |
| **2.2.0** | 2.2.x | `v0.4.5` | **0.4.4** | **YES** | Transitive: backend → reqwest 0.12.5 → hyper 1.4.1 → h2 0.4.4 |
| **2.2.1** | 2.2.x | `v0.4.8` | **0.4.4** | **YES** | Transitive, same chain |
| **2.2.2** | 2.2.x | `v0.4.8` | — | **YES** | Retag: same as 2.2.1 (lock check skipped, result carried forward) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.4.5 | NO | At the fixed version |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.4.5 | NO | At the fixed version ("2.2.3+") |

**Summary for the in-scope stream (2.2.x):** 2.2.0, 2.2.1, and 2.2.2 are affected. 2.2.3 and 2.2.4 already ship h2 0.4.5 and are not affected.

**Cross-stream (2.1.x):** not affected according to the available lock data, so Case A (cross-stream comment and preemptive tasks) does not apply.

### Data provenance note: conflicting fixture data

The two fixtures disagree about h2 in the 2.2.x stream:
- The **issue fixture** (`vuln-issue-transitive.md`, "Lock file evidence") gives h2 **0.4.4** for 2.2.0–2.2.2 and **0.4.5** for 2.2.3+. Those tags are affected, then fixed.
- The **shared matrix fixture's** "h2 versions by tag" table gives `v0.4.5`/`v0.4.8` = 0.4.8 and `v0.4.11`/`v0.4.12` = 0.4.9. On that data every 2.2.x tag would be NOT affected.

The table above uses the issue fixture for 2.2.x. It is the CVE-specific simulated `Cargo.lock` output for this eval, and it agrees with the manifest and dependency chain evidence for the same tags. The matrix fixture's h2 table is used only for 2.1.x, which the issue fixture does not cover. In a live triage, this conflict would be resolved by re-running `git show <tag>:Cargo.lock` before confirming the table. The skill forbids assuming dependency versions.

## 2.3.5 – Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) → reqwest → hyper → h2
  Type: transitive (3 levels deep)
  Profile: production (reqwest is a runtime [dependencies] entry, not a dev/build dependency)

Resolved versions in affected lock files (2.2.0 – 2.2.2):
  reqwest 0.12.5 → hyper 1.4.1 → h2 0.4.4   (vulnerable)
Resolved version in fixed lock files (2.2.3+):
  h2 0.4.5                                   (fixed)

Manifest evidence (backend/Cargo.toml, all versions):
  [dependencies]
  reqwest = { version = "0.12", features = ["json"] }
  # h2 is NOT a direct dependency

First appeared: 2.1.0 (initial project setup; reqwest has always depended on hyper/h2)
Present in all versions (vulnerable only where the resolved h2 is < 0.4.5)

Remediation: two-tier.
  1. Preferred: bump the direct dependency (reqwest, and hyper with it) so the resolved
     closure includes h2 >= 0.4.5.
  2. Fallback: pin h2 directly (cargo add h2@0.4.5 / cargo update -p h2 --precise 0.4.5)
     if the reqwest bump is not viable.
```

**Dependency scope decision:** production runtime dependency. It is not dev-only, build-only, or feature-gated, so there is no `dev-dependency` label, no priority override, and no VEX feature-gate prompt.

**Remediation complexity:** low to moderate. h2 0.4.5 is semver-compatible with h2 0.4.4, so hyper 1.x's `h2 = "0.4"` requirement should accept it without intermediate maintainers releasing anything. Coordination with the reqwest or hyper maintainers is only needed if one of them pins h2 to an exact vulnerable version.

## 2.5 – Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | `release/0.4.z` | _not inspected (no HEAD data in fixtures; `git show` not permitted)_ | UNCONFIRMED |

Observation: tags `v0.4.11` and `v0.4.12`, cut from `release/0.4.z`, already resolve h2 0.4.5. That suggests the branch is already fixed. Under the evidence rules, HEAD must be checked with `git -C /home/dev/repos/rhtpa-backend show release/0.4.z:Cargo.lock | grep -A2 'name = "h2"'` before switching to the dependency-bump-only variant. Until then, remediation uses the standard upstream backport + downstream propagation pair, with the two-tier transitive approach (see `remediation.md`).

## Step 3 – Affects Versions Correction (proposed, scoped to 2.2.x)

```
Current:  [RHTPA 2.2.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

The PSIRT version is correct but incomplete. 2.2.3 and 2.2.4 are excluded because they ship h2 0.4.5. Version IDs would come from `getJiraIssueTypeMetaWithFields` (Step 3.1). No ProdSec account ID is configured, so the correction comment has no @mention. The comment would include the Comment Footnote. Not executed (simulated).

## Steps 4–7 (simulated summary)

- **4.1/4.2 Duplicates and siblings:** JQL search for `labels = CVE-2026-99010` was not run. No sibling data was supplied, so none are assumed.
- **4.3 Cross-CVE overlap:** skipped. The Upstream Affected Component field is not configured.
- **5 Lifecycle:** Product pages not fetched. The 2.2.x versions are assumed in support for this eval.
- **6 Already fixed:** no resolved siblings were supplied. Note that the latest 2.2.x release (2.2.4) already ships the fix.
- **7 Concurrent triage:** skipped. The Upstream Affected Component field is not configured.
- **7.5 Release Jira:** the release Epic and release Task for the next 2.2.x release ("RHTPA 2.2.<next> Release Tasks" / "RHTPA 2.2.<next> CVE triage") would be found or created, each with its own confirmation. Shown as placeholders in `remediation.md`.
