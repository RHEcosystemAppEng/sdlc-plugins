# Step 2 – Version Impact Analysis: CVE-2026-55123 (tokio < 1.42.0)

Evidence source: the cross-stream version impact data supplied with the issue
(simulated `git show <tag>:Cargo.lock | grep -A2 'name = "tokio"'` output). The
mock security matrix has no tokio lock-file rows, so no tokio versions were
invented beyond the supplied data.

## Version impact table

| Version | Stream | Konflux repo | Backend tag (pinned) | tokio | Affected? | Notes |
|---|---|---|---|---|---|---|
| RHTPA 2.1.0 | 2.1.x (rhtpa-2.1) | rhtpa-release.0.3.z | `v0.3.8` | 1.40.0 | **YES** | outside issue scope |
| RHTPA 2.1.1 | 2.1.x (rhtpa-2.1) | rhtpa-release.0.3.z | `v0.3.12` | 1.40.0 | **YES** | outside issue scope |
| RHTPA 2.2.0 | 2.2.x (rhtpa-2.2) | rhtpa-release.0.4.z | `v0.4.5` | 1.41.1 | **YES** | in scope |
| RHTPA 2.2.1 | 2.2.x (rhtpa-2.2) | rhtpa-release.0.4.z | `v0.4.8` | 1.41.1 | **YES** | in scope |
| RHTPA 2.2.2 | 2.2.x (rhtpa-2.2) | rhtpa-release.0.4.z | `v0.4.8` (retag) | — | **YES** | same as 2.2.1 (backend retag, result carried forward) |
| RHTPA 2.2.3 | 2.2.x (rhtpa-2.2) | rhtpa-release.0.4.z | `v0.4.11` | not provided | UNVERIFIED | requires `git show v0.4.11:Cargo.lock`; not in supplied evidence |
| RHTPA 2.2.4 | 2.2.x (rhtpa-2.2) | rhtpa-release.0.4.z | `v0.4.12` | not provided | UNVERIFIED | requires `git show v0.4.12:Cargo.lock`; not in supplied evidence |

Fix threshold: tokio **1.42.0**. Every version with supplied evidence ships a vulnerable tokio:
1.40.0 in 2.1.x and 1.41.1 in 2.2.x.

Development stream (Step 2.2): no unreleased Jira version data is available in this
eval, so no dev-stream HEAD check was performed. 2.2.x is the latest configured stream.

## Cross-stream impact summary

| Stream | Affected versions | In TC-8020 scope? | Sibling CVE Jira? | Action |
|---|---|---|---|---|
| rhtpa-2.2 (2.2.x) | 2.2.0, 2.2.1, 2.2.2 (retag) | Yes | n/a (this issue) | Case A: standard remediation (Depend) |
| rhtpa-2.1 (2.1.x) | 2.1.0, 2.1.1 | No | **None** (JQL returned no results) | Case B: preemptive remediation (Related, `security-preemptive`) |

## Step 2.3.5 – Dependency chain

```
Dependency chain for tokio:
  backend (workspace) -> tokio
  Type: assumed direct (tokio is a core async runtime dependency of the Rust backend).
        Not verified against Cargo.toml in this eval. /implement-task must confirm
        direct vs transitive before choosing the remediation approach.
  Profile: production runtime dependency (not dev-only, so the dev-dependency label
           and Normal-priority override do not apply)
  Present in: all checked versions of 2.1.x and 2.2.x
```

## Step 2.5 – Upstream fix status

| Stream | Ecosystem | Repository | Upstream Branch | tokio at HEAD | Fixed? |
|---|---|---|---|---|---|
| 2.1.x | Cargo | backend | `release/0.3.z` | not provided | not confirmed |
| 2.2.x | Cargo | backend | `release/0.4.z` | not provided | not confirmed |

The upstream fix is not confirmed on either branch, so both streams use the
**upstream backport + downstream propagation** task pair, not the dependency-bump variant.

## Step 3 – Affects Versions correction (scoped to 2.2.x)

- Current: `[RHTPA 2.2.0, RHTPA 2.2.1]`
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`. 2.2.2 is added because it is a backend retag of 2.2.1. 2.2.3 and 2.2.4 are added only if lock-file verification shows tokio < 1.42.0.
- 2.1.x versions are **not** added to TC-8020 because they are outside the issue's stream scope.
- Version IDs are discovered dynamically via `getJiraIssueTypeMetaWithFields`. If RHTPA 2.2.2 has no Jira version, flag it to the project admin.

## Steps 4–7 summary

- Step 4: the sibling JQL `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020` returned no results, so there are no duplicates and no companion tracker for rhtpa-2.1.
- Step 4.3: the cross-CVE overlap search (tokio / pscomponent:org/rhtpa-server / rhtpa-2.2) found no covering remediation, as per the scenario.
- Step 4.4: no `security-preemptive` task exists for CVE-2026-55123, so no reconciliation is needed.
- Step 5: lifecycle is not checked externally in this eval. All matrix versions are assumed supported.
- Step 6: there are no resolved siblings, so this is not already fixed.
- Step 7: no concurrent triage was detected.
- Step 7.5: the release Epic and Task for 2.2.x ("RHTPA <next 2.2.z> Release Tasks" / "... CVE triage") are found or created with individual confirmation. Preemptive 2.1.x tasks are **not** linked to release Jira.
