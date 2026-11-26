# Step 2 – Version Impact Analysis: CVE-2026-55123 (tokio < 1.42.0)

## 2.1 – Supportability matrix (from security-matrix.md, both streams)

| Stream | Konflux repo | Versions | backend tag | Lock file | Upstream branch |
|---|---|---|---|---|---|
| 2.1.x | rhtpa-release.0.3.z | 2.1.0, 2.1.1 | v0.3.8, v0.3.12 | `Cargo.lock` | `release/0.3.z` |
| 2.2.x | rhtpa-release.0.4.z | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | v0.4.5, v0.4.8, v0.4.8 (retag), v0.4.11, v0.4.12 | `Cargo.lock` | `release/0.4.z` |

## 2.2 – Development stream

No unreleased RHTPA Jira version data was available. Version discovery is a Jira call, and Jira calls were not allowed. 2.2.x is the latest stream (no forward pointer), and no development stream was detected.

## 2.3 – tokio versions at pinned commits

The tokio versions come from the cross-stream version impact analysis that the issue and the task supplied (`git show <tag>:Cargo.lock`). The mock matrix contains no tokio lock file data for tags v0.4.11 and v0.4.12.

## 2.4 – Version impact table

Version Impact for CVE-2026-55123 (tokio < 1.42.0):

| Version | Stream | Pinned tag | tokio | Affected? | Notes |
|---|---|---|---|---|---|
| RHTPA 2.1.0 | rhtpa-2.1 (2.1.x) | v0.3.8 | 1.40.0 | **YES** | Outside this issue's scope; cross-stream impact |
| RHTPA 2.1.1 | rhtpa-2.1 (2.1.x) | v0.3.12 | 1.40.0 | **YES** | Outside this issue's scope; cross-stream impact |
| RHTPA 2.2.0 | rhtpa-2.2 (2.2.x) | v0.4.5 | 1.41.1 | **YES** | In scope |
| RHTPA 2.2.1 | rhtpa-2.2 (2.2.x) | v0.4.8 | 1.41.1 | **YES** | In scope |
| RHTPA 2.2.2 | rhtpa-2.2 (2.2.x) | v0.4.8 | — | **YES** | Retag of 2.2.1 (backend `v0.4.8`), same result as 2.2.1 |
| RHTPA 2.2.3 | rhtpa-2.2 (2.2.x) | v0.4.11 | not provided | **UNVERIFIED** | No tokio lock file data supplied. Needs `git show v0.4.11:Cargo.lock` |
| RHTPA 2.2.4 | rhtpa-2.2 (2.2.x) | v0.4.12 | not provided | **UNVERIFIED** | No tokio lock file data supplied. Needs `git show v0.4.12:Cargo.lock` |

The impact is not inferred for 2.2.3 and 2.2.4, because the skill forbids fabricating dependency versions. The engineer must verify them before the Affects Versions correction is finalised.

### Cross-stream impact summary

| Stream | In issue scope? | Affected versions | tokio | Own CVE Jira? | Action |
|---|---|---|---|---|---|
| rhtpa-2.2 (2.2.x) | Yes (TC-8020) | 2.2.0, 2.2.1, 2.2.2 (retag); 2.2.3 and 2.2.4 unverified | 1.41.1 | Yes: TC-8020 | Case B: standard remediation tasks (Depend) |
| rhtpa-2.1 (2.1.x) | **No** | 2.1.0, 2.1.1 | 1.40.0 | **No** (sibling JQL returned 0 results) | Case A: cross-stream comment + **preemptive** tasks (Related, `security-preemptive`) |

## 2.3.5 – Dependency chain

```
Dependency chain for tokio:
  backend (workspace) → tokio
  Type: assumed direct runtime dependency (tokio is the async runtime). This was not
        verified with `cargo tree`, which was not allowed in this eval
  Profile: production (runtime dependency; not dev-only, so no dev-dependency label)
  Present in: all checked versions (2.1.x and 2.2.x)

Remediation: bump tokio to >= 1.42.0 in Cargo.lock (cargo update -p tokio or a
Cargo.toml bump). If tokio turns out to be transitive, use the two-tier approach.
```

## 2.5 – Upstream fix status

| Stream | Ecosystem | Repository | Upstream Branch | Version at HEAD | Fixed? |
|---|---|---|---|---|---|
| 2.1.x | Cargo | backend | release/0.3.z | not checked (no git access) | Unknown, treated as NOT fixed |
| 2.2.x | Cargo | backend | release/0.4.z | not checked (no git access) | Unknown, treated as NOT fixed |

Step 2.5 could not confirm that the fix is already on the upstream branches. Both streams therefore use the **upstream backport + downstream propagation** task pair. If the engineer confirms that a branch HEAD already ships tokio >= 1.42.0, switch that stream to the dependency-bump variant.

## Step 3 – Affects Versions correction (scoped to 2.2.x)

- Current: `[RHTPA 2.2.0, RHTPA 2.2.1]`
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`. 2.2.2 is a retag of 2.2.1 and ships tokio 1.41.1. Add RHTPA 2.2.3 and 2.2.4 only if lock file verification shows tokio < 1.42.0.
- RHTPA 2.1.0 and 2.1.1 are **not** added to TC-8020. They belong to stream 2.1.x, which is outside this issue's scope.
- Jira version IDs must be discovered with `getJiraIssueTypeMetaWithFields`. If RHTPA 2.2.2 is not registered in Jira, flag it to the project admin.

## Steps 4–7 summary

- **Step 4 (siblings):** JQL `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020` returned **no results**. There are no duplicates and no companion tracker for 2.1.x.
- **Step 4.3 (cross-CVE overlap):** no data was supplied, so no overlap is assumed.
- **Step 4.4 (preemptive reconciliation):** no existing `security-preemptive` tasks for CVE-2026-55123 were supplied.
- **Step 5 (lifecycle):** the product pages could not be fetched. All listed versions are treated as supported, pending verification.
- **Step 6 (already fixed):** there are no resolved siblings, so it is not already fixed.
- **Step 7 (concurrent triage):** no concurrent triage on component `tokio` was supplied, so the triage proceeds.
- **Step 7.5 (release Jira):** find or create the 2.2.x release Epic and Task ("RHTPA <next 2.2.z> Release Tasks" / "RHTPA <next 2.2.z> CVE triage"). The version has to be confirmed with the engineer. Preemptive 2.1.x tasks are not linked to release Jira.
