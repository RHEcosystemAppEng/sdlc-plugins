# Remediation -- TC-8004

## Triage Outcome

**Case A: Affected** -- the 2.1.x stream ships vulnerable h2 versions. Remediation tasks are required for the 2.1.x stream only.

The 2.2.x stream is NOT affected (ships h2 >= 0.4.8 in all versions). No remediation tasks are needed for the 2.2.x stream.

## Sibling Issue Check

JQL search for sibling Vulnerability issues with CVE-2026-33501 returned empty results. No duplicates or companions exist.

## Ecosystem and Task Strategy

The vulnerable library (h2) is a Cargo (Rust) dependency -- a source dependency ecosystem. Per the remediation templates, this requires **two tasks**:

1. **Upstream backport task** -- bump h2 to >= 0.4.8 in the source repository (backend) on the release/0.3.z branch
2. **Downstream propagation task** -- update the backend reference in the Konflux release repo (rhtpa-release.0.3.z) to pick up the upstream fix

## Proposed Remediation Tasks

### Task 1: Upstream Backport (2.1.x stream)

**Summary**: Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

**Description**:

> ## Repository
>
> backend
>
> ## Target Branch
>
> release/0.3.z
>
> ## Description
>
> Remediate CVE-2026-33501: Memory exhaustion via CONTINUATION frames in the h2 crate.
> The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).
>
> Affected versions: RHTPA 2.1.0 (tag v0.3.8, h2 0.4.5), RHTPA 2.1.1 (tag v0.3.12, h2 0.4.5)
> Source commit(s): v0.3.8, v0.3.12
>
> Upstream fix: https://github.com/hyperium/h2/pull/812
> Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7
>
> ## Implementation Notes
>
> - Update h2 dependency to >= 0.4.8 in Cargo.lock
> - Target branch: release/0.3.z
> - Check for pinned versions or transitive dependency constraints that might prevent the bump
> - If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)
>
> ### Coordination Guidance
>
> This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.
>
> ## Acceptance Criteria
>
> - [ ] h2 dependency is >= 0.4.8
> - [ ] No other dependency conflicts introduced
> - [ ] Existing tests pass
>
> ## Test Requirements
>
> - [ ] Existing test suite passes with the updated dependency
>
> ## Dependencies
>
> - Depends on: TC-8004 (parent tracking issue)

**Proposed Jira call**:
```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)",
  description: <upstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

---

### Task 2: Downstream Propagation (2.1.x stream)

**Summary**: Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

**Description**:

> ## Repository
>
> rhtpa-release.0.3.z
>
> ## Target Branch
>
> main
>
> ## Description
>
> Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-33501 fix from the upstream backport task.
>
> The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.
>
> ## Implementation Notes
>
> - Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
> - Update the backend reference to the merged commit or new release tag
> - Verify the Konflux build pipeline triggers successfully
>
> ## Acceptance Criteria
>
> - [ ] backend reference updated to include the fix
> - [ ] Konflux rebuild triggers new container image
>
> ## Test Requirements
>
> - [ ] Container image builds successfully with the updated reference
>
> ## Dependencies
>
> - Depends on: <upstream-task-key> (upstream backport must merge first)
> - Depends on: TC-8004 (parent tracking issue)

**Proposed Jira call**:
```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <downstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

## Proposed Jira Linkage

```
# Link upstream task to Vulnerability
jira.create_link(
  inwardIssue: "TC-8004",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)

# Link downstream task to Vulnerability
jira.create_link(
  inwardIssue: "TC-8004",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)

# Link downstream task as blocked by upstream task
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)
```

## No Remediation for 2.2.x Stream

The 2.2.x stream does NOT require remediation. All 2.2.x versions (2.2.0 through 2.2.4) ship h2 >= 0.4.8, which is at or above the fix threshold. No tasks are created for this stream.

## Post-Triage Actions

The following actions are proposed after engineer confirmation:

1. **Add label** `ai-cve-triaged` to TC-8004
2. **Post summary comment** to TC-8004 documenting:
   - Version impact table (mixed: 2.1.x affected, 2.2.x not affected)
   - Affects Versions correction (remove RHTPA 2.2.0, add RHTPA 2.1.1)
   - Remediation tasks created for 2.1.x stream only
   - @mention of issue reporter
3. **Transition** TC-8004 to In Progress
