# Remediation — TC-8001 (CVE-2026-31812)

## Version Impact Summary

Issue is scoped to the **2.2.x** stream. Version impact for CVE-2026-31812
(quinn-proto < 0.11.14):

| Version | Tag | quinn-proto | Affected? | Notes |
|---------|-----|-------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | |

Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 ship
the fixed version. This is **Case B** (affected versions exist) -- create
remediation tasks.

Cross-stream note: 2.1.x versions (2.1.0, 2.1.1) also ship quinn-proto 0.11.9
and are affected, but those are outside this issue's scope (tracked by a
companion issue for the rhtpa-2.1 stream).

## Remediation Task Creation

Ecosystem: **Cargo** (source dependency) -- create **two tasks** for the 2.2.x stream:

1. **Upstream backport task** -- fix in source repo (rhtpa-backend)
2. **Downstream propagation subtask** -- update reference in Konflux release repo
   (rhtpa-release.0.4.z), blocked by the upstream task

---

### Task 1: Upstream Backport Task

**Proposed Jira issue creation** (requires confirmation):

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

#### Task Description

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto Panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is retag of v0.4.8)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is shipped to customers. Coordinate with Product
Security for CVE assignment, advisory preparation, and formal
disclosure. Fix must be released via a security advisory with
explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Protocol (upstream task)

After `create_issue` returns the new task key (e.g., TC-XXXX):

1. **Re-fetch the description** from Jira (do not hash the string passed to
   `create_issue`, since Jira normalizes content during storage):
   ```
   upstream_desc = jira.get_issue("TC-XXXX", fields=["description"])
   ```

2. **Write the description to a temp file** and compute the SHA-256 digest
   using `scripts/sha256-digest.py`:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The script auto-detects the format (ADF JSON or markdown) and outputs a
   format-tagged digest (e.g., `sha256-md:<64-char-hex>` or
   `sha256-adf:<64-char-hex>`).

3. **Post the digest comment** on the upstream task BEFORE creating any issue
   links or other comments:
   ```
   jira.add_comment("TC-XXXX", "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

4. **Then create issue links** (Depend link to TC-8001).

---

### Task 2: Downstream Propagation Subtask

**Proposed Jira issue creation** (requires confirmation):

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

#### Task Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14 on release/0.4.z.
Once that PR merges, update the source pinning in this Konflux release
repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product
Security for CVE assignment, advisory preparation, and formal
disclosure. Fix must be released via a security advisory with
explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Protocol (downstream subtask)

After `create_issue` returns the new subtask key (e.g., TC-YYYY):

1. **Re-fetch the description** from Jira:
   ```
   downstream_desc = jira.get_issue("TC-YYYY", fields=["description"])
   ```

2. **Compute the SHA-256 digest** using `scripts/sha256-digest.py`:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```

3. **Post the digest comment** BEFORE creating any issue links or other comments:
   ```
   jira.add_comment("TC-YYYY", "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

4. **Then create issue links** (Depend link to TC-8001, Blocks link from
   upstream task).

---

## Jira Linkage (proposed)

After both tasks are created and digest comments posted:

1. **Link upstream task to CVE issue:**
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: "<upstream-task-key>", type: "Depend")
   ```

2. **Link downstream subtask to CVE issue:**
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: "<downstream-task-key>", type: "Depend")
   ```

3. **Link downstream subtask as blocked by upstream task:**
   ```
   jira.create_link(inwardIssue: "<upstream-task-key>", outwardIssue: "<downstream-task-key>", type: "Blocks")
   ```

4. **Transition TC-8001 to In Progress** (if not already).

5. **Add ai-cve-triaged label** to TC-8001.

6. **Post summary comment** on TC-8001 documenting the version impact table,
   Affects Versions correction, triage outcome, links to remediation tasks,
   and an @mention of the vulnerability reporter using an ADF mention node.
   The comment MUST include the Comment Footnote:
   ```
   This comment was AI-generated by sdlc-workflow/triage-security v0.13.6.
   ```

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks (Cargo is a source dependency ecosystem)
- [x] **Cross-stream coverage**: 2.1.x stream is also affected but outside this
      issue's scope -- cross-stream impact comment will be posted (Case A)
- [x] **Link types**: "Depend" for tasks linked to TC-8001, "Blocks" for
      upstream -> downstream within the stream
- [x] **Coordination guidance**: both tasks include the `customer-shipped`
      guidance in Implementation Notes, advising coordination with Product
      Security for CVE assignment, advisory preparation, and formal disclosure
