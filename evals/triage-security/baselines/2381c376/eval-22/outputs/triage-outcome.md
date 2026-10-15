# Triage Outcome for TC-8021

## Summary

CVE-2026-31812 affects quinn-proto versions before 0.11.14, causing a denial-of-service panic when a remote attacker sends a QUIC transport frame that creates an excessive number of streams. The issue TC-8021 is scoped to stream 2.2.x.

## Version Impact Table

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | Outside issue scope |
| 2.1.1 | 2.1.x | 0.11.9 | YES | Outside issue scope |
| 2.2.0 | 2.2.x | 0.11.9 | YES | In scope |
| 2.2.1 | 2.2.x | 0.11.12 | YES | In scope |
| 2.2.2 | 2.2.x | -- | YES | In scope; retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | Fixed |
| 2.2.4 | 2.2.x | 0.11.14 | NO | Fixed |

## Triage Decision: Case A + Case B (Affected with cross-stream impact)

### Rationale

- **Supported versions within scope (2.2.x) are affected**: versions 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto < 0.11.14.
- **Versions 2.2.3 and 2.2.4 are NOT affected**: they ship quinn-proto 0.11.14 (the fixed version).
- **Cross-stream impact (Case A)**: stream 2.1.x is also affected (versions 2.1.0 and 2.1.1 ship quinn-proto 0.11.9). Since TC-8021 is scoped to 2.2.x only, the 2.1.x impact is flagged for cross-stream awareness.
- **Concurrent triage (Step 7)**: no concurrent triages detected on quinn-proto -- safe to proceed with remediation task creation.
- **Upstream fix available for 2.2.x (Step 2.5)**: the upstream branch `release/0.4.z` already ships quinn-proto 0.11.14 (confirmed at tags v0.4.11 and v0.4.12). This means the 2.2.x remediation uses the **dependency bump** variant rather than the upstream backport variant.

### Affects Versions Correction (Step 3)

**Proposed Jira mutation (not executed):**

```
jira.edit_issue("TC-8021", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-jira-id>"},
    {"id": "<RHTPA-2.2.1-jira-id>"},
    {"id": "<RHTPA-2.2.2-jira-id>"}
  ]
})
```

- Current: `[RHTPA 2.0.0]` (incorrect -- RHTPA 2.0.0 does not correspond to any supported stream)
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
- Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields`
- A correction comment with ProdSec @mention (if configured) would be posted

### Case A: Cross-Stream Impact (Step 8)

Stream 2.1.x (versions 2.1.0, 2.1.1) is also affected but is outside TC-8021's scope (`[rhtpa-2.2]`).

**Proposed actions (not executed):**

1. **Post cross-stream impact comment on TC-8021:**
   > Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. Stream 2.1.x versions 2.1.0 (quinn-proto 0.11.9) and 2.1.1 (quinn-proto 0.11.9) ship the vulnerable dependency. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.

2. **Search for existing sibling CVE Jira for 2.1.x** with label CVE-2026-31812 and stream suffix `[rhtpa-2.1]`. If none exists, create preemptive remediation tasks for 2.1.x with `security-preemptive` label and "Related" link to TC-8021.

3. **If no sibling CVE Jira exists for 2.1.x**, the following preemptive tasks would be created:

   a. **Preemptive upstream backport task (2.1.x)**:
      - Summary: `Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)`
      - Labels: `["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]`
      - Link: Related to TC-8021 (not Depend, because this is preemptive)
      - Note: upstream branch `release/0.3.z` does NOT yet ship the fix, so this requires an upstream backport (not a dependency bump)

   b. **Preemptive downstream propagation task (2.1.x)**:
      - Summary: `Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)`
      - Labels: `["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]`
      - Link: Related to TC-8021, Blocks relationship to upstream task

### Case B: Remediation Tasks for 2.2.x (Step 8)

Since the upstream branch `release/0.4.z` already ships the fixed version (quinn-proto 0.11.14), the remediation uses the **dependency bump + downstream propagation** variant (2 tasks).

**Proposed Task 1 -- Dependency Bump (not executed):**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <dependency-bump-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

Task description follows the dependency bump template:
- Repository: backend (from Ecosystem Mappings)
- Target Branch: release/0.4.z
- Remediation action: `cargo update -p quinn-proto` to pull in 0.11.14
- Dependency type: direct or transitive (to be confirmed via manifest inspection)
- Affected versions: 2.2.0 (v0.4.5), 2.2.1 (v0.4.8), 2.2.2 (retag of 2.2.1)
- Source commits: v0.4.5, v0.4.8
- Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
- Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq
- Coordination guidance (upstream context): "This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs."

Post-creation: description digest comment posted before any links.

Link: `Depend` from TC-8021 to this task.

**Proposed Task 2 -- Downstream Propagation (not executed):**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <downstream-propagation-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

Task description follows the downstream propagation template:
- Repository: rhtpa-release.0.4.z (Konflux release repo for 2.2.x)
- Target Branch: main
- Source pinning method: `artifacts.lock.yaml` (download URL contains tag)
- Update the backend reference to the merged commit or new release tag that includes quinn-proto >= 0.11.14
- Blocked by: Task 1 (dependency bump must merge first)

Post-creation: description digest comment posted before any links.

Links:
- `Depend` from TC-8021 to this task
- `Blocks` from Task 1 (dependency bump) to Task 2 (downstream propagation)

### Release Jira Orchestration (Step 7.5)

For stream 2.2.x, release Jira structure would be resolved:

1. Search for existing release Epic matching `"RHTPA 2.2.* Release Tasks"`
2. If found, reuse it; if not, propose creation with default version based on latest released version (2.2.4) -> default to RHTPA 2.2.5
3. Find or create release Task `"RHTPA <version> CVE triage"` under the Epic
4. Cross-CVE dedup check (Step 7.5.3): inspect release Task's linked remediation tasks for matching upstream component (quinn-proto). If no existing coverage, proceed with new task creation.
5. After remediation tasks are created, link them:
   - Remediation tasks -> release Task (Blocks)
   - TC-8021 -> release Task (Related)

### Post-Triage Actions (not executed)

1. **Add `ai-cve-triaged` label** to TC-8021
2. **Post summary comment** on TC-8021 documenting:
   - Version impact table
   - Affects Versions correction: `[RHTPA 2.0.0]` -> `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
   - Remediation tasks created (dependency bump + downstream propagation for 2.2.x)
   - Cross-stream impact on 2.1.x
   - Release Jira references
   - @mention of the issue reporter (PSIRT analyst)
   - Comment Footnote per `shared/comment-footnote.md`
3. **Transition TC-8021 to In Progress**

## Summary of All Proposed Jira Mutations

| # | Operation | Target | Details |
|---|-----------|--------|---------|
| 1 | Assign issue | TC-8021 | Assign to current user |
| 2 | Transition | TC-8021 | New -> Assigned |
| 3 | Edit field (Affects Versions) | TC-8021 | `[RHTPA 2.0.0]` -> `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]` |
| 4 | Add comment | TC-8021 | Affects Versions correction rationale |
| 5 | Add comment | TC-8021 | Cross-stream impact notice (2.1.x affected) |
| 6 | Create issue (Task) | TC project | Dependency bump: update quinn-proto to 0.11.14 (rhtpa-2.2) |
| 7 | Add comment (digest) | New task from #6 | Description digest |
| 8 | Create issue (Task) | TC project | Downstream propagation: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2) |
| 9 | Add comment (digest) | New task from #8 | Description digest |
| 10 | Create link (Depend) | TC-8021 -> Task #6 | CVE depends on upstream remediation |
| 11 | Create link (Depend) | TC-8021 -> Task #8 | CVE depends on downstream remediation |
| 12 | Create link (Blocks) | Task #6 -> Task #8 | Downstream blocked by upstream |
| 13 | Create link (Blocks) | Task #6 -> Release Task | Remediation blocks release |
| 14 | Create link (Blocks) | Task #8 -> Release Task | Remediation blocks release |
| 15 | Create link (Related) | Release Task -> TC-8021 | CVE traceability to release |
| 16 | Add label | TC-8021 | `ai-cve-triaged` |
| 17 | Add comment | TC-8021 | Post-triage summary with version impact, remediation links, @reporter mention |
| 18 | Transition | TC-8021 | Assigned -> In Progress |

All mutations above are **proposed actions only** -- none have been executed. Each would require engineer confirmation in interactive mode before execution.
