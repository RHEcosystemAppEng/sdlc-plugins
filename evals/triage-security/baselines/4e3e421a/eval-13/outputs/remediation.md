# TC-8001 — Steps 3–8: Triage Operations and Remediation

Nothing below was executed. Every Jira mutation is a **planned** operation that needs the engineer's explicit
confirmation in a live interactive run. Placeholder keys (`<T1>`, `<T2>`, ...) are used because no Jira issues
were created, and no keys are invented.

---

## Step 3 — Affects Versions correction (planned)

| | Value |
|---|---|
| Current (PSIRT) | RHTPA 2.0.0 |
| Proposed (scoped to 2.2.x) | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |
| Rationale | Lock files at the pinned tags show quinn-proto 0.11.9 (v0.4.5) and 0.11.12 (v0.4.8, also used by the 2.2.2 retag), both below 0.11.14. Tags v0.4.11 and v0.4.12 (2.2.3, 2.2.4) ship 0.11.14. RHTPA 2.0.0 is not in the supportability matrix. |

Version IDs would be looked up at runtime with `getJiraIssueTypeMetaWithFields` (issue type 10024). No IDs are hardcoded.
Planned: `jira.edit_issue(TC-8001, versions=[...])`, followed by a correction comment that includes the Comment Footnote
(sdlc-workflow/triage-security v0.13.10). The comment has no ProdSec @mention because no ProdSec account ID is configured.

## Step 4 — Duplicate, sibling, overlap and reconciliation check

- Sibling JQL (planned): `project = TC AND issuetype = 10024 AND labels = "CVE-2026-31812" AND key != TC-8001`.
  The eval data contains no sibling issues, so I assume none exist. That means **no 2.1.x CVE Jira exists**, and Case A
  creates preemptive tasks for 2.1.x.
- Step 4.3 cross-CVE overlap: skipped because the Upstream Affected Component field is not configured.
- Step 4.4 preemptive reconciliation: no existing `security-preemptive` tasks appear in the eval data.

## Step 5 — Lifecycle check

The lifecycle page (https://access.example.com/product-life-cycle/rhtpa) was not fetched. Both 2.1.x and 2.2.x are
assumed to be in support because both appear in the supportability matrix. The engineer should verify this.

## Step 6 — Already fixed check

No resolved sibling issues exist, so there is no already-fixed scenario. The later 2.2.x releases (2.2.3, 2.2.4) already
ship 0.11.14. This is recorded as context, but the affected released versions 2.2.0–2.2.2 remain in the impact table.

## Step 7 — Concurrent triage detection

Skipped because the Upstream Affected Component field is not configured.

## Step 7.5 — Release Jira orchestration (planned, unresolved in eval)

The stream-to-release-version mapping needs Jira version data, which this eval does not provide. In a live run, the
skill would search for or create `"RHTPA <next-2.2.z> Release Tasks"` (Epic) and `"RHTPA <next-2.2.z> CVE triage"`
(child Task), confirming each one individually. **Treated as unresolved/skipped here.** Remediation tasks are still
created. The release-linking steps (remediation -> release Task `Blocks`, CVE -> release Task `Related`) are listed
below as conditional. Preemptive (2.1.x) tasks are not linked to release Jira. The cross-CVE dedup check (7.5.3) is
not applicable because the Upstream Affected Component field is not configured.

---

## Step 8 — Decision

- Supported versions affected: **yes**.
- The issue is **scoped** (`[rhtpa-2.2]`) and another stream (2.1.x) is also affected, which gives
  **Case A** (cross-stream comment + preemptive tasks for 2.1.x) **plus Case B** (standard tasks for 2.2.x).
- Ecosystem: Cargo, a source dependency, so each stream gets **2 tasks**: upstream backport + downstream propagation.
- Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`. The 2.1.x tasks also get `security-preemptive`.
  There is no `dev-dependency` label because there is no evidence of a dev-only scope.

### Pre-creation checklist

- [x] Task count per stream = 2 (Cargo source dependency)
- [x] Cross-stream coverage: 2.1.x gets preemptive tasks (no sibling CVE Jira found)
- [x] Link types: Depend (2.2.x tasks <-> TC-8001), Related (2.1.x preemptive tasks <-> TC-8001), Blocks (upstream -> downstream)
- [x] Preemptive label on 2.1.x tasks
- [x] Coordination guidance: omitted because the Source Repositories table has no Deployment Context column
- [x] Release Jira linking: conditional (Step 7.5 unresolved)
- [x] Dedup consistency: N/A

---

## Task T1 — 2.2.x upstream backport

**Summary:** `Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)`
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`

```markdown
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (remote DoS via a crafted QUIC STREAMS frame).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (quinn-proto 0.11.9), RHTPA 2.2.1 (0.11.12), RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8 (2.2.2 is a backend retag of v0.4.8)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: undetermined from triage evidence. Run `cargo tree -i quinn-proto` to classify it as direct or transitive.
- Tags v0.4.11 and v0.4.12 already ship quinn-proto 0.11.14. Check whether release/0.4.z HEAD already contains the fix.
  If it does, this task reduces to confirming the lock file and tagging a release.
- If the vulnerable dependency is dev-only or build-only, the remediation priority is Normal regardless of CVE
  severity. Add the `dev-dependency` label to the task.

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (e.g., quinn / reqwest; confirm with cargo tree)
- Bump the direct dependency to a version whose transitive closure includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes to the direct dependency

**Fallback: pin the transitive dependency directly**
- Cargo: `cargo add quinn-proto@0.11.14` to add it as a direct dependency, overriding the transitive resolution
- Document why the direct dependency bump was not viable in the PR description

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

### T1 — creation and description digest steps (in order)

1. **Create:** `jira.create_issue(projectKey: "TC", issueTypeName: "Task", summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)", description: <T1 description>, labels: ["ai-generated-jira","Security","CVE-2026-31812"])` returns `<T1>`.
2. **Re-fetch the stored description** (do NOT hash the string passed to `create_issue`, because Jira normalizes content on storage):
   `jira.get_issue(<T1>, fields=["description"])`
3. **Write the fetched description to a temp file**, e.g. `/tmp/task-desc.md`. MCP returns markdown. The REST fallback returns ADF JSON.
4. **Compute the digest with the script** (never by hand):
   `python3 scripts/sha256-digest.py /tmp/task-desc.md`
   The script outputs `sha256-md:<64-hex>` for markdown or `sha256-adf:<64-hex>` for ADF. Check that the exit code is 0 and that the value has the full 64 hex characters. Keep the format tag.
5. **Post the standalone digest comment** on `<T1>` immediately, as a single-line ADF paragraph:
   `jira.add_comment(<T1>, "[sdlc-workflow] Description digest: <tagged-digest from step 4>")`
   This comment is separate from any footnoted summary comment. It contains no extra text, no placeholder, and no abbreviated hash.
6. **Only after the digest comment exists:** create T1's links (Step 8 linkage below).

---

## Task T2 — 2.2.x downstream propagation (blocked by T1)

**Summary:** `Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)`
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`

```markdown
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <T1>.

The upstream backport (<T1>) bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: backend is pinned via `artifacts.lock.yaml` (download URL contains the tag, e.g., `v0.4.12`)
- **Dependency type**: carried forward from <T1> (undetermined at triage time)
- Update the backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback approach), verify the pinning is reflected
  in the downstream build's lock file after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <T1> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### T2 — creation and description digest steps (in order)

1. **Create:** `jira.create_issue(projectKey: "TC", issueTypeName: "Task", summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)", description: <T2 description with the real <T1> key substituted>, labels: ["ai-generated-jira","Security","CVE-2026-31812"])` returns `<T2>`.
2. **Re-fetch:** `jira.get_issue(<T2>, fields=["description"])`. Hash the stored description, not the create payload.
3. **Write it to** `/tmp/task-desc.md`.
4. **Compute:** `python3 scripts/sha256-digest.py /tmp/task-desc.md` gives `sha256-md:<64-hex>` or `sha256-adf:<64-hex>`. Check the exit code.
5. **Post the standalone digest comment** on `<T2>`:
   `jira.add_comment(<T2>, "[sdlc-workflow] Description digest: <tagged-digest>")`
6. **Only after that:** create T2's links (`Depend` from TC-8001, `Blocks` from T1).

---

## Task T3 — 2.1.x upstream backport (PREEMPTIVE)

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

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (remote DoS via a crafted QUIC STREAMS frame).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (quinn-proto 0.11.9), RHTPA 2.1.1 (0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: undetermined from triage evidence. Run `cargo tree -i quinn-proto` at v0.3.12 to classify it.
- If the vulnerable dependency is dev-only or build-only, the remediation priority is Normal regardless of CVE
  severity. Add the `dev-dependency` label to the task.

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto
- Bump the direct dependency to a version whose transitive closure includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes to the direct dependency

**Fallback: pin the transitive dependency directly**
- Cargo: `cargo add quinn-proto@0.11.14`
- Document why the direct dependency bump was not viable in the PR description

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (originating tracking issue, stream 2.2.x — Related link)
```

### T3 — creation and description digest steps (in order)

1. **Create:** `jira.create_issue(projectKey: "TC", issueTypeName: "Task", summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)", description: <T3 description with preemptive prefix>, labels: ["ai-generated-jira","Security","CVE-2026-31812","security-preemptive"])` returns `<T3>`.
2. **Re-fetch:** `jira.get_issue(<T3>, fields=["description"])`
3. **Write it to** `/tmp/task-desc.md`.
4. **Compute:** `python3 scripts/sha256-digest.py /tmp/task-desc.md` and check the exit code and the full tagged 64-hex output.
5. **Post the standalone digest comment** on `<T3>`: `"[sdlc-workflow] Description digest: <tagged-digest>"`
6. **Only after that:** create the `Related` link from TC-8001.

---

## Task T4 — 2.1.x downstream propagation (PREEMPTIVE, blocked by T3)

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
CVE-2026-31812 fix from <T3>.

The upstream backport (<T3>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: backend is pinned via `artifacts.lock.yaml` (download URL contains the tag, e.g., `v0.3.12`)
- **Dependency type**: carried forward from <T3>
- Update the backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly, verify the pinning is reflected in the downstream
  build's lock file after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <T3> (upstream backport must merge first)
- Depends on: TC-8001 (originating tracking issue, stream 2.2.x — Related link)
```

### T4 — creation and description digest steps (in order)

1. **Create:** `jira.create_issue(... summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)", labels: ["ai-generated-jira","Security","CVE-2026-31812","security-preemptive"])` returns `<T4>`.
2. **Re-fetch:** `jira.get_issue(<T4>, fields=["description"])`
3. **Write it to** `/tmp/task-desc.md`.
4. **Compute:** `python3 scripts/sha256-digest.py /tmp/task-desc.md`
5. **Post the standalone digest comment** on `<T4>`: `"[sdlc-workflow] Description digest: <tagged-digest>"`
6. **Only after that:** create T4's links (`Related` from TC-8001, `Blocks` from T3).

---

## Full ordered execution plan (after engineer confirmation)

Digest comments always come right after each task's creation, **before** any link or other comment that touches that task.

| # | Operation |
|---|---|
| 1 | Create T1 (2.2.x upstream) |
| 2 | Re-fetch T1 description -> `scripts/sha256-digest.py` -> post `[sdlc-workflow] Description digest: <tag>:<hex>` on T1 |
| 3 | Create T2 (2.2.x downstream) |
| 4 | Re-fetch T2 description -> `scripts/sha256-digest.py` -> post digest comment on T2 |
| 5 | Link `Depend`: inward TC-8001 -> outward T1 |
| 6 | Link `Depend`: inward TC-8001 -> outward T2 |
| 7 | Link `Blocks`: inward T1 -> outward T2 |
| 8 | (If release Task exists) `Blocks`: T1 -> release Task, T2 -> release Task. `Related`: release Task -> TC-8001 |
| 9 | Case A: post the cross-stream impact comment on TC-8001 (with footnote): "Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x (2.1.0, 2.1.1 ship 0.11.9) based on lock file analysis. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage." |
| 10 | Create T3 (2.1.x upstream, preemptive) |
| 11 | Re-fetch T3 description -> `scripts/sha256-digest.py` -> post digest comment on T3 |
| 12 | Create T4 (2.1.x downstream, preemptive) |
| 13 | Re-fetch T4 description -> `scripts/sha256-digest.py` -> post digest comment on T4 |
| 14 | Link `Related`: inward TC-8001 -> outward T3. Link `Related`: inward TC-8001 -> outward T4 |
| 15 | Link `Blocks`: inward T3 -> outward T4 |
| 16 | Comment on TC-8001 listing preemptive tasks (with footnote): "Preemptive remediation tasks created for streams without CVE Jiras: - 2.1.x: <T3>, <T4> (security-preemptive) ..." |
| 17 | Transition TC-8001 to In Progress (discover the transition dynamically). The assignee was already set in Step 0.8 |
| 18 | Comment on TC-8001: "Remediation tasks created: <T1> (upstream backport), <T2> (downstream propagation, blocked by <T1>)" (with footnote) |
| 19 | Post-triage: add the `ai-cve-triaged` label to TC-8001 |
| 20 | Post-triage summary comment on TC-8001: version impact table, the Affects Versions correction (2.0.0 -> 2.2.0/2.2.1/2.2.2), outcome (remediation created), links to T1–T4, release Jira refs (unresolved), dedup results (none), an ADF mention of the issue reporter (account ID from issue data), and the Comment Footnote (`sdlc-workflow/triage-security v0.13.10`) |

Notes:
- Digest comments are standalone, single-line comments **without** the footnote, as the digest protocol requires.
  Every other comment above carries the Comment Footnote.
- Each digest value must be freshly computed by `scripts/sha256-digest.py` from the re-fetched description. No digest
  values appear in this document because no tasks were actually created. Writing an example hash would break the protocol.
