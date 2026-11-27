# TC-8020 — Step 2 Version Impact Analysis (with cross-stream impact)

Evidence source: the cross-stream version impact analysis in the issue input (simulated `git show <tag>:Cargo.lock | grep -A2 'name = "tokio"'` output) plus the supportability matrices for both streams. The mock lock file data in `security-matrix-mock.md` has no tokio section, so versions with no supplied tokio data are marked **NOT VERIFIED**. No values were filled in by guesswork.

## 2.1 – Supportability matrix (both streams enumerated from Version Streams)

| Stream | Konflux repo | Versions | Backend pin (tag) | Upstream branch |
|---|---|---|---|---|
| 2.1.x (`rhtpa-2.1`) | rhtpa-release.0.3.z | 2.1.0, 2.1.1 | v0.3.8, v0.3.12 | release/0.3.z |
| 2.2.x (`rhtpa-2.2`) | rhtpa-release.0.4.z | 2.2.0, 2.2.1, 2.2.2 (retag of 2.2.1), 2.2.3, 2.2.4 | v0.4.5, v0.4.8, v0.4.8, v0.4.11, v0.4.12 | release/0.4.z |

Matrix format validation: both streams have Supportability Matrix, Ecosystem Mappings (correct columns), Source Pinning Method, and Forward Pointer → Pass.
Matrix staleness: both matrices are 152 days old (see data-extraction.md); proceeding with the current matrix.

## 2.2 – Development stream

Unreleased Jira versions (`getJiraIssueTypeMetaWithFields`, prefix `RHTPA`) were not available in this eval. No development stream is configured in Version Streams beyond 2.1.x and 2.2.x, so no development-head row is included. **Action:** confirm in Jira whether an unreleased RHTPA version (for example 2.3 or 3.0) exists. If one does, check tokio at its branch HEAD before closing out triage.

## 2.4 – Version impact table

Version Impact for CVE-2026-55123 (tokio < 1.42.0, fixed in 1.42.0):

| Version | Stream | Backend tag | tokio | Affected? | In TC-8020 scope? | Notes |
|---|---|---|---|---|---|---|
| RHTPA 2.1.0 | rhtpa-2.1 | v0.3.8 | 1.40.0 | **YES** | No (cross-stream) | 1.40.0 < 1.42.0 |
| RHTPA 2.1.1 | rhtpa-2.1 | v0.3.12 | 1.40.0 | **YES** | No (cross-stream) | 1.40.0 < 1.42.0 |
| RHTPA 2.2.0 | rhtpa-2.2 | v0.4.5 | 1.41.1 | **YES** | Yes | 1.41.1 < 1.42.0 |
| RHTPA 2.2.1 | rhtpa-2.2 | v0.4.8 | 1.41.1 | **YES** | Yes | 1.41.1 < 1.42.0 |
| RHTPA 2.2.2 | rhtpa-2.2 | v0.4.8 | — | **YES** | Yes | same as 2.2.1 (backend retag, carried forward) |
| RHTPA 2.2.3 | rhtpa-2.2 | v0.4.11 | not supplied | **NOT VERIFIED** | Yes | run `git show v0.4.11:Cargo.lock \| grep -A2 'name = "tokio"'` |
| RHTPA 2.2.4 | rhtpa-2.2 | v0.4.12 | not supplied | **NOT VERIFIED** | Yes | run `git show v0.4.12:Cargo.lock \| grep -A2 'name = "tokio"'` |

### Cross-stream impact summary

| Stream | Affected versions | Own CVE Jira? | Handling |
|---|---|---|---|
| **rhtpa-2.2** (issue scope) | 2.2.0, 2.2.1, 2.2.2 (+ 2.2.3/2.2.4 pending verification) | TC-8020 (this issue) | Case B: standard remediation tasks |
| **rhtpa-2.1** (outside scope) | 2.1.0, 2.1.1 | **None.** JQL `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020` returned no rhtpa-2.1 sibling | Case A: cross-stream comment + **preemptive** remediation tasks |

## 2.3.5 – Dependency chain context

```
Dependency chain for tokio (Cargo):
  backend (workspace) → tokio            [expected; not confirmed]
  Type: NOT DETERMINED from available evidence. Cargo.toml was not inspected.
        tokio is normally a direct runtime dependency of a Rust async server.
  Profile: production (presumed runtime; it is shipped in the server binary)
  Present in: all checked versions (2.1.0 through 2.2.2)
  tokio drift: 1.40.0 (2.1.x) → 1.41.1 (2.2.x); no checked version reaches 1.42.0

Remediation: if tokio is direct, bump it to >= 1.42.0 in Cargo.toml/Cargo.lock.
If it is transitive, bump the direct dependency that pulls it in, and fall back
to pinning tokio directly.
```

This is not a dev-only or build-only dependency, so the `dev-dependency` label and the Normal-priority override do not apply. It is not a feature-gated optional dependency, so the VEX "not in execute path" option does not apply.

## 2.5 – Upstream fix status

| Stream | Ecosystem | Repository | Upstream Branch | tokio at HEAD | Fixed? |
|---|---|---|---|---|---|
| 2.2.x | Cargo | rhtpa-backend | release/0.4.z | not supplied | **UNKNOWN** |
| 2.1.x | Cargo | rhtpa-backend | release/0.3.z | not supplied | **UNKNOWN** |

Command to run: `git -C /home/dev/repos/rhtpa-backend show release/0.4.z:Cargo.lock | grep -A2 'name = "tokio"'` (and the same for `release/0.3.z`).

The upstream fix is not confirmed on either branch, so the remediation plan uses the **upstream backport + downstream propagation** variant. If either branch already has tokio >= 1.42.0, switch that stream's first task to the **dependency bump** variant (`cargo update -p tokio`).

## Step 3 – Affects Versions correction (scoped to rhtpa-2.2)

| | Versions |
|---|---|
| Current (PSIRT) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Proposed | RHTPA 2.2.0, RHTPA 2.2.1, **RHTPA 2.2.2** (+ RHTPA 2.2.3 / 2.2.4 if verification shows tokio < 1.42.0) |
| Excluded | RHTPA 2.1.0, RHTPA 2.1.1. They are affected but belong to stream rhtpa-2.1, outside TC-8020's scope (see cross-stream.md) |

The PSIRT versions are correct but incomplete. Version IDs must be found at runtime with `getJiraIssueTypeMetaWithFields(projectIdOrKey: "TC", issueTypeId: "10024")`. If any matrix version has no RHTPA Jira version, flag it to the project admin. After confirmation, post this correction comment, with the footnote and no ProdSec mention because none is configured:

> Corrected Affects Versions: [RHTPA 2.2.0, RHTPA 2.2.1] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
> Based on lock file analysis at pinned commits from security-matrix.md (2.2.2 is a backend retag of 2.2.1).
> Scoped to stream rhtpa-2.2 per issue suffix.
>
> ---
> This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0.

## Steps 4–7 summary

| Step | Result |
|---|---|
| 4.1 Same-stream duplicates | None found. Not a duplicate |
| 4.2 Cross-stream siblings | None found (no rhtpa-2.1 CVE Jira). No Related links to create |
| 4.3 Cross-CVE overlap | Skipped (Upstream Affected Component / PS Component / Stream fields not configured in Security Configuration) |
| 4.4 Preemptive reconciliation | Searched for `labels = 'security-preemptive' AND labels = 'CVE-2026-55123'` with `(rhtpa-2.2)` in the summary. No data was supplied, so treated as no match and remediation proceeds |
| 5 Lifecycle | Product pages were not fetched (eval). **Pending:** confirm that 2.1.x and 2.2.x are within support. Drop any EOL versions, which would also drop preemptive tasks for an EOL 2.1.x |
| 6 Already fixed | No resolved siblings. Not already fixed |
| 7 Concurrent triage | Skipped (Upstream Affected Component field not configured) |
| 7.5 Release Jira | See remediation.md (rhtpa-2.2 only; preemptive tasks are not linked to release Jira) |
