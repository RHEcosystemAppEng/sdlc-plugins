# Step 7 / 7.5 / 8 – Remediation: TC-8004 (CVE-2026-33501, h2 < 0.4.8)

## Decision

- Supported versions affected? **Yes**: 2.1.0 and 2.1.1 (2.1.x stream).
- Issue scoped? **No** (unscoped) → **Case A skipped** (it applies only to scoped issues).
- → **Case B**: create remediation tasks for **affected streams only**.

| Stream | Affected? | Remediation |
|--------|-----------|-------------|
| **2.1.x** (rhtpa-release.0.3.z / backend `release/0.3.z`) | YES | 2 tasks (Cargo = source dependency) |
| 2.2.x (rhtpa-release.0.4.z / backend `release/0.4.z`) | NO, all versions ship h2 >= 0.4.8 | **No tasks** |

- Ecosystem: Cargo → source dependency → **2 tasks** for 2.1.x.
- Upstream fix on `release/0.3.z` could not be confirmed (Step 2.5) → **upstream backport
  + downstream propagation** variant.
- No `security-preemptive` label: the stream is covered by this unscoped CVE issue.
- No `dev-dependency` label: h2 is a production runtime dependency (HTTP/2 stack).

## Step 7 – Concurrent triage detection
Skipped, because the Upstream Affected Component custom field is not configured.

## Step 7.5 – Release Jira orchestration (2.1.x only)
Jira search not run. Proposed, each with its own confirmation:
- 7.5.1 Find or create Epic **"RHTPA 2.1.x Release Tasks"** (next 2.1.z version, e.g. 2.1.2,
  for the engineer to choose; version is not inferred automatically).
- 7.5.2 Find or create Task **"RHTPA <2.1.z> CVE triage"** as a child of the Epic.
- 7.5.3 Cross-CVE dedup: no existing remediation task known for h2 on 2.1.x → no dedup, so create tasks.
No release Jira for 2.2.x (not affected).

---

## Task 1: Upstream backport (2.1.x)

**Summary**: `[2.1.x] CVE-2026-33501: bump h2 to >= 0.4.8 in rhtpa-backend release/0.3.z`
**Issue type**: Task | **Project**: TC | **Labels**: `CVE-2026-33501`, `security`, `pscomponent:org/rhtpa-server`
**Due date**: 2026-08-01

```
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames (the
accumulated header block has no size limit, so a peer can consume unbounded server memory).
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (h2 0.4.5), RHTPA 2.1.1 (h2 0.4.5)
Source commit(s): backend v0.3.8 (2.1.0), backend v0.3.12 (2.1.1)

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: transitive, expected (chain: backend (workspace) → hyper → h2;
  confirm with `cargo tree -i h2`)
- h2 is a production runtime dependency, so the CVE priority applies (no dev-dependency label).

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in h2 (e.g. hyper / reqwest / tonic)
- Bump it to a version whose transitive closure includes h2 >= 0.4.8. Because
  0.4.5 → 0.4.8 is semver-compatible, `cargo update -p h2` may be enough
- Verify the bump does not introduce breaking API changes

**Fallback: pin the transitive dependency directly**
- `cargo add h2@0.4.8` to override the transitive resolution
- Document why the direct dep bump was not viable in the PR description

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8 in Cargo.lock on release/0.3.z
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)
```

## Task 2: Downstream propagation (2.1.x)

**Summary**: `[2.1.x] CVE-2026-33501: update rhtpa-backend reference in rhtpa-release.0.3.z`
**Issue type**: Task | **Project**: TC | **Labels**: `CVE-2026-33501`, `security`, `pscomponent:org/rhtpa-server`
**Due date**: 2026-08-01

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from <TASK-1-KEY>.

The upstream backport (<TASK-1-KEY>) bumps h2 to 0.4.8 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release repo so
the next 2.1.x build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g. `v0.3.12`)
- **Dependency type**: transitive, carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
  (e.g. v0.3.13+)
- If the upstream fix pinned h2 directly (fallback), check that the pin shows up in
  the downstream build's Cargo.lock after the reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <TASK-1-KEY> (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

(Coordination Guidance omitted: Source Repositories table has no Deployment Context column.)

## Jira linkage (after confirmation)

1. Each new task → TC-8004, type **Depend**.
2. Task 1 → Task 2, type **Blocks** (downstream blocked by upstream).
3. Task 1 and Task 2 → 2.1.x release Task, type **Blocks** (if Step 7.5 is active).
4. Release Task ↔ TC-8004, type **Related**.
5. Post a description digest comment on each task (shared/description-digest-protocol.md).
6. Transition TC-8004 to Assigned/In Progress and assign it to the current user.
7. Comment on TC-8004: "Remediation tasks created: <TASK-1-KEY> (upstream backport),
   <TASK-2-KEY> (downstream propagation, blocked by <TASK-1-KEY>)", with Comment Footnote.

## Pre-creation checklist

- [x] Task count per stream: 2.1.x gets 2 (Cargo source dep); 2.2.x gets 0 (not affected)
- [x] Cross-stream coverage: n/a (unscoped issue covers all streams; Case A skipped)
- [x] Link types: Depend (to TC-8004), Blocks (upstream → downstream, tasks → release Task)
- [x] Preemptive labels: none needed
- [x] Coordination guidance: omitted (no deployment context configured)
- [x] Release Jira linking: planned for the 2.1.x release Task
- [x] Dedup consistency: no dedup'd streams

## Post-triage summary (planned)

- Add label `ai-cve-triaged` to TC-8004.
- Summary comment: version impact table (2.1.x affected, 2.2.x not affected), Affects
  Versions correction ([RHTPA 2.1.0, RHTPA 2.2.0] → [RHTPA 2.1.0, RHTPA 2.1.1]), outcome
  (remediation created for 2.1.x only), task keys, release Epic/Task keys, no dedup,
  ADF @mention of the issue reporter, Comment Footnote (triage-security v0.14.0).

All Jira mutations are proposals only. None were executed in this eval.
