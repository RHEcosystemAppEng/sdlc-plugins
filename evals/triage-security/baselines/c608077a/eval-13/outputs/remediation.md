# Step 8 – Remediation: TC-8001 (CVE-2026-31812, quinn-proto < 0.11.14)

## Decision

- The issue is scoped to **2.2.x**, where 2.2.0, 2.2.1 and 2.2.2 are affected. That makes this **Case B**.
- Another stream, **2.1.x** (2.1.0 and 2.1.1), is also affected. That makes this **Case A** as well: post a cross-stream comment and create preemptive tasks, assuming no 2.1.x CVE Jira exists.
- Ecosystem is Cargo, a source dependency, so each stream gets **2 tasks**:
  - 2.2.x: the upstream fix is already available, so use the **dependency bump + downstream propagation** variant.
  - 2.1.x: the upstream fix is not available, so use **upstream backport + downstream propagation**, with the preemptive variant.
- Step 7.5 (release Jira): find or create the "RHTPA 2.2.x Release Tasks" Epic and its "CVE triage" Task. Each needs individual confirmation and the exact version comes from Jira version discovery. Non-preemptive 2.2.x tasks would then be linked to the release Task (Blocks), and TC-8001 would be linked to it (Related). Step 7.5.3 dedup is skipped because Upstream Affected Component is not configured.
- Labels on every task: `ai-generated-jira`, `Security`, `CVE-2026-31812`. Preemptive tasks also get `security-preemptive`.
- Coordination Guidance subsection is omitted because the Source Repositories table has no Deployment Context column (backward-compat rule).
- Note for the engineer: 2.2.3 and later already ship quinn-proto 0.11.14. For 2.2.x, Task 1 is mostly verification that `release/0.4.z` stays at 0.11.14 or higher, and Task 2 confirms the Konflux reference points at a fixed tag. The engineer may decline these two at the confirmation gate.

Every Jira mutation below needs engineer confirmation first. None of them were executed here.

---

## Task 1 – 2.2.x Dependency bump

**Summary**: `Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x)`
**Labels**: `["ai-generated-jira", "Security", "CVE-2026-31812"]`

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream —
a package manager update is sufficient.

Affected versions: RHTPA 2.2.0 (v0.4.5, quinn-proto 0.11.9), RHTPA 2.2.1 (v0.4.8, quinn-proto 0.11.12), RHTPA 2.2.2 (retag of 2.2.1, v0.4.8)
Source commit(s): v0.4.5, v0.4.8
Not affected: RHTPA 2.2.3 (v0.4.11) and RHTPA 2.2.4 (v0.4.12) already ship quinn-proto 0.11.14

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend (workspace) → quinn → quinn-proto; verify exact chain with `cargo tree -i quinn-proto`)
- **Remediation action**: run the appropriate package manager update command:
  - **Cargo**: `cargo update -p quinn-proto` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update (latest tags v0.4.11/v0.4.12
  already resolve 0.11.14 — confirm branch HEAD has not regressed)
- If the vulnerable dependency is dev-only or build-only (identified
  in Step 2.3.5), the remediation priority is Normal regardless of CVE
  severity. Add `dev-dependency` label to the task.

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

### Task 1 – Description digest comment steps (right after creation, before any link or other comment)

1. `bump_task = jira.create_issue(projectKey: "TC", issueTypeName: "Task", summary: ..., description: <above>, labels: [...])`, which returns `<T1-key>`.
2. Re-fetch the stored description: `jira.get_issue(<T1-key>, fields=["description"])`. Do not hash the string passed to `create_issue`, because Jira normalizes content.
3. Write the fetched description to a temp file, e.g. `/tmp/task-desc.md`.
4. Compute the digest: `python3 scripts/sha256-digest.py /tmp/task-desc.md`. Check the exit code. The output is `sha256-md:<64 hex>` for MCP markdown or `sha256-adf:<64 hex>` for REST ADF JSON.
5. Post a standalone ADF comment on `<T1-key>` whose body is exactly one line: `[sdlc-workflow] Description digest: <full tagged digest output>`. Keep the tag. Do not use a placeholder, an abbreviated hash, or extra text.
6. Only after that, create the links:
   - `TC-8001 → <T1-key>`, type `Depend` (inward TC-8001, outward T1)
   - `<T1-key> → <2.2.x release Task>`, type `Blocks` (if Step 7.5 is active)

---

## Task 2 – 2.2.x Downstream propagation

**Summary**: `Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)`
**Labels**: `["ai-generated-jira", "Security", "CVE-2026-31812"]`

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <T1-key>.

The dependency bump (<T1-key>) bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: transitive — carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
  (current pin v0.4.12 already ships quinn-proto 0.11.14; confirm no regression)
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

- Depends on: <T1-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Task 2 – Description digest comment steps

1. `downstream_task = jira.create_issue(...)`, which returns `<T2-key>`.
2. `jira.get_issue(<T2-key>, fields=["description"])`, then write the result to `/tmp/task-desc.md`.
3. `python3 scripts/sha256-digest.py /tmp/task-desc.md`, which outputs the tagged digest.
4. `jira.add_comment(<T2-key>, "[sdlc-workflow] Description digest: <tagged-digest>")` as a standalone single-line ADF comment.
5. Then create the links:
   - `TC-8001 → <T2-key>`, type `Depend`
   - `<T1-key> → <T2-key>`, type `Blocks` (downstream is blocked by the bump)
   - `<T2-key> → <2.2.x release Task>`, type `Blocks` (if Step 7.5 is active)

---

## Task 3 – 2.1.x Upstream backport (PREEMPTIVE)

**Summary**: `Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)`
**Labels**: `["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]`

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

Remediate CVE-2026-31812: quinn-proto panic (DoS) on QUIC frames creating an
excessive number of streams. The vulnerable dependency (quinn-proto < 0.11.14)
must be updated to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (v0.3.8, quinn-proto 0.11.9), RHTPA 2.1.1 (v0.3.12, quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: transitive (chain: backend (workspace) → quinn → quinn-proto; verify exact chain with `cargo tree -i quinn-proto`)
- If the vulnerable dependency is dev-only or build-only (identified
  in Step 2.3.5), the remediation priority is Normal regardless of CVE
  severity. Add `dev-dependency` label to the task.

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (see dependency
  chain above)
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

### Task 3 – Description digest comment steps

1. `upstream_task = jira.create_issue(..., labels: [..., "security-preemptive"])`, which returns `<T3-key>`.
2. `jira.get_issue(<T3-key>, fields=["description"])`, then write the result to `/tmp/task-desc.md`.
3. `python3 scripts/sha256-digest.py /tmp/task-desc.md`, which outputs the tagged digest.
4. `jira.add_comment(<T3-key>, "[sdlc-workflow] Description digest: <tagged-digest>")` as a standalone single-line ADF comment.
5. Then create the link `TC-8001 → <T3-key>`, type **`Related`**. It is preemptive and the originating CVE belongs to a different stream. No release Task link is needed because the task is preemptive.

---

## Task 4 – 2.1.x Downstream propagation (PREEMPTIVE)

**Summary**: `Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)`
**Labels**: `["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]`

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
CVE-2026-31812 fix from <T3-key>.

The upstream backport (<T3-key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: transitive — carried forward from upstream task
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

- Depends on: <T3-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Task 4 – Description digest comment steps

1. `downstream_task = jira.create_issue(..., labels: [..., "security-preemptive"])`, which returns `<T4-key>`.
2. `jira.get_issue(<T4-key>, fields=["description"])`, then write the result to `/tmp/task-desc.md`.
3. `python3 scripts/sha256-digest.py /tmp/task-desc.md`, which outputs the tagged digest.
4. `jira.add_comment(<T4-key>, "[sdlc-workflow] Description digest: <tagged-digest>")` as a standalone single-line ADF comment.
5. Then create the links:
   - `TC-8001 → <T4-key>`, type `Related`
   - `<T3-key> → <T4-key>`, type `Blocks`

No digest values appear in this file. A real digest has to be computed by
`scripts/sha256-digest.py` from the description re-fetched after creation in Jira.
Inventing or hardcoding a hash is prohibited by `shared/description-digest-protocol.md`.

---

## Comments on TC-8001 (after all task links). Each ends with the Comment Footnote.

1. **Cross-stream impact** (Case A):
   > Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x (RHTPA 2.1.0, 2.1.1 ship quinn-proto 0.11.9) based on lock file analysis. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.
2. **Preemptive task list**:
   > Preemptive remediation tasks created for streams without CVE Jiras:
   > - 2.1.x: <T3-key>, <T4-key> (security-preemptive)
   >
   > These tasks use the "Related" link type and carry the security-preemptive label. When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link them and remove the label.
3. **Remediation task list**:
   > Remediation tasks created: <T1-key> (dependency bump), <T2-key> (downstream propagation, blocked by <T1-key>)
4. **Post-triage summary**: covers the version impact table, the Affects Versions correction `[RHTPA 2.0.0] → [RHTPA 2.2.0, 2.2.1, 2.2.2]`, the outcome (remediation created), T1–T4 keys, release Epic/Task keys, a note that no dedup applied, and an ADF @mention of the TC-8001 reporter.

Footnote appended to every comment (ADF rule + paragraph):
> ---
> This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0.

## Remaining TC-8001 updates

- Transition to Assigned/In Progress if not already in an indeterminate-category status.
- Assign to the current user.
- Add the `ai-cve-triaged` label.
