# Step 8 -- Remediation

## Triage Outcome

**Case B: Affected -- create remediation tasks.**

Versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream ship h2 0.4.4, which is within the affected range (< 0.4.5). Remediation tasks are required.

Ecosystem: **Cargo** (source dependency) -- 2 tasks: upstream backport + downstream propagation.

### Cross-stream Impact (Case A)

The issue is scoped to `[rhtpa-2.2]`. Checking the 2.1.x stream for cross-stream impact:
- 2.1.0 (tag v0.3.8): h2 = 0.4.5 -- NOT affected
- 2.1.1 (tag v0.3.12): h2 = 0.4.5 -- NOT affected

No cross-stream impact detected. Stream 2.1.x is not affected. No cross-stream notice or preemptive tasks required.

---

## Remediation Task 1: Upstream Backport Task

**Proposed Jira API call:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-99010: bump h2 to 0.4.5 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99010"]
)
```

### Task Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99010: h2 memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.5) must be updated to the fixed
version (0.4.5+).

Affected versions: 2.2.0, 2.2.1, 2.2.2
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is retag of v0.4.8)

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99010

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend -> reqwest -> hyper -> h2, 3 levels deep)

h2 is a transitive dependency of the backend workspace. It enters the dependency
tree through the following chain:

```
backend (workspace) -> reqwest -> hyper -> h2
```

h2 is NOT a direct dependency in Cargo.toml. The workspace declares
`reqwest = { version = "0.12", features = ["json"] }` as a direct dependency,
and reqwest pulls in hyper, which pulls in h2.

### Remediation approach (transitive dependency)

The vulnerable package h2 is a **transitive** dependency (pulled in through
intermediate packages). Use a two-tier approach:

**Preferred: bump the direct dependency (reqwest)**
- Check if a newer version of `reqwest` (the direct dependency) includes
  h2 >= 0.4.5 in its transitive closure
- Bump reqwest to that version in `backend/Cargo.toml`
- Run `cargo update -p reqwest` and verify h2 resolves to >= 0.4.5
  in `Cargo.lock`
- Verify the reqwest bump does not introduce breaking API changes to the
  backend codebase

**Fallback: pin h2 directly**
If bumping reqwest is not viable (no release available with the fix,
or breaking API changes in the newer reqwest version):
- `cargo add h2@0.4.5` to add h2 as a direct dependency, overriding
  the transitive resolution
- This forces Cargo to resolve h2 to at least 0.4.5 regardless of what
  reqwest/hyper request
- Document why the reqwest bump was not viable in the PR description

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.5 in Cargo.lock
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8060 (parent tracking issue)

---

### Description Digest Protocol (Upstream Task)

After creating the upstream backport task via `jira.create_issue`, the following digest protocol steps are performed:

1. **Re-fetch the task description** from Jira:
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```
   The description is re-fetched from the API (not the string passed to `create_issue`),
   because Jira normalizes content during storage.

2. **Write the description to a temp file** and compute the SHA-256 digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The script auto-detects the format (markdown or ADF JSON) and outputs a format-tagged
   digest (e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`).

3. **Post the digest comment** on the upstream task (BEFORE creating issue links or other comments):
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   The comment body is exactly one line: `[sdlc-workflow] Description digest: sha256-md:<64-char-hex>`.

4. **After the digest comment**, create issue links:
   - Depend link: `jira.create_link(inwardIssue: "TC-8060", outwardIssue: <upstream-task-key>, type: "Depend")`

---

## Remediation Task 2: Downstream Propagation Subtask

**Proposed Jira API call:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-99010 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99010"]
)
```

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99010 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps h2 to 0.4.5
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: transitive -- carried forward from upstream task
  (chain: backend -> reqwest -> hyper -> h2)
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned h2 directly (fallback approach via `cargo add h2@0.4.5`),
  verify the pinning is reflected in the downstream build's Cargo.lock after the
  source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8060 (parent tracking issue)

---

### Description Digest Protocol (Downstream Task)

After creating the downstream propagation task via `jira.create_issue`, the following digest protocol steps are performed:

1. **Re-fetch the task description** from Jira:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```
   The description is re-fetched from the API (not the string passed to `create_issue`),
   because Jira normalizes content during storage.

2. **Write the description to a temp file** and compute the SHA-256 digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The script auto-detects the format and outputs a format-tagged digest.

3. **Post the digest comment** on the downstream task (BEFORE creating issue links or other comments):
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   The comment body is exactly one line: `[sdlc-workflow] Description digest: sha256-md:<64-char-hex>`.

4. **After the digest comment**, create issue links:
   - Depend link: `jira.create_link(inwardIssue: "TC-8060", outwardIssue: <downstream-task-key>, type: "Depend")`
   - Blocks link: `jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")`

---

## Jira Linkage Summary

After both tasks are created and their digest comments are posted:

1. **Upstream task -> TC-8060**: Depend link (upstream task depends on the Vulnerability issue)
2. **Downstream task -> TC-8060**: Depend link (downstream task depends on the Vulnerability issue)
3. **Downstream task -> Upstream task**: Blocks link (upstream backport must merge before downstream propagation)

## Post-Triage Summary

After all triage actions are complete:

1. **Add `ai-cve-triaged` label** to TC-8060.
2. **Transition TC-8060 to In Progress** (if not already).
3. **Post summary comment** on TC-8060 documenting:
   - Version impact table (2.2.0-2.2.2 affected, 2.2.3-2.2.4 not affected)
   - Affects Versions correction (proposed): Current [RHTPA 2.2.0] -> Proposed [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
   - Triage outcome: remediation tasks created
   - Dependency chain: h2 is transitive via backend -> reqwest -> hyper -> h2
   - Remediation tasks: <upstream-task-key> (upstream backport), <downstream-task-key> (downstream propagation, blocked by <upstream-task-key>)
   - @mention of reporter psirt-analyst using ADF mention node:
     ```json
     { "type": "mention", "attrs": { "id": "557058:psirt-analyst-mock-id", "text": "@psirt-analyst" } }
     ```

   The summary comment includes the Comment Footnote:
   ```
   ---
   This comment was AI-generated by sdlc-workflow/triage-security v0.13.6.
   ```
