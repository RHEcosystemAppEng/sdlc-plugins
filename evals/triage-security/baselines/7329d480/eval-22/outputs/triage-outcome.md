# Triage Outcome

## Issue Summary

- **Issue**: TC-8021
- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Affected range**: versions before 0.11.14
- **Fixed version**: 0.11.14
- **CVSS**: 7.5 (High)
- **Stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)

## Version Impact Summary

### In-scope stream (2.2.x)

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | (retag) | YES | same as 2.2.1 |
| 2.2.3 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 0.11.14 | NO | ships fixed version |

### Out-of-scope stream (2.1.x)

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | |
| 2.1.1 | 0.11.9 | YES | |

## Affects Versions Correction (Step 3)

PSIRT assigned `RHTPA 2.0.0`, which does not match any version in the supportability matrix or configured version streams. Based on lock file analysis scoped to the 2.2.x stream:

- **Current**: `[RHTPA 2.0.0]`
- **Proposed**: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14, which is at or above the fix threshold.

## Concurrent Triage Detection (Step 7)

No concurrent triages detected for upstream component `quinn-proto`. Proceeded silently to Case A/B/C branching.

## Triage Decision: Case A + Case B

### Case A -- Affected (create remediation tasks for 2.2.x)

The in-scope 2.2.x stream has affected versions (2.2.0, 2.2.1, 2.2.2). Since quinn-proto is a **Cargo** (source dependency) ecosystem, two remediation tasks are required:

1. **Upstream backport task**: Bump quinn-proto from the affected version to >= 0.11.14 in the `rhtpa-backend` source repository on the `release/0.4.z` branch. The upstream fix PR is [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048). Note that versions 2.2.3+ already ship 0.11.14, so the upstream branch (`release/0.4.z`) may already have the fix -- the upstream fix check (Step 2.5) would confirm this. If already fixed upstream, the upstream task is simplified to a Konflux release repo tag bump.

2. **Downstream propagation subtask**: Update the source pinning in `artifacts.lock.yaml` in the Konflux release repo `rhtpa-release.0.4.z` to reference a backend tag that includes quinn-proto >= 0.11.14 (e.g., a tag at or after v0.4.11, which already ships 0.11.14). This subtask is blocked by the upstream task.

Both tasks are linked to the Vulnerability issue TC-8021 with "Depend" link type.

### Case B -- Cross-stream impact (2.1.x also affected)

The version impact analysis reveals that the **2.1.x** stream (outside this issue's scope) is also affected:
- 2.1.0 ships quinn-proto 0.11.9 (affected)
- 2.1.1 ships quinn-proto 0.11.9 (affected)

Actions for Case B:
1. Post a cross-stream impact comment on TC-8021 noting that quinn-proto < 0.11.14 also affects stream 2.1.x.
2. Search for sibling Vulnerability issues with the CVE-2026-31812 label and a `[rhtpa-2.1]` stream suffix.
3. If a sibling CVE Jira exists for 2.1.x, link it as "Related" and skip preemptive task creation for that stream (it will be triaged through its own issue).
4. If no sibling CVE Jira exists for 2.1.x, create preemptive remediation tasks with the `security-preemptive` label and "Related" link type to TC-8021:
   - Upstream task: bump quinn-proto on the `release/0.3.z` branch
   - Downstream task: update `artifacts.lock.yaml` in `rhtpa-release.0.3.z`

### Post-Triage Actions

1. Add the `ai-cve-triaged` label to TC-8021.
2. Post a summary comment on TC-8021 documenting:
   - The version impact table
   - The Affects Versions correction (RHTPA 2.0.0 to RHTPA 2.2.0, 2.2.1, 2.2.2)
   - Links to all created remediation tasks
   - Cross-stream impact notice for 2.1.x
   - @mention of the issue reporter
   - Comment Footnote per shared/comment-footnote.md
