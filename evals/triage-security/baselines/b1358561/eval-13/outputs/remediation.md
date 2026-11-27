# TC-8001 — Steps 4–8 Remediation Plan (CVE-2026-31812, quinn-proto < 0.11.14)

No Jira calls were made. Every mutation below is a **proposed** action that would run only after explicit engineer confirmation.

## Pre-remediation checks (Steps 4–7.5)

| Step | Result |
|------|--------|
| 4 Sibling search | Would run `project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8001`. No sibling data was supplied, so I assume **no sibling exists for 2.1.x** and no same-stream duplicate exists. |
| 4.3 Cross-CVE overlap | Skipped because the Upstream Affected Component field is not configured. |
| 4.4 Preemptive reconciliation | No existing `security-preemptive` tasks are known. |
| 5 Lifecycle | Product pages were not fetched (external calls are forbidden). 2.1.x and 2.2.x are treated as supported because both are configured streams. The engineer should verify. |
| 6 Already fixed | No resolved siblings are known, so this check does not apply. |
| 7 Concurrent triage | Skipped because the Upstream Affected Component field is not configured. |
| 7.5 Release Jira | Find or create "RHTPA 2.2.5 Release Tasks" Epic + "RHTPA 2.2.5 CVE triage" Task. The default is the next patch after the latest matrix release, 2.2.4. Each needs individual confirmation. 7.5.3 dedup is skipped because there is no Upstream Affected Component field. The 2.1.x tasks are preemptive and are not linked to release Jira. |

## Decision

- Scoped issue (2.2.x). In-scope versions 2.2.0, 2.2.1, and 2.2.2 are affected, so this is **Case B**.
- Stream 2.1.x (2.1.0, 2.1.1) is also affected and has no known CVE Jira, so this is **Case A**: a cross-stream comment plus **preemptive** tasks.
- Ecosystem: Cargo (source dependency), so each stream gets **2 tasks**.
  - 2.2.x: upstream `release/0.4.z` already ships 0.11.14 (Step 2.5), so it uses the **dependency bump + downstream propagation** variant.
  - 2.1.x: no upstream fix evidence on `release/0.3.z`, so it uses **upstream backport + downstream propagation**.
- Security level: TC-8001 shows none. Before each `create_issue`, re-read it live with `jira.get_issue(TC-8001, fields=["security"])`. If a level is set, pass `security: {id, name}` on every create. Otherwise omit it.
- Engineer caveat for 2.2.x: 2.2.3 and 2.2.4 already ship the fix. Tasks 1 and 2 may close quickly as verify-only. They are kept because the skill's Case B rule creates tasks for an affected scoped stream.

### Pre-creation checklist
- [x] Task count per stream: 2 (Cargo)
- [x] Cross-stream coverage: 2.1.x is covered by preemptive tasks
- [x] Link types: Depend (2.2.x to TC-8001), Related (2.1.x preemptive to TC-8001), Blocks (upstream/bump to downstream)
- [x] Preemptive labels on both 2.1.x tasks
- [x] Coordination guidance: omitted (no Deployment Context column)
- [x] Release Jira linking: 2.2.x non-preemptive tasks Block the release Task; TC-8001 is Related to it
- [x] Dedup consistency: not applicable

---

## Task 1 (2.2.x): Dependency bump

- **Summary:** `Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`
- **Issue type:** Task, project TC

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream —
a package manager update is sufficient.

quinn-proto before 0.11.14 does not validate the number of streams requested in a
STREAMS frame; a remote attacker can trigger unbounded stream-state allocation and a
panic (denial of service, CVSS 7.5).

Affected versions: RHTPA 2.2.0 (quinn-proto 0.11.9), RHTPA 2.2.1 (0.11.12), RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8 (backend tags from supportability matrix)
Not affected: RHTPA 2.2.3 (v0.4.11) and 2.2.4 (v0.4.12) already ship quinn-proto 0.11.14

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: unverified — confirm with `cargo tree -i quinn-proto` (likely transitive via quinn)
- **Remediation action**: run the appropriate package manager update command:
  - **Cargo**: `cargo update -p quinn-proto` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update
- Released tags v0.4.11/v0.4.12 on this branch already contain quinn-proto 0.11.14;
  if release/0.4.z HEAD already resolves >= 0.11.14, record that and close as no-op
- If the vulnerable dependency is dev-only or build-only, the remediation priority
  is Normal regardless of CVE severity. Add `dev-dependency` label to the task.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

**Description digest steps (run right after creating Task 1, before any link or other comment):**
1. `bump_task = jira.create_issue(projectKey: "TC", issueTypeName: "Task", summary: <above>, description: <above>, labels: [...], security: <TC-8001 level if any>)` returns `<T1>`.
2. Re-fetch the stored description: `jira.get_issue(<T1>, fields=["description"])`. Do not hash the string passed to `create_issue`, because Jira normalizes stored content.
3. Write the fetched description to `/tmp/task-desc.md`. This is markdown from MCP, or ADF JSON from the REST fallback.
4. Run `python3 scripts/sha256-digest.py /tmp/task-desc.md`, check that the exit code is 0, and capture the full tagged output (`sha256-md:<64 hex>` or `sha256-adf:<64 hex>`).
5. Post a **standalone** ADF comment on `<T1>` whose body is exactly one line: `[sdlc-workflow] Description digest: <full tagged digest from step 4>`. Do not add extra text. Do not use a placeholder or truncated hash. Keep the format tag. The literal hash is computed at runtime, so it is not shown here.
6. Only after the digest comment exists, continue to Task 2.

---

## Task 2 (2.2.x): Downstream propagation (blocked by Task 1)

- **Summary:** `Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <T1>.

The dependency bump (<T1>) bumps quinn-proto to 0.11.14 on release/0.4.z.
Once that PR merges, update the source pinning in this Konflux release repo so
the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: unverified (likely transitive) — carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- The current pin `v0.4.12` (RHTPA 2.2.4) already ships quinn-proto 0.11.14; if <T1>
  closes as no-op, verify the pin is >= v0.4.11 and close this task accordingly
- If the upstream fix pinned a transitive dependency directly (fallback approach),
  verify the pinning is reflected in the downstream build's lock file after the
  source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <T1> (upstream dependency bump must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Description digest steps (right after creating Task 2, before any link or comment):**
1. `jira.create_issue(...)` returns `<T2>`.
2. `jira.get_issue(<T2>, fields=["description"])`, then write the result to `/tmp/task-desc.md`.
3. `python3 scripts/sha256-digest.py /tmp/task-desc.md`. Check that the exit code is 0 and capture the full tagged digest.
4. Post a standalone comment on `<T2>`: `[sdlc-workflow] Description digest: <tagged digest>`.

---

## Task 3 (2.1.x, preemptive): Upstream backport

- **Summary:** `Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (remote DoS).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (quinn-proto 0.11.9), RHTPA 2.1.1 (quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12 (backend tags from supportability matrix)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: unverified — confirm with `cargo tree -i quinn-proto` (likely transitive via quinn)
- If the vulnerable dependency is dev-only or build-only, the remediation priority
  is Normal regardless of CVE severity. Add `dev-dependency` label to the task.

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

When the vulnerable package is a **transitive** dependency (pulled in
through intermediate packages), use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (e.g., quinn / reqwest)
- Bump the direct dependency to a version whose transitive closure
  includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes to the
  direct dependency

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable:
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

**Description digest steps (right after creating Task 3, before the Related/Blocks links or any comment):**
1. `jira.create_issue(..., labels: [..., "security-preemptive"], security: <TC-8001 level if any>)` returns `<T3>`.
2. `jira.get_issue(<T3>, fields=["description"])`, then write the result to `/tmp/task-desc.md`.
3. `python3 scripts/sha256-digest.py /tmp/task-desc.md`. Check that the exit code is 0 and capture the full tagged digest.
4. Post a standalone comment on `<T3>`: `[sdlc-workflow] Description digest: <tagged digest>`.

---

## Task 4 (2.1.x, preemptive): Downstream propagation (blocked by Task 3)

- **Summary:** `Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)`
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

```
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
CVE-2026-31812 fix from <T3>.

The upstream backport (<T3>) bumps quinn-proto to 0.11.14 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release repo so
the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: unverified (likely transitive) — carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback approach),
  verify the pinning is reflected in the downstream build's lock file after the
  source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <T3> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Description digest steps (right after creating Task 4, before any link or comment):**
1. `jira.create_issue(...)` returns `<T4>`.
2. `jira.get_issue(<T4>, fields=["description"])`, then write the result to `/tmp/task-desc.md`.
3. `python3 scripts/sha256-digest.py /tmp/task-desc.md`. Check that the exit code is 0 and capture the full tagged digest.
4. Post a standalone comment on `<T4>`: `[sdlc-workflow] Description digest: <tagged digest>`.

---

## Linking (only after each task's digest comment is posted)

| # | Link | Type |
|---|------|------|
| 1 | TC-8001 (inward) to `<T1>` (outward) | Depend |
| 2 | TC-8001 to `<T2>` | Depend |
| 3 | `<T1>` to `<T2>` | Blocks |
| 4 | TC-8001 to `<T3>` | Related (preemptive) |
| 5 | TC-8001 to `<T4>` | Related (preemptive) |
| 6 | `<T3>` to `<T4>` | Blocks |
| 7 | `<T1>`, `<T2>` (inward) to release Task "RHTPA 2.2.5 CVE triage" (outward) | Blocks |
| 8 | release Task (inward) to TC-8001 (outward) | Related |

## Other TC-8001 mutations (each confirmed; every comment ends with the Comment Footnote)

Footnote: a horizontal rule, then "This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0."

1. Step 0.8: assign to the current user and transition New to Assigned.
2. Step 3: `edit_issue(TC-8001, versions=[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2])` using dynamically discovered IDs. Comment: "Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]. Based on lock file analysis at pinned commits from security-matrix.md. Scoped to stream 2.2.x per issue suffix." No ProdSec @mention because it is not configured.
3. Case A cross-stream comment: "Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x based on lock file analysis. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage."
4. Case A preemptive-task comment, posted after T3 and T4 have their digests and links: "Preemptive remediation tasks created for streams without CVE Jiras: 2.1.x: `<T3>`, `<T4>` (security-preemptive) ..."
5. Remediation-task comment: "Remediation tasks created: `<T1>` (dependency bump), `<T2>` (downstream propagation, blocked by `<T1>`)."
6. Transition to In Progress, skipped if TC-8001 is already Assigned (indeterminate category) or later.
7. Add label `ai-cve-triaged`.
8. Post-triage summary comment: version impact table, Affects Versions correction, outcome (Case B + Case A), task keys T1–T4, release Epic/Task keys, dedup "none", and an ADF mention of the TC-8001 reporter (account ID from issue data, which was not present in the mock), followed by the footnote.
