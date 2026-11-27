# TC-8020 — Step 7.5 / Step 8 Remediation Plan

Outcome: **affected, so remediation is needed** (not Case C). TC-8020 is **scoped** to rhtpa-2.2, and rhtpa-2.1 is also affected but has no CVE Jira. Both paths apply:

- **Case B**: standard remediation tasks for **rhtpa-2.2** (the issue's own stream).
- **Case A**: a cross-stream impact comment plus **preemptive** remediation tasks for **rhtpa-2.1** (details and comments are in cross-stream.md).

Ecosystem is Cargo, a source dependency, so each stream gets **2 tasks**: an upstream backport and a downstream propagation. The plan uses the backport variant because the upstream fix status is UNKNOWN (see version-impact.md, 2.5). That makes **4 Tasks** in total. No Vulnerability issues are created.

Every create, link, transition and comment below is **proposed and needs engineer confirmation**. None was executed in this eval. Task keys are shown as placeholders (`<TASK-…>`).

---

## Step 7.5 – Release Jira orchestration (rhtpa-2.2 only)

Release Jira applies to **non-preemptive** remediation only. The rhtpa-2.1 preemptive tasks are not linked to a release Task.

| Sub-step | Action for rhtpa-2.2 (2.2.x family) |
|---|---|
| 7.5.1 | Search `project = TC AND issuetype = Epic AND summary ~ 'RHTPA 2.2' AND summary ~ 'Release Tasks' ORDER BY created DESC`. If none is found, propose **"RHTPA 2.2.5 Release Tasks"** (the next patch after the latest matrix release, 2.2.4). Needs individual confirmation: Accept / Specify / Skip |
| 7.5.2 | Find or create the child Task **"RHTPA 2.2.5 CVE triage"** under the Epic (individual confirmation) |
| 7.5.3 | Cross-CVE dedup **skipped** because the Upstream Affected Component field is not configured |

Placeholders: `<RELEASE-EPIC-2.2>`, `<RELEASE-TASK-2.2>`.

---

## Case B – rhtpa-2.2 standard remediation tasks

### Task B1: upstream backport (rhtpa-2.2)

- **Summary:** `Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)`
- **Issue type:** Task, project TC
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-55123`
- **Security:** parent TC-8020's security level (`{id, name}`); omit only if TC-8020 has none
- **Priority / fixVersion:** prompt the engineer (no defaults configured)

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: tokio use-after-free when a spawned task is aborted
while holding a borrowed reference (memory corruption, potential code execution;
CVSS 8.1). The vulnerable dependency (tokio < 1.42.0) must be updated to the
fixed version (1.42.0+).

Affected versions: RHTPA 2.2.0 (tokio 1.41.1), RHTPA 2.2.1 (tokio 1.41.1),
RHTPA 2.2.2 (retag of 2.2.1); RHTPA 2.2.3 and 2.2.4 pending lock file verification
Source commit(s): backend v0.4.5, v0.4.8 (from rhtpa-release.0.4.z security-matrix.md)

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: to be confirmed. tokio is expected to be a direct dependency
  of the backend workspace; verify in Cargo.toml
- tokio is a production runtime dependency (not dev-only); no dev-dependency label

### Remediation approach (direct dependency)

- Update tokio dependency to >= 1.42.0 in Cargo.lock (and Cargo.toml version
  requirement if it caps below 1.42.0)
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in tokio
- Bump it to a version whose transitive closure includes tokio >= 1.42.0
- Verify the bump does not introduce breaking API changes

**Fallback: pin the transitive dependency directly**
- Cargo: `cargo add tokio@1.42.0` to override the transitive resolution
- Document why the direct dep bump was not viable in the PR description

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8020 (parent tracking issue)
```

### Task B2: downstream propagation (rhtpa-2.2)

- **Summary:** `Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-55123`
- **Security:** parent TC-8020's security level

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-55123 fix from <TASK-B1>.

The upstream backport (<TASK-B1>) bumps tokio to 1.42.0 on release/0.4.z.
Once that PR merges, update the source pinning in this Konflux release repo
so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: carried forward from <TASK-B1>
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned tokio directly (fallback approach), verify the
  pinning is reflected in the downstream build's lock file
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <TASK-B1> (upstream backport must merge first)
- Depends on: TC-8020 (parent tracking issue)
```

### Case B creation and linkage order

1. Create B1, then post the description digest comment on B1 (`[sdlc-workflow] Description digest: sha256-…`). The digest goes on before any links.
2. Create B2, then post the description digest comment on B2.
3. Link TC-8020 (inward) → B1 (outward), type **Depend**.
4. Link TC-8020 (inward) → B2 (outward), type **Depend**.
5. Link B1 (inward) → B2 (outward), type **Blocks** (upstream blocks downstream).
6. If release Jira is active: B1 → `<RELEASE-TASK-2.2>` **Blocks**, B2 → `<RELEASE-TASK-2.2>` **Blocks**, and `<RELEASE-TASK-2.2>` (inward) → TC-8020 (outward) **Related**.
7. Transition TC-8020 to In Progress. Skip this if it is already in Assigned or a later indeterminate status after Step 0.8.
8. Comment on TC-8020: "Remediation tasks created: <TASK-B1> (upstream backport), <TASK-B2> (downstream propagation, blocked by <TASK-B1>)", followed by the footnote.

---

## Case A – rhtpa-2.1 preemptive remediation tasks

rhtpa-2.1 (versions 2.1.0 and 2.1.1, tokio 1.40.0) is affected and has **no CVE Jira**, so create preemptive tasks. They differ from the Case B tasks in four ways:

- they carry the extra `security-preemptive` label
- the Description section starts with a preemptive prefix
- they link to TC-8020 with **Related**, not Depend
- they are not linked to release Jira

### Task A1: upstream backport (rhtpa-2.1), preemptive

- **Summary:** `Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`
- **Security:** parent TC-8020's security level

```
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-55123: tokio use-after-free when a spawned task is aborted
while holding a borrowed reference (memory corruption, potential code execution;
CVSS 8.1). The vulnerable dependency (tokio < 1.42.0) must be updated to the
fixed version (1.42.0+).

Affected versions: RHTPA 2.1.0 (tokio 1.40.0), RHTPA 2.1.1 (tokio 1.40.0)
Source commit(s): backend v0.3.8, v0.3.12 (from rhtpa-release.0.3.z security-matrix.md)

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: to be confirmed. tokio is expected to be a direct dependency
  of the backend workspace; verify in Cargo.toml
- tokio is a production runtime dependency (not dev-only); no dev-dependency label
- Note: 1.40.0 → 1.42.0 crosses two minor releases; check tokio changelog and
  MSRV for the 0.3.z toolchain

### Remediation approach (direct dependency)

- Update tokio dependency to >= 1.42.0 in Cargo.lock (and Cargo.toml version
  requirement if it caps below 1.42.0)
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in tokio
- Bump it to a version whose transitive closure includes tokio >= 1.42.0
- Verify the bump does not introduce breaking API changes

**Fallback: pin the transitive dependency directly**
- Cargo: `cargo add tokio@1.42.0` to override the transitive resolution
- Document why the direct dep bump was not viable in the PR description

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8020 (originating CVE Jira, stream rhtpa-2.2)
```

### Task A2: downstream propagation (rhtpa-2.1), preemptive

- **Summary:** `Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`
- **Security:** parent TC-8020's security level

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-55123 fix from <TASK-A1>.

The upstream backport (<TASK-A1>) bumps tokio to 1.42.0 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release repo
so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: carried forward from <TASK-A1>
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned tokio directly (fallback approach), verify the
  pinning is reflected in the downstream build's lock file
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <TASK-A1> (upstream backport must merge first)
- Related to: TC-8020 (originating CVE Jira, stream rhtpa-2.2)
```

### Case A creation and linkage order

1. Create A1, then post its description digest comment.
2. Create A2, then post its description digest comment.
3. Link TC-8020 (inward) → A1 (outward), type **Related**.
4. Link TC-8020 (inward) → A2 (outward), type **Related**.
5. Link A1 (inward) → A2 (outward), type **Blocks**.
6. Do **not** link A1 or A2 to any release Task, and do **not** use Depend.
7. Post the preemptive task list comment on TC-8020 (see cross-stream.md).

---

## Pre-creation checklist

- [x] **Task count per stream:** Cargo is a source dependency, so 2 tasks for rhtpa-2.2 (B1, B2) and 2 for rhtpa-2.1 (A1, A2).
- [x] **Cross-stream coverage:** the only affected stream outside scope is rhtpa-2.1. It has no sibling CVE Jira, so it gets preemptive tasks A1 and A2.
- [x] **Link types:** B1 and B2 use Depend to TC-8020. A1 and A2 use Related to TC-8020. B1 Blocks B2, and A1 Blocks A2.
- [x] **Preemptive labels:** A1 and A2 carry `security-preemptive`. B1 and B2 do not.
- [x] **Coordination guidance:** omitted, because Source Repositories has no Deployment Context column (backward-compatibility rule).
- [x] **Release Jira linking:** B1 and B2 Block `<RELEASE-TASK-2.2>`, and TC-8020 is Related to it, if Step 7.5 is accepted. Preemptive tasks are excluded.
- [x] **Dedup consistency:** no stream was dedup'd (7.5.3 skipped).

## Open items before execution

1. Verify tokio at v0.4.11 and v0.4.12 (RHTPA 2.2.3 and 2.2.4). If they are below 1.42.0, add them to Affects Versions and to B1's affected list.
2. Check tokio at the HEAD of `release/0.4.z` and `release/0.3.z`. If either already has >= 1.42.0, use the dependency-bump template (`cargo update -p tokio`) for B1 or A1.
3. Confirm the product lifecycle for 2.1.x and 2.2.x. If 2.1.x is EOL, drop A1 and A2 and the cross-stream comment becomes informational only.
4. Refresh the stale matrices (152 days old). There may be newer 2.1.x or 2.2.x releases.
5. The due date (2026-08-15) has already passed; flag this to the engineer and ProdSec.

## Post-triage summary (after all actions)

- Add the label `ai-cve-triaged` to TC-8020.
- Post a summary comment on TC-8020 containing:
  - the version impact table
  - the Affects Versions correction (2.2.0, 2.2.1 → 2.2.0, 2.2.1, 2.2.2)
  - the outcome: remediation created for rhtpa-2.2 (B1, B2) and preemptive tasks for rhtpa-2.1 (A1, A2)
  - the release Epic and Task keys
  - dedup: none
  - an ADF @mention of the TC-8020 reporter (`{ "type": "mention", "attrs": { "id": "<reporter-account-id>", "text": "@<reporter-name>" } }`)
  - the Comment Footnote: "This comment was AI-generated by sdlc-workflow/triage-security v0.14.0."
