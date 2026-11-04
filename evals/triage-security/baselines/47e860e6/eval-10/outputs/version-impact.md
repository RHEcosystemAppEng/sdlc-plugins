# Step 2 – Version Impact Analysis: CVE-2026-55123 (tokio < 1.42.0)

Sources: the supportability matrices for both streams (security-matrix-mock.md) and the tokio lock-file versions from the cross-stream analysis in the issue fixture. That analysis stands in for `git show <tag>:Cargo.lock | grep -A2 'name = "tokio"'`. The mock lock-file tables have no tokio rows, so the tokio values below come from the provided Step 2 analysis only.

## Version impact table

| Version | Stream | Build | backend tag | tokio | Affected? | Notes |
|---------|--------|-------|-------------|-------|-----------|-------|
| RHTPA 2.1.0 | 2.1.x (rhtpa-2.1) | 0.3.8 | `v0.3.8` | 1.40.0 | **YES** | Outside this issue's scope |
| RHTPA 2.1.1 | 2.1.x (rhtpa-2.1) | 0.3.12 | `v0.3.12` | 1.40.0 | **YES** | Outside this issue's scope |
| RHTPA 2.2.0 | 2.2.x (rhtpa-2.2) | 0.4.5 | `v0.4.5` | 1.41.1 | **YES** | In scope |
| RHTPA 2.2.1 | 2.2.x (rhtpa-2.2) | 0.4.8 | `v0.4.8` | 1.41.1 | **YES** | In scope |
| RHTPA 2.2.2 | 2.2.x (rhtpa-2.2) | 0.4.9 | `v0.4.8` | — | **YES** | Same as 2.2.1 (backend retag of `v0.4.8`) |
| RHTPA 2.2.3 | 2.2.x (rhtpa-2.2) | 0.4.11 | `v0.4.11` | not provided | UNVERIFIED | No tokio evidence supplied. Must run `git show v0.4.11:Cargo.lock` |
| RHTPA 2.2.4 | 2.2.x (rhtpa-2.2) | 0.4.12 | `v0.4.12` | not provided | UNVERIFIED | No tokio evidence supplied. Must run `git show v0.4.12:Cargo.lock` |

Development stream (Step 2.2): 2.2.x is the latest stream and no newer stream is configured, so no development stream was detected. (In a live run, unreleased RHTPA Jira versions would be checked.)

Following the "do not fabricate data" guardrail, 2.2.3 and 2.2.4 are not marked YES or NO. The engineer must confirm them with a lock-file check. This does not change the result, because 2.2.x is affected either way.

## Cross-stream impact summary

| Stream | In issue scope? | Affected versions | tokio | Sibling CVE Jira (Step 4 JQL) | Action |
|--------|-----------------|-------------------|-------|-------------------------------|--------|
| 2.2.x (rhtpa-2.2) | Yes (TC-8020) | 2.2.0, 2.2.1, 2.2.2 (+2.2.3/2.2.4 unverified) | 1.41.1 | TC-8020 itself | Case B: standard remediation (Depend) |
| 2.1.x (rhtpa-2.1) | **No** | 2.1.0, 2.1.1 | 1.40.0 | **None found** | Case A: cross-stream comment + **preemptive** tasks (Related, `security-preemptive`) |

## Step 2.3.5 – Dependency chain

The chain could not be traced in this eval because `cargo tree` and `git show` were not run. tokio is normally a direct dependency of Rust async services, but the remediation tasks list it as "direct (to be confirmed by `cargo tree -i tokio`)". It is a runtime dependency, not dev-only, so priority keeps the CVE severity.

## Step 2.5 – Upstream fix status

| Stream | Ecosystem | Repository | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|------------|-----------------|-----------------|--------|
| 2.1.x | Cargo | rhtpa-backend | release/0.3.z | not checked (no evidence supplied) | Not confirmed |
| 2.2.x | Cargo | rhtpa-backend | release/0.4.z | not checked (no evidence supplied) | Not confirmed |

Neither branch has a confirmed fix, so the **upstream backport + downstream propagation** variant is used for both streams. If a live `git -C /home/dev/repos/rhtpa-backend show <branch>:Cargo.lock` shows tokio >= 1.42.0, switch the first task to the dependency-bump variant.

## Step 3 – Affects Versions correction (scoped to 2.2.x)

- Current: [RHTPA 2.2.0, RHTPA 2.2.1]
- Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2] (plus 2.2.3 / 2.2.4 only if the lock-file check confirms tokio < 1.42.0)
- RHTPA 2.1.0 and 2.1.1 are **not** added to TC-8020 because they belong to stream 2.1.x, which this issue does not cover.
- Version IDs would come from `getJiraIssueTypeMetaWithFields`. If RHTPA 2.2.2 has no Jira version, the project admin is notified.
- A correction comment with the footnote would be posted. No ProdSec @mention, because none is configured.

## Steps 4–7

- **4.1/4.2 Siblings:** the JQL `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020` returned **no results**. There are no same-stream duplicates and no companion tracker for rhtpa-2.1.
- **4.3 Cross-CVE overlap:** skipped because the Upstream Affected Component field is not configured in Security Configuration.
- **4.4 Preemptive reconciliation:** the search for `security-preemptive` + `CVE-2026-55123` tasks with `(rhtpa-2.2)` in the summary returned nothing, so standard task creation goes ahead.
- **5 Lifecycle:** not queried (no external calls). All listed versions are assumed in support, pending a product-pages check.
- **6 Already fixed:** there are no resolved siblings, so it is not already fixed.
- **7 Concurrent triage:** skipped because the Upstream Affected Component field is not configured.
- **7.5 Release Jira:** for 2.2.x, find or create "RHTPA <next 2.2.z> Release Tasks" and "RHTPA <next 2.2.z> CVE triage". The version is chosen by the engineer with individual confirmation. Preemptive 2.1.x tasks are **not** linked to release Jira.
