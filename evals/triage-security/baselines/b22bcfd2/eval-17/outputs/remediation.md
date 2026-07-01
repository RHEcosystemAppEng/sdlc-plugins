# Step 8 -- Remediation

## Triage Decision

The version impact table shows that within the issue's scoped stream (2.2.x), versions 2.2.0, 2.2.1, and 2.2.2 are affected. This is **Case A: Affected -- create remediation tasks**.

Additionally, stream 2.1.x is also affected (2.1.0 and 2.1.1), triggering **Case B: Cross-stream impact** notification.

The ecosystem is **Cargo** (a source dependency ecosystem), so **two tasks** are created per affected stream: an upstream backport task and a downstream propagation subtask.

---

## Case A -- Remediation Tasks for Stream 2.2.x (Current Scope)

### Task 1: Upstream Backport Task

**Proposed Jira Issue Creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task Description:**

> ## Repository
>
> rhtpa-backend
>
> ## Target Branch
>
> release/0.4.z
>
> ## Description
>
> Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
> The vulnerable dependency (quinn-proto < 0.11.14) must be updated
> to the fixed version (0.11.14+).
>
> Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
> Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is retag of v0.4.8)
>
> Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
> Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq
>
> ## Implementation Notes
>
> - Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
> - Target branch: release/0.4.z (from Ecosystem Mappings)
> - Check for pinned versions or transitive dependency constraints
>   that might prevent the bump
> - If a direct bump introduces breaking changes, assess whether a
>   code-level workaround is viable (see upstream changelog)
>
> ## Acceptance Criteria
>
> - [ ] quinn-proto dependency is >= 0.11.14
> - [ ] No other dependency conflicts introduced
> - [ ] Existing tests pass
>
> ## Test Requirements
>
> - [ ] Existing test suite passes with the updated dependency
>
> ## Dependencies
>
> - Depends on: TC-8001 (parent tracking issue)

**Post-creation digest protocol (proposed):**

1. Re-fetch the task description from Jira after `create_issue`:
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```
2. Write the re-fetched description to a temp file and compute SHA-256 digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The digest is computed from the **re-fetched** description (via Jira API after create_issue), not from the description string passed to create_issue. This accounts for any ADF transformations Jira applies.
3. Post digest comment **before** creating issue links or other comments:
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: sha256-adf:<hex>")
   ```
4. **Then** create the Depend link to TC-8001:
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <upstream-task-key>, type: "Depend")
   ```

---

### Task 2: Downstream Propagation Subtask

**Proposed Jira Issue Creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task Description:**

> ## Repository
>
> rhtpa-release.0.4.z
>
> ## Target Branch
>
> main
>
> ## Description
>
> Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
> CVE-2026-31812 fix from <upstream-task-key>.
>
> The upstream backport (<upstream-task-key>) bumps quinn-proto to 0.11.14
> on release/0.4.z. Once that PR merges, update the source pinning in this
> Konflux release repo so the next build ships the fix.
>
> ## Implementation Notes
>
> - Source pinning method: artifacts.lock.yaml (download URL contains tag)
> - Update the rhtpa-backend reference to the merged commit or new release tag
> - Verify the Konflux build pipeline triggers successfully
>
> ## Acceptance Criteria
>
> - [ ] rhtpa-backend reference updated to include the fix
> - [ ] Konflux rebuild triggers new container image
>
> ## Test Requirements
>
> - [ ] Container image builds successfully with the updated reference
>
> ## Dependencies
>
> - Depends on: <upstream-task-key> (upstream backport must merge first)
> - Depends on: TC-8001 (parent tracking issue)

**Post-creation digest protocol (proposed):**

1. Re-fetch the task description from Jira after `create_issue`:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```
2. Write the re-fetched description to a temp file and compute SHA-256 digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The digest is computed from the **re-fetched** description (via Jira API after create_issue), not from the description string passed to create_issue.
3. Post digest comment **before** creating issue links or other comments:
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: sha256-adf:<hex>")
   ```
4. **Then** create the linkages:
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-key>, type: "Depend")
   jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
   ```

---

## Jira Linkage (Proposed)

After creating both tasks and posting digest comments:

1. **Depend links** -- each task linked to the Vulnerability issue TC-8001 with type "Depend"
2. **Blocks link** -- downstream subtask blocked by upstream task with type "Blocks"
3. **Transition** -- propose transitioning TC-8001 to "In Progress"
4. **Assign** -- propose assigning TC-8001 to the current user

---

## Case B -- Cross-Stream Impact Notice

The version impact analysis reveals that stream **2.1.x** is also affected:

- RHTPA 2.1.0: quinn-proto 0.11.9 (affected)
- RHTPA 2.1.1: quinn-proto 0.11.9 (affected)

**Proposed cross-stream impact comment on TC-8001:**

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis.
> This stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.

A search for sibling CVE Jiras with label CVE-2026-31812 and stream suffix `[rhtpa-2.1]` would determine whether a companion issue exists for stream 2.1.x. If no companion issue exists, proactive preemptive remediation tasks would be created for stream 2.1.x with the `security-preemptive` label and "Related" link type to TC-8001.

---

## Post-Triage Summary (Proposed)

**Proposed actions on TC-8001:**

1. Add label `ai-cve-triaged` to mark the issue as triaged
2. Post a summary comment documenting:
   - Version impact table (all versions across all streams)
   - Affects Versions correction (RHTPA 2.0.0 replaced with RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2)
   - Triage outcome: remediation tasks created for stream 2.2.x
   - Links to all remediation tasks (upstream backport + downstream propagation)
   - @mention of the vulnerability issue reporter using ADF mention node
   - Cross-stream impact notice for stream 2.1.x
   - Comment Footnote per `shared/comment-footnote.md` (skill: triage-security)

All actions above are **proposed** and require explicit engineer confirmation before execution. No Jira mutations are performed without approval.
