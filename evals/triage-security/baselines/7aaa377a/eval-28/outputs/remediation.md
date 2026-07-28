# Step 8 — Remediation

## Triage Outcome

Versions RHTPA 2.2.0, 2.2.1, and 2.2.2 are affected (ship h2 0.4.4, within the vulnerable range < 0.4.5). Versions 2.2.3 and 2.2.4 are not affected (ship h2 0.4.5, the fixed version). This is **Case B** — affected versions exist, so remediation tasks are required.

Ecosystem is **Cargo** (source dependency category), so **two tasks** are created: an upstream backport task and a downstream propagation subtask.

---

## Task 1: Upstream Backport Task

### Proposed Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-99010: bump h2 to 0.4.5 (rhtpa-2.2)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99010"]
)
```

### Task Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99010: h2 memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.5) must be updated to the fixed version (0.4.5+).

Affected versions: RHTPA 2.2.0 (v0.4.5), RHTPA 2.2.1 (v0.4.8), RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/hyperium/h2/pull/800
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99010

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend -> reqwest -> hyper -> h2, 3 levels deep)

### Remediation approach (transitive dependency)

The vulnerable package h2 is a **transitive** dependency pulled in through intermediate packages. Use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in h2: `reqwest` (chain: reqwest -> hyper -> h2)
- Bump `reqwest` to a version whose transitive closure includes h2 >= 0.4.5
- Check reqwest releases (e.g., reqwest 0.12.6+ or later) for a version that pulls in hyper with h2 >= 0.4.5
- Verify the bump does not introduce breaking API changes to reqwest

**Fallback: pin the transitive dependency directly**
If bumping reqwest is not viable (breaking API changes, no release available with the fix):
- Cargo: `cargo add h2@0.4.5` to add h2 as a direct dependency, overriding the transitive resolution
- Document why the reqwest bump was not viable in the PR description

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.5
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8060 (parent tracking issue)

---

### Post-Creation Digest Protocol (Upstream Task)

After creating the upstream backport task:

1. **Re-fetch the task description** from Jira:
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```
2. **Write the description to a temp file** and compute the SHA-256 digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The script auto-detects the format (ADF or markdown) and outputs a format-tagged digest (e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`).
3. **Post the digest comment** (BEFORE creating issue links or other comments):
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
4. **Then create issue links**:
   - Depend link: TC-8060 -> <upstream-task-key>
   ```
   jira.create_link(inwardIssue: "TC-8060", outwardIssue: <upstream-task-key>, type: "Depend")
   ```

---

## Task 2: Downstream Propagation Subtask

### Proposed Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-99010 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99010"]
)
```

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-99010 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps h2 to 0.4.5 on release/0.4.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: transitive — carried forward from upstream task (chain: backend -> reqwest -> hyper -> h2, 3 levels deep)
- Update the backend reference to the merged commit or new release tag
- If the upstream fix pinned h2 directly via `cargo add h2@0.4.5` (fallback approach), verify the pinning is reflected in the downstream build's Cargo.lock after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8060 (parent tracking issue)

---

### Post-Creation Digest Protocol (Downstream Task)

After creating the downstream propagation subtask:

1. **Re-fetch the task description** from Jira:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```
2. **Write the description to a temp file** and compute the SHA-256 digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The script auto-detects the format (ADF or markdown) and outputs a format-tagged digest (e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`).
3. **Post the digest comment** (BEFORE creating issue links or other comments):
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
4. **Then create issue links**:
   - Depend link: TC-8060 -> <downstream-task-key>
   ```
   jira.create_link(inwardIssue: "TC-8060", outwardIssue: <downstream-task-key>, type: "Depend")
   ```
   - Blocks link: <upstream-task-key> -> <downstream-task-key>
   ```
   jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
   ```

---

## Post-Triage Summary

After both remediation tasks are created and linked:

1. **Add the `ai-cve-triaged` label** to TC-8060.

2. **Post a summary comment** to TC-8060 documenting:
   - The version impact table (RHTPA 2.2.0-2.2.2 affected, 2.2.3-2.2.4 not affected)
   - The Affects Versions correction (if any)
   - The triage outcome: remediation tasks created
   - Links to remediation tasks: <upstream-task-key> (upstream backport), <downstream-task-key> (downstream propagation, blocked by <upstream-task-key>)
   - @mention of the reporter (psirt-analyst) using ADF mention node:
     ```json
     { "type": "mention", "attrs": { "id": "557058:psirt-analyst-mock-id", "text": "@psirt-analyst" } }
     ```
   - Comment Footnote: "This comment was AI-generated by sdlc-workflow/triage-security v0.13.7."

3. **Transition TC-8060 to In Progress** (if not already transitioned).
