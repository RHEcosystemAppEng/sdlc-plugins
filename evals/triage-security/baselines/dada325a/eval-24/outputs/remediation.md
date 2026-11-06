# Triage TC-8001: Steps 2 to 8 (Version Impact, Triage Operations, Remediation)

> Eval mode: lock file versions come from the "Mock Lock File Data" section of
> `security-matrix-mock.md`, which simulates `git show <tag>:Cargo.lock` output. No Jira
> mutations were executed. Every proposed mutation below would need engineer
> confirmation in interactive mode.

## Step 2: Version Impact Analysis

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Pinned tag (backend) | quinn-proto | Affected? | Notes |
|---|---|---|---|---|---|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | outside issue scope |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | outside issue scope |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.8 | (same as 2.2.1) | YES | backend retag of 2.2.1; lock check skipped |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | fix shipped |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | |

Development stream (Step 2.2): there is no Jira version metadata in the fixtures, so no
unreleased development version could be identified. 2.2.x is the latest configured
stream and has no forward pointer.

Dependency chain (Step 2.3.5): the fixtures contain no Cargo.toml or dependency-tree
data, so the chain cannot be traced from evidence. quinn-proto is normally pulled in
transitively, for example through quinn and reqwest/h3, but this is **not verified**.
The tasks therefore list both remediation approaches. Profile is assumed to be
production (there is no evidence of a dev-only declaration).

Upstream fix status (Step 2.5):

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|---|---|---|---|---|
| 2.1.x | Cargo | release/0.3.z | not available in fixtures | Not confirmed. Last released tag v0.3.12 ships 0.11.9 |
| 2.2.x | Cargo | release/0.4.z | not available in fixtures | Fix already shipped in tags v0.4.11 and v0.4.12 (0.11.14) |

## Step 3: Affects Versions Correction (scoped to 2.2.x)

| | Value |
|---|---|
| Current (PSIRT) | RHTPA 2.0.0 |
| Proposed | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |
| Rationale | RHTPA 2.0.0 is not a supported version in any configured stream. Lock file evidence shows 2.2.0 to 2.2.2 ship quinn-proto < 0.11.14, while 2.2.3 and 2.2.4 ship 0.11.14. |

The version IDs would be discovered dynamically through `getJiraIssueTypeMetaWithFields`.
The correction comment includes the Comment Footnote. No ProdSec @mention is added
because that field is not configured.

## Steps 4 to 7

- **Step 4 (duplicates/siblings):** in interactive mode this runs JQL for
  `labels = CVE-2026-31812`. The fixtures supply no sibling issues, so this run assumes
  **no same-stream duplicate and no 2.1.x companion Vulnerability issue**. Step 4.3
  (cross-CVE overlap) is skipped because Upstream Affected Component is not configured.
  Step 4.4: no preemptive tasks exist to reconcile.
- **Step 5 (lifecycle):** the product pages were not fetched. The 2.1.x and 2.2.x
  versions are treated as supported, as listed in the matrix.
- **Step 6 (already fixed):** there are no resolved siblings. Within 2.2.x, the fix
  already ships in 2.2.3 and 2.2.4.
- **Step 7 (concurrent triage):** skipped because Upstream Affected Component is not
  configured.
- **Step 7.5 (release Jira):** the target release would be resolved through Jira for the
  affected streams (find or create the "RHTPA <version> Release Tasks" Epic and the
  "RHTPA <version> CVE triage" Task, each with individual confirmation). Preemptive tasks
  are not linked to release Jira.

## Step 8: Remediation Decision

- **Scoped stream 2.2.x (Case B):** 2.2.0 to 2.2.2 are affected, but the latest 2.2.x
  release (2.2.4, `v0.4.12`) and 2.2.3 (`v0.4.11`) already ship quinn-proto 0.11.14.
  The fix is already on the release/0.4.z line and has already been propagated to the
  Konflux release repo, so **no new remediation tasks are needed for 2.2.x**.
  Recommendation: keep TC-8001 open with corrected Affects Versions. Record in the
  summary comment that the fix shipped in RHTPA 2.2.3, so the engineer can move it to
  the appropriate fixed/verified state.
- **Other stream 2.1.x (Case A, cross-stream impact):** 2.1.0 and 2.1.1 both ship
  quinn-proto 0.11.9 (affected). There is no 2.1.x CVE Jira, so this run creates a
  cross-stream impact comment and **preemptive** remediation tasks: a Cargo source
  dependency gets 2 tasks (upstream backport and downstream propagation).

Coordination guidance: the Source Repositories table has **no Deployment Context
column**. rhtpa-backend defaults to `upstream`, and per the backward-compatibility rule
**no `### Coordination Guidance` subsection is added** to the task descriptions below.

### Cross-stream impact comment (on TC-8001)

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x based on
lock file analysis (2.1.0 @ v0.3.8 and 2.1.1 @ v0.3.12 ship quinn-proto 0.11.9).
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

---
_Generated by sdlc-workflow/triage-security_
```

---

### Task 1: Upstream backport (2.1.x, preemptive)

- **Summary:** Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)
- **Issue type:** Task
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- **Link:** TC-8001 → this task, type `Related` (preemptive)

```markdown
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (remote denial of
service through a STREAMS frame that requests an unbounded number of streams).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (quinn-proto 0.11.9), RHTPA 2.1.1 (quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: not determined from triage evidence (no manifest/dependency-tree
  data available). Run `cargo tree -i quinn-proto` to determine whether it is direct
  or transitive, then follow the matching approach below.
- If the vulnerable dependency is dev-only or build-only, the remediation priority is
  Normal regardless of CVE severity. Add `dev-dependency` label to the task.

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

When the vulnerable package is a **transitive** dependency (pulled in
through intermediate packages), use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (e.g. `cargo tree -i quinn-proto`)
- Bump the direct dependency to a version whose transitive closure
  includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes to the
  direct dependency

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable (breaking API changes,
no release available with the fix):
- Cargo: `cargo add quinn-proto@0.11.14` to add as a direct
  dependency, overriding the transitive resolution
- Document why the direct dep bump was not viable in the PR description

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

---

### Task 2: Downstream propagation (2.1.x, preemptive)

- **Summary:** Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)
- **Issue type:** Task
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- **Links:** TC-8001 → this task (`Related`); Task 1 → this task (`Blocks`)

```markdown
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from <Task 1 key>.

The upstream backport (<Task 1 key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: carried forward from the upstream task (to be confirmed there)
- Update the backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback
  approach), verify the pinning is reflected in the downstream build's
  lock file after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <Task 1 key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

Note: neither task description contains a `### Coordination Guidance` subsection. This
is intentional, because the Source Repositories table has no Deployment Context column.

---

## Creation and linkage sequence (simulated, confirmation required)

1. Create Task 1, then post its description digest comment
   (`[sdlc-workflow] Description digest: sha256-md:<hex>`) before any link.
2. Create Task 2, then post its description digest comment.
3. Links: TC-8001 → Task 1 (`Related`), TC-8001 → Task 2 (`Related`), Task 1 → Task 2 (`Blocks`).
4. Comment on TC-8001 (with Comment Footnote):
   ```
   Preemptive remediation tasks created for streams without CVE Jiras:
   - 2.1.x: <Task 1 key>, <Task 2 key> (security-preemptive)

   These tasks use the "Related" link type and carry the security-preemptive
   label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
   reconciliation will link them and remove the label.
   ```

## Pre-creation checklist

- [x] Task count per stream: 2.1.x Cargo gets 2 tasks; 2.2.x gets 0 (fix already shipped in 2.2.3+)
- [x] Cross-stream coverage: 2.1.x has preemptive tasks
- [x] Link types: Related (preemptive to originating CVE), Blocks (upstream to downstream)
- [x] Preemptive labels: `security-preemptive` on both 2.1.x tasks
- [x] Coordination guidance: omitted because there is no Deployment Context column (rhtpa-backend defaults to `upstream`)
- [x] Release Jira linking: not applied to preemptive tasks
- [x] Dedup consistency: no dedup (Step 7.5.3 has no matching component field configured)

## Post-Triage Summary (simulated)

- Add label `ai-cve-triaged` to TC-8001.
- Summary comment on TC-8001 containing: the version impact table; the Affects Versions
  correction (RHTPA 2.0.0 → RHTPA 2.2.0, 2.2.1, 2.2.2); the outcome (2.2.x already fixed
  in RHTPA 2.2.3, with preemptive 2.1.x remediation tasks created); the task keys; no
  release Jira or dedup results; an ADF @mention of the TC-8001 reporter; and the
  Comment Footnote.
