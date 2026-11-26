# Step 8 – Remediation: TC-8001 (CVE-2026-31812, quinn-proto)

## Decision

- The issue is **scoped** to 2.2.x, and 2.2.x versions 2.2.0, 2.2.1 and 2.2.2 are affected. This is **Case B**: create remediation tasks for 2.2.x.
- Another stream, 2.1.x (2.1.0, 2.1.1), is also affected. This is **Case A**: post a cross-stream impact comment. No sibling CVE Jira for 2.1.x was found (assumed), so **preemptive** tasks are created for 2.1.x.
- Ecosystem: Cargo is a **source dependency**, so each stream gets **2 tasks**: an upstream backport and a downstream propagation task. The downstream task is blocked by the upstream task.
- Step 7.5.3 dedup: not applicable, because the Upstream Affected Component field is not configured.
- Security level: every `create_issue` passes `security: <TC-8001 security level {id, name}>`, read live from `jira.get_issue(TC-8001)`. It is omitted only if TC-8001 has no level.
- Coordination guidance: the Source Repositories table has no Deployment Context column, so per the backward-compatibility rule the Coordination Guidance subsection is **omitted**.

Note for the engineer: 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14, so the latest 2.2.x release is fixed. The 2.2.x tasks still record the work against `release/0.4.z`. If the engineer confirms that branch HEAD is already at 0.11.14 or later, switch Task 1 to the dependency bump variant, or treat it as a verification-only task.

### Pre-creation checklist
- [x] Task count per stream: 2 (source dependency) for 2.2.x and 2 for 2.1.x
- [x] Cross-stream coverage: 2.1.x gets preemptive tasks
- [x] Link types: Depend (TC-8001 → 2.2.x tasks), Related (TC-8001 → 2.1.x preemptive tasks), Blocks (upstream → downstream in each stream)
- [x] Preemptive labels: `security-preemptive` on both 2.1.x tasks
- [x] Coordination guidance: omitted (no Deployment Context column)
- [x] Release Jira linking: 2.2.x tasks Block the release Task, and TC-8001 is Related to the release Task. Preemptive tasks are not linked.
- [x] Dedup consistency: N/A

All Jira mutations below need explicit engineer confirmation. None were executed in this eval.

---

## Task 1 – Upstream backport (2.2.x)

**Summary:** `Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)`
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`

```markdown
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (remote DoS via
a crafted STREAMS frame causing unbounded stream state allocation).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (quinn-proto 0.11.9), RHTPA 2.2.1 (0.11.12), RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend → ... → quinn → quinn-proto; confirm exact chain from Cargo.lock)
- Note: release tags v0.4.11 and v0.4.12 on this branch already resolve quinn-proto 0.11.14; first verify `release/0.4.z` HEAD — if already >= 0.11.14, no code change is needed beyond confirming the lock file.

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (see dependency chain above)
- Bump the direct dependency to a version whose transitive closure includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes to the direct dependency

**Fallback: pin the transitive dependency directly**
- Cargo: `cargo add quinn-proto@0.11.14` (or `cargo update -p quinn-proto --precise 0.11.14`)
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

## Task 2 – Downstream propagation (2.2.x)

**Summary:** `Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)`
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`

```markdown
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <upstream-task-key from Task 1>.

The upstream backport (<upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
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

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

## Task 3 – Upstream backport, PREEMPTIVE (2.1.x)

**Summary:** `Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)`
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

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

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (remote DoS).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (quinn-proto 0.11.9), RHTPA 2.1.1 (0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: transitive (chain: backend → ... → quinn → quinn-proto; confirm exact chain from Cargo.lock)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto
- Bump it to a version whose transitive closure includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes

**Fallback: pin the transitive dependency directly**
- Cargo: `cargo add quinn-proto@0.11.14`
- Document why the direct dep bump was not viable in the PR description

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (originating tracking issue, stream 2.2.x — Related link)
```

## Task 4 – Downstream propagation, PREEMPTIVE (2.1.x)

**Summary:** `Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)`
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

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
CVE-2026-31812 fix from <upstream-task-key from Task 3>.

The upstream backport (<upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: transitive — carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the pinning is reflected in the downstream build's lock file
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (originating tracking issue — Related link)
```

---

## Execution sequence with description digest comments

Digest protocol (`shared/description-digest-protocol.md`), applied to **every** task:
1. Create the task with `jira.create_issue(...)`.
2. **Re-fetch** the stored description from Jira with `jira.get_issue(<key>, fields=["description"])`. Do **not** hash the string passed to `create_issue`, because Jira normalizes content on storage.
3. Write the re-fetched description to a temp file and compute the digest with `python3 scripts/sha256-digest.py /tmp/task-desc.md`. Check that the exit code is 0. The output is format-tagged: `sha256-md:<64-hex>` from the MCP/markdown path, or `sha256-adf:<64-hex>` from the REST/ADF path. Never compute SHA-256 by hand, never abbreviate, and never use a placeholder.
4. Post a **standalone** ADF comment whose single line is exactly `[sdlc-workflow] Description digest: <tagged-digest>`, including the tag. Nothing else goes on that line, and it is not merged into any other comment.
5. Only **after** the digest comment is posted, create issue links or other comments involving that task.

### Ordered steps

```
# --- Stream 2.2.x (Case B, standard) ---

# 1. Upstream backport task
up22 = jira.create_issue(projectKey: "TC", issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)",
  description: <Task 1 description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"],
  security: <TC-8001 security level>)
# 1a. Digest (before any link/comment)
desc = jira.get_issue(<up22-key>, fields=["description"])      # re-fetch stored description
#     write desc → /tmp/task-desc.md
python3 scripts/sha256-digest.py /tmp/task-desc.md              # → sha256-md:<64-hex> | sha256-adf:<64-hex>
jira.add_comment(<up22-key>, "[sdlc-workflow] Description digest: <tagged-digest>")

# 2. Downstream propagation task (description references <up22-key>)
down22 = jira.create_issue(projectKey: "TC", issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)",
  description: <Task 2 description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"],
  security: <TC-8001 security level>)
# 2a. Digest (before any link/comment)
desc = jira.get_issue(<down22-key>, fields=["description"])
#     write desc → /tmp/task-desc.md
python3 scripts/sha256-digest.py /tmp/task-desc.md
jira.add_comment(<down22-key>, "[sdlc-workflow] Description digest: <tagged-digest>")

# 3. Links — only after both digests are posted
jira.create_link(inwardIssue: "TC-8001",    outwardIssue: <up22-key>,   type: "Depend")
jira.create_link(inwardIssue: "TC-8001",    outwardIssue: <down22-key>, type: "Depend")
jira.create_link(inwardIssue: <up22-key>,   outwardIssue: <down22-key>, type: "Blocks")
# Release Jira (if Step 7.5 produced a release Task)
jira.create_link(inwardIssue: <up22-key>,   outwardIssue: <release-task-key>, type: "Blocks")
jira.create_link(inwardIssue: <down22-key>, outwardIssue: <release-task-key>, type: "Blocks")
jira.create_link(inwardIssue: <release-task-key>, outwardIssue: "TC-8001", type: "Related")

# --- Stream 2.1.x (Case A, preemptive) ---

# 4. Cross-stream impact comment on TC-8001 (with Comment Footnote)
jira.add_comment("TC-8001", "Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s)
  2.1.x based on lock file analysis. These streams are tracked by companion issues
  (see Related links) or may require separate PSIRT triage." + footnote)

# 5. Preemptive upstream backport task
up21 = jira.create_issue(projectKey: "TC", issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)",
  description: <Task 3 description with preemptive prefix>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"],
  security: <TC-8001 security level>)
# 5a. Digest (before any link/comment)
desc = jira.get_issue(<up21-key>, fields=["description"])
python3 scripts/sha256-digest.py /tmp/task-desc.md
jira.add_comment(<up21-key>, "[sdlc-workflow] Description digest: <tagged-digest>")

# 6. Preemptive downstream propagation task
down21 = jira.create_issue(projectKey: "TC", issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <Task 4 description with preemptive prefix>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"],
  security: <TC-8001 security level>)
# 6a. Digest (before any link/comment)
desc = jira.get_issue(<down21-key>, fields=["description"])
python3 scripts/sha256-digest.py /tmp/task-desc.md
jira.add_comment(<down21-key>, "[sdlc-workflow] Description digest: <tagged-digest>")

# 7. Links — only after both digests are posted
jira.create_link(inwardIssue: "TC-8001",  outwardIssue: <up21-key>,   type: "Related")
jira.create_link(inwardIssue: "TC-8001",  outwardIssue: <down21-key>, type: "Related")
jira.create_link(inwardIssue: <up21-key>, outwardIssue: <down21-key>, type: "Blocks")

# 8. Preemptive task-list comment on TC-8001 (with footnote)
"Preemptive remediation tasks created for streams without CVE Jiras:
 - 2.1.x: <up21-key>, <down21-key> (security-preemptive) ..."

# --- Wrap-up ---
# 9. Transition TC-8001: skip if already in Assigned (indeterminate) or later; otherwise In Progress
# 10. Remediation task list comment on TC-8001 (with footnote):
#     "Remediation tasks created: <up22-key> (upstream backport), <down22-key>
#      (downstream propagation, blocked by <up22-key>)"
# 11. Add label `ai-cve-triaged` to TC-8001
# 12. Post-triage summary comment on TC-8001: version impact table, Affects Versions
#     correction (RHTPA 2.0.0 → RHTPA 2.2.0, 2.2.1, 2.2.2), outcome, all task keys,
#     release Epic/Task keys, dedup results (none), ADF @mention of the TC-8001 reporter,
#     and the Comment Footnote.
```

The `<tagged-digest>` value is shown here as a placeholder only because no task was actually created in this eval. A real run posts the full 64-hex, format-tagged output from `scripts/sha256-digest.py`.

### Comment Footnote (appended to every non-digest comment)

ADF `rule` node followed by the paragraph: "This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0."
