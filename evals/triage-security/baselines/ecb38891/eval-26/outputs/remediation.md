# Step 8 — Remediation

## Triage Outcome

All 2.2.x versions ship criterion 0.5.1, which is within the affected range (< 0.5.2). This is **Case B: Affected -- create remediation tasks**.

However, criterion is a **dev-only dependency** (declared in `[dev-dependencies]`). Per the dependency scope decision tree, remediation tasks are still created for supply chain risk but with modified labels and priority:

- **Label**: `dev-dependency` added to the labels array
- **Priority**: Normal (overriding CVE severity of CVSS 5.3 Medium)
- **Description note**: includes a statement that the dependency is dev/build-only and not shipped in production

Since Cargo is a source dependency ecosystem, two tasks are created per the ecosystem classification table: upstream backport + downstream propagation.

---

## Task 1: Upstream Backport Task

**Proposed Jira creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-99001: bump criterion to 0.5.2 (rhtpa-2.2)",
  description: <upstream-task-description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99001", "dev-dependency"],
  priority: "Normal"
)
```

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority**: Normal (overridden from CVE severity per dev-dependency decision tree)

### Upstream Task Description

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99001: path traversal in criterion benchmark output.
The vulnerable dependency (criterion < 0.5.2) must be updated
to the fixed version (0.5.2+).

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

Affected versions: RHTPA 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4
Source commit(s): v0.4.5, v0.4.8, v0.4.11, v0.4.12

CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct dev-dependency
- **Dependency scope**: dev-only ([dev-dependencies] in backend/Cargo.toml) -- NOT shipped in production, used for benchmarks only
- This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only).

### Remediation approach (direct dependency)

- Update criterion dependency to >= 0.5.2 in backend/Cargo.toml [dev-dependencies]
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8050 (parent tracking issue)
```

### Description Digest Protocol (Upstream Task)

After creating the upstream task, perform the description digest protocol:

1. **Re-fetch the description** from Jira after `create_issue`:
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```

2. **Write the description to a temp file** and compute the SHA-256 digest using the script:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The script auto-detects the format (ADF or markdown) and outputs a tagged digest (e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`).

3. **Post the digest comment** on the upstream task (BEFORE creating issue links or other comments):
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   The digest comment uses the marker `[sdlc-workflow] Description digest:` so consumers can locate it.

4. **Then create issue links**:
   - Depend link: TC-8050 -> <upstream-task-key>
   ```
   jira.create_link(inwardIssue: "TC-8050", outwardIssue: <upstream-task-key>, type: "Depend")
   ```

---

## Task 2: Downstream Propagation Subtask

**Proposed Jira creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-99001 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <downstream-task-description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99001", "dev-dependency"],
  priority: "Normal"
)
```

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority**: Normal (overridden from CVE severity per dev-dependency decision tree)

### Downstream Task Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99001 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps criterion to 0.5.2
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct dev-dependency -- carried forward from upstream task
- **Dependency scope**: dev-only -- NOT shipped in production
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully
- This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only).

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8050 (parent tracking issue)
```

### Description Digest Protocol (Downstream Task)

After creating the downstream task, perform the description digest protocol:

1. **Re-fetch the description** from Jira after `create_issue`:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```

2. **Write the description to a temp file** and compute the SHA-256 digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```

3. **Post the digest comment** on the downstream task (BEFORE creating issue links or other comments):
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

4. **Then create issue links** (after the digest comment):
   - Depend link: TC-8050 -> <downstream-task-key>
   ```
   jira.create_link(inwardIssue: "TC-8050", outwardIssue: <downstream-task-key>, type: "Depend")
   ```
   - Blocks link: upstream blocks downstream
   ```
   jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
   ```

---

## Post-Triage Summary

After remediation tasks are created:

1. **Add the `ai-cve-triaged` label** to TC-8050.

2. **Post a summary comment** on TC-8050 including:
   - Version impact table
   - Affects Versions correction (RHTPA 2.2.0 -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2, RHTPA 2.2.3, RHTPA 2.2.4)
   - Triage outcome: remediation tasks created with dev-dependency handling
   - Links to all remediation tasks created (upstream + downstream)
   - Dependency scope note: criterion is a dev-only dependency, not shipped in production; tasks have Normal priority and dev-dependency label
   - @mention of the vulnerability reporter using ADF mention node:
     ```json
     { "type": "mention", "attrs": { "id": "<reporter-account-id>", "text": "@<reporter-name>" } }
     ```
   - Comment Footnote: "This comment was AI-generated by sdlc-workflow/triage-security v0.13.7."

3. **Transition TC-8050 to In Progress** (if not already).
